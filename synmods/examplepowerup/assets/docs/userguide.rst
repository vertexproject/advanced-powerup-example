.. toctree::
    :titlesonly:

.. highlight:: none

.. _userguide:

.. storm-cortex:: default
.. storm-svc:: synmods.examplepowerup.service.ExamplePowerup examplepowerup {"foo": "bar"}
.. storm-opts:: {"vars": {"pkgname": "synapse-examplepowerup"}}

User Guide
##########

Synapse-ExamplePowerup adds new Storm commands.

Getting Started
===============

Check with your Admin to enable permissions.

Examples
========

Use foo thing to do bar that i care about
-----------------------------------------

Enrich some nodes with examplepowerup.enrich and yield the results:

.. storm:: [ inet:fqdn=vertex.link ] | examplepowerup.enrich --yield

Search for some nodes:

.. storm:: examplepowerup.search lol --yield

Use of ``meta:source`` nodes
============================

Synapse-ExamplePowerup uses a ``meta:source`` node and ``-(seen)>`` light
weight edges to track nodes observed from the ExamplePowerup API.

.. storm:: meta:source=3faafd06b11d05ed4f8a126236de63c3

Storm can be used to filter nodes to include/exclude nodes which have been observed
by Synapse-ExamplePowerup.  The following example shows how to filter the
results of a query to include only results observed by Synapse-ExamplePowerup:

.. storm:: #cool.tag.lift +{ <(seen)- meta:source=3faafd06b11d05ed4f8a126236de63c3 }

