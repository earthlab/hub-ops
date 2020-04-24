Git Crypt
=====================


Setup git-crypt
--------------------

The files in :code:`secrets/` are encrypted with `git-crypt <https://www.agwa.name/projects/git-crypt/>`_.
This allows
us to store sensitive information in the repository "in plain sight". Travis
knows how to decrypt these files and by the end of this section so will you.

1) To begin, install :code:`git-crypt`. On OSX use:

.. code:: bash

    brew install git-crypt

Alternatively, follow the instructions on https://www.agwa.name/projects/git-crypt/

2) Obtain a copy of :code:`hub-ops.gitcrypt.key`. You can ask Leah Wasser or Max
   Joseph for a copy. Copy the file into your checkout of :code:`hub-ops`
3) From the checkout directory run

.. code:: bash

    cat hub-ops.gitcrypt.key | git-crypt unlock -

or

   .. code:: bash

       git-crypt unlock hub-ops.gitcrypt.key

You should now be able to see plain text files in :code:`secrets/`.

4) Add your name to the list of people to contact in step 2.
