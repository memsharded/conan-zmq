from conans import ConanFile, CMake
import os


class ZMQConan(ConanFile):
    """ ONGOING Work, tested in Win, VS 12, still to be tested
    for other settings
    """
    name = "ZMQ"
    version = "4.1.1"
    url = "https://github.com/memsharded/conan-zmq.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"static": [True, False]}
    default_options = "static=True"

    def source(self):
        self.run("git clone https://github.com/zeromq/zeromq4-1.git")
        self.run("cd zeromq4-1 && git checkout 203cd808e249c06e1818cc3d70de4e48caf5f92b")

    def build(self):
        cmake = CMake(self.settings)
        try:
            os.makedirs("build")
        except:
            pass
        self.run('cd build && cmake ../zeromq4-1 %s -DZMQ_BUILD_TESTS=OFF' % cmake.command_line)
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy_headers("*", "zeromq4-1/include")
        if self.options.static:
            self.copy("*libzmq-mt-s*.lib", "lib", "build/lib", keep_path=False)
            self.copy("*.a", "lib", "build/lib", keep_path=False)  # Linux
        else:
            self.copy("*libzmq-mt-4_1_1.lib", "lib", "build/lib", keep_path=False)
            self.copy("*libzmq-mt-gd-4_1_1.lib", "lib", "build/lib", keep_path=False)
            self.copy("*.dll", "bin", "build/bin", keep_path=False)
            self.copy("libzmq.so", "lib", "build/lib", keep_path=False)  # Linux

    def package_info(self):
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["libzmq-static.a"] if self.options.static else ["libzmq.so"]
        else:
            stat_fix = "s" if self.options.static else ""
            debug_fix = "gd" if self.settings.build_type == "Debug" else ""
            fix = ("-%s%s" % (stat_fix, debug_fix)) if stat_fix or debug_fix else ""
            self.cpp_info.libs = ["libzmq-mt%s-4_1_1" % fix]

        if self.options.static:
            if self.settings.compiler == "Visual Studio":
                self.cpp_info.libs.append("ws2_32")
            self.cpp_info.defines = ["ZMQ_STATIC"]

            if not self.settings.os == "Windows":
                self.cpp_info.cppflags = ["-pthread"]
