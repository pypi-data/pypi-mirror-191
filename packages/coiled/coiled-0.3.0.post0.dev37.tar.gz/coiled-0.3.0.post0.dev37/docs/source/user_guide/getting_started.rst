Coiled clusters in 10 minutes
=============================

In this guide you will:

#. Sign up for Coiled
#. Install the Coiled Python library
#. Log in to your Coiled account
#. Configure your cloud provider
#. Run your Dask computation in your cloud account

Here's a video walkthrough of the process:

.. raw:: html

    <iframe width="560" height="315" src="https://www.youtube.com/embed/q_5onf9mpsw?start=153" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

1. Sign up
----------

`Sign up for Coiled <https://cloud.coiled.io/signup>`_ using GitHub, Google, or your email address.

2. Install
----------

.. tabs::

    .. tab:: Install with pip

        .. code-block:: bash

            pip install coiled 'dask[complete]'

    .. tab:: Install with conda

        .. code-block:: bash

            conda install -c conda-forge coiled
        
.. _coiled-setup:

3. Log in
---------

You can log in using the ``coiled login`` command line tool:

.. code-block:: bash

    $ coiled login

You'll then navigate to https://cloud.coiled.io/profile on the Coiled web
app where you can create and manage API tokens.

.. code-block:: bash

    Please login to https://cloud.coiled.io/profile to get your token
    Token:

Your token will be saved to :doc:`Coiled's local configuration file <configuration>`.

.. note:: **For Windows users**
   
   Unless you are using WSL, you will need to go to a command prompt or PowerShell window within an environment that includes coiled (see the next step) to login via ``coiled login``.
   
   Additionally, users should provide the token as an argument, i.e. ``coiled login --token <your-token>`` from the command line or ``!coiled login --token <your-token>`` from a Jupyter notebook, since the Windows clipboard will not be active at the "Token" prompt.

4. Configure your cloud provider
--------------------------------

Use the CLI tool to quickly configure your GCP or AWS account (see :doc:`cli_setup`)::

    coiled setup wizard

:ref:`no-cloud-provider`

.. _first-computation:

5. Run your Dask computation
----------------------------

Next, spin up a Dask cluster in your cloud by creating a :class:`coiled.Cluster` instance
and connecting this cluster to the Dask ``Client``.

.. code-block:: python

    import coiled

    # create a remote Dask cluster with Coiled
    cluster = coiled.Cluster(name="my-cluster")

    # connect a Dask client to the cluster
    client = cluster.get_client()

    # link to Dask scheduler dashboard
    print("Dask scheduler dashboard:", client.dashboard_link)


.. note::
   If you're using a :doc:`Team account <teams>`, be sure to specify
   the ``account=`` option when creating a cluster:

   .. code-block:: python

      cluster = coiled.Cluster(account="<my-team-account-name>")

   Otherwise, the cluster will be created in your personal Coiled account.

You will then see a widget showing the cluster state overview and progress bars as resources are provisioned (this may take a minute or two).

.. figure:: images/widget-gif.gif
   :alt: Terminal dashboard displaying the Coiled cluster status overview, configuration, and Dask worker states.

Once the cluster is ready, you can submit a Dask DataFrame computation for execution. Navigate to the `Dask scheduler dashboard <https://docs.dask.org/en/stable/dashboard.html>`_ (see ``Dashboard Address`` in the widget) for real-time diagnostics on your Dask computations.

.. code-block:: python

    import dask

    # generate random timeseries of data
    df = dask.datasets.timeseries("2000", "2005", partition_freq="2w").persist()

    # perform a groupby with an aggregation
    df.groupby("name").aggregate({"x": "sum", "y": "max"}).compute()

You can also monitor your cluster, access the Dask scheduler dashboard, and see cluster state and worker logs from https://cloud.coiled.io.

.. figure:: images/cloud-cluster-dashboard.png
    :width: 100%
    :alt: Cluster dashboard on the Coiled cloud web app with rows for each cluster and columns for cluster name, status, number of workers, software environment, last seen timestamp, and cost (in credits).
   
    Cluster dashboard (click to enlarge)

Lastly, you can stop the running cluster using the following commands. By default, clusters will shut down after 20 minutes of inactivity.

.. code-block:: python

    # Close the cluster
    cluster.close()

    # Close the client
    client.close()

Learn more about options for launching Dask clusters :doc:`here <cluster_creation>`.
