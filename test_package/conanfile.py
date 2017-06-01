from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "memsharded")

class ZMQTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libzmq/4.1.5@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        print ("Running test")
        os.chdir("bin")
        print("FILES: %s" % os.listdir("."))
        server = ".%sserver" % os.sep
        import subprocess
        pid = subprocess.Popen(server)
        print ("Lets launch client for ", server)
        import time
        time.sleep(1)
        self.run(".%sclient > null" % os.sep)
        pid.terminate()
