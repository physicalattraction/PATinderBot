# PATinderBot
Automatically like or nope users and create photo collages of Tinder recommendations

## Credits

The general idea of this Tinderbot is shared by Github user rtt here:
https://gist.github.com/rtt/5a2e0cfa638c938cca59

## General use

- Install the requirements by typing from the project dir: `pip install -r requirements/local.txt`
- Create a secrets file (see below)
- Run module `tinder_bot`
- Adjust `schools.json` after each run (see below)
- Enjoy photo collages in folder `img` 

## Secrets file

TODO: Describe how to get an access token

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
