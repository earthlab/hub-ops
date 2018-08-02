Authentication for your hub
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
have a UC Boulder account.

User whitelist and admin accounts
---------------------------------

You can control what users can login by creating a whitelist of usernames. This
is independent of which authenticator you use. All authenticators eventually
assign a user a username. This is then checked against the whitelist. You can
also create a list of admin users, these people get special privileges like
being able to restart individual user's servers.

To add the users :code:`swiss-roll` and :code:`bbq-pizza` to the whitelist use
the following snippet in your hub's :code:`values.yaml`:

.. code-block:: yaml

    jupyterhub:
      auth:
        whitelist:
          users:
            - swiss-roll
            - bbq-pizza

With this setup no one except these two users will be able to login.

To make a user the above two users admins and let them access individual user's
servers use the following snippet:

.. code-block:: yaml

    jupyterhub:
      auth:
        admin:
          access: true
          users:
            - swiss-roll
            - bbq-pizza


GitHub OAuth
------------

GitHub authentication is good if you want people who already have a GitHub
account to login.

For full details check the `GitHub Authentication section <https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#github>`_
of the zero2jupyterhub guide.

Create a OAuth application on GitHub by going to |location_link|,

.. |location_link| raw:: html

   <a href="https://github.com/settings/developers" target="_blank">Github developer settings</a>

in "OAuth apps" create a new app. You will have to provide a name and description.
The most important field is "Authorization callback URL" which has to be set to
:code:`https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback`.
Once you create the app you will be provided with a Client ID and a Client secret.
You will need to add both in :code:`secrets/<NAMEOFYOURHUB>.yaml`.

An example of what to add to your secrets file:

.. code-block:: yaml

    jupyterhub:
      auth:
        type: github
        github:
          clientId: "5636ad98ccccbbbbaaaa"
          clientSecret: "3683566baaaabbbbccccxxxxff1ba7198a3022be"

The public part of the configuration has to be done in :code:`<NAMEOFYOURHUB>/values.yaml`:

.. code-block:: yaml

    jupyterhub:
      auth:
        type: github
        github:
          callbackUrl: "https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback"
          org_whitelist:
            - "earthlab"
        scopes:
          - "read:user"

In this example configuration only users who are members of the :code:`earthlab`
organisation on GitHub will be allowed to login. To allow anyone to login remove
that part of the configuration.


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

The public part of the configuration has to be done in :code:`<NAMEOFYOURHUB>/values.yaml`:

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
See the :code:`hub-images/` subdirectory for how to create a custom image.

The public part of the configuration has to be done in :code:`<NAMEOFYOURHUB>/values.yaml`:

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
