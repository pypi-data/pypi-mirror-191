Manually configure your cloud provider
======================================

Coiled creates and manages Dask clusters in your own cloud provider account. This allows you to make use of security/data access controls, compliance standards, and promotional credits that you already have in place.

To set up Coiled with the default network and container registry options, where Coiled creates a VPC in your account and uses Google Artifact Registry or Amazon Elastic Container Registry for storing your Python environments, see :doc:`cli_setup`.

To configure Coiled to use a custom network configuration (e.g. your pre-existing VPC) or a different container registry for your Python environment (e.g. Docker Hub), see the manual configuration instructions for :doc:`AWS <aws_configure>` or :doc:`GCP <gcp_configure>`.

.. toctree::
   :maxdepth: 1
   :hidden:

   aws_configure
   gcp_configure