#!/usr/bin/env python3
#
# Copyright 2020, Data61, CSIRO (ABN 41 687 119 230)
#
# SPDX-License-Identifier: BSD-2-Clause
#

import subprocess
import os, sys
import argparse
import time
import termios
import threading
import signal
import shutil
import pathlib


def parse_args(parser):
    parser.add_argument('-b', '--binary', dest="qemu_sim_binary", type=str,
                        help="QEMU binary", default="qemu-system-aarch64")
    parser.add_argument('-d', '--gdbserver', dest="qemu_gdbserver", action='store_true',
                        help="Tell QEMU to wait for gdb on port 1234")
    parser.add_argument('-M', '--machine', dest="qemu_sim_machine", type=str,
                        help="QEMU Machine", default="virt,virtualization=on,highmem=off,secure=off,gic-version=3")
    parser.add_argument('-c', '--cpu', dest='qemu_sim_cpu', type=str,
                        help="QEMU CPU", default="cortex-a53")
    parser.add_argument('-o', '--cpu-opt', dest='qemu_sim_cpu_opt', type=str,
                        help="QEMU CPU Options", default="")
    parser.add_argument('-g', '--graphic', dest='qemu_sim_graphic_opt', type=str,
                        help="QEMU Graphic Options", default="-nographic")
    parser.add_argument('-s', '--serial', dest='qemu_sim_serial_opt', type=str,
                        help="QEMU Serial Options", default="")
    parser.add_argument('-m', '--mem-size', dest='qemu_sim_mem_size', type=str,
                        help="QEMU Memory Size Option", default="2048")
    parser.add_argument('-a', '--args', dest='qemu_sim_args', type=str,
                        help="Arguments to pass onto QEMU", default="")
    parser.add_argument('-k', '--kernel', dest='qemu_sim_kernel_file', type=str,
                        help="Kernel file to pass onto QEMU", default="")
    parser.add_argument('-i', '--initrd', dest='qemu_sim_initrd_file', type=str,
                        help="Initrd file to pass onto QEMU", default="platform/qemu-arm-virt/images/proc-image-arm-qemu-arm-virt")
    parser.add_argument('--extra-qemu-args', dest='qemu_sim_extra_args', type=str,
                        help="Additional arguments to pass onto QEMU", default="-smp 4 -drive if=none,file={},id=hd0 -device virtio-blk-device,drive=hd0 -global virtio-mmio.force-legacy=false")
    parser.add_argument('--extra-cpu-opts', dest='qemu_sim_extra_cpu_opts', type=str,
                        help="Additional cpu options to append onto the existing CPU options",
                        default="")
    parser.add_argument('--disk-image', dest='disk_image', type=str,
                        help="Specifies the image file of the block device",
                        default="disk.img")
    parser.add_argument('-n', '--nic', dest='qemu_sim_nic_opt', type=str,
                        help="QEMU NIC Options", default="")


def notice(message):
    sys.stderr.write("{}: {}".format(sys.argv[0], message))
    sys.stderr.flush()


def get_qemu_arg(prefix, property, property2=""):
    return prefix + property + property2 if property else ""


class ConanBuildInfo:
    def __init__(self):
        self.values = dict()
        cwd = pathlib.Path.cwd()
        for conanbuildinfo_file in cwd.rglob("conanbuildinfo.txt"):
            activeSection = None
            for line in conanbuildinfo_file.read_text().split("\n"):
                if len(line) > 0 and line[0] == "[":
                    activeSection = line[1:line.rfind("]")]
                    self.values[activeSection] = []
                elif activeSection != None and len(line.strip()) > 0:
                    self.values[activeSection].append(line.strip())

    def qemu_binrary(self, qemu_sim_binary):
        path = None
        for line in self.values.get("ENV_qemu", []):
            kv = line.split("=")
            if kv[0] == 'PATH':
                path = kv[1][2:-2].replace('","', ":")
        return shutil.which(qemu_sim_binary, path=path)


class Simulate:
    def __init__(self, args):
        self.args = args
        self.simulate = None
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)

        mode = termios.tcgetattr(self.fd)
        mode[0] = mode[0] & ~(termios.BRKINT | termios.ICRNL | termios.INPCK | termios.ISTRIP | termios.IXON)
        mode[2] = mode[2] & ~(termios.CSIZE | termios.PARENB)
        mode[2] = mode[2] | termios.CS8
        mode[3] = mode[3] & ~(termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
        mode[6][termios.VMIN] = 1
        mode[6][termios.VTIME] = 0
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, mode)

    def wait_simulate(self):
        while not self.simulate.poll():
            self.simulate.wait()
            exit(0)
        delay = 5  # in seconds
        # Force a newline onto the output stream.
        sys.stderr.write('\n')
        msg = "QEMU failed; resetting terminal in {d} seconds".format(d=delay) \
            + "--interrupt to abort\n"
        notice(msg)
        time.sleep(delay)

        pid = os.getpid()
        os.killpg(pid, signal.SIGQUIT)

    def reset(self):
        if self.simulate:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            os.killpg(self.simulate.pid, signal.SIGKILL)
            self.simulate = None
        print("")
        # subprocess.call("tput reset", shell=True)

    def __del__(self):
        self.reset()

    def run(self):
        notice(self.full_command)
        if self.gdbserver_entry != "":
            notice('waiting for GDB on port 1234...')

        self.simulate = subprocess.Popen(self.full_command, shell=True, close_fds=True, preexec_fn=os.setsid, stdin=subprocess.PIPE, bufsize=0)
        threading.Thread(target = self.wait_simulate).start()

        line = ""
        while not self.simulate.poll():
            if sys.stdin.readable():
                c = sys.stdin.read(1)
                if c == '\3':
                    break
                if c == '\n' or c == '\r':
                    if line == "quit" or line == 'poweroff':
                        break
                    line = ""
                else:
                    line += c
                self.simulate.stdin.write(bytes(c, encoding="utf8"))
        self.reset()

    @property
    def images_entry(self):
        qemu_sim_initrd_file = self.args.qemu_sim_initrd_file
        if not os.path.isfile(qemu_sim_initrd_file):
            this_file = os.path.abspath(__file__)
            if os.path.islink(this_file):
                this_file = os.readlink(this_file)
            dirname = os.path.dirname(this_file)
            qemu_sim_initrd_file = os.path.join(dirname, "..", qemu_sim_initrd_file)
        if os.path.isfile(qemu_sim_initrd_file):
            if self.args.qemu_sim_kernel_file == "":
                return "-kernel " + qemu_sim_initrd_file
            else:
                return "-kernel " + self.args.qemu_sim_kernel_file + " -initrd " + qemu_sim_initrd_file
        else:
            raise Exception("File `%s` no found." % self.args.qemu_sim_initrd_file)

    @property
    def cpu_entry(self):
        return get_qemu_arg("-cpu ", self.args.qemu_sim_cpu, self.args.qemu_sim_cpu_opt) + get_qemu_arg(",", self.args.qemu_sim_extra_cpu_opts)

    @property
    def machine_entry(self):
        return get_qemu_arg("-machine ", self.args.qemu_sim_machine)

    @property
    def gdbserver_entry(self):
        return "-s -S" if self.args.qemu_gdbserver else ""

    @property
    def mem_size_entry(self):
        return get_qemu_arg("-m size=", self.args.qemu_sim_mem_size)

    @property
    def extra_args_entry(self):
        if self.args.disk_image:
            disk_image = os.path.join(os.getcwd(), self.args.disk_image)
            if not os.path.isfile(disk_image):
                dirname = os.path.dirname(os.path.abspath(__file__))
                disk_image = os.path.join(dirname, self.args.disk_image)
            if not os.path.isfile(disk_image):
                raise Exception("File `%s` no found." % self.args.disk_image)
            return self.args.qemu_sim_extra_args.format(disk_image)
        else:
            return self.args.qemu_sim_extra_args

    @property
    def qemu_sim_binary(self):
        qemu_sim_binary = ConanBuildInfo().qemu_binrary(self.args.qemu_sim_binary)
        if qemu_sim_binary is None:
            raise Exception(f"Program {self.args.qemu_sim_binary} not found")
        return qemu_sim_binary

    @property
    def netdev_entry(self):
        return "-netdev user,id=netdev0,net=192.168.76.0/24,dhcpstart=192.168.76.9 -device virtio-net-device,netdev=netdev0,mac=e6:c8:ff:99:76:01"

    @property
    def full_command(self):
        return ' '.join([
                    self.qemu_sim_binary, self.args.qemu_sim_graphic_opt,
                    self.args.qemu_sim_serial_opt, self.args.qemu_sim_nic_opt,
                    self.machine_entry, self.cpu_entry,
                    self.images_entry, self.mem_size_entry,
                    self.gdbserver_entry,
                    self.extra_args_entry,
                    self.netdev_entry
        ])

def main():
    parser = argparse.ArgumentParser()
    Simulate(parse_args(parser)).run()


if __name__ == "__main__":
    main()
