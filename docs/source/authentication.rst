.. _authentication:

Hub Authentication
===========================

This section documents the different options of configuring authentication
for a hub and how to setup each one of them for your hub. Each hub can have
a differently configured authentication mechanism

Available auth methods:

* Google OAuth
* GitHub OAuth
* Hash authentication

Below we explain how to configure each option.

`GitHub OAuth` is good when you want to provide logins to people who have a
GitHub account already.

`Google OAuth` is good for a hub that is used by UC Boulder students as they
will not need to create a new account.

`Hash authentication` is good for workshops with participants who might not
have a UC Boulder account. The Hash authenticator is not part of the default
JupyterHub setup we use, so you will have to create a :ref:`self-made-hub-image`.


User Whitelist and Admin Accounts
---------------------------------

You can control what users can login by creating a whitelist of usernames. This
is independent of which authenticator you use. All authenticators eventually
assign a user a username, and that username is then checked against the whitelist. You can
also create a list of admin users, these people get special privileges like
being able to restart individual user's servers.

To add the users :code:`swiss-roll` and :code:`bbq-pizza` to the whitelist use
the following snippet in the file :code:`hub-configs/<hubname>.yaml`:

.. code-block:: yaml

    auth:
      whitelist:
        users:
          - swiss-roll
          - bbq-pizza

With this setup no one except these two users will be able to login.

To allow a user to log in with admin access:

.. code-block:: yaml

    auth:
      admin:
        access: true
        users:
          - swiss-roll
          - bbq-pizza


GitHub Authentication
---------------------

GitHub authentication is good if all of your users have a GitHub
account (this is probably true if you are using GitHub as part of your teaching).

For a full description on using GitHub authentication with JupyterHub, check
the `GitHub Authentication section <https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#github>`_
of the zero2jupyterhub guide.

To use GitHub Authentication, you need to create a GitHub OAuth app for the hub.

Creating a GitHub OAuth app
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We want the authentication apps to be owned by the `earthlab <https://github.com/earthlab>`_ organization. You can either create the app there (if you have permission) or you can create the app in your own account and then transfer it to earthlab once you have everything configured.

Follow the instructions for `Creating an OAuth app <https://docs.github.com/en/developers/apps/creating-an-oauth-app>`_ on the GitHub documentation. Note that these assume you are creating in your personal account. If you are instead using the organization account, choose the :code:`Settings` tab on the organiation homepage.

Use the following settings::

  Application name: set this to hubname
  Homepage Url: https://hub.earthdatascience.org/hubname
  Authorization Callback Url: https://hub.earthdatascience.org/hubname/hub/oauth_callback

Then click "Register Application". Once you register the application, you will get a ClientID (this is public) and a Client Secret (this is private).

Adding GitHub configuration
---------------------------

There is a public and a private part to the configuration. First, the private part. Add the ID and Secret to the :code:`secrets/hubname/yaml` file. Here is an example::

.. code-block:: yaml

    auth:
      type: github
      github:
        clientId: "5636ad98ccccbbbbaaaa"
        clientSecret: "3683566baaaabbbbccccxxxxff1ba7198a3022be"


.. note::

  To modify the secrets files you need to first unlock those files
  using git-crypt. Then, git-crypt will ensure they are re-encypted before being pushed to GitHub. See :ref:`git-crypt` for details.

The public part of the configuration is done in :code:`hub-configs/<hubname>.yaml`:

.. code-block:: yaml

  auth:
    admin:
      access: true
      users:
        - usernameA
        - usernameB
    whitelist:
      users:
        - usernameA
        - usernameC
        - usernameD
    type: github
    github:
      callbackUrl: "https://hub.earthdatascience.org/hubname/hub/oauth_callback"

In this example configuration only the users listed under admin or whitelist will be allowed to login.

Google OAuth
------------

The Google OAuth setup is good if you want students from UC Boulder to be able
to login without needing an additional account.

For full details check the `Google Authentication section <https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#google>`_
of the zero2jupyterhub guide.

Create a OAuth application in the Google Developer console by going to `<https://console.developers.google.com/apis/credentials?project=ea-jupyter>`_. Make
sure you are in the "credentials" section of "API&Services".

Click "Create credentials" and select "OAuth client ID" from the dropdown.
Select "Web application" in the next menu. Fill out the form. The most important
field is "Authorized redirect URIs". Set this to :code:`https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback`.

Once you create the app you will be provided with a Client ID and a Client secret. You
need to add both in :code:`secrets/<NAMEOFYOURHUB>.yaml`.

An example of what to add to your secrets file:

.. code-block:: yaml

    jupyterhub:
      auth:
        google:
          clientId: "12345678988-abcdabcdat331tvltueu44elt98rb54f.apps.googleusercontent.com"
          clientSecret: "abcabcabcababcabcabc-abc"

The public part of the configuration has to be done in :code:`hub-charts/<NAMEOFYOURHUB>/values.yaml`:

.. code-block:: yaml

    jupyterhub:
      auth:
        type: google
        google:
          callbackUrl: "https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback"
          hostedDomain: "colorado.edu"
          loginService: "Colorado University"

In this configuration only users with a Google account that ends in :code:`colorado.edu`
will be able to login.


Hash authenticator
------------------

The Hash authenticator setup is good for hubs that are used during a workshop
with participants who do not have a UC Boulder account.

To be able to use the hash authenticator you will need to have a custom image
for your hub as the Hash authenticator package is not installed by default.
You will have to create a :ref:`self-made-hub-image`.

The public part of the configuration has to be done in :code:`hub-charts/<NAMEOFYOURHUB>/values.yaml`:

.. code-block:: yaml

    jupyterhub:
      hub:
        extraConfig:
          auth: |
            c.JupyterHub.authenticator_class = 'hashauthenticator.HashAuthenticator'
          admin: |
            c.Authenticator.admin_users = {'leah-admin', 'tim-admin'}
            c.JupyterHub.admin_access = True

An example of what to add to your :code:`secrets/<NAMEOFYOURHUB>.yaml`:

.. code-block:: yaml

    jupyterhub:
      hub:
        extraConfig:
          auth: |
            c.HashAuthenticator.secret_key = 'not-secret-at-all-replace-me!'
