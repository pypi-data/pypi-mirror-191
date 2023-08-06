#!/usr/bin/env python3

import argparse
import os
import inspect
import sys
import shutil
import platform
import pathlib
import signal
from collections import namedtuple, OrderedDict
import re
import json
from conannio import Simulate, parse_args, QuickBoot

try:
    import yaml
    from six import StringIO  # Python 2 and 3 compatible
    from conan.errors import ConanException
    from conans.client.conan_api import Conan
    from conans.client.output import ConanOutput
    from conans.client.userio import UserIO
    from conans.model.ref import ConanFileReference, PackageReference
    from conans.client.graph.printer import print_graph
    from conans.client.output import Color
    from conans.client.command import Command, Extender
    from conans.util.files import save, load
    from conans.cli.exit_codes import USER_CTRL_C, ERROR_SIGTERM
    conan_installed = True
except:
    def load(path, binary=False, encoding="auto"):
        """ Loads a file content """
        with open(path, 'rb') as handle:
            return handle.read()
    conan_installed = False

disable_recpes = ['nio-capi', 'stream-benchmarks', 'mbedtls', 'user-profile', 'stress-ng']
only_host_build = ['qemu', 'sel4-osf']


class ProfileData(namedtuple("ProfileData", ["profiles", "settings", "options", "env", "conf"])):
    def __bool__(self):
        return bool(self.profiles or self.settings or self.options or self.env or self.conf)
    __nonzero__ = __bool__


def git_to_http(url):
    return url.replace("git@", "https://").replace(":", "/")


def disable_output(func):
    def run(*args, **kwargs):
        args[0].conan_api.user_io = UserIO(out=ConanOutput(StringIO()))
        v = func(*args, **kwargs)
        args[0].conan_api.user_io = UserIO(out=args[0].conan_api.out)
        return v
    return run


def read_yaml_to_ordered_dict(yaml_path, object_pairs_hook=OrderedDict):
    Loader = yaml.Loader

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    with open(yaml_path) as stream:
        dict_value = yaml.load(stream, OrderedLoader)
        return dict_value


class Recipe:
    def __init__(self, recipe_path, user=None, channel=None):
        self.conan_api, _, _ = Conan.factory()
        self.conan_api.create_app()
        self.command = Command(self.conan_api)
        self.cwd = str(recipe_path)
        version = None

        yaml_file = pathlib.Path(self.cwd, "config.yml")
        if yaml_file.is_file():
            data = read_yaml_to_ordered_dict(yaml_file)
            for version, path in data["versions"].items():
                self.cwd = os.path.join(os.path.dirname(yaml_file), path["folder"])
                break
        self.full_conanfile = os.path.join(self.cwd, 'conanfile.py')
        self.conanfile = self.conan_api.app.loader.load_export(self.full_conanfile, None, version, None, None)
        self.standalone = self.conanfile.source.__qualname__ == 'ConanFile.source' or not (self.conanfile.conan_data and "sources" in self.conanfile.conan_data)
        self.partial_reference = self.conanfile.display_name + '@'
        if not (user is None and channel is None):
            self.partial_reference += f'{user}/{channel}'

        self.reference = ConanFileReference.loads(self.partial_reference)
        self.package = None
        self.build_mode = {
            True: self.reference.name in only_host_build,
            False: self.reference.name not in only_host_build
        }
        self.keep_source = False
        self.keep_build = False
        self.debug_bulld = False
        self.release_build = True
        self.force_build = False
        self.env_host = []

    @disable_output
    def export(self):
        self.conan_api.export(self.cwd, self.reference.name, self.reference.version, self.reference.user, self.reference.channel)

    def run(self, fake=False):
        if self.standalone:
            self.standalone_create(build_type="Debug" if self.debug_bulld else "Release", fake=fake)
            return True
        if self.build_mode[False]:
            if self.release_build and (self.force_build or not self.package.exist):
                self.create(build_type="Release", fake=fake)
            if self.debug_bulld and (self.force_build or not self.package.exist):
                self.create(build_type="Debug", fake=fake)
        if self.build_mode[True] and (self.force_build or not self.package.exist):
            self.create(profile_build='default', profile_host=None, build_type="Release", fake=fake)

    def upload(self, all, skip_upload):
        policy = "skip-upload" if skip_upload else None
        if self.reference.name == 'sel4-osf':
            all = False
        self.conan_api.upload(self.reference.name, remote_name="nio",
                              confirm=True, parallel_upload=True,  # integrity_check=True,
                              policy=policy, all_packages=all)

    def standalone_create(self, profile_build="default", profile_host="sel4", build_type="Release", fake=False):
        base_args = f'-if=build -pr:h=sel4 -pr:b=default -s build_type={build_type}'
        relpath_conanfile = os.path.relpath(self.full_conanfile)
        sel4_command = '-r=nio --build=missing ' + self.conanfile.sel4_sdk
        install_command = f'{base_args} -r=nio -g json --build=missing {relpath_conanfile} {self.partial_reference}'
        build_command = f'-if=build {relpath_conanfile}'
        export_command = f'{base_args} -f {relpath_conanfile}'
        if fake:
            print("conan install", sel4_command)
            print("conan install", install_command)
            print("conan build", build_command)
            print("conan export-pkg", export_command)
        else:
            self.command.install(sel4_command.split())
            self.command.install(install_command.split())
            self.command.build(build_command.split())
            self.command.export_pkg(export_command.split())

    def create(self, profile_build="default", profile_host="sel4", build_type="Release", fake=False):
        args = ['-r=nio', '-tf=None', '--build=missing', f'-s build_type={build_type}']
        for e in self.env_host:
            args.append(' -e ' + e)
        if self.reference.name in only_host_build and self.force_build:
            args.append("-e source=1")
        if self.keep_source:
            args.append('-ks')
        if self.keep_build:
            args.append('-kb')
        args.append(f'-pr:b={profile_build}')
        if profile_host:
            args.append('-pr:h=' + profile_host)
        reference_str = str(self.reference)
        if self.reference.user is None and self.reference.channel is None:
            reference_str += '@'
        conanfile = os.path.relpath(self.full_conanfile)
        args.extend([f'--build={self.reference.name}', f'{conanfile}', f'{reference_str}'])
        args = ' '.join(args)
        if fake:
            print("conan create", args)
        else:
            self.command.create(args.split())

    def install(self, profile_build="default", profile_host="sel4", build_type="Release"):
        settings = ["build_type={}".format(build_type)]
        profile_build = ProfileData(profiles=[profile_build], settings=settings,
                                    options=None, env=None, conf=None) if profile_build else None
        self.conan_api.install(remote_name="nio",
                               settings=["build_type={}".format(build_type)],
                               install_folder="build",
                               profile_names=[profile_host],
                               profile_build=profile_build,
                               cwd=self.cwd,
                               build=["missing"])

    @disable_output
    def info(self):
        if self.standalone:
            FakePackage = namedtuple('FakePackage', ['exist', 'dependencies'])
            self.package = FakePackage(False, [])
            return self.package

        if self.package is None:
            profile_build = ProfileData(profiles=['default'], settings=None,
                                        options=None, env=None, conf=None) if not self.build_mode[True] else None
            try:
                self.deps_graph, _ = self.conan_api.info(self.partial_reference, "nio", build=[],
                                                         profile_names=['default' if self.build_mode[True] else 'sel4'],
                                                         profile_build=profile_build)
            except:
                self.deps_graph, _ = self.conan_api.info(self.partial_reference, "nio", build=[],
                                                         profile_build=profile_build)

            for node in self.deps_graph.nodes:
                if str(node.ref) == str(self.reference):
                    self.package = node
                    layout = self.conan_api.app.cache.package_layout(self.reference)
                    self.package.exist = layout.package_exists(PackageReference(self.reference, self.package.package_id))
                    break

        return self.package

    def remove(self, remove_source):
        args = self.conanfile.name + ' -f'
        args += ' -s' if remove_source else ""
        self.command.remove(args.split())

    def update_depends_version(self):
        def change_version(ver):
            reference = ConanFileReference.loads(ver)
            reference = reference._replace(user=self.reference.user, channel=self.reference.channel)
            return str(reference)

        def update_version(dep_list):
            return [change_version(dep) for dep in dep_list]

        def fix_requires(requires_name):
            need_save = False
            if requires_name in conandata_yaml:
                need_save = True
                requires = conandata_yaml[requires_name]
                if type(requires) == dict:
                    new_requires = {}
                    for v, d in requires.items():
                        new_requires[v] = update_version(d)
                    conandata_yaml[requires_name] = new_requires
                elif type(requires) == list:
                    conandata_yaml[requires_name] = update_version(requires)
            return need_save


        conandata_yaml_file = os.path.join(self.cwd, 'conandata.yml')
        if not os.path.exists(conandata_yaml_file):
            return
        with open(conandata_yaml_file, encoding='utf-8') as f:
            conandata_yaml = yaml.full_load(f)
            need_save1 = fix_requires('requires')
            need_save2 = fix_requires('tool_requires')
            if need_save1 or need_save2:
                with open(conandata_yaml_file, 'w', encoding='utf-8') as f:
                    yaml.dump(conandata_yaml, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


class SeL4Center:
    conan_artifactory = 'https://artifactory-cn.nevint.com/artifactory/api/conan/ds-nvos-sel4-sdk-local'
    conan_user = 'ds.conan.public.s'
    conan_api_key = 'AKCp8nyrzLRSN1Lv3UNjddnT4uA1XD5Gcg8w5fpuAVDevZwKot9RKT3Ebmh3RxwEc9JtNPLkn'

    def __init__(self) -> None:
        self.conan_api, _, _ = Conan.factory()
        self.conan_api.create_app()
        self.builded = {True: [], False: []}
        self.recipes = {}
        self.cwd = os.getcwd()
        self.sdk_version, self.channel = self.get_version()
        self.cache_exists = self.init()

    def get_version(self):
        try:
            v = self.conan_api.app.cache.config.get_item('sel4sdk.version')
            c = self.conan_api.app.cache.config.get_item('sel4sdk.channel')
        except:
            v, c = None, None
        return v, c

    def set_version(self, sdk_version, channel):
        if sdk_version == '_' or channel == '_' or not sdk_version or not channel:
            if self.conan_api.app.cache.config.has_section('sel4sdk'):
                self.conan_api.app.cache.config.rm_item('sel4sdk')
                self.sdk_version, self.channel = None, None
        else:
            self.conan_api.app.cache.config.set_item('sel4sdk.version', sdk_version)
            self.conan_api.app.cache.config.set_item('sel4sdk.channel', channel)
            self.sdk_version, self.channel = sdk_version, channel

    @disable_output
    def raw_new(self, name, version, template, defines=None, basedir="recipes", conandata=None):
        def new_config(version, folder="all"):
            return f"""versions:\n  "{version}":\n    folder: {folder}\n"""

        reference = "%s/%s" % (name, version)
        template = os.path.join(os.path.dirname(os.path.realpath(__file__)), "docs/package_templates", template)

        recipes_path = pathlib.Path(basedir)

        self.conan_api.new(reference, cwd=recipes_path, template=template, defines=defines)
        if conandata:
            save(recipes_path.joinpath('all/conandata.yml'), conandata)
            save(recipes_path.joinpath('config.yml'), new_config(version))
        return recipes_path

    def new(self, name, version, url, branch, source=False, basedir="recipes", conandata=None):
        def new_conandata(version, url, branch=None, commitid=None):
            text = f"""sources:\n  "{version}":\n    url: "{url}"\n"""
            if branch:
                text += f"""    branch: "{branch}" \n"""
            if commitid:
                text += f"""    commit: "{commitid}" \n"""
            return text

        name = name or os.path.basename(url).split(".")[0]
        version = version or branch

        if source:
            recipes_path = pathlib.Path(url)
            conanfile = recipes_path.joinpath('conanfile.py')
            if not conanfile.exists():
                packages = set()
                for cmake_list in recipes_path.rglob("CMakeLists.txt"):
                    text = cmake_list.read_text()
                    for package in re.findall(r'.*find_package\W*([\w]*)', text):
                        packages.add("""        self.requires("%s/???")""" % package)

                defines = {"requirements": "\n".join(packages) or "        pass"}
                self.raw_new(name, version, "bare_source", defines, str(recipes_path), conandata)
                print("New successfully:", recipes_path)
            else:
                print("Already exists:", os.path.realpath(conanfile))
        else:
            template = None
            recipes_path = pathlib.Path(os.path.join(basedir, name))
            git_src = recipes_path.joinpath("src")
            git_command = 'git clone %s %s -b %s %s' % (url, "--depth=1" if not source else "", version, git_src)
            self.conan_api.app.runner(git_command)
            if list(git_src.rglob("configure")) or list(git_src.rglob("autogen.sh")):
                template = "autotools"
            elif list(git_src.rglob("CMakeLists.txt")):
                template = "cmake"
            shutil.rmtree(git_src)
            defines = {"nio_homepage": git_to_http(url)}
            conandata = conandata or new_conandata(version, url, branch)
            self.raw_new(name, version, template, defines, str(recipes_path), conandata)
            print("New successfully:", recipes_path)

        return True

    def add_recipe_path(self, recipe_path, export=True):
        recipe = None
        if recipe_path.joinpath('config.yml').is_file():
            recipe = Recipe(recipe_path, self.sdk_version, self.channel)
            if recipe.reference.name in disable_recpes:
                return
            if export:
                recipe.export()
        if recipe_path.joinpath('conanfile.py').is_file():
            recipe = Recipe(recipe_path, self.sdk_version, self.channel)
        if recipe:
            self.recipes[recipe.reference.name] = recipe

    def explore(self, export=True):
        if self.recipes:
            return
        recipe_root = pathlib.Path(self.cwd, "recipes")

        if recipe_root.is_dir():
            for recipe_path in recipe_root.iterdir():
                self.add_recipe_path(recipe_path, export)
            # self.generate_simple_recipes(export)
        else:
            recipe_root = pathlib.Path(self.cwd)
            self.add_recipe_path(recipe_root, export)

    def build_one(self, recipe, deps=True, host_build=False, fake=False):
        dependencies = recipe.info().dependencies
        if len(dependencies) > 0 and deps:
            for dep in dependencies:
                if dep.dst.name not in self.recipes:
                    recipe.install()
                    break
                sub_recipe = self.recipes[dep.dst.name]
                # All dependent packages force the build
                # sub_recipe.force_build = recipe.force_build
                self.build_one(sub_recipe, host_build=dep.build_require or host_build, fake=fake)
            self.build_one(recipe, False, host_build, fake=fake)
        elif recipe.reference not in self.builded[host_build]:
            self.builded[host_build].append(recipe.reference)
            recipe.build_mode[host_build] = True
            recipe.run(fake)

    def get_recipes(self, recipes_name=None):
        if recipes_name:
            nofound = 0
            for name in recipes_name:
                if name not in self.recipes:
                    print("The recipe was not found:", name)
                    nofound += 1
            if nofound > 0:
                exit(1)
        else:
            recipes_name = list(self.recipes.keys())
        return recipes_name

    def upload(self, recipes_names=None, all=True, skip_upload=False):
        if not self.cache_exists:
            return False
        self.explore(False)
        recipes_names = self.get_recipes(recipes_names)
        for name in recipes_names:
            self.recipes[name].upload(all, skip_upload)
        return True

    def build(self, recipes_names=None, keep_source=False, keep_build=False, debug_bulld=True, release_build=True, deps=True, force=False, fake=False, env_host=[]):
        if not self.cache_exists:
            return False
        self.explore()
        recipes_names = self.get_recipes(recipes_names)

        for name in recipes_names:
            v = self.recipes[name]
            self.conan_api.out.write("Checking: ")
            self.conan_api.out.write(str(v.reference) + ' ', Color.BRIGHT_CYAN)
            info = v.info()
            if info.exist:
                self.conan_api.out.writeln("Cache", Color.GREEN)
            else:
                self.conan_api.out.writeln("Missing", Color.YELLOW)
            v.keep_source = keep_source
            v.keep_build = keep_build
            v.debug_bulld = debug_bulld
            v.release_build = release_build
            v.force_build = force
            v.env_host = env_host
        for name in recipes_names:
            if name not in only_host_build:
                sel4_osf = self.recipes.get('sel4-osf')
                if sel4_osf and not sel4_osf.info().exist:
                    self.build_one(sel4_osf, deps=deps, host_build=True, fake=fake)
                break
        for name in recipes_names:
            self.build_one(self.recipes[name], deps=deps, host_build=name in only_host_build, fake=fake)
        return True

    def info(self, recipes_names, detailed=False, show_package_id=False):
        if not self.cache_exists:
            return False
        self.explore()
        recipes_names = self.get_recipes(recipes_names)

        count = 1
        keys = sorted(self.recipes.keys())

        for key in keys:
            if key not in recipes_names:
                continue
            recipe = self.recipes[key]
            info = recipe.info()
            if detailed:
                self.conan_api.out.writeln("%s:" % str(recipe.reference), Color.RED)
                print_graph(recipe.deps_graph, self.conan_api.out)
            else:
                package_id = (":" + info.package_id) if show_package_id else ""
                self.conan_api.out.write("%3d %s%s - " % (count, recipe.reference, package_id), Color.BRIGHT_CYAN)
                if info.exist:
                    self.conan_api.out.writeln('Cache', Color.BRIGHT_GREEN)
                else:
                    self.conan_api.out.writeln('Missing', Color.BRIGHT_YELLOW)
            count += 1
        return True

    @disable_output
    def conan_config(self, name, passwd):
        try:
            if name and passwd:
                self.conan_api.config_init(True)
                self.conan_api.remote_add('nio', self.conan_artifactory)
                self.conan_api.user_set(name, "nio")
                self.conan_api.authenticate(name, passwd, 'nio')
        except ConanException as E:
            print(E)
            raise E
        successful = self.conan_api.users_list('nio')['remotes'][0]['authenticated']
        if successful:
            print("Initialization successful!")
        return successful

    @disable_output
    def init(self):
        self.conan_api.config_init(False)
        try:
            info = self.conan_api.users_list('nio')
        except:
            self.conan_api.remote_add('nio', self.conan_artifactory)
            self.conan_api.user_set(self.conan_user, "nio")
            info = self.conan_api.users_list('nio')
        for remote in info['remotes']:
            if remote['name'] == 'nio' and not remote['authenticated']:
                self.conan_api.authenticate(self.conan_user, self.conan_api_key, 'nio')
                break
        return self.conan_api.users_list('nio')['remotes'][0]['authenticated'] == True

    def generate_simple_recipes(self, export=True):
        simple_recipes_conf = pathlib.Path(self.cwd, "recipes/simple_recipes.yml")
        basedir = pathlib.Path(self.cwd, "simple_recipes")
        if not simple_recipes_conf.is_file():
            return
        with open(simple_recipes_conf) as stream:
            simple_recipes = yaml.load(stream, Loader=yaml.FullLoader)
            for name, recipe in simple_recipes.items():
                if name in disable_recpes:
                    continue
                recipe_path = basedir.joinpath(name)
                for version, info in recipe['sources'].items():
                    defines = {"nio_homepage": git_to_http(info['url'])}
                    template = recipe['template']
                    del recipe['template']
                    recipe_path = self.raw_new(name, version, template=template, basedir=str(recipe_path), defines=defines, conandata=yaml.dump(recipe))
                    self.add_recipe_path(recipe_path, export)
                    break

    def remove(self, recipes_names, src=False):
        if not self.cache_exists:
            return False
        self.explore(False)
        recipes_names = self.get_recipes(recipes_names)
        for key in sorted(self.recipes.keys()):
            if key not in recipes_names:
                continue
            self.recipes[key].remove(src)
        return True

    def update_depends_version(self):
        if not self.cache_exists:
            return False
        self.explore(False)
        recipes_names = self.get_recipes()
        for name in recipes_names:
            self.recipes[name].update_depends_version()

class DiskRunner:
    def __init__(self):
        self.output_data = {}
        user_presets_path = os.path.join(os.getcwd(), "CMakeUserPresets.json")
        if not os.path.exists(user_presets_path):
            return
        data = json.loads(load(user_presets_path))
        for include in data["include"]:
            if os.path.exists(include):
                cmake_presets = json.loads(load(include))
                configure_preset = cmake_presets["configurePresets"][0]

                output_file = os.path.join(configure_preset.get("binaryDir"), 'output.yml')
                if os.path.exists(output_file):
                    self.output_data[configure_preset['name']] = read_yaml_to_ordered_dict(output_file)

    def add_argument(self, parser):
        for _, output in self.output_data.items():
            if output.get('platform') == 'qemu-arm-virt':
                parse_args(parser)
                return
        parser.add_argument('-u', '--serial-device', default=None,
                            help='The serial device connected to the hardware, not set to auto-find.')
        parser.add_argument('-e', '--ethernet', default=None,
                            help='The name of the Ethernet device connected to the hardware, not set to auto-find.')
        parser.add_argument('-w', '--write-disk', default=False,
                            action='store_false', help='Write disk.img to the SD card')

    def run_disk(self, args):
        data = self.output_data[args.build_type]
        if not data:
            print(f"Disk image file not found, please run 'niobuild build' to build.")
        if data['platform'] == 'qemu-arm-virt':
            if args.disk_image[0] != '/':
                args.disk_image = data['disk_image']
            if args.qemu_sim_initrd_file[0] != '/':
                args.qemu_sim_initrd_file = data['initrd']
            Simulate(args).run()
        else:
            boot = QuickBoot(data, args.serial_device, args.ethernet)
            boot.wait_prompt(True)
            boot.config_net()
            if args.write_disk:
                boot.flash_disk()
            boot.boot()
            boot.console()
        return True


class DockerRunner(object):
    def __init__(self, images=None, args=''):
        self.DOCKER_IMAGE_NAME = images or "artifactory.nevint.com:5022/sel4/ubuntu-" + platform.machine() + ":latest"
        USER = os.getlogin()
        UID = os.getuid()
        GID = os.getgid()
        HOME = os.path.expanduser('~')
        CWD = os.getcwd()
        PASSWD_FILE = os.path.join(HOME, '.local/passwd')
        with open(PASSWD_FILE, 'w', encoding='utf-8') as file:
            file.write(f"{USER}:x:{UID}:{GID}:,,,:{HOME}:/bin/bash")
        COMMON_VOLUMES = f"--volume={CWD}:{CWD} --volume={PASSWD_FILE}:/etc/passwd:ro --volume={HOME}:{HOME} --volume=/dev/null:{HOME}/.bashrc --volume=/dev/null:{HOME}/.profile"
        CURRENT_USER = f"--user={UID}:{GID}"
        self.docker_cmd = f"docker run {args} -t --rm {COMMON_VOLUMES} {CURRENT_USER} --workdir={CWD} {self.DOCKER_IMAGE_NAME} "

    def run(self, args):
        print("Running in Docker %s ..." % self.DOCKER_IMAGE_NAME)
        if isinstance(args, list):
            args = ' '.join(args)
        os.system("docker pull " + self.DOCKER_IMAGE_NAME)
        print(self.docker_cmd + args)
        os.system(self.docker_cmd + args)


class BuildCommand:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-d', '--docker', default=False,
                                 action='store_true', help='Run the build.py in a docker environment')
        self.parser.add_argument('-i', '--docker-image', default=None, help='Customized docker image')
        self.parser.add_argument('--docker-args', default='',
                                    help='Add argmuemt for Docker')

        self.subparsers = self.parser.add_subparsers()

        for m in inspect.getmembers(self, predicate=inspect.ismethod):
            method_name, method = m[0], m[1]
            if method_name.startswith("cmd_"):
                method()

    def run(self):
        opt = self.parser.parse_args()
        if 'func' not in opt:
            self.parser.print_help()
            exit(1)
        if opt.func.__name__ == "conan_shell" or opt.docker_image:
            opt.docker = True

        if (not opt.docker and not os.path.exists("/.dockerenv") and shutil.which(b'docker')) \
                and (not conan_installed or not shutil.which("aarch64-linux-gnu-gcc")):
            opt.docker = True
        if os.path.exists("/.dockerenv") or not opt.docker:
            if conan_installed:
                if not opt.func(opt):
                    print("Using conan for the first time, enter your username and password to login 'https://artifactory-cn.nevint.com'")
                    if opt.docker:
                        print(f"{sys.argv[0]} --docker init <username> <password>\n ")
                    else:
                        print(f"{sys.argv[0]} init <username> <password>\n ")
                    exit(1)
            else:
                print("No conan is found, install conan or run it in a docker with the --docker")
                print(f'    {sys.argv[0]} --docker {" ".join(sys.argv[1:])}')
        else:
            docker_image, docker_args = opt.docker_image, opt.docker_args
            if hasattr(opt, 'qemu_gdbserver') and opt.qemu_gdbserver == True:
                docker_args += ' -p 1234:1234'
            if opt.func.__name__ in ["conan_shell", "conan_run"]:
                docker_args += ' -i'
            argv = sys.argv[:1]
            for key in self.subparsers.choices.keys():
                for j in range(len(sys.argv)):
                    if sys.argv[j] == key:
                        argv.extend(sys.argv[j:])
                        break
            DockerRunner(docker_image, docker_args).run(argv)

    def cmd_upload(self):
        def conan_upload(args):
            return SeL4Center().upload(args.recipes, args.all, args.skip_upload)

        upload_parser = self.subparsers.add_parser(
            'upload', help="Uploads a recipe and binary packages to a remote.")
        upload_parser.set_defaults(func=conan_upload)
        upload_parser.add_argument('-a', '--all', default=False,
                                   action='store_true', help='Upload both package recipe and packages')
        upload_parser.add_argument('--skip-upload', default=False,
                                   action='store_true', help='Do not upload anything, just run the checks and the compression')
        upload_parser.add_argument('recipes', default=[], nargs='*',
                                   help="The name of recipes, you can specify multiple recipes")

    def cmd_login(self):
        def conan_login(args):
            return SeL4Center().conan_config(args.username, args.password)

        login_parser = self.subparsers.add_parser('init', help="Initialize the configuration of the seL4-sdk.")
        login_parser.set_defaults(func=conan_login)
        login_parser.add_argument('-u' '--username', dest="username",
                                  help='Username you want to use. If no name is provided it will show the current user')
        login_parser.add_argument('-p', '--password', dest="password",
                                  help='User password. Use double quotes if password with spacing, and escape quotes if existing. If empty, the password is requested interactively (not exposed)')

    def cmd_build(self):
        def conan_build(args):
            r = SeL4Center()
            succeed = r.build(args.recipes, deps=args.disable_depend,
                              keep_source=args.keep_source, keep_build=args.keep_build,
                              debug_bulld=args.enable_debug, force=args.force,
                              release_build=not args.disable_release,
                              fake=args.fake_build, env_host=args.env_host)
            if succeed and args.upload:
                succeed = r.upload(args.recipes)
            return succeed

        build_parser = self.subparsers.add_parser(
            'build', help="Builds a binary package for a recipe (conanfile.py).")
        build_parser.set_defaults(func=conan_build)
        build_parser.add_argument('-d', '--enable-debug', default=False,
                                  action='store_true', help='Enable Debug build')
        build_parser.add_argument('--disable-release', default=False,
                                  action='store_true', help='Disable Release build')
        build_parser.add_argument('-dd', '--disable-depend', default=True,
                                  action='store_false', help='The package dependency is not rebuilt')
        build_parser.add_argument('-f', '--force', default=False,
                                  action='store_true', help="Force rebuild the package and all dependent packages, using '--disable-depend' does not build the dependent package")
        build_parser.add_argument('-k', '-ks', '--keep-source', default=False,
                                  action='store_true', help='Do not remove the source folder in the local cache, even if the recipe changed. Use this for testing purposes only')
        build_parser.add_argument('-kb', '--keep-build', default=False,
                                  action='store_true', help='Do not remove the build folder in local cache. Implies --keep-source. Use this for testing purposes only')
        build_parser.add_argument('-u', '--upload', default=False,
                                  action='store_true', help="After the build is successful, upload to a remote")
        build_parser.add_argument('-e', '--env', nargs=1, dest="env_host", default=[],
                                  action=Extender if conan_installed else None, help="Environment variables that will be set during the package build (host machine). e.g.: -e CXX=/usr/bin/clang++")
        build_parser.add_argument('--fake-build', default=False,
                                  action='store_true', help="This is a fake build that just shows the build process")
        build_parser.add_argument('recipes', default=[], nargs='*',
                                  help="The name of recipes, you can specify multiple recipes")

    def cmd_info(self):
        def conan_info(args):
            return SeL4Center().info(args.recipes, args.detailed, args.package_id)

        info_parser = self.subparsers.add_parser(
            'info', help="Gets information about the dependency graph of a recipe.")
        info_parser.set_defaults(func=conan_info)
        info_parser.add_argument('-p', '-id', '--package-id', default=False,
                                 action='store_true', help="Show the package_id of recipe")
        info_parser.add_argument('-a', '--detailed', default=False,
                                 action='store_true', help="After the build is successful, upload to a remote")
        info_parser.add_argument('recipes', default=[], nargs='*',
                                 help="The name of recipes, you can specify multiple recipes")

    def cmd_new(self):
        def conan_new(args):
            return SeL4Center().new(None, None, args.url, args.branch, args.source)

        new_parser = self.subparsers.add_parser(
            'new', help="Creates a new package recipe template with a 'conanfile.py' and optionally.")
        new_parser.set_defaults(func=conan_new)
        new_parser.add_argument('-s', '--source', default=False,
                                action='store_true', help="Create a package with embedded sources")
        new_parser.add_argument('-b', '--branch', default=None, required=True,
                                help="A branch of the software's git repository")
        new_parser.add_argument('-u', '--url', default=None, required=True,
                                help="A git repository or A local directory, if use the -s argument, It is a directory that already exists")

    def cmd_remove(self):
        def conan_remove(args):
            return SeL4Center().remove(args.recipes, args.src)

        parser = self.subparsers.add_parser('remove', help="Clear local recipes.")
        parser.set_defaults(func=conan_remove)
        parser.add_argument('recipes', default=[], nargs='*',
                            help="The name of recipes, you can specify multiple recipes")
        parser.add_argument('-s', '--src', default=False,
                            action='store_true', help="Remove source folders")

    def cmd_shell(self):
        def conan_shell(args):
            if not args.command:
                args.command.append("/bin/bash")
            os.system(" ".join(args.command))
            return True

        shell_parser = self.subparsers.add_parser(
            'shell', help="Execute Docker's shell commands.")
        shell_parser.set_defaults(func=conan_shell)
        shell_parser.add_argument('command', default=[], nargs='*',
                                  help="shell command, For example: ls")

    def cmd_version(self):
        def conan_version(args):
            r = SeL4Center()
            if not args.sel4_sdk_version and not args.release_candidate:
                r.conan_api.out.write("seL4-SDK version: ")
                r.conan_api.out.write(r.sdk_version, Color.BRIGHT_GREEN)
                r.conan_api.out.write(", Release Candidate: ")
                r.conan_api.out.writeln(r.channel or 'None' + ' ', Color.BRIGHT_GREEN)
            elif args.sel4_sdk_version and args.release_candidate:
                r.set_version(args.sel4_sdk_version, args.release_candidate)
            else:
                parser.print_help()
                exit(0)
            if args.update_recipes:
                r.update_depends_version()
            return True

        parser = self.subparsers.add_parser('version', help="show or set the version of the seL4-SDK.")
        parser.set_defaults(func=conan_version)
        parser.add_argument('-v', '--sel4-sdk-version', default=None,
                            help="The major version of seL4-SDK, e.g.: v0.0.8")
        parser.add_argument('-c', '--release-candidate', default=None,
                            help="Release candidate for seL4-SDK, e.g.: rc01")
        # TODO:
        # parser.add_argument('-g', '--use-git-branch', default=None,
        #                         help="Set the version by git's branch")
        parser.add_argument('-u', '--update-recipes', default=False,
                            action='store_true', help="Update all dependent versions of recipes")

    def cmd_run(self):
        runer = DiskRunner()
        def conan_run(args):
            return runer.run_disk(args)

        parser = self.subparsers.add_parser('run', help="Run the seL4 OS.")
        parser.add_argument("build_type", choices=["release", "debug"],
                            help="Run seL4 of the release/debug type")
        parser.set_defaults(func=conan_run)
        runer.add_argument(parser)


    def cmd_flash(self):
        def sel4_flash(args):
            print('Please look forward to it.')
            return True
        parser = self.subparsers.add_parser('flash', help="Flash disk.img to the hardware.")
        parser.set_defaults(func=sel4_flash)


def main():
    def ctrl_c_handler(_, __):
        print('You pressed Ctrl+C!')
        sys.exit(USER_CTRL_C)

    def sigterm_handler(_, __):
        print('Received SIGTERM!')
        sys.exit(ERROR_SIGTERM)

    signal.signal(signal.SIGINT, ctrl_c_handler)
    signal.signal(signal.SIGTERM, sigterm_handler)
    BuildCommand().run()


if __name__ == "__main__":
    main()
