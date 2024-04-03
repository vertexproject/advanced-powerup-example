.. toctree::
    :titlesonly:

.. highlight:: none

.. _adminguide:

.. storm-cortex:: default
.. storm-pre:: auth.user.add visi
.. storm-pre:: auth.role.add ninjas
.. storm-svc:: synmods.examplepowerup.service.ExamplePowerup examplepowerup {"foo": "bar"}
.. storm-opts:: {"vars": {"pkgname": "synapse-examplepowerup"}}

Admin Guide
###########

Configuration
=============

Permissions
-----------

.. storm:: --hide-query pkg.perms.list $pkgname

You may add rules to users/roles directly from storm:

.. storm:: auth.user.addrule visi power-ups.examplepowerup.user

or:

.. storm:: auth.role.addrule ninjas power-ups.examplepowerup.user

Workflows
=========

Synapse-ExamplePowerup provides the following workflows in Optic:

.. storm:: --hide-query for $d in $lib.pkg.get($pkgname).optic.displays { $lib.print("Title: {t}", t=$d.title) }

Node Actions
============

Synapse-ExamplePowerup provides the following node actions in Optic:

.. storm:: --hide-query for $a in $lib.pkg.get($pkgname).optic.actions { $lib.print("Name : {n}", n=$a.name) $lib.print("Desc : {d}", d=$a.descr) $forms=$a.forms if $forms { $f=$lib.str.join(", ", $a.forms) $lib.print("Forms: {f}", f=$f) } else { $lib.print("Forms: Any") } $lib.print("") }

Onload Events
=============

Update your documentation to reflect any ``onload`` events in use...

Synapse-ExamplePowerup does not use any ``onload`` events.

OR

Synapse-ExamplePowerup uses an ``onload`` event to do something.
