from conans import ConanFile, CMake, tools
import os


class ZMQTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "lib")

    def test(self):
        if tools.cross_building(self.settings):
            return
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
