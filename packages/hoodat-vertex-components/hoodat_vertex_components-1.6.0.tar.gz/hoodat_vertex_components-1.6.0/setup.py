# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoodat_vertex_components',
 'hoodat_vertex_components.components',
 'hoodat_vertex_components.components.add_py',
 'hoodat_vertex_components.components.bytetrack_from_video',
 'hoodat_vertex_components.components.bytetrack_from_video.tools',
 'hoodat_vertex_components.components.bytetrack_from_videos',
 'hoodat_vertex_components.components.bytetrack_from_videos.tools',
 'hoodat_vertex_components.components.haar_from_frames',
 'hoodat_vertex_components.components.make_cascade_file',
 'hoodat_vertex_components.components.make_cascade_file.tests',
 'hoodat_vertex_components.components.pyscenedetect',
 'hoodat_vertex_components.components.query_database_output_data.src',
 'hoodat_vertex_components.components.query_database_output_string.src',
 'hoodat_vertex_components.components.stitch_videos',
 'hoodat_vertex_components.components.video_in_database',
 'hoodat_vertex_components.components.video_to_frames']

package_data = \
{'': ['*'],
 'hoodat_vertex_components.components': ['query_database_output_data/*',
                                         'query_database_output_string/*'],
 'hoodat_vertex_components.components.stitch_videos': ['sample/*']}

install_requires = \
['google-cloud-aiplatform>=1.12.1,<2.0.0',
 'kfp>=1.8.12,<2.0.0',
 'pytz>=2022.5,<2023.0']

setup_kwargs = {
    'name': 'hoodat-vertex-components',
    'version': '1.6.0',
    'description': 'Re-usable kfp components for hoodat',
    'long_description': "# Hoodat Pipeline Components\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nThis repository provides an SDK and a set of components that perform\ntasks in hoodat.\n\nIt is modelled after this repository of shared components for GCP:\nhttps://github.com/kubeflow/pipelines/tree/google-cloud-pipeline-components-1.0.1/components/google-cloud\n\n## To create new release of package and push to pypi:\n\n1. Update the version with commitizen:\n\n```shell\n#\xa0cz bump --dry-run\ncz bump\n```\n\n2. Push to main branch\n\n```shell\ngit push\n```\n\n3. Create a new release in github.\n\nThe package will be built and pushed to pypi in a github action.\n\n##\xa0Makefile\n\nThere is a Makefile at the root of this project which provides some\nuseful functionality for developing and publishing components. In the\nnext sections of this document some of this funcitonality will be\ndescribed.\n\nImportant to the use of the Makefile is the creation of an `env.sh`\nfile with necessary arguments populated. See `env.sh.example` for an\nexample of what this file should look like. Copy it to `env.sh` and\nreplace the default arguments with your own.\n\n### To create a new component with your own Dockerfile\n\nNew components should be added to the\n`hoodat_vertex_components/components` subdirectory. See already existing\nexamples. Here is a common file structure for a component:\n\n```\n├── make_cascade_file\n│   ├── Dockerfile\n│   ├── cascades.csv\n│   ├── component.yaml\n│   ├── make_cascade_file.py\n│   ├── poetry.lock\n│   ├── pyproject.toml\n│   └── tests\n│       └── test_filter_cascades.py\n```\n\n#### To run a components docker container in interactive mode\n\nThis function will be useful for running a components docker image\ninteractively. Update the `env.sh` with the name of the component and\nrun:\n\n```sh\nmake run_interactive\n```\n\n#### To run a pipeline with a single component in it\n\nIt may be useful to test a component in a pipeline. To do this, update\nthe `env.sh` with the name of the component and run:\n\n```sh\nmake push_and_pipeline\n```\n\n### To create a new python component\n\nLook at video_to_frames for an example.\n\nOnce you're happy, run:\n\n```sh\nCOMPONENT_NAME=video_to_frames\ncd hoodat_vertex_components/components/$COMPONENT_NAME\npoetry run python component.py\n```\n",
    'author': 'Eugene Brown',
    'author_email': 'efbbrown@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
