import re

import flask
app = flask.Flask(__name__)

state = []

@app.route('/')
def hello_world():
  return 'Hello World v0.1'

@app.route('/slack/slash/zah', methods=['POST'])
def slash_zah():
  # If you print something out it'll appear in
  # https://dashboard.heroku.com/apps/smerbot/logs
  print(flask.request.values)
  # Prints out:
  # CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('token', 'FwydmeYg2VrS4vToSryWBkEK'), ('team_id', 'TEKDUUF5G'), ('team_domain', 'ncss-2019-tutors'), ('channel_id', 'CFAULCTD4'), ('channel_name', 'smerbot'), ('user_id', 'UF4GJ5Y9K'), ('user_name', 'smerity'), ('command', '/zah'), ('text', 'FOR FREEDOM &lt;3'), ('response_url', 'https://hooks.slack.com/commands/TEKDUUF5G/519641740450/KbKW7axMjgzD2UKDqtAmY8bn'), ('trigger_id', '521043154998.495470967186.4555af6499a8c3638393811d5d2e6478')])])
  ###
  # For https://api.slack.com/slash-commands "Sending an immediate response"
  # You can reply with plain text
  #return '... butzah!'
  # and will replace the /slash command with '...butzah!'
  # (i.e. the user's request won't appear, only the bot response)
  ###
  # or with a JSON response
  resp = {'text': '... butzah!'}
  # If you want to see the command as well as the reply, set the response type
  resp['response_type'] = 'in_channel'
  # You can also add attachments
  attachments = [{'text': 'Context: Zah butzah is a game from when NCSS ran on Z80 CPUs'}]
  # We can also add multiple attachments
  if 'text' in flask.request.values and flask.request.values['text']:
    user_command = flask.request.values['text']
    msg = {'text': f'... and you said "{user_command}"'}
    attachments.append(msg)
  resp['attachments'] = attachments
  print(resp)
  # flask.jsonify handles converting the payload and setting the content type
  return flask.jsonify(resp)

@app.route('/slack/slash/smerlock', methods=['POST'])
def slash_smerlock():
  location = None
  attachments = []
  # Let's see if the user has noted their location
  if 'text' in flask.request.values:
    user_message = flask.request.values['text']
    match = re.match('I am locked out( at (?P<location>.*))?', user_message)
    if match and match.group('location'):
        location = match.group('location')
  #
  resp = {}
  resp['response_type'] = 'in_channel'
  if location:
    resp = {'text': "You're locked out in {location}. Finding someone to help you now!"}
  if not location:
    resp = {'text': 'Where are you locked out?'}
    location_buttons = {
      'callback_id': 'lockout_location',
      'text': 'Choose a location',
      'fallback': "If you can't select a location the helper will message you",
      "actions": [
        {'name': 'location', 'text': 'Main Building', 'type': 'button', 'value': 'main'},
        {'name': 'location', 'text': 'ABS', 'type': 'button', 'value': 'abs'},
        {'name': 'location', 'text': "Women's College", 'type': 'button', 'value': 'womens'},
        {'name': 'location', 'text': 'SIT', 'type': 'button', 'value': 'sit'},
      ]
    }
    attachments.append(location_buttons)
  resp['attachments'] = attachments
  return flask.jsonify(resp)

if __name__ == '__main__':
  app.run()
