from conans import ConanFile, CMake, tools
import os


class ZMQConan(ConanFile):
    """ ZMQ is a network, sockets on steroids library. 
    Safe for use in commercial applications LGPL v3 with static linking exception
    """
    name = "ZMQ"
    version = "4.1.1"
    license = "LGPL"
    url = "https://github.com/memsharded/conan-zmq.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "FindZeroMQ.cmake"

    def source(self):
        self.run("git clone https://github.com/zeromq/zeromq4-1.git")
        self.run("cd zeromq4-1 && git checkout 203cd808e249c06e1818cc3d70de4e48caf5f92b")
        tools.replace_in_file("zeromq4-1/CMakeLists.txt", "project(ZeroMQ)", """project(ZeroMQ)

        string(REPLACE "/MD" ${CONAN_LINK_RUNTIME} CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
        string(REPLACE "/MDd" ${CONAN_LINK_RUNTIME} CMAKE_CXX_FLAGS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG})
        string(REPLACE "/MD" ${CONAN_LINK_RUNTIME} CMAKE_C_FLAGS_RELEASE ${CMAKE_C_FLAGS_RELEASE})
        string(REPLACE "/MDd" ${CONAN_LINK_RUNTIME} CMAKE_C_FLAGS_DEBUG ${CMAKE_C_FLAGS_DEBUG})
""")
        tools.replace_in_file("zeromq4-1/CMakeLists.txt",
                                'check_library_exists(iphlpapi printf "" HAVE_IPHLAPI)',
                                """set(HAVE_WS2_32 1)
                                set(HAVE_RPCRT4 1)
                                set(HAVE_IPHLAPI 1)""")
            
    def build(self):
        cmake = CMake(self.settings)
        print "CMAKE COMMAND LINE ", cmake.command_line
        self.run('cmake zeromq4-1 %s -DZMQ_BUILD_TESTS=OFF' % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy_headers("*", "zeromq4-1/include")
        self.copy("FindZeroMQ.cmake")
        if not self.options.shared:
            self.copy("*libzmq-mt-s*.lib", "lib", "lib", keep_path=False)
            self.copy("*.a", "lib", "build/lib", keep_path=False)  # Linux
        else:
            self.copy("*libzmq-mt-4_1_1.lib", "lib", "lib", keep_path=False)
            self.copy("*libzmq-mt-gd-4_1_1.lib", "lib", "lib", keep_path=False)
            self.copy("*.dll", "bin", "bin", keep_path=False)
            self.copy("libzmq.so", "lib", "lib", keep_path=False)  # Linux

    def package_info(self):
        if not self.settings.os == "Windows":
            self.cpp_info.libs = ["libzmq-static.a"] if not self.options.shared else ["libzmq.so"]
        else:
            stat_fix = "s" if not self.options.shared else ""
            debug_fix = "gd" if self.settings.build_type == "Debug" else ""
            fix = ("-%s%s" % (stat_fix, debug_fix)) if stat_fix or debug_fix else ""
            self.cpp_info.libs = ["libzmq-mt%s-4_1_1" % fix]

        if not self.options.shared:
            if self.settings.compiler == "Visual Studio":
                self.cpp_info.libs.append("ws2_32")
            self.cpp_info.defines = ["ZMQ_STATIC"]

            if not self.settings.os == "Windows":
                self.cpp_info.cppflags = ["-pthread"]
