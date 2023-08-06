=======================
Package Synchronization
=======================

.. toctree::
   :maxdepth: 1
   :hidden:

   package_sync_production
   package_sync_limitations
   package_sync_compatibility


Package sync scans your local Python environment and replicates it on the cluster—even local packages and Git dependencies. It's easier than building a Docker image, plus it launches significantly faster.

Here's an example showing how your cluster can (magically!) import packages you have in your local environment, in this case ``httpx`` and ``my_local_package``:

.. code-block:: python

    import coiled
    import dask

    import httpx
    from . import my_local_package


    @dask.delayed
    def func():
        # This function requires `httpx` and `my_local_package` to be installed.
        data = httpx.get("https://my-api.io/foo")
        return my_local_package.process(data)


    # Notice we don't tell Coiled what packages we need.
    # The local environment is automatically replicated on the cluster.
    cluster = coiled.Cluster()
    client = dask.distributed.Client(cluster)

    # When `func` runs on the cluster, `httpx` and `my_local_package` are already there.
    result = func.compute()

Package sync is used by default when you :doc:`create a cluster <cluster_creation>`. To *not* use package sync, you must :doc:`create <software_environment_creation>` and :ref:`specify <cluster-senv>` a software environment instead.

Why do I need this?
===================

Your code imports many Python packages, like pandas and NumPy. You have those installed on your computer, but for your code to run on many machines in the cloud, pandas, NumPy, and everything else must also be installed on those machines. Not only do they need to be installed, but they need to be the same versions as you have locally. Otherwise, you could get errors, or even incorrect results.

Package sync ensures all these versions match without any extra work on your part. It means you can just call :obj:`coiled.Cluster` from anywhere you run Python and get a matching environment in the cloud.

Achieving this is usually a major pain point with most distributed computing systems, Dask included. Often, to solve it, you'd build and maintain a Docker image, or provide a list of dependencies to install on the cluster. Not only is this extra work, but it easily gets out of date. Package sync both eliminates the extra work, and ensures your cluster has the right packages every time.

Using package sync
==================

There's nothing you really need to do to use package sync—it just works.

Package sync is compatible with most ways you can use Python, such as conda environments, Python virtual environments, or even packages installed in the system Python environment (see the full :doc:`compatibility table <package_sync_compatibility>`).

When you create a :obj:`~.Cluster`, package sync will scan all the conda and pip packages that are installed for the current Python interpreter. This list of packages will be installed on every machine in the cluster as it starts, using an optimized process that installs significantly faster than either a typical ``conda install`` or a Docker image pull. (Optimized pip package installation is coming soon.)

.. _pkg-sync-performance:

Performance
===========

Package sync clusters typically launch as fast, and in some cases much faster, than clusters using an equivalent Docker image. (Even faster if you include image build time.) Currently, you'll get the best performance using conda instead of pip or other package managers.

If you don't change any packages locally, re-launching a cluster using the same environment is faster for the following 24 hours.

Note that your internet connection speed is *not* important for package sync performance: the cluster downloads packages directly from their sources (conda-forge, PyPI, etc.); they're not uploaded from your computer (besides :ref:`local dependencies <pkg-sync-local>`).

.. _pkg-sync-local:

Path or Git dependencies
========================

If you have local packages installed, such as with ``pip install -e <some-directory>``, package sync will try to install them on the cluster. The packages will be built on your machine (see :ref:`limitations <local-pkgs-wheels>`), then uploaded to and installed on the cluster.

If you've installed a package from Git, such as with ``pip install git+ssh://git@github.com/dask/distributed.git@d74f5006``, the same process will occur. The reason we upload the package from your machine, instead of pulling it from Git on the cluster, is to avoid issues with private Git repos: your local credentials can stay local, instead of needing to get them onto the cluster!

.. _pkg-sync-pep517:

.. note::
    When installing packages from Git, you may need to add the ``--use-pep517`` flag to pip, like::

        pip install git+https://github.com/dask/distributed.git --use-pep517

    Without this flag, for some packages pip may not record sufficient metadata to tell that the package was installed from Git, versus from a normal ``pip install distributed``.

.. warning::
    Your compiled local packages are currently uploaded to storage controlled by Coiled, then downloaded by your cluster. Only your cluster can access these files, and they are deleted after 24h. While this will change in the future, if having a copy of your source code under Coiled's control violates your organization's security policies, we recommend not using package sync with local code currently.

.. _pkg-sync-ignoring:

Ignoring packages
=================

If you have packages installed locally that you don't want synced to the cluster, you can list them in the ``package_sync_ignore`` argument to :obj:`coiled.Cluster`. This is generally not needed, though, because package sync installation on the cluster is so fast that installing extra, unused packages has a negligible effect on cluster startup time.

Note that only these exact packages are ignored—their dependencies may still be installed. Additionally, if another package depends on them, they will still be installed.

.. _pkg-sync-cross-platform:

Cross-platform fuzzing
======================

When using a macOS or Windows machine to launch clusters (which always run Linux), you may not get exactly the same versions of all packages on the cluster as you have locally. This occurs because packages sometimes require slightly different dependencies on different platforms. If package sync tried to install the exact same versions of everything you have on macOS, for example, onto Linux, some versions might not exist for Linux, or might have incompatible requirements, and installation would fail.

Therefore, package sync uses a looser version match with cross-platform clusters. Specifically, we only match ``major.minor`` in the version number, not the exact version (typically ``major.minor.patch``).

When launching a cluster from Linux, though, the exact versions of all packages will be matched. This is the recommended way to run workloads that require the highest degree of reproducibility. See :doc:`package_sync_production` for details.

Mandatory packages
==================

Package sync will refuse to start a cluster if you don't have these basic packages for running Dask installed locally::

    dask
    distributed
    tornado
    cloudpickle
    msgpack

Additionally, package sync ensures that the versions of these packages match exactly with what you have locally, even cross-platform.