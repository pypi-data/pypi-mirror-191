================================
Using Package Sync in Production
================================

When running production workloads, it's best practice to have a *deterministic* software environment: to always have the same set of packages installed every time. You don't want a critical pipeline to go down because a buggy new version of a dependency was just released.

*Package sync is fully deterministic for same-platform clusters*: the conda and pip packages installed on the cluster are exactly what is installed on the client. Therefore, as long as you lock down the client environment, the cluster's Python environment will be locked down as well.

**The best practices for using package sync in production are:**

1. :ref:`Ensure your client environment is consistent <consistent-client-env>`
2. :ref:`Launch clusters from Linux clients <linux-client>`

.. _consistent-client-env:

Ensure client environment is consistent
=======================================

Package sync works with nearly any method of reproducing a Python environment, from deterministic tools like Poetry to a ``requirements.txt`` file, because it just scans the currently-installed packages. Examples of these methods include:

* `Poetry <https://python-poetry.org/>`_
* `conda-lock <https://github.com/conda/conda-lock>`_
* `pip-tools <https://pip-tools.readthedocs.io/en/latest/>`_
* ``requirements.txt`` for pip packages
* ``environment.yaml`` for conda
* Docker (though in some cases, you may want to just run the Docker image on the cluster; see notes :ref:`here <when-not-pkg-sync>`)

Note that clusters using package sync are only as deterministic as your environment. If you use an ``environment.yaml`` or ``requirements.txt``, for example, it's possible that without any changes to that file, the packages that get installed on your client—and therefore cluster—could change, just because a new version of a package was released.

Tools like Poetry, conda-lock, or pip-tools are made to address this problem. They create a lockfile that specifies every package, including transitive dependencies, so you're guaranteed to always get the same environment, even when packages you don't realize you depend on release new versions. By commiting the lockfile to version control, it's also easy to roll back to past versions of the environment.

.. _linux-client:

Launch clusters from Linux
==========================

The package versions installed on the cluster will match exactly as long as the client (the machine calling :obj:`coiled.Cluster`) is running Linux (see the :ref:`cross-platform section <pkg-sync-cross-platform>` for details).

Luckily, if you're running an automated system in production, it's very, very likely that the client will be running Linux. Examples of places you might create a cluster from in production:

* CI systems (GitHub Actions, CircleCI, etc.)
* Kubernetes
* Prefect Cloud
* Dagster
* AWS ECS, AWS Fargate, GCP Cloud Run
* Anything else running a Docker image

In all of these, the client creating the cluster would be running on Linux.


.. _when-not-pkg-sync:

When to not use package sync in production
==========================================

* You need system dependencies that :ref:`can't be installed with package sync <pkg-sync-system-deps>`.
* You already have a Docker image you'd like to use, and infrastructure to build and maintain that image.

  If you're already using Docker, you still could use package sync to get :ref:`faster cluster startup <pkg-sync-performance>` than you would :ref:`running the image on the cluster <software-docker>` (assuming you only have conda and pip packages in the image, not :ref:`system dependencies <pkg-sync-system-deps>`).

  However, it might make sense to keep using your Docker image on the cluster if it already works for you. If you already have a system you're happy with, no need to change it!

* Your organization has security scanning pipelines for Docker images or other such restrictions, and expects only those images to be run.
