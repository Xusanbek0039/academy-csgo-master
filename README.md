# CSGO:Panel
<p align="center">
<img src="https://forthebadge.com/images/badges/made-with-python.svg">
<img src="https://forthebadge.com/images/badges/open-source.svg">
</p>

## About this project
This is a Django powered website functioning as a webpanel for CSGO with support for stats query, Direct premium subscription using Khalti payment gateway, querying of gameservers
and some basic forms.

## Requirements
These are the basic requiremnts you will need. All other dependencies are in requirements.txt
- Python 3.9.2
- Django 3.2.6

## Installation
- Recommended to use a virtual environment. I personally use `virtualenv` 
- Then install required dependencies using `pip install requirements.txt`
- Create an `.env` file in root project directory. Check the `.env_saple` file for keys to add.
- Then run `python manage.py migrate`.

You will need some prior django experience if you wish to successfully customize and host this panel yourself.