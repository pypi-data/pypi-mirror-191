# PIC-rucio-client
Below is a couple of scripts that facilitate other tests to interact with Rucio's server. In each one of them, the amount and scope corresponding to the person are owed (and in the case that the RSEs are desired, although it is not necessary) First of all, here is a script to do simple uploads of randoms files. Then, Replication of those files in the deterministic RSE. See [pre-commit](https://docs.google.com/document/d/1jm3LKKI0sTP6Gx0p5PQXRti2NzK_JqG1ITFs761W0KU/edit#heading=h.mkngky6253k8) for instructions.

# gitlab-ci
`gitlab-ci` validates you `.gitlab-ci.yml` file from command-line, before you have commited wrong CI configuration to your repository!

Just as https://docs.gitlab.com/ee/ci/lint.html does, but you don't have to open browser every time.

The better way to use it - use as pre-commit hooks.

# How to package this scripts
See this [guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for more instructions
