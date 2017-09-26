'''
This is an example of the server-side logic to handle slash commands in
Python with Flask.
Detailed documentation of Slack slash commands:
https://api.slack.com/slash-commands
Slash commands style guide:
https://medium.com/slack-developer-blog/slash-commands-style-guide-4e91272aa43a#.6zmti394c

'''

# import your app object
from flask import request, jsonify, abort
from flask import Flask
import json
import subprocess
application = Flask(__name__)

# The parameters included in a slash command request (with example values):
#   token=gIkuvaNzQIHg97ATvDxqgjtO
#   team_id=T0001
#   team_domain=example
#   channel_id=C2147483705
#   channel_name=test
#   user_id=U2147483697
#   user_name=Steve
#   command=/weather
#   text=94070
#   response_url=https://hooks.slack.com/commands/1234/5678

@application.route('/slash-command-url', methods=['POST'])
def slash_command():
    """Parse the command parameters, validate them, and respond.
    Note: This URL must support HTTPS and serve a valid SSL certificate.
    """
    token = request.form.get('token', None)
    text = request.form.get('text', None)
    user_id = request.form.get('user_id', None)
    with open('secure.json') as secure:
        slack_token = json.load(secure)['slack-authorization-token']
    if token != slack_token:
        return 'This request could not be validated'
    if 'author' in text or 'Author' in text: # This is the context this example is interested in
        email, user_name = get_user(user_id)
        authorize(email, user_name)
    return 'User {0} {1} has been updated to Author'.format(user_name, email)



def get_user(user_id):

    with open('slack_user_list.json') as infile:
        users = json.load(infile)
    for u in users:
        if u['id'] == user_id:
            return u['email'], u['user_name']

def authorize(email, user_name):

    command = 'wp user create {0} {1} --porcelain --allow-root --path=/var/www/html/'.format(user_name, email)
    subprocess.call(command, shell=True)
    
    command = 'wp user set-role {0} author --allow-root --path=/var/www/html/'.format(email)
    subprocess.call(command, shell=True)

