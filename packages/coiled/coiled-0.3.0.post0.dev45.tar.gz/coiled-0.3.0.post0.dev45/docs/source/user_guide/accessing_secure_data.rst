==================
Remote Data Access
==================

You'll probably need your Dask workers to process private data (e.g. in S3), so you will need a way for those workers
to authenticate.

In most cases, Coiled handles this for you and you can run the same code on your cluster that you do locally.


AWS
===

Suppose you have an object in an S3 bucket ``s3://david-auth-example/hello.txt`` that's only accessible from your AWS account.

You might have code like this that you run locally to read some data from S3:

.. code-block::

  def read_object():
      s3 = boto3.client("s3")
      data = s3.get_object(Bucket='david-auth-example', Key="hello.txt")
      return data["Body"].read()
  
  text = read_object()

When this code runs on your local machine, it's using the AWS credentials you have in your local environment.
What would you need to do to make this code work on a Coiled cluster?

Personal STS tokens
-------------------

Our goal is to make the transition from running locally to running in a cluster as seamless as possible, so
by default Coiled uses your local credentials to create a temporary STS token
(encrypted in transit) that we send to the cluster.

Coiled does this by setting environment variables ``AWS_SECRET_ACCESS_KEY`` and ``AWS_SESSION_TOKEN`` on the cluster. These variables do not contain your actual credentials, but rather the temporary STS token Coiled creates for you.

The identity we use for this is whichever one Boto on your local machine uses by default.
For example, it could come from environment variables or a ``~/.aws/credentials`` file.

If you want to check which identity Coiled will use for this by default, you can (if you have the AWS CLI installed) run ``aws sts get-caller-identity`` or in Python:

.. code-block::

  import boto3
  sts = boto3.client("sts")
  sts.get_caller_identity()

If the ``read_object`` function above worked locally, it will work on the cluster too.

You can turn off this default by specifying ``coiled.Cluster(..., credentials=None)`` when you start your cluster.

Google Cloud
============

When you configure Coiled to use your Google Cloud account (``coiled setup gcp``), we ask for two service accounts: one which Coiled will use to run instances on your behalf, and also the :ref:`data access service account <data_access_service_account>`  which will control what permissions those instances have.

You can give your workers permissions within Google Cloud by assigning permissions to that data access service account.


Service-agnostic authentication
===============================

When you create your cluster, you can specify custom environment variables by passing a dictionary 
whose keys will become environment variables on the cluster:

.. code-block::

  cluster = coiled.Cluster(environ={"AUTH_TOKEN_FOR_CUSTOM_DATABASE": "some-token"})


If none of the above options work for you, you can use this to send a token to use directly in your code that runs on the cluster.