import os
import platform


def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)


if __name__ == "__main__":
    system('conan export memsharded/testing')

    if platform.system() == "Windows":
        for (build_type, runtime, arch, static) in [("Debug", "MDd", "x86", "True"),
                                                    ("Release", "MD", "x86", "True"),
                                                    ("Debug", "MDd", "x86_64", "True"),
                                                    ("Release", "MD", "x86_64", "True"),
                                                    ("Debug", "MDd", "x86", "False"),
                                                    ("Release", "MD", "x86", "False"),
                                                    ("Debug", "MDd", "x86_64", "False"),
                                                    ("Release", "MD", "x86_64", "False")
                                                    ]:
            system('conan test -s compiler="Visual Studio" -s compiler.version=12'
                          ' -s build_type=%s -s compiler.runtime=%s -s arch=%s -o ZMQ:static=%s'
                          %(build_type, runtime, arch, static))
    else:
        system('conan test -s compiler="gcc" -s build_type=Debug')
        system('conan test -s compiler="gcc" -s build_type=Release')
