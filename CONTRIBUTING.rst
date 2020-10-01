=======================
Contributing Guidelines
=======================

This repository contains the code needed to maintain and update the Earth Lab
Jupyter Hub.

Get Started!
============

To work on the hub-ops repo, you will need to setup the following.

1. Fork the repository on GitHub
--------------------------------

To create your own copy of the repository on GitHub, navigate to the
`earthlab/hub-ops <https://github.com/earthlab/hub-ops>`_ repository
and click the **Fork** button in the top-right corner of the page.

2. Clone your fork locally
--------------------------

Use ``git clone`` to get a local copy of your Hub-Ops repository on your
local filesystem::

    $ git clone git@github.com:your_name_here/hub-ops.git
    $ cd hub-ops/

3. Set up your fork for local development
-----------------------------------------

Install Dependencies
^^^^^^^^^^^^^^^^^^^^

Next you can install the development requirements::

    $ pip install -r dev-requirements.txt
    $ pre-commit install

4. Create a branch for local development
----------------------------------------

Use the ``git checkout`` command to create your own branch, and pick a name
that describes the changes that you are making::

    $ git checkout -b name-of-your-bugfix-or-feature

Now you can make your changes locally.

There are two protected branches in this repo - `master` and `staging`. Travis
runs on both branches, and both branches are deployed to the same Google Cloud
cluster.

If you are proposing changes that affect deployment (e.g. changing `.travis.yml`
or `deploy.py`) make and test those changes on the `staging` branch before
creating a feature branch from `master`. See the `operations guide <https://earthlab-hub-ops.readthedocs.io/en/latest/daily-operations/index.html>`_ for details.

5. Build the Docs Locally
-------------------------

Ensure that the tests pass, and the documentation builds successfully::

    $ make html

**Note to Windows users**

To use ``make`` you will need to install and configure GNU Make for Windows,
e.g., using chocolatey: https://chocolatey.org/packages/make


6. Commit and push your changes
-------------------------------

Once you are sure that all tests are passing, you can commit your changes
and push to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request on GitHub
----------------------------------

When submitting a pull request:

- All existing tests should pass. Please make sure that the test
  suite passes, both locally and on
  `Travis CI <https://travis-ci.org/earthlab/hub-ops>`_
  Status on
  Travis will be visible on a pull request. If you want to enable
  Travis CI on your own fork, please read the
  `getting started docs <https://docs.travis-ci.com/user/getting-started/>`_.

- New functionality should include tests. Please write reasonable
  tests for your code and make sure that they pass on your pull request.

- Classes, methods, functions, etc. should have docstrings. The first
  line of a docstring should be a standalone summary. Parameters and
  return values should be documented explicitly.

- The API documentation is automatically generated from docstrings, which
  should conform to NumpPy styling. For examples, see the `Napoleon docs
  <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_.

- Please note that tests are also run via Travis-CI on our documentation.
  So be sure that any ``.rst`` file submissions are properly formatted and
  tests are passing.


Documentation Updates
=====================

Improving the documentation and testing for code already in Hub-Ops
is a great way to get started if you'd like to make a contribution. Please note
that our documentation files are in
`ReStructuredText (.rst)
<http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_
format and format your pull request accordingly.

To create a vignette for an Hub-Ops workflow, create a ``.py`` file that shows the
necessary steps to complete the workflow. Make sure the file name begins with
``plot`` in order to ensure that the vignette is correctly built. Store the
vignette in the ``examples`` folder within the ``hub-ops`` directory. Hub-Ops
uses Sphinx Gallery to build vignettes. Help for formatting and building
vignettes can be found on `their website <https://sphinx-gallery.github.io>`_.


To build the documentation, use the command::

    $ make docs

By default ``make docs`` will only rebuild the documentation if source
files (e.g., .py or .rst files) have changed. To force a rebuild, use
``make -B docs``.
You can preview the generated documentation by opening
``docs/_build/html/index.html`` in a web browser.


Code Style
==========

- Hub-Ops currently only supports Python 3 (3.5+). Please test code locally
  in Python 3 when possible (all supported versions will be automatically
  tested on Travis CI).

- Hub-Ops uses a pre-commit hook that runs the black code autoformatter.
  Be sure to execute `pre-commit install` as described above, which will cause
  black to autoformat code prior to commits. If this step is skipped, black
  may cause build failures on Travis CI due to formatting issues.

- Follow `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ when possible.
  Some standards that we follow include:

    - The first word of a comment should be capitalized with a space following
      the ``#`` sign like this: ``# This is a comment here``
    - Variable and function names should be all lowercase with words separated
      by ``_``.
    - Class definitions should use camel case - example: ``ClassNameHere`` .

- Imports should be grouped with standard library imports first,
  3rd-party libraries next, and Hub-Ops imports third following PEP 8
  standards. Within each grouping, imports should be alphabetized. Always use
  absolute imports when possible, and explicit relative imports for local
  imports when necessary in tests.
