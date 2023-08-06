:notoc:

.. _user-guide:

===========
Coiled Docs
===========

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Start Here

   getting_started

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Using Coiled Clusters

   cluster_creation
   cluster_scaling
   cluster_reuse
   cluster_management
   package_sync
   software_environment

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Cloud Providers

   backends
   cli_setup
   manual_configure
   cloud-provider-reference

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Coiled Features

   accessing_secure_data
   analytics
   performance_reports
   logging
   gpu
   configuration
   teams
   security

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Guides

   examples
   tutorials/index
   best_practices

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Help

   support
   faq
   troubleshooting/index

.. toctree::
   :maxdepth: 1
   :hidden:
   :caption: Reference

   quick_reference
   api
   release_notes
   oss-foundations

👋 Welcome to Coiled's documentation!

How Coiled works
----------------

Coiled handles the creation and management of Dask clusters in the cloud
through a continuously running control plane.

.. figure:: images/coiled-architecture.png
   :width: 100%
   :alt: Coiled Architecture

   Coiled Architecture (click image to enlarge)

* **User Environment**

  This is where you use the Coiled Python package along
  with your preferred tools to create Dask clusters and submit Dask
  computations. This could be a Jupyter Notebook on your laptop, a Python script
  on a cloud-hosted VM, or Python code within a task in a workflow management
  system.

* **Coiled Cloud**

  `Coiled Cloud <https://cloud.coiled.io/>`_ provides a dashboard that
  you can use to manage clusters, users, teams, software environments, etc.
  Coiled Cloud also handles provisioning the necessary cloud infrastructure in your cloud account for
  your Dask clusters so you don't have to!

* **Cloud Computing Environment**

  This is the cloud environment where Dask clusters will be created and where
  your Dask computations will run. You can configure Coiled to run in your AWS or Google Cloud account (see :doc:`cli_setup`).


Where does Coiled run?
----------------------

Coiled creates and manages Dask clusters in your own :doc:`cloud provider account <backends>`.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-6 col-md-6 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Use Coiled with AWS
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-aws.png
      :width: 35%
      :alt: Use Coiled with Amazon Web Services (AWS)

   +++

   .. link-button:: cli_setup
      :type: ref
      :text: Get Started with AWS
      :classes: btn-full btn-block stretched-link

   ---


   Use Coiled with GCP
   ^^^^^^^^^^^^^^^^^^^

   .. figure:: images/logo-gcp.png
      :width: 100%
      :alt: Use Coiled with Google Cloud Platform (GCP)

   +++

   .. link-button:: cli_setup
      :type: ref
      :text: Get Started with GCP
      :classes: btn-full btn-block stretched-link


What can you do with Coiled?
----------------------------

`Coiled <https://coiled.io>`_ provides cluster-as-a-service functionality to
provision hosted Dask clusters on demand. It takes the DevOps out of data
science and enables data engineers and data scientists to spend more time on
their real job and less time setting up networking, managing fleets of Docker
images, etc.

.. panels::
   :card: border-0
   :container: container-lg pb-3
   :column: col-md-4 col-md-4 col-md-4 p-2
   :body: text-center border-0
   :header: text-center border-0 h4 bg-white
   :footer: border-0 bg-white

   Managed Dask Clusters
   ^^^^^^^^^^^^^^^^^^^^^

   Securely deploy Dask clusters from anywhere you run Python.

   +++

   .. link-button:: cluster_creation
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---


   Package Sync
   ^^^^^^^^^^^^

   Package sync replicates your local Python environment onto the custer, automatically.

   +++

   .. link-button:: package_sync
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link

   ---


   Manage Teams & Costs
   ^^^^^^^^^^^^^^^^^^^^

   Manage teams, collaborate, set resource limits, and track costs.

   +++

   .. link-button:: teams
      :type: ref
      :text: Learn more
      :classes: btn-full btn-block stretched-link
