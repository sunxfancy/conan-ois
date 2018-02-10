from conans.model.conan_file import ConanFile
from conans import CMake
import os


############### CONFIGURE THESE VALUES ##################
default_user = "sunxfancy"
default_channel = "ci"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)


class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "OIS/1.3@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.so*", dst="bin", src="lib")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        self.run("cd bin && .%sexample" % (os.sep))
