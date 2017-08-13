# PATinderBot
Automatically like or nope users and create photo collages of Tinder recommendations

## Credits

The general idea of this Tinderbot is shared by Github user rtt here:
https://gist.github.com/rtt/5a2e0cfa638c938cca59

## General use

- Install the requirements by typing from the project dir: `pip install -r requirements/local.txt`
- Create a secrets file (see below)
- Run module tinder_bot
- Adjust schools.json after each run (see below)
- Enjoy photo collages in folder img 

## Secrets file

You need to store your Facebook ID and a Facebook authentication token in the file secrets.json.
This file secrets.json is not in the Git repository, since it contains your personal information.
To create it, perform the following:

- Copy secrets_template.json to secrets.json
- Visit the following URL to find your Facebook ID, and fill it in the secrets file:
    http://findmyfbid.com/
- Visit the following URL in your browser:
    NOTE: I found that the redirect did work in Firefox, but not in Chrome
    https://www.facebook.com/_login.php?skip_api_login=1&api_key=464891386855067&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.6%2Fdialog%2Foauth%3Fredirect_uri%3Dfbconnect%253A%252F%252Fsuccess%26scope%3Demail%252Cpublic_profile%26response_type%3Dtoken%26client_id%3D464891386855067%26ret%3Dlogin%26logger_id%3D7bcb1270-830d-4da5-8142-7b89e95757b5&cancel_url=fbconnect%3A%2F%2Fsuccess%3Ferror%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied&display=page&locale=nl_NL&logger_id=7bcb1270-830d-4da5-8142-7b89e95757b5
- Log in in Facebook, and authorize Tinder (click OK)
- Look up the auth_token in the URL in the address bar and fill it in the secrets file

A Facebook auth_token typically expires in 1 hour.

## School selection

PATinderBot will automatically create a file called schools.json, which is not in the Git 
repository, since this information is personal. All schools that are not defined in this file,
are added automatically. Each school gets a status:

- 0: NOPE 
- 1: LIKE (if a user has any school in this category, the user is liked)
- 2: NO ACTION (recently added, not reviewed yet)

In order to take action on the added schools, you have to manually assign them a 0 or 1.
The name of the school in schools.json is only shown as information to the user, to judge
whether a school shall be assigend a 0 or a 1, but is not used by the program.

## Photo collages

PATinderBot will automatically create photo collages with relevant information of the user in 
the folder img, which is not in the Git repository. It will be created automatically. It will 
also append all user information in text format to a file in the image directory.
