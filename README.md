# GmailAPI
Python Wrapper for Gmail API

## Instalation
* Once cloned, install all the packages specified in the requirements.txt
* Get credentials from google for Gmail API and store it as `credentials.json` in the working dirrectory
* Install MySQL drivers(mysql-dev(el) for linux based system)
* run `python3 store_data.py` to provide access and store emails in database
* run `python3 update_mail.py` to take actions based on rules listed in `rule.json`
* Read `Filter_instructions.md` and change `rule.json accordingly`
