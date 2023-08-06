.. _package-sync-limitations:

Package Sync Limitations
========================

.. _pkg-sync-system-deps:

System dependencies aren't synced
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package sync doesn't handle non-Python, system-level packages you've installed with a system package manager like ``apt`` or ``homebrew``. It's rare these days, but some Python packages `cannot simply be pip-installed <https://twitter.com/ocefpaf/status/753992589938860032>`_ and need extra system dependencies to function. In these cases, you can:

1. (preferred) install system dependencies with conda instead. It's likely you can find everything you need on `conda-forge <https://conda-forge.org/feedstock-outputs/>`_. Package sync will then mirror all these dependencies automatically, including the non-Python ones.
2. (advanced) not use package sync, and use Docker instead. You'll have to build and publish your own Docker image, :ref:`register it as a software environment <software-docker>`, and :ref:`specify that when creating the cluster <cluster-senv>`.


Dependencies don't update on running clusters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you install a new package, or edit a local dependency, *after* launching a cluster, the cluster doesn't update automatically. You have to re-create the cluster to pick up any changes.


Local data files aren't copied
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Local files are not synced to the cluster. Local *packages* (importable Python code) are synced, but if your code relies on a file like ``local_data.csv``, you'll need to `get it on the cluster another way <https://stackoverflow.com/q/43796774/17100540>`_, such as the `Client.upload_file <https://distributed.dask.org/en/stable/api.html#distributed.Client.upload_file>`_ command.


Unsolvable environments
^^^^^^^^^^^^^^^^^^^^^^^
Your environment needs to be consistent with what your package manager would accept as a valid environment. For example, this will fail::

    dask==2022.1.10
    distributed==2022.05.1

Pip will error out trying to install this environment, as will conda, because ``distributed==2022.05.1`` requires exactly ``dask==2022.05.1``. If you manage to get your local environment into a state where both those incompatible packages are installed, package sync will not be able to synchronize it.


.. _local-pkgs-wheels:

Local packages must be buildable as wheels
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Your :ref:`local package <pkg-sync-local>` must work with ``pip wheel <package>``. If you have compiled dependencies, you must be running on the same platform as the cluster (64bit linux)—we do not try to cross compile your package!


Packages that have special build requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have packages installed with pip that don't have pre-built wheels available, and have requirements beyond what is included
in the standard ``build-essentials`` and ``python-dev`` ubuntu packages, you'll find package sync fails. If your package
is available in a conda repo, we suggest using that instead.


Packages that do not list their Python build time requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This is a slight variant of compiled packages missing build time system dependencies. If a package uses the deprecated
``setup.py`` and imports something that is not listed as a `PEP 517 build requirement <https://peps.python.org/pep-0517/#build-requirements>`_
or ``setup_requires``, the build will also fail.

An example of this is ``crick 0.0.3``, which imports ``numpy`` and ``Cython`` in `setup.py <https://github.com/dask/crick/blob/0.0.3/setup.py#L4>`_
but does not list them as build dependencies.


ARM clusters aren't supported yet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Package sync is not currently available for clusters using ARM instances (even when launched from ARM clients).


.. _pip-pypi-only:

Pip packages must be from PyPI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Other package indexes besides `PyPI <https://pypi.org/>`_ are not supported yet.
