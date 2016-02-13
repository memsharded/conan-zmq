from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "testing")
username = os.getenv("CONAN_USERNAME", "memsharded")

class ZMQTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "ZMQ/4.1.1@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake . %s' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")

    def test(self):
        server = "bin%sserver" % os.sep
        import subprocess
        pid = subprocess.Popen(server)
        print "Lets launch client for ", server

        os.chdir("bin")
        self.run(".%sclient > null" % os.sep)
        pid.terminate()
