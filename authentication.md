# Authentication for the hubs

This section documents the different options for configuring authentication
for a hub that are available and how to setup each one of them.

Available auth methods:
* Google OAuth
* GitHub OAuth


## GitHub OAuth

For full details check the [GitHub Authentication section](https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#github)
of the zero2jupyterhub guide.

Create a OAuth application on GitHub by going to https://github.com/settings/developers,
in "OAuth apps" create a new app. You will have to provide a name and description.
The most important field is "Authorization callback URL" which has to be set to
`https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback`. Once you
create the app you will be provided with a Client ID and a Client secret. You
need both in `secrets/<NAMEOFYOURHUB>.yaml`.

An example of what to add to your secrets file:
```
jupyterhub:
  auth:
    type: github
    github:
      clientId: "5636ad98ccccbbbbaaaa"
      clientSecret: "3683566baaaabbbbccccxxxxff1ba7198a3022be"
```
The public part of the configuration has to be done in `<NAMEOFYOURHUB>/values.yaml`:
```
jupyterhub:
  auth:
    type: github
    github:
      callbackUrl: "https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback"
      org_whitelist:
        - "earthlab"
    scopes:
      - "read:user"
```


## Google OAuth

For full details check the [Google Authentication section](https://zero-to-jupyterhub.readthedocs.io/en/latest/authentication.html#google)
of the zero2jupyterhub guide.

Create a OAuth application in the Google Developer console by going to https://console.developers.google.com/apis/credentials?project=ea-jupyter. Make
sure you are in the "credentials" section of "API&Services".

Click "Create credentials" and select "OAuth client ID" from the dropdown.
Select "Web application" in the next menu. Fill out the form. The most important
field is "Authorized redirect URIs". Set this to `https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback`.

Once you create the app you will be provided with a Client ID and a Client secret. You
need both in `secrets/<NAMEOFYOURHUB>.yaml`.

An example of what to add to your secrets file:
```
jupyterhub:
  auth:
    google:
      clientId: "12345678988-abcdabcdat331tvltueu44elt98rb54f.apps.googleusercontent.com"
      clientSecret: "abcabcabcababcabcabc-abc"
```
The public part of the configuration has to be done in `<NAMEOFYOURHUB>/values.yaml`:
```
jupyterhub:
auth:
  type: google
  google:
    callbackUrl: "https://hub.earthdatascience.org/<NAMEOFYOURHUB>/hub/oauth_callback"
    hostedDomain: "colorado.edu"
    loginService: "Colorado University"
```
