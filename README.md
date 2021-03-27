# PATinderBot
Automatically like or nope users and create photo collages of Tinder recommendations

## Credits

The general idea of this Tinderbot is shared by Github user rtt here:
https://gist.github.com/rtt/5a2e0cfa638c938cca59

## General use

- Have Tinder working normally on your phone, including recommendation settings
- Install the requirements by typing from the project dir: `pip install -r requirements/local.txt`
- Create a secrets file (see below)
- Run module `tinder_bot`
- After each run, choose if you want to move the contents from `schools_review_words.json` to `schools_approve_words.json` or to `schools_reject_words.json`
- Enjoy photo collages in folder `img` 

## Authentication

The authentication should work automatically, however is broken at the moment. In `secrets.json` (not in the Git repository), there are three fields for authentication: your phone number, a refresh token and an access token. You should fill in the phone number (including the country code) as a string, as shown in the file `secrets_template.json`. The code makes an API call to request a One Time Password (OTP) which is received on your phone, and asks you for input it. However, this part is broken, the sms is never sent. Therefore, you need to take your phone, log out, log in there with phone number, obtain an OTP, and fetch a refresh token manually using this OTP.

## School selection

PATinderBot will automatically create files called `schools_approve_words`, `schools_reject_words.json` and `school_review_words.json`, which is not in the Git repository, since this information is personal. All words in schools that are not defined in any of these files, are added automatically to `school_review_words.json`. Each school gets a Vote based on the words in the name of the school. After each run, you might want to move the contents from `schools_review_words.json` to `schools_approve_words.json` or to `schools_reject_words.json`

## Photo collages

PATinderBot will automatically create photo collages with relevant information of the user in the folder img. The folder will be created automatically and is not present in the Git repository.
