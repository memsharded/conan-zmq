from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="memsharded", channel="stable", visual_versions=["10", "12", "14", "15"])
    builder.add_common_builds(shared_option_name="libzmq:shared")
    
    named_builds = {}
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["compiler"] == "Visual Studio" and settings["compiler.version"] == "10" and settings["arch"] == "x86_64":
            continue
        if settings["compiler"] in ("gcc", "apple-clang"):
            name = "%s_%s" % (settings["compiler"], settings["compiler.version"].replace(".", ""))
        elif settings["compiler"] == "Visual Studio":
            name = "%s_%s_%s" % (settings["compiler"].replace(" ", ""), settings["compiler.version"], settings["arch"])
        named_build = named_builds.setdefault(name, [])
        named_build.append([settings, options, env_vars, build_requires])
    builder.builds = []
    builder.named_builds = named_builds

    builder.run()