Conan package for libzmq 4.1.5

CI

[![Build Status](https://travis-ci.org/memsharded/conan-zmq.svg?branch=release%2F4.1.5)](https://travis-ci.org/memsharded/conan-zmq)
[![Build status](https://ci.appveyor.com/api/projects/status/awaafv2eorvs3pni?svg=true)](https://ci.appveyor.com/project/memsharded/conan-zmq)

This package has the ``shared`` option (by default False = static library), you can use:

```bash
$ conan install -o libzmq:shared=True
```

or in your conanfile.txt

```
[requires]
libzmq/4.1.5@memsharded/stable

[options]
libzmq:shared=True