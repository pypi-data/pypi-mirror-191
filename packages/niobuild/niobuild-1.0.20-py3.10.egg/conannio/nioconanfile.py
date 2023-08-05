
from conan import ConanFile
from conan.tools.files import get
from conan.errors import ConanInvalidConfiguration
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
import os
import yaml
import pathlib

required_conan_version = ">=1.50.0"


class NioConanFile(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}

    platform = "qemu-arm-virt" # Start qemu with the simulate program to run seL4
    # platform = "rdb2"          # Generate disk.img to support S32G-rdb2 boot
    # platform = "vdf"           # Generate disk.img to support S32G-VDF boot

    def init(self):
        self.sel4_sdk = self.conan_data.get('sel4')
        if '@' not in self.sel4_sdk:
            self.sel4_sdk += '@'

    def layout(self):
        cmake_layout(self)

    def generate(self):
        CMakeToolchain(self).generate()
        CMakeDeps(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.disk_image()

    def package_info(self):
        self.user_info.deploy = self.runtime_deploy()
        self.user_info.sel4_sysroot = self.conf.get("tools.build:sel4_sysroot")

    def apply_conandata_requires(self, name, filter=None):
        def _f(): pass
        filter_func = lambda name : True
        if isinstance(filter, dict):
            filter_func = lambda name : filter.get(name, False)
        elif isinstance(filter, type(_f)):
            filter_func = filter

        requires = self.conan_data.get(name)
        if requires:
            if name == 'requires':
                requires_func = self.requires
            elif name == 'tool_requires':
                requires_func = self.tool_requires
            else:
                raise ConanInvalidConfiguration("name must be 'requires' or 'tool_requires' ")

            if isinstance(requires, dict):
                version = self.version if self.version else list(requires.keys())[0]
                entries = requires.get(version, [])
            elif isinstance(requires, list):
                entries = requires
            else:
                raise ConanInvalidConfiguration("conandata.yml 'patches' should be a list or a dict {version: list}")
            for it in entries:
                if filter_func(it.split('/')[0]):
                    requires_func(it)

    def requirements(self):
        self.apply_conandata_requires('requires')

    def build_requirements(self):
        self.apply_conandata_requires('tool_requires')

    def source(self):
        try:
            info = self.conan_data['sources'][self.version]
            url = info['url']
            if url[:4] == 'git@':
                branch = info.get('branch', self.version)
                if 'commit' in info and info['commit']:
                    self.run("git clone %s %s" % (url, self.source_folder))
                    self.run("cd %s && git checkout %s -b compile_commit && cd -" % (self.source_folder, info['commit']))
                else:
                    self.run("git clone --depth 1 %s -b %s %s" % (url, branch, self.source_folder))
            else:
                get(self, **info, destination=self.source_folder, strip_root=True)
        except:
            raise ConanInvalidConfiguration("The code for the package cannot be downloaded.")

    def runtime_deploy(self, base_path=None):
        import pathlib
        deploy_files = []
        deploy_match = self.conan_data.get('deploy')
        if deploy_match:
            if 'files' not in deploy_match and 'install_script' not in deploy_match:
                version = self.version if self.version else list(deploy_match.keys())[0]
                deploy_match = deploy_match.get(version, [])
            package_folder = pathlib.Path(base_path or self.package_folder)
            for deploy in deploy_match:
                for file in deploy_match[deploy]:
                    for fn in package_folder.glob(file):
                        deploy_files.append(str(fn.relative_to(package_folder)))

        return deploy_files

    def disk_image(self, images_output="disk.img"):
        def package_to_files(prefix, packages):
            files = []
            for p in packages:
                if p == self.name:
                    deploy = self.runtime_deploy()
                    rootpath = self.package_folder
                else:
                    deploy = eval(self.deps_user_info[p].deploy)
                    rootpath = self.deps_cpp_info[p].rootpath
                for d in deploy:
                    fn = os.path.join(rootpath, d)
                    if os.path.exists(fn):
                        files.append(fn + '|' + os.path.join(prefix, os.path.dirname(d)))
            return ":".join(files)

        def part_args(part, value):
            platform_dir = f'{sel4_sysroot}/platform/{self.platform}'
            if part == 'uboot':
                value['paths'] = f'{platform_dir}/uboot-{self.platform}.bin'
            elif part == 'boot':
                value['paths'] = f'{platform_dir}/images'
            elif part == 'root':
                value['paths'] = f'{platform_dir}/root_image'

            if 'files' in value:
                value['paths'] = '|'.join(value['files'])
            if 'packages' in value:
                prefix = value.get('prefix', '/usr')
                packages_files = package_to_files(prefix, value['packages'])
                if packages_files:
                    if 'paths' in value:
                        packages_files += ':' + value['paths']
                    value['paths'] = packages_files
                del value['packages']
            args = ",".join([k+'='+str(v) for k, v in value.items()])
            return f"part={part},{args}"

        sel4_sysroot = self.conf.get("tools.build:sel4_sysroot")
        if sel4_sysroot == None:
            raise ConanInvalidConfiguration("seL4-osf did not install successfully, reinstall the seL4-osf package.")
        if 'partitions' not in self.conan_data:
            return

        partitions = self.conan_data['partitions']
        command = f'python3 {sel4_sysroot}/tools/disk_gen.py --fs DISK --output {images_output} --compiler {sel4_sysroot}/bin/aarch64-sel4-gcc --strip=--keep-file-symbols'

        parts = [part_args(part, value) for part, value in partitions.items()]
        parts.append('gpt,format=raw,paths={sel4_sysroot}/platform/{self.platform}/uboot-{self.platform}.bin')
        command += ' --param "' + ";".join(parts) + '"'

        ld_paths = [os.path.join(sel4_sysroot, 'lib'), os.path.join(self.package_folder, 'lib')]
        for _, dep in self.deps_cpp_info.dependencies:
            ld_paths.extend(dep.lib_paths)
        if ld_paths:
            command += ' --ld_paths "' + ";".join(ld_paths) + '"'

        self.run(command)
        if self.platform == 'qemu-arm-virt':
            simulate = os.path.join(self.build_folder, "simulate")
            if os.path.exists(simulate) or os.path.islink(simulate):
                os.unlink(simulate)
            os.symlink(os.path.join(sel4_sysroot, "bin/simulate"), simulate)
        output = {
            'platform': self.platform,
            'sel4_sysroot': sel4_sysroot,
            'disk_image': os.path.join(self.build_folder, images_output),
        }
        platform_path = pathlib.Path(sel4_sysroot, 'platform', self.platform)
        for uboot in platform_path.rglob("uboot*.bin"):
            output['uboot'] = str(uboot)

        for initrd in platform_path.rglob("proc-image*"):
            output['initrd'] = str(initrd)
        for dtb in platform_path.rglob("kernel.dtb"):
            output['dtb'] = str(dtb)

        with open(os.path.join(self.build_folder, 'output.yml'), 'w', encoding='utf-8') as f:
            yaml.dump(output, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
