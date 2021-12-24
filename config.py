import json

with open('credetials.json') as f:
	config= json.load(f)


MAILGUN_DOMAIN= config['MAILGUN_DOMAIN']
MAILGUN_API_KEY=config['MAILGUN_API_KEY']
FROM_EMAIL=config['FROM_EMAIL']
USER=config['USER']
PASSWORD=config['PASSWORD']
HOST=config['HOST']
DATABASE=config['DATABASE']
JWT_DATABASE_SECRET=config['JWT_DATABASE_SECRET']

