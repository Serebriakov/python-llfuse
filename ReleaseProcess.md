# Steps for Releasing a New Version #

  * Bump version in `setup.py`
  * Add release date to `Changes.txt`
  * Check `hg status -u`, if necessary run `hg purge` to avoid undesired files in the tarball.
  * `./setup.py build_cython`
  * `./setup.py build_ext --inplace build_sphinx upload_docs`
  * `./setup.py sdist upload --sign`
  * hg commit, hg tag