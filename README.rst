advanced-powerup-example
========================

This is an example of an Advanced Power-Up for Synapse. This can be used as a reference for building your own Power-Ups.

Using this Repo
---------------

This repository is designed to be able to be forked and modified as needed. If this is being used as the basis
for an Advanced Power-Up, the following steps should be done:

#. Setup a Python 3.11 environment as needed (using tools such as ``venv`` or ``pyenv``). Install the requirements:

  ::

    python -m pip install -U -r requirements.txt

#. Replace the ``3faafd06b11d05ed4f8a126236de63c3`` guid value in the repository with a random value. You can use
  ``python -m synapse.tools.guid`` to generate a random guid for this purpose. This ensures that your Power-Up will
  have a unique guid for its ``meta:source`` node. You can use the following commands to do that:

  ::

    export NEW_GUID="$(python -m synapse.tools.guid)"
    echo "Updating guid to $NEW_GUID" && find ./synmods/ -type f -exec sed -i "s/3faafd06b11d05ed4f8a126236de63c3/$NEW_GUID/gI" {} \;
    # add the changed files and commit them.
    git add -p
    git commit -m "Updated meta:source guid to $NEW_GUID"

#. Many files have ``examplepowerup`` in their path, and references to that string in their contents
   (``examplepowerup``, ``ExamplePowerup``). You can go through the following steps to move the files and update their
   contents. The following example renames the powerup to ``mypowerup``.

  ::

    export NEW_SVC_NAME=MyPowerup
    export NEW_LOWER_NAME=$(echo "$NEW_SVC_NAME" | tr '[:upper:]' '[:lower:]')
    git mv synmods/examplepowerup synmods/$NEW_LOWER_NAME
    for FILE in $(find ./synmods/$NEW_LOWER_NAME/ -type f -name *examplepowerup*); do NEWFILE=$(echo $FILE | sed -e "s/examplepowerup/$NEW_LOWER_NAME/"); echo "Moving $FILE to $NEWFILE"; git mv $FILE $NEWFILE; done
    find ./synmods/$NEW_LOWER_NAME/ -type f -exec sed -i "s/examplepowerup/$NEW_LOWER_NAME/g" {} \;
    find ./synmods/$NEW_LOWER_NAME/ -type f -exec sed -i "s/ExamplePowerup/$NEW_SVC_NAME/g" {} \;
    find ./docker/ -type f -exec sed -i "s/ExamplePowerup/$NEW_SVC_NAME/g" {} \;
    find ./docker/ -type f -exec sed -i "s/examplepowerup/$NEW_LOWER_NAME/g" {} \;
    sed -i "s/examplepowerup/$NEW_LOWER_NAME/g" pyproject.toml
    sed -i "s/examplepowerup/$NEW_LOWER_NAME/g" .bumpversion.cfg
    git add -p
    git commit -m "Updated repo to use $NEW_SVC_NAME / $NEW_LOWER_NAME"


Running Tests
-------------

You can use ``pytest`` to execute the unit tests. A ``pytest.ini`` file is provided to provide configurations for
running tests:

  ::

    python -m pytest <pytest arguments>


CI Configurations
-----------------

This repository contains an example CI configuration for use with CircleCI. You can adapt this configuration to other
CI systems as needed.

Docker Images
-------------

Docker images can be built using the ``docker/scripts/build.sh`` script. This script will also set the current ``git``
commit in the ``version.py`` file.

  ::

    # Build an untagged image for the ``examplepowerup``.
    ./docker/scripts/build.sh

This script tags an optional ``tag`` argument. It will be used to set the tag of the image.

  ::

    # Build an untagged image for the ``examplepowerup:mycooltag``.
    ./docker/scripts/build.sh mycooltag

You can modify this script as needed. You can also setup your own CI processes to build images.

Deploying Your Advanced Powerup
-------------------------------

Once a container has been built and is available, you can deploy the service. This follows the same process that is
described in the Synapse `Deployment Guide`_.

**Inside the AHA container**

Generate a one-time use provisioning URL:

  ::

    python -m synapse.tools.aha.provision.service 00.mypowerup

You should see output that looks similar to this::

    one-time use URL: ssl://aha.<yournetwork>:27272/<guid>?certhash=<sha256>

**On the Host**

Create the container directory:

  ::

    mkdir -p /srv/syn/00.mypowerup/storage
    chown -R 999 /srv/syn/00.mypowerup/storage

Create the ``/srv/syn/00.mypowerup/docker-compose.yaml`` file with contents:

  ::

    version: "3.3"
    services:
      00.mypowerup:
        user: "999"
        # Make sure you are using an appropriate tag for your docker containers!
        image: mypowerup:latest
        network_mode: host
        restart: unless-stopped
        volumes:
            - ./storage:/vertex/storage
        environment:
            - SYN_MYPOWERUP_AHA_PROVISION=ssl://aha.<yournetwork>:27272/<guid>?certhash=<sha256>
            - SYN_MYPOWERUP_FOO=someConfigurationValue

.. note::

    Don't forget to replace your one-time use provisioning URL!

Start the container:

  ::

    docker-compose --file /srv/syn/00.mypowerup/docker-compose.yaml up -d

Remember, you can view the container logs in real-time using:

  ::

    docker-compose --file /srv/syn/00.mypowerup/docker-compose.yaml logs -f

**On the Cortex**

From a Storm console add the service to the Cortex:

  ::

    storm> service.add mypowerup aha://mypowerup...


You should then see your service listed with the Storm ``service.list`` command.

  ::

    storm> service.list

    Storm service list (iden, ready, name, service name, service version, url):
        3ebff1cd081f96e146c7b42d2510998c true (mypowerup) (mypowerup @ 0.0.1): aha://mypowerup...

    1 services


Building Wheel packages
-----------------------

If you need to build a wheel package for distribution, you can readily do that using the following tools:

  ::

    # Set the current git commit version
    python -m vtx_common.tools.replace_commit ./synmods/*/version.py

    # Build the package documentation. This requires having pandoc available.
    python -m vtx_common.tools.buildpkg synmods/*/assets/*.yaml

    # Build the wheel
    python -m build --wheel

The ``.whl`` file should now be located in the ``./dist`` directory.

Bumpversion
-----------

The ``bumpversion`` tool can be used to increment the version of the powerup. This can be done as part of any release
processes you use for the powerup. The bumpversion configuration will automatically update the Storm package version
and the version tracked in the ``version.py`` file.

When the project is ready to be tagged for release from the initial ``0.0.1`` version of the library, you can do the
following:

  ::

    # The --new-version value takes precdene over major/minor/patch arguments.
    bumpversion --new-version 0.1.0 patch

Once the version has been bumped, push the current head and the new tag. For example:

  ::

    git push && git push origin v0.1.0

After that, you can use ``bumpversion major``, ``bumpversion minor``, and ``bumpversion patch`` commands to update the
major, minor, and patch numbers easily.


.. _Deployment Guide: https://synapse.docs.vertex.link/en/latest/synapse/deploymentguide.html
.. _Devops Guide: https://synapse.docs.vertex.link/en/latest/synapse/devopsguide.html
