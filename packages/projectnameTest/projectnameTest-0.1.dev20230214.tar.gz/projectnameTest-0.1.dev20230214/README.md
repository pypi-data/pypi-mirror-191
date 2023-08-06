# Test runs
## Run python tests locally in the build folder 
### Not installed depencencies
Inside the docker container of 2.9 [Link](https://gitlab.dune-project.org/docker/ci/-/blob/master/dune-2.9/Dockerfile) the dune modules are not installed,
since `DUNECI_INSTALL_STAGE` is not set to 1, see [Link](https://gitlab.dune-project.org/docker/ci/-/blob/master/base-common/duneci-install-module#L118-L119)

Running the python tests of projectnameTest fails using the following commands. (To get this working i had to set 
`set (CMAKE_PREFIX_PATH "/duneci/modules/dune-common/build-cmake")` in the toplevel CMakeLists.txt)
```shell
docker container run -it --entrypoint /bin/bash registry.dune-project.org/docker/ci/dune:2.9
git clone https://gitlab.dune-project.org/alexander.mueller/testpythonbindings.git
cd testpythonbindings/
dunecontrol --only=projectnameTest all
cd build-cmake
ctest --verbose
```

`test1.py` and `test2.py` fails with:

```python
 ValueError: Key INSTALL_PREFIX is expected to be unique across the given metadata. Got {'/usr/local', '/duneci/install'}
```

<details>
  <summary>Full test results</summary>

```shell
duneci@e7fac7d916b9:~/testpythonbindings/build-cmake$ ctest --verbose
UpdateCTestConfiguration  from :/duneci/testpythonbindings/build-cmake/DartConfiguration.tcl
Parse Config file:/duneci/testpythonbindings/build-cmake/DartConfiguration.tcl
UpdateCTestConfiguration  from :/duneci/testpythonbindings/build-cmake/DartConfiguration.tcl
Parse Config file:/duneci/testpythonbindings/build-cmake/DartConfiguration.tcl
Test project /duneci/testpythonbindings/build-cmake
Constructing a list of tests
Done constructing a list of tests
Updating test list for fixtures
Added 0 tests to meet fixture requirements
Checking test dependency graph...
Checking test dependency graph end
test 1
Start 1: pytest1

1: Test command: /duneci/testpythonbindings/build-cmake/run-in-dune-env "python" "test1.py"
1: Test timeout computed to be: 3600
1: Comparing build directories of installed dune modules with given build directories
1: DUNE-INFO: Generating dune-py module in /duneci/modules/dune-common/build-cmake/dune-env/.cache/dune-py
1: Help on package projectnameTest:
1:
1: NAME
1:     projectnameTest
1:
1: DESCRIPTION
1:     # SPDX-FileCopyrightText: Copyright © DUNE Project contributors, see file LICENSE.md in module root
1:     # SPDX-License-Identifier: LicenseRef-GPL-2.0-only-with-DUNE-exception
1:
1: PACKAGE CONTENTS
1:     _projectnameTest
1:
1: FUNCTIONS
1:     add(...) method of builtins.PyCapsule instance
1:         add(i: int, j: int) -> int
1:         
1:         A function which adds two numbers
1:
1: FILE
1:     /duneci/testpythonbindings/build-cmake/python/projectnameTest/__init__.py
1:
1:
1: Traceback (most recent call last):
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/common/__init__.py", line 86, in FieldVector
1:     return globals()[fv](values)
1: KeyError: 'FieldVector_3'
1:
1: During handling of the above exception, another exception occurred:
1:
1: Traceback (most recent call last):
1:   File "/duneci/testpythonbindings/projectnameTest/python/test/test1.py", line 17, in <module>
1:     v = FieldVector([0, 1, 2])
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/common/__init__.py", line 90, in FieldVector
1:     cls = _loadVec(includes, typeName).FieldVector
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/common/__init__.py", line 74, in _loadVec
1:     return generator.load(
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/generator.py", line 172, in load
1:     return self.post(moduleName, source, postscript, extraCMake)
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/generator.py", line 124, in post
1:     module = builder.load(moduleName, source, self.typeName[0], extraCMake)
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 374, in load
1:     self.initialize()
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 616, in initialize
1:     super().initialize()
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 213, in initialize
1:     self.build_dunepy_from_template(self.dune_py_dir)
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 448, in build_dunepy_from_template
1:     force = Builder.generate_dunepy_from_template(dunepy_dir, force=force)
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 121, in generate_dunepy_from_template
1:     context["install_prefix"] = metaData.unique_value_across_modules("INSTALL_PREFIX")
1:   File "/duneci/modules/dune-common/build-cmake/python/dune/packagemetadata.py", line 496, in unique_value_across_modules
1:     raise ValueError(f"Key {key} is expected to be unique across the given metadata. Got {values}")
1: ValueError: Key INSTALL_PREFIX is expected to be unique across the given metadata. Got {'/usr/local', '/duneci/install'}
1/2 Test #1: pytest1 ..........................***Failed    0.59 sec
test 2
Start 2: pytest2

2: Test command: /duneci/testpythonbindings/build-cmake/run-in-dune-env "python" "test2.py"
2: Test timeout computed to be: 3600
2: Comparing build directories of installed dune modules with given build directories
2: DUNE-INFO: Generating dune-py module in /duneci/modules/dune-common/build-cmake/dune-env/.cache/dune-py
2: Traceback (most recent call last):
2:   File "/duneci/testpythonbindings/projectnameTest/python/test/test2.py", line 20, in <module>
2:     grid = dune.grid.structuredGrid(lowerLeft,upperRight,elements)
2:   File "/duneci/modules/dune-grid/build-cmake/python/dune/grid/core.py", line 13, in structuredGrid
2:     return yaspGrid(domain, dimgrid=len(lower), coordinates="equidistantoffset")
2:   File "/duneci/modules/dune-grid/build-cmake/python/dune/grid/_grids.py", line 253, in yaspGrid
2:     constructor = equidistantOffsetCoordinates(
2:   File "/duneci/modules/dune-grid/build-cmake/python/dune/grid/_grids.py", line 165, in equidistantOffsetCoordinates
2:     mod = moduleYaspCoordinates(dim,ctype)
2:   File "/duneci/modules/dune-grid/build-cmake/python/dune/grid/_grids.py", line 159, in moduleYaspCoordinates
2:     module = builder.load(moduleName, source, "yasp coordinates dim={dim} ctype={ct}".format(ct = ctype, dim = dim))
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 374, in load
2:     self.initialize()
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 616, in initialize
2:     super().initialize()
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 213, in initialize
2:     self.build_dunepy_from_template(self.dune_py_dir)
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 448, in build_dunepy_from_template
2:     force = Builder.generate_dunepy_from_template(dunepy_dir, force=force)
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/generator/cmakebuilder.py", line 121, in generate_dunepy_from_template
2:     context["install_prefix"] = metaData.unique_value_across_modules("INSTALL_PREFIX")
2:   File "/duneci/modules/dune-common/build-cmake/python/dune/packagemetadata.py", line 496, in unique_value_across_modules
2:     raise ValueError(f"Key {key} is expected to be unique across the given metadata. Got {values}")
2: ValueError: Key INSTALL_PREFIX is expected to be unique across the given metadata. Got {'/usr/local', '/duneci/install'}
2/2 Test #2: pytest2 ..........................***Failed    0.60 sec

0% tests passed, 2 tests failed out of 2

Label Time Summary:
python    =   1.19 sec*proc (2 tests)
quick     =   1.19 sec*proc (2 tests)

Total Test time (real) =   1.19 sec

The following tests FAILED:
1 - pytest1 (Failed)
2 - pytest2 (Failed)
Errors while running CTest
```

</details>

### Installed
We use the same container but install the modules as similar? to https://gitlab.dune-project.org/docker/ci/-/blob/master/base-common/duneci-install-module#L118-L119.
(To get this working i had to set
`set (CMAKE_PREFIX_PATH "/duneci/install/lib/cmake/dune-common")` in the toplevel CMakeLists.txt)
and removing the modules folder afterwards yields with the following commands
```shell
docker container run -it --entrypoint /bin/bash registry.dune-project.org/docker/ci/dune:2.9
cd modules/
dunecontrol  --only=dune-common make install
cd ..
rm -rf modules/
git clone https://gitlab.dune-project.org/alexander.mueller/testpythonbindings.git
cd testpythonbindings/
/duneci/install/bin/dunecontrol --only=projectnameTest all
```
the following error

```
ERROR: The path "/duneci/modules" given in DUNE_CONTROL_PATH does not exist.
Execution of dunecontrol terminated due to errors!
```
I suppose this is on purpose but why is the installation performed into the folder `/duneci/install/bin`and not into `/usr/bin` or `usr/local/bin`?
Somehow the installed `dune-common` should not depend on the downloaded build folder?
But my Linux knowledge is not good enough here, maybe.

### Test with homegrown MWE docker container
For the container see `DockerImages/DockerFile`
**`test1.py` and `test2.py` fails with:

```shell
docker container run -it --entrypoint /bin/bash rath3t/dunepythonbindings:installedmodules
git clone https://gitlab.dune-project.org/alexander.mueller/testpythonbindings.git
cd testpythonbindings/
dunecontrol --only=projectnameTest all
cd build-cmake
ctest --verbose
```



```python
build dir /usr/local/lib/cmake/dune-common for module dune-common is expected to be unique across the given metadata - found /dune/dune-common/build-cmake
2: Dune python package could not be found.
```

<details>
  <summary>Full test results</summary>

```shell
root@e4f98ef9aa1e:/testpythonbindings/build-cmake# ctest --verbose
UpdateCTestConfiguration  from :/testpythonbindings/build-cmake/DartConfiguration.tcl
Parse Config file:/testpythonbindings/build-cmake/DartConfiguration.tcl
UpdateCTestConfiguration  from :/testpythonbindings/build-cmake/DartConfiguration.tcl
Parse Config file:/testpythonbindings/build-cmake/DartConfiguration.tcl
Test project /testpythonbindings/build-cmake
Constructing a list of tests
Done constructing a list of tests
Updating test list for fixtures
Added 0 tests to meet fixture requirements
Checking test dependency graph...
Checking test dependency graph end
test 1
    Start 1: pytest1

1: Test command: /testpythonbindings/build-cmake/run-in-dune-env "python" "test1.py"
1: Test timeout computed to be: 3600
1: Comparing build directories of installed dune modules with given build directories
1: build dir /usr/local/lib/cmake/dune-common for module dune-common is expected to be unique across the given metadata - found /dune/dune-common/build-cmake
1: Dune python package could not be found.
1/2 Test #1: pytest1 ..........................***Skipped   0.10 sec
test 2
    Start 2: pytest2

2: Test command: /testpythonbindings/build-cmake/run-in-dune-env "python" "test2.py"
2: Test timeout computed to be: 3600
2: Comparing build directories of installed dune modules with given build directories
2: build dir /usr/local/lib/cmake/dune-common for module dune-common is expected to be unique across the given metadata - found /dune/dune-common/build-cmake
2: Dune python package could not be found.
2/2 Test #2: pytest2 ..........................***Skipped   0.10 sec

100% tests passed, 0 tests failed out of 2

Label Time Summary:
python    =   0.20 sec*proc (2 tests)
quick     =   0.20 sec*proc (2 tests)

Total Test time (real) =   0.20 sec

The following tests did not run:
          1 - pytest1 (Skipped)
          2 - pytest2 (Skipped)

```

</details>

Not removing the dune folder where dune-common is downloaded (commenting `RUN rm -rf dune/`) in `DockerImages/DockerFile` yields the same error.

It can be used via the docker image `rath3t/dunepythonbindings: installedmodulesNotDeletedBuildDir`.

# Questions
## Not installed python tests
- Is this repository almost setup correctly in terms of python bindings? I got inspired by `dumux`, since I also want to have a module with its own namespace.
- Why does the above tests complain with a reference to `/dune/dune-common/build-cmake` even when the module is installed and this folder is removed?
- How to run the python tests correctly without installing the module projectnameTest? 
  - What needs to be present and how (installed dependencies) to circumvent the errors from above?
  - Is there a magic combination of running these targets?
        ```
        build_tests
        projectnameTest
        _projectnameTest
        test_python
        build_python_tests
        ```
      I consider `metadata_install_python_package_dune,install_python_package_dune,install_python` as not needed for this question. Just from the naming they are use by installing the package

## Installing the local python module to run python tests with installed module
How should the module be installed:
From [dune-project.org/dev/adding_python](https://dune-project.org/dev/adding_python/ )
`pip install -v --pre --log logfile --find-links file://$PWD/dist packagename==0.1` 
or using `metadata_install_python_package_dune,install_python_package_dune,install_python`  in some cobination.

Can I then copy the test above `test1.py` and `test2.py` somewhere and then can I test it with `python test1.py` or does this still happen inside the venv and I have to write
`run-in-dune-env python test1.py`? But where should the file `run-in-dune-env` be in this case, since all build directories are potentially deleted?




git-045b90667d172f1b92a5178ffaff13cef28ba463
