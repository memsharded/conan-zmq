import os
import platform


def system(command):
    retcode = os.system(command)
    if retcode != 0:
        raise Exception("Error while executing:\n\t %s" % command)


if __name__ == "__main__":
    system('conan export memsharded/testing')

    if platform.system() == "Windows":
        system('conan test -s compiler="Visual Studio" -s compiler.version=12 -s build_type=Debug '
                          '-s compiler.runtime=MDd')
        system('conan test -s compiler="Visual Studio" -s compiler.version=12 '
                          '-s build_type=Release -s compiler.runtime=MD')
    else:
        system('conan test -s compiler="gcc" -s build_type=Debug')
        system('conan test -s compiler="gcc" -s build_type=Release')
