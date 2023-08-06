# Hoodat Pipeline Components

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository provides an SDK and a set of components that perform
tasks in hoodat.

It is modelled after this repository of shared components for GCP:
https://github.com/kubeflow/pipelines/tree/google-cloud-pipeline-components-1.0.1/components/google-cloud

## To create new release of package and push to pypi:

1. Update the version with commitizen:

```shell
# cz bump --dry-run
cz bump
```

2. Push to main branch

```shell
git push
```

3. Create a new release in github.

The package will be built and pushed to pypi in a github action.

## Makefile

There is a Makefile at the root of this project which provides some
useful functionality for developing and publishing components. In the
next sections of this document some of this funcitonality will be
described.

Important to the use of the Makefile is the creation of an `env.sh`
file with necessary arguments populated. See `env.sh.example` for an
example of what this file should look like. Copy it to `env.sh` and
replace the default arguments with your own.

### To create a new component with your own Dockerfile

New components should be added to the
`hoodat_vertex_components/components` subdirectory. See already existing
examples. Here is a common file structure for a component:

```
├── make_cascade_file
│   ├── Dockerfile
│   ├── cascades.csv
│   ├── component.yaml
│   ├── make_cascade_file.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── tests
│       └── test_filter_cascades.py
```

#### To run a components docker container in interactive mode

This function will be useful for running a components docker image
interactively. Update the `env.sh` with the name of the component and
run:

```sh
make run_interactive
```

#### To run a pipeline with a single component in it

It may be useful to test a component in a pipeline. To do this, update
the `env.sh` with the name of the component and run:

```sh
make push_and_pipeline
```

### To create a new python component

Look at video_to_frames for an example.

Once you're happy, run:

```sh
COMPONENT_NAME=video_to_frames
cd hoodat_vertex_components/components/$COMPONENT_NAME
poetry run python component.py
```
