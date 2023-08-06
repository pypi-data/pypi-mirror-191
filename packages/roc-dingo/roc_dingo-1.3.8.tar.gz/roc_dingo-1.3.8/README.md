DINGO PLUGIN README
===================

[![pipeline status](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/pipeline.svg)](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/pipelines)
[![coverage report](https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO/badges/develop/coverage.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/coverage.html/)
[![tests status](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/pie.svg)](https://roc.pages.obspm.fr/Pipelines/Plugins/DINGO/report.html)

This directory contains the source files of the Data INGestOr (DINGO), a plugin of the ROC pipeline used to ingest data into the ROC database.
DINGO is developed with and run under the POPPY framework.

## User guide

### Pre-requisites

The following software must be installed:
- Python 3.8
- pip tool
- poetry (optional)
- git (optional)

### Install a stable release with pip

To install the roc-dingo plugin with pip:

``pip install roc-dingo``

## Nominal usage

roc-dingo is designed to be called from a pipeline running with the POPPy framework.

The plugin can be used in Python programs using "import roc.dingo".

## Developer guide

### Install a local copy from source files

To install a local copy of the roc-dingo plugin:

1. Retrieve a copy of the source files from https://gitlab.obspm.fr/ROC/Pipelines/Plugins/DINGO (restricted access)
2. Use `pip install` or `poetry install` command to install local instance

### Publish a new version

1. Update the plugin version in pyproject.toml
2. Update the plugin descriptor using ``python bump_descriptor.py -m <message>``
3. Update `poetry.lock` file running `poetry lock`
4. Always commit in `develop` branch first
5. Merge in `master/main` branch and tag the version

N.B. When a new tag is pushed in gitlab, tests are automatically run in pipeline, then plugin published in pypi.

Authors
-------

* Florence HENRY florence.henry@obspm.fr (maintainer)
* Xavier BONNIN xavier.bonnin@obspm.fr (maintainer)
* Sonny LION sonny.lion@obspm.fr (author)

License
-------

This project is licensed under CeCILL-C.

Acknowledgments
---------------

* Solar Orbiter / RPW Operation Centre (ROC) team
