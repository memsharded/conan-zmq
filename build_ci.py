import sys
from conan.packager import ConanMultiPackager

args = " ".join(sys.argv[1:]) # Pass additional parameters to "conan test" command, maybe "--build missing"
builder = ConanMultiPackager(args, username="memsharded", channel="testing")

builder.add_common_builds(shared_option_name="ZMQ:shared", visual_versions=[12, 14])

builder.pack()