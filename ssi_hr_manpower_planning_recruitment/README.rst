.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
HR - Manpower Planning - Recruitment
====================================

Connects the manpower planning (MPP) of ``ssi_hr_manpower_planning`` to the recruitment
vacancies of ``ssi_hr_recruitment``. From a running planning, the HR user opens a wizard
that proposes one line per job position that still has vacant formation, with the
remaining quantity. After completing the expected join date and the reason, the wizard
creates one draft recruitment vacancy per line, linked to the planning. The vacancies go
through the standard approval of recruitment vacancies, and the planning shows how many
of them were requested.


Work Instruction
================

* `Create Recruitment Vacancy from Manpower Planning <docs/manpower_planning/index.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-hr-manpower-planning
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *HR - Manpower Planning - Recruitment*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-hr-manpower-planning/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
