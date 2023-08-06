# drfaster
Optimizations to the predictions process


## Local Release process

0. Update HISTORY.rst:

```shell script
vi HISTORY.rst
```

1. Update version in setup.py

```shell script
# for sanity that you see the right version built.
make sdist
```

2. Open PR and merge to master. Find the standalone job in jenkins to publish the package. This will start a CD process that publishes to artifactory, test-pypi, and pypi.

3. Create a PR in the `quantum-builders` repository.  Modify the file `libraries/python_sci.matrix.yaml`. Add a new entry for the new version: copy&paste the previous entry and update the version number, unless you have made changes to how datarobot-drfaster builds.

4. (OPTIONAL) To run the full build locally (for testing purposes, NOT required, builds in a Docker Container with the standard DataRobot compiler version and other infrastructure), run:

```shell script
pip install . ; quantum-python datarobot-drfaster
```

More details are documented [here](https://docs.google.com/document/d/11lPYEoLSlo7zMU0xVV93egvXc7bSjhp9naPiDRtLCFU/edit).
