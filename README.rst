
=======================================================
djwip: datajoint-python work-in-progress utilities/misc
=======================================================
:Author: C.Turner
:Status: DRAFT

THIS IS NOT ACTUALLY ACCURATE - repo is not official in any way.

Overview
========

Grab-Bag for various datajoint-python addons/features/misc which
have not been discussed/slated/included for official merge into
datajoint-python proper.

Current proposed structure:

- ``djwip/ext``: stabilized/'semi-official' wip utilities which are
  feature complete but for various reasons cannot/will not be
  merged into datajoint proper.

- ``djwip/future``: integration branch for features being merged
  into mainline - e.g. 'alpha'/'beta' modules/features.

- ``djwip/<github-username>`` : per-developer sandbox; allows scratch
  development and distribution without impacting other code

These directories should be suitable for import as python modules, eg:

  >>> import djwip.ext.frobnicator as frob
  >>> from djwip.future import KeystoneXL
  >>> import djwip.ixcat as mydj

Unit Tests
----------

Unit tests are kept in a separate directory heirarchy ``tests`` which
mirrors the above. Anything moved into ext or future should have a
unit test; per-user areas, as works in progress can by in any state
of operation, though it would be ideal if code is appropriately
labeled as functional, etc.

Related Files
-------------

Related files such as pip requirements / setup scripts / documentation
etc should be kept within ``<github-username>`` directories or optionally
per-feature subdirectories of same until they are migrated to the
relatively stable djwip/ext or djwip/future area.

Requirements
============

- datajoint requirements
- various per-addon requirements

