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
            if self.settings.arch == 'x86':
                installer.install("libx11-dev:i386")
            elif self.settings.arch == 'x86_64':
                installer.install("libx11-dev:amd64")

    def source(self):
        get("https://github.com/wgois/OIS/archive/v1-3.zip")
        os.rename('CMakeLists-OIS.txt', '{0}/CMakeLists.txt'.format(self.folder))
        apply_patches('patches', self.folder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_dir='_build')
        cmake.build()

    def package(self):
        self.copy(pattern="*.h", dst="include/OIS", src="{0}/includes".format(self.folder))
        self.copy("*.lib", dst="lib", src="_build", keep_path=False)
        self.copy("*.a", dst="lib", src="_build", keep_path=False)
        self.copy("*.so", dst="lib", src="_build", keep_path=False)
        self.copy("*.dll", dst="bin", src="_build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['OIS']
        if self.settings.os == 'Linux':
            self.cpp_info.libs.append('X11')
        elif self.settings.os == 'Macos':
            self.cpp_info.exelinkflags.extend([
                "-framework IOKit",
                "-framework Cocoa",
                "-framework Carbon"
            ])
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == 'iOS':
            self.cpp_info.exelinkflags.append("-framework UIKit")
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags

