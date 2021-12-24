import json

with open('credentials.json', encoding='utf-8') as f:
	config= json.load(f)


MAILGUN_DOMAIN= config['MAILGUN_DOMAIN']
MAILGUN_API_KEY=config['MAILGUN_API_KEY']
FROM_EMAIL=config['FROM_EMAIL']
USER=config['USER']
PASSWORD=config['PASSWORD']
HOST=config['HOST']
PORT=config['PORT']
DATABASE=config['DATABASE']
JWT_SECRET_KEY=config['JWT_SECRET_KEY']
