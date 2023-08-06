# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slutil', 'slutil.adapters', 'slutil.cli', 'slutil.model', 'slutil.services']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['slutil = slutil.main:start_cli']}

setup_kwargs = {
    'name': 'slutil',
    'version': '0.9.0',
    'description': 'Command-line utility to view slurm jobs',
    'long_description': '# slutil\n\n*A modern slurm experience.*\n\nA command line utility to view Slurm jobs. Written with rich and click.\n\n\n```\nUsage: slutil [OPTIONS] COMMAND [ARGS]...\n\nCommands:\n  report  Get status of multiple jobs\n  status  Get status of a slurm job.\n  submit  Submit a slurm job.\n```\n\n## Contributing\n\nPushes to `main` are forbidden, all changes must go through a PR before merging. All tests must pass for a PR to be merged. Code is to be formatted with `black`. Built with poetry.\n\n## submit\n\nAdd metadata to an `sbatch` command and store data in the database\n\n**Must** be used to log jobs in the database.\n\n```\nUsage: slutil submit [OPTIONS] SBATCH_FILE DESCRIPTION\n\n  Submit a slurm job.\n\n  SBATCH_FILE is a path to the .sbatch file for the job\n\n  DESCRIPTION is a text field describing the job\n\nOptions:\n  --help  Show this message and exit.\n```\n\n## report\n\nView list of recent jobs\n\n- Count parameter specifies the number of jobs to be displayed. Defaults to 10.\n- Truncated to screen width by default, `-v` to enable word-wrap.\n\n```\nUsage: slutil report [OPTIONS]\n\n  Get status of multiple jobs\n\nOptions:\n  -c, --count INTEGER\n  -v, --verbose\n  --help               Show this message and exit.\n```\n\n## status\n\nDisplays the data on a specific job\n\n```\nUsage: slutil status [OPTIONS] SLURM_ID\n\n  Get status of a slurm job.\n\n  SLURM_ID is the id of the job to check.\n\nOptions:\n  --help  Show this message and exit.\n```',
    'author': 'Eugene Prout',
    'author_email': 'eugene.prout1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
