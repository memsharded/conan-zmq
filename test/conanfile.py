from conans import ConanFile, CMake
import os


class ZMQTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "ZMQ/4.1.1@memsharded/testing"
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake . %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")

    def test(self):
        server = "bin\server"
        import subprocess
        pid = subprocess.Popen(server)
        print "Lets launch client for ", server

        os.chdir("bin")
        self.run("client > null")
        pid.terminate()
