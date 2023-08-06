# FILM PLUGIN README

[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM/pipelines)

This directory contains the source files of the Rpw FILe Maker (FILM), a plugin of the ROC pipelines dedicated to the RPW L0, L1 and HK files production.

FILM has been developed with the [POPPY framework](https://poppy-framework.readthedocs.io/en/latest/).

## Quickstart

### Installation with pip

To install the plugin using pip:

```
pip install roc-film
```

### Installation from the repository

First, retrieve the `FILM` repository from the ROC gitlab server:

```
git clone https://gitlab.obspm.fr/ROC/Pipelines/Plugins/FILM.git
```

You will need a personal access token to reach the package registry in the ROC Gitlab server.

Then, install the package (here using (poetry)[https://python-poetry.org/]):

```
poetry install"
```

NOTES:

    - It is also possible to clone the repository using SSH
    - To install poetry: `pip install poetry`

## Usage

The roc-film plugin is designed to be run in a POPPy-built pipeline.
Nevertheless, it is still possible to import some classes and methods in Python files.

### How to release a new version of the plugin?

1. Checkout to the git *develop* branch (and make pull to be sure to work from the latest commit in the gitlab server)

2. First update metadata (version, dependencies, etc.) in the plugin *pyproject.toml* file.

3. Then make sure the *descriptor.json* and *poetry.lock* files are also up-to-date.

To update the *descriptor.json* file, run the command:

    python bump_descriptor.py -m <modification_message>

To update the *poetry.lock* file, enter:

    poetry lock

N.B. *poetry* Python package must be installed (see https://python-poetry.org/).

4. Commit the changes in the *develop* branch. Make sure to commit with a comprehensive enough message.
5. Checkout to the *master* branch and merge the *develop* branch into *master*
6. Create a new git tag `X.Y.Z` for the new version of the plugin (must be the same version than in the *pyproject.toml* file)
7. Push both the *master* branch and the tag to the gitlab server
8. Do a rebase of *develop* onto the *master* branch
9. Push the up-to-date *develop* branch to the gitlab server

N.B. This procedure only concerns the version release. It is assumed that any other changes in the code have been already validated previously.

## CONTACT

* Xavier BONNIN xavier.bonnin@obspm.fr (author, maintainer)
* Florence HENRY florence.henry@obspm.fr (maintainer)


License
-------

This project is licensed under CeCILL-C.

Acknowledgments
---------------

* Solar Orbiter / RPW Operation Centre (ROC) team
