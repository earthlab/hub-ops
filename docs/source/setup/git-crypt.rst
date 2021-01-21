Git Crypt
=========

We use `git-crypt <https://www.agwa.name/projects/git-crypt/>`_ to store the proxy secret tokens for each hub. Note that secrets requires for GitHub Actions are stored in the :code:`Settings` section in repository as per the `Actions docs <https://docs.github.com/en/actions/reference/encrypted-secrets>_`.

Setup git-crypt
--------------------

The files in :code:`secrets/` are encrypted with `git-crypt <https://www.agwa.name/projects/git-crypt/>`_.
`git-crypt` allows us to store sensitive information in the repository "in
plain sight".

1) To begin, install :code:`git-crypt`. On OSX use:

.. code:: bash

    brew install git-crypt

Alternatively, follow the instructions on https://www.agwa.name/projects/git-crypt/

2) Obtain a copy of :code:`hub-ops.gitcrypt.key`. You can ask Leah Wasser, Karen Cranston, or Max
   Joseph for a copy. Copy the file into your checkout of :code:`hub-ops`
3) From the checkout directory run:

.. code:: bash

    cat hub-ops.gitcrypt.key | git-crypt unlock -

or

   .. code:: bash

       git-crypt unlock hub-ops.gitcrypt.key

You should now be able to see plain text files in :code:`secrets/`.

4) Add your name to the list of people to contact in step 2.


Working With Encrypted Files
-----------------------------
Once you have setup git-crypt and unlocked the files locally, you will be able
to see all of the secret keys and edit things as need be. When you commit and
push, `git-crypt` will re-encrypt the files so that nothing secret is pushed
in plain text to GitHub. 
