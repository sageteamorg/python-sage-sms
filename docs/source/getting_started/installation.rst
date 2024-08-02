Installation Guide
==================

Step 1: Create a Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's a good practice to use a virtual environment to manage dependencies for your project. To create a virtual environment, use the following command:

.. code-block:: bash

    python -m venv .venv

Replace ``.venv`` with your preferred name for the virtual environment.

Step 2: Activate the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activate the virtual environment using the following command:

- On Windows:

  .. code-block:: bash

      .venv\Scripts\activate

- On macOS and Linux:

  .. code-block:: bash

      source .venv/bin/activate

Step 3: Install ``python-sage-sms``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With the virtual environment activated, install the ``python-sage-sms`` package using pip:

.. code-block:: bash

    pip install python-sage-sms

Install using Poetry
--------------------

Poetry is a dependency management tool for Python that ensures you have the right package versions and dependencies.

Step 1: Install Poetry
~~~~~~~~~~~~~~~~~~~~~~

If you haven't installed Poetry yet, you can do so by following the official installation instructions at the `Poetry website <https://python-poetry.org/docs/#installation>`_.

Step 2: Create a New Project (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're starting a new project, you can create it using Poetry:

.. code-block:: bash

    poetry new myproject
    cd myproject

Replace ``myproject`` with your preferred project name.

Step 3: Add ``python-sage-sms`` as a Dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add ``python-sage-sms`` to your project dependencies using the following command:

.. code-block:: bash

    poetry add python-sage-sms

This will install the package and update the ``pyproject.toml`` file with the new dependency.

Step 4: Activate the Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Poetry automatically manages a virtual environment for your project. To activate it, use:

.. code-block:: bash

    poetry shell

Verification
------------

To verify the installation, you can run a simple script to import the package:

.. code-block:: python

    # Import the factory class from the package
    from sage_sms.factory import SMSBackendFactory

    # Define settings for the SMS provider
    settings = {
        "debug": False,
        "provider": {
            "NAME": "provider_name",
            "API_KEY": "your_api_key"
        }
    }

    # Settings and The base package path for the backends
    factory = SMSBackendFactory(settings, "sage_sms.backends")

    # Get the SMS provider class and instantiate it
    sms_provider_class = factory.get_backend()
    sms_provider = sms_provider_class(settings)

    # Send a test SMS message
    sms_provider.send_one_message("+1234567890", "Hello, World!")

Run the script using the Python interpreter within your virtual environment or Poetry shell to ensure everything is set up correctly.
