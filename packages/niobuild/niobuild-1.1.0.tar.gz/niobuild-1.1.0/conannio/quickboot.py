#!/usr/bin/env python3

import os
import time
import sys
import pathlib
import threading
import selectors
import socket
import select
import termios
import tty
import fcntl
from fbtftp.base_handler import BaseHandler
from fbtftp.base_handler import ResponseData
from fbtftp.base_server import BaseServer


def get_enternet_ip(ifname=None):
    import psutil
    if_stat = psutil.net_if_stats()

    found = False
    for en, info in psutil.net_if_addrs().items():
        found = en == ifname
        # print(en, info[0].address)
        if ifname == None and if_stat[en].isup and (if_stat[en].duplex == psutil.NIC_DUPLEX_FULL and if_stat[en].speed != 0):
            found = True
        if found:
            if info[0].family == socket.AF_INET and (en[:2] != 'lo' or info[0].address != '127.0.0.1'):
                print(en, info[0].address)
                return info[0]


class FileResponseData(ResponseData):
    def __init__(self, path):
        fs = pathlib.Path(path)
        self.data = fs.read_bytes()
        self._size = fs.stat().st_size
        self.offset = 0

    def read(self, n):
        data = self.data[self.offset: self.offset + n]
        self.offset += n
        return data

    def size(self):
        return self._size

    def close(self):
        pass


class StaticHandler(BaseHandler):
    def __init__(self, server_addr, peer, path, options, root, stats_callback):
        self._root = root
        super().__init__(server_addr, peer, path, options, stats_callback)

    def get_response_data(self):
        return FileResponseData(os.path.join(self._root, self._path))


class StaticServer(BaseServer, threading.Thread):
    def __init__(self, root, address='0.0.0.0', port=69, retries=3, timeout=3):
        self._root = root
        self._handler_stats_callback = self.print_session_stats
        threading.Thread.__init__(self)
        BaseServer.__init__(self, address, port, retries, timeout, self.print_server_stats)
        self.start()

    def get_handler(self, server_addr, peer, path, options):
        filename = self._root.get(path)
        if filename and os.path.exists(filename):
            print("Get:", filename)
            return StaticHandler(
                server_addr, peer, os.path.basename(filename), options, os.path.dirname(filename),
                self._handler_stats_callback)

    def get_file_stat(self, path):
        filename = self._root.get(path)
        if filename and os.path.exists(filename):
            return os.stat(filename)

    def run_once(self):
        """
        Uses edge polling object (`socket.epoll`) as an event notification
        facility to know when data is ready to be retrived from the listening
        socket. See http://linux.die.net/man/4/epoll .
        """
        events = self._selector.select(1)
        for key, mask in events:
            if not mask & selectors.EVENT_READ:
                continue
            if key.fd == self._listener.fileno():
                self.on_new_data()
                continue

    def run(self):
        try:
            BaseServer.run(self)
        except KeyboardInterrupt:
            BaseServer.close(self)

    def close(self):
        BaseServer.close(self)

    @staticmethod
    def print_session_stats(stats):
        pass

    @staticmethod
    def print_server_stats(stats):
        pass


class Uboot:
    def __init__(self, port=None, baud=115200, trace_enabled=True):
        import serial
        from serial.tools import list_ports
        self._port = None
        if port is None:
            port_list = list(list_ports.comports())
            for i in port_list:
                if i.hwid != 'n/a':
                    port = i.device
                    break
        if not port:
            print("Not found serial port.")
            exit()
        else:
            print("Found serial:", port)
        try:
            self._port = serial.Serial(port, baud)
        except:
            raise Exception("could not open serial port {}".format(port))

    def sendbreak(self):
        termios.tcsendbreak(self._port.fd, 0)

    def read(self, count):
        return self._port.read(count)

    def readline(self, show=False):
        line = self._port.readline()
        try:
            line = line.decode()
            if show:
                print(line, end='')
        except:
            line = ""
        return line

    def write(self, data):
        if isinstance(data, str):
            data = data.encode()
        self._port.write(data)
        self._port.flush()

    def wait_prompt(self, show=True):
        line = ''
        while '=> ' not in line:
            c = self.read(1).decode()
            if show:
                print(c, end='')
            line = line + c if c != '\r' else ''

    def command(self, cmd='', show=False):
        self.write(cmd + '\r')
        self.wait_prompt(show)


class QuickBoot(Uboot):
    def __init__(self, root, serial_port=None, ethernet=None):
        self.server = StaticServer(root=root)
        Uboot.__init__(self, serial_port)

    def __del__(self):
        self.server.close()
        self.server.join()

    def config_net(self):
        count = 0
        ip = None
        while count < 10.0 and ip is None:
            ip = get_enternet_ip()
            if ip == None:
                time.sleep(0.5)
                count += 0.5
        if ip == None:
            return
        ips = ip.address.split('.')
        ip3 = int(ips[3])
        ip3 += 1 if ip3 < 250 else -1
        ips[3] = str(ip3)
        board_ip = '.'.join(ips)

        self.command("setenv ipaddr " + board_ip, True)
        self.command("setenv netmask " + ip.netmask, True)
        self.command('setenv serverip ' + ip.address, True)
        self.command("ping " + ip.address, True)

    def boot(self):
        self.command("tftp ${fdt_addr} dtb", True)
        self.command("tftp initrd", True)
        self.command("bootefi 0x80080000", True)

    def flash_disk(self):
        stat = self.server.get_file_stat('disk_image')
        if stat:
            self.command("tftp 0x80080000 disk_image", True)
            self.command("mmc write 0x80080000 0 0x%x" % int(stat.st_size/512), True)

    def console(self):
        print("\n")
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        new_settings = termios.tcgetattr(self._port.fd)
        new_settings[3] = new_settings[3] & ~termios.ECHO
        fcntl.fcntl(self._port.fd, fcntl.F_SETFL,
                    fcntl.fcntl(self._port.fd, fcntl.F_GETFL) & ~os.O_NONBLOCK)

        new_settings[2] &= ~(termios.PARENB | termios.PARODD)
        new_settings[2] &= ~(termios.PARENB | termios.PARODD)
        new_settings[2] |= termios.CLOCAL
        termios.tcsetattr(self._port.fd, termios.TCSADRAIN, new_settings)
        tty.setraw(self._port.fd)

        tty.setraw(0)
        line = ''
        MAGIC = ['quit', 'exit']
        quit = False
        while not quit:
            r, _, _ = select.select([fd, self._port.fd], [], [])
            if fd in r:
                buf = os.read(0, 1)
                if buf in b'\r\n\x03':
                    line = ''
                else:
                    line += buf.decode()
                if line in MAGIC:
                    quit = True
                if line == '~b':
                    self.sendbreak()
                    line = ''
                if len(buf):
                    os.write(self._port.fd, buf)
            if self._port.fd in r:
                buf = os.read(self._port.fd, 4096)
                if len(buf):
                    os.write(1, buf)
        termios.tcsetattr(fd, termios.TCSANOW, old_settings)
        print("")


def main():
    root = {
        'disk_image': '/Users/zhiguo.zhu/works/conan/sel4-example/build/Release/disk.img',
        'uboot': '/Users/zhiguo.zhu/.conan/data/sel4-osf/develop/_/_/package/a5ad5696abf650a25eea8f377806b3d5fe234e6e/platform/rdb2/uboot-rdb2.bin',
        'initrd': '/Users/zhiguo.zhu/.conan/data/sel4-osf/develop/_/_/package/a5ad5696abf650a25eea8f377806b3d5fe234e6e/platform/rdb2/proc-image-arm-s32g',
        'dtb': '/Users/zhiguo.zhu/.conan/data/sel4-osf/develop/_/_/package/a5ad5696abf650a25eea8f377806b3d5fe234e6e/platform/rdb2/kernel.dtb',
    }
    boot = QuickBoot(root, None, "en4")
    boot.wait_prompt(True)
    boot.config_net()
    # boot.flash_disk()
    boot.boot()
    boot.console()


if __name__ == '__main__':
    main()
