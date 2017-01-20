from conans import ConanFile
import os
import fnmatch
from conans.tools import get, patch, SystemPackageTool
from conans import CMake


def apply_patches(source, dest):
    for root, dirnames, filenames in os.walk(source):
        for filename in fnmatch.filter(filenames, '*.patch'):
            patch_file = os.path.join(root, filename)
            dest_path = os.path.join(dest, os.path.relpath(root, source))
            patch(base_path=dest_path, patch_file=patch_file)


class OisConan(ConanFile):
    name = "OIS"
    description = "OIS (Object Oriented Input System) is a cross-platform library to deal with input devices such as keyboards, mice and joysticks"
    version = "1.3"
    folder = 'OIS-1-3'
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", 'CMakeLists-OIS.txt', 'patches*']
    url = "http://github.com/sixten-hilborn/conan-ois"
    license = "https://opensource.org/licenses/mit-license.php"

    def system_requirements(self):
        if self.settings.os == "Linux":
            installer = SystemPackageTool()
            installer.update()
            installer.install("libx11-dev")

    def source(self):
        get("https://github.com/wgois/OIS/archive/v1-3.zip")
        os.rename('CMakeLists-OIS.txt', '{0}/CMakeLists.txt'.format(self.folder))
        apply_patches('patches', self.folder)

    def build(self):
        self.makedir('_build')
        self.cbuild('_build')

    def makedir(self, path):
        if self.settings.os == "Windows":
            self.run("IF not exist {0} mkdir {0}".format(path))
        else:
            self.run("mkdir {0}".format(path))

    def cbuild(self, where, moar=''):
        cmake = CMake(self.settings)
        cd_build = 'cd ' + where
        self.run_and_print('%s && cmake .. %s %s' % (cd_build, cmake.command_line, moar))
        self.run_and_print("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        self.copy(pattern="*.h", dst="include/OIS", src="{0}/includes".format(self.folder))
        self.copy("*.lib", dst="lib", src="_build", keep_path=False)
        self.copy("*.a", dst="lib", src="_build", keep_path=False)
        self.copy("*.so", dst="lib", src="_build", keep_path=False)
        self.copy("*.dll", dst="bin", src="_build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['OIS']

    def run_and_print(self, command):
        self.output.warn(command)
        self.run(command)
