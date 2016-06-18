from conans import ConanFile, CMake, tools
import os


class ZMQConan(ConanFile):
    """ ZMQ is a network, sockets on steroids library. 
    Safe for use in commercial applications LGPL v3 with static linking exception
    """
    name = "libzmq"
    version = "4.1.5"
    version_flat = "4_1_5"
    license = "LGPL"
    url = "https://github.com/memsharded/conan-zmq.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "FindZeroMQ.cmake"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/zeromq/zeromq4-1.git")
        self.run("cd zeromq4-1 && git checkout v4.1.5")
        tools.replace_in_file("zeromq4-1/CMakeLists.txt", "project(ZeroMQ)", """project(ZeroMQ)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
""")
          
    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake zeromq4-1 %s -DZMQ_BUILD_TESTS=OFF -DZMQ_BUILD_FRAMEWORK=OFF' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy_headers("*", "zeromq4-1/include")
        self.copy("FindZeroMQ.cmake")
        if not self.options.shared:
            self.copy("*libzmq*-mt-s*.lib", "lib", "lib", keep_path=False)
            self.copy("*.a", "lib", "lib", keep_path=False)  # Linux
        else:
            self.copy("*libzmq*-mt-%s.lib" % self.version_flat, "lib", "lib", keep_path=False)
            self.copy("*libzmq*-mt-gd-%s.lib" % self.version_flat, "lib", "lib", keep_path=False)
            self.copy("*.dll", "bin", "bin", keep_path=False)
            self.copy("*.dylib", "lib", "lib", keep_path=False)
            self.copy("libzmq.so", "lib", "lib", keep_path=False)  # Linux

    def package_info(self):
        if not self.settings.os == "Windows":
            shared_ext = "so" if self.settings.os == "Linux" else "dylib"
            self.cpp_info.libs = ["libzmq-static.a"] if not self.options.shared else ["libzmq.%s" % shared_ext]
        else:
            ver = ""
            if self.settings.compiler == "Visual Studio":
                if str(self.settings.compiler.version) in ["11", "12", "14"]:  
                    ver = "-v%s0" % self.settings.compiler.version
                else:
                    ver = "-"
            stat_fix = "s" if not self.options.shared else ""
            debug_fix = "gd" if self.settings.build_type == "Debug" else ""
            fix = ("-%s%s" % (stat_fix, debug_fix)) if stat_fix or debug_fix else ""
            self.cpp_info.libs = ["libzmq%s-mt%s-%s" % (ver, fix, self.version_flat)]

        if not self.options.shared:
            if self.settings.compiler == "Visual Studio":
                self.cpp_info.libs.append("ws2_32")
            self.cpp_info.defines = ["ZMQ_STATIC"]

            if not self.settings.os == "Windows":
                self.cpp_info.cppflags = ["-pthread"]
        
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "dl", "rt"])
