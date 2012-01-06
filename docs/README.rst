====================
Track multiple Tracs
====================

:Project title: MultiTrac
:Project id: multitrac
:Author: NiteoWeb Ltd.
:Source: https://github.com/niteoweb/MultiTrac
:Docs: http://readthedocs.org/docs/multitrac
:Framework: Pyramid

Quick Start
===========

Start hacking away on this project by running::

  $ cd ~/work
  $ mkdir multitrac
  $ cd multitrac
  $ git clone git@github.com:niteoweb/MultiTrac.git
  $ virtualenv -p python2.6 --no-site-packages ./
  $ bin/python bootstrap.py -c development.cfg
  $ bin/buildout -c development.cfg
  $ bin/paster serve etc/development.ini
