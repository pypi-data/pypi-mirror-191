# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'xefab', 'xefab.hosts', 'xefab.hosts.uchicago', 'xefab.tasks']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'decopatch>=1.4.10,<2.0.0',
 'fabric>=3.0.0,<4.0.0',
 'fsspec>=2023.1.0,<2024.0.0',
 'gnupg>=2.3.1,<3.0.0',
 'makefun>=1.15.0,<2.0.0',
 'pandas',
 'pymongo',
 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['xefab = xefab.main:program.run',
                     'xf = xefab.main:program.run'],
 'xefab.tasks': ['dali = xefab.hosts.uchicago.dali',
                 'midway = xefab.hosts.uchicago.midway',
                 'osg = xefab.hosts.osg']}

setup_kwargs = {
    'name': 'xefab',
    'version': '0.1.4',
    'description': 'Top-level package for xefab.',
    'long_description': "=====\nxefab\n=====\n\nFabric based task execution for the XENON dark matter experiment\n\n\nInstallation\n------------\n\nTo install xefab, its recomended to use pipx_:\n\n.. code-block:: console\n\n    $ pipx install xefab\n\nAlternatively you can install it using pip:\n\n.. code-block:: console\n\n    $ pip install xefab\n\nUsage\n-----\n\nYou can list the available tasks and options by running xefab without any options.\n\n.. code-block:: console\n\n    $ xefab\n    Usage: xefab [--core-opts] <subcommand> [--subcommand-opts] ...\n\n    Core options:\n\n    --complete                         Print tab-completion candidates for given parse remainder.\n    --hide=STRING                      Set default value of run()'s 'hide' kwarg.\n    --print-completion-script=STRING   Print the tab-completion script for your preferred shell (bash|zsh|fish).\n    --prompt-for-login-password        Request an upfront SSH-auth password prompt.\n    --prompt-for-passphrase            Request an upfront SSH key passphrase prompt.\n    --prompt-for-sudo-password         Prompt user at start of session for the sudo.password config value.\n    --write-pyc                        Enable creation of .pyc files.\n    -d, --debug                        Enable debug output.\n    -D INT, --list-depth=INT           When listing tasks, only show the first INT levels.\n    -e, --echo                         Echo executed commands before running.\n    -f STRING, --config=STRING         Runtime configuration file to use.\n    -F STRING, --list-format=STRING    Change the display format used when listing tasks. Should be one of: flat (default), nested,\n                                        json.\n    -h [STRING], --help[=STRING]       Show core or per-task help and exit.\n    -H STRING, --hosts=STRING          Comma-separated host name(s) to execute tasks against.\n    -i, --identity                     Path to runtime SSH identity (key) file. May be given multiple times.\n    -l [STRING], --list[=STRING]       List available tasks, optionally limited to a namespace.\n    -p, --pty                          Use a pty when executing shell commands.\n    -R, --dry                          Echo commands instead of running.\n    -S STRING, --ssh-config=STRING     Path to runtime SSH config file.\n    -t INT, --connect-timeout=INT      Specifies default connection timeout, in seconds.\n    -T INT, --command-timeout=INT      Specify a global command execution timeout, in seconds.\n    -V, --version                      Show version and exit.\n    -w, --warn-only                    Warn, instead of failing, when shell commands fail.\n\n    Subcommands:\n\n    show-config                        Get a config from the config server.\n    admin.get-xenonnt-keys\n    admin.github-cli\n    admin.github-token\n    admin.list-xenon1t-members\n    admin.list-xenonnt-members\n    admin.user-db\n    dali.download-file                 Download a file from a remote server.\n    dali.squeue (dali.job-queue)       Get the job-queue status.\n    dali.start-jupyter                 Start a jupyter notebook on remote host.\n    dali.submit-job                    Submit a job to the dali batch queue\n    dali.upload-file                   Upload a file to a remote server.\n    install.chezmoi\n    install.github-cli\n    install.gnupg\n    install.go\n    install.gopass\n    midway.download-file               Download a file from a remote server.\n    midway.squeue (midway.job-queue)   Get the job-queue status.\n    midway.start-jupyter               Start a jupyter notebook on remote host.\n    midway.submit-job                  Submit a job to the dali batch queue\n    midway.upload-file                 Upload a file to a remote server.\n    osg.condor-q (osg.job-queue)\n    secrets.github-token\n    secrets.setup\n    secrets.setup-utilix-config\n\n\n    Remote Hosts:\n\n    dali     dali-login2.rcc.uchicago.edu,dali-login1.rcc.uchicago.edu\n    midway   midway2.rcc.uchicago.edu,midway2-login1.rcc.uchicago.edu,midway2-login2.rcc.uchicago.edu\n    osg      login.xenon.ci-connect.net\n\nSome tasks are registered to run on a specific host. When you run them, the --hosts option will be ignored.\n\ne.g. if you run\n\n.. code-block:: console\n\n    $ xefab midway start-jupyter\n\nThe task will be run on the midway host, not the host you specified with --hosts.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n.. _pipx: https://github.com/pypa/pipx\n",
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jmosbacher/xefab',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
