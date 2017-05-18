from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="memsharded", channel="testing", visual_versions=["10", "12", "14", "15"])
    builder.add_common_builds(shared_option_name="libzmq:shared")
    builder.run()
