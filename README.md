Brewing 101 XBlock
==================

Overview
--------

This is a demonstration implementation of an edX XBlock that explores several
features:

* Different types of scopes
* Retrieving and displaying data from the containing course
* AJAX interaction between web client and server
* Studio modifiable settings
* Publishing grade for the lesson
* and more

There are two parts of this XBlock:

1. Poll - The student is asked if he/she has brewed before. This poll is optional the poll results are stored.

2. Exercise - The user is presented with an exercise to solve. The user is to calculate and enter the answer, then click the submit button.

This project was scaffolded using the xblock-sdk generator:

```workbench-make-xblock```

The studio functionality is adapted from scormxblock:

* https://github.com/appsembler/edx_xblock_scorm


Source of formula

* http://www.morebeer.com/brewingtechniques/library/backissues/issue5.4/palmer_sb.html


Installation
------------

Refer to the edX XBlock installation instructions:

* http://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html

Testing
-------

Testing is broken. It appears the tests need to run through manage.py:

```python manage.py test```

But manage.py needs to be run from 


Currently the following error occurs when running

```ERROR: Failure: ImproperlyConfigured (Requested setting DEFAULT_INDEX_TABLESPACE, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.)```
