from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "memsharded")

class ZMQTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libzmq/4.1.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        print "Running test"
        os.chdir("bin")
        server = ".%sserver" % os.sep
        import subprocess
        pid = subprocess.Popen(server)
        print "Lets launch client for ", server
        self.run(".%sclient > null" % os.sep)
        pid.terminate()
