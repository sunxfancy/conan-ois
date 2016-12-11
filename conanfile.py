from conans import ConanFile
import os
import glob
from conans.tools import get
from conans import CMake


class OisConan(ConanFile):
    name = "OIS"
    version = "1.3"
    folder = 'OIS-1-3'
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = ["CMakeLists.txt", 'CMakeLists-OIS.txt']
    url="http://github.com/sixten-hilborn/conan-ois"
    license="https://opensource.org/licenses/mit-license.php"
            
    def source(self):
        get("https://github.com/wgois/OIS/archive/v1-3.zip")
        os.rename('CMakeLists-OIS.txt', '{0}/CMakeLists.txt'.format(self.folder))

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            pass         
        else:
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
        self.output.warn('%s && cmake .. %s %s' % (cd_build, cmake.command_line, moar))
        self.run('%s && cmake .. %s %s' % (cd_build, cmake.command_line, moar))
        self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))


    def package(self):
        self.copy(pattern="*.h", dst="include/OIS", src="{0}/includes".format(self.folder), keep_path=False)
        self.copy("*.lib", dst="lib", src="_build/lib", keep_path=False)
        self.copy("*.a", dst="lib", src="_build/lib", keep_path=False)
        self.copy("*.dll", dst="bin", src="_build/bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['OIS']
