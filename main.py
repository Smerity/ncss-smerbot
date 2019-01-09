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
    resp['text'] = f"So you're locked out at {location}? We're finding someone to help you now!"
  if not location:
    resp['text'] = 'Where are you locked out?'
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

@app.route('/slack/action-endpoint', methods=['POST'])
def action_endpoint():
  print('Action received:', flask.request.values)
  # Prints (if responding to the smerlock):
  # ImmutableMultiDict([('payload', '{"type":"interactive_message","actions":[{"name":"location","type":"button","value":"womens"}],"callback_id":"lockout_location","team":{"id":"TEKDUUF5G","domain":"ncss-2019-tutors"},"channel":{"id":"CFAULCTD4","name":"smerbot"},"user":{"id":"UF4GJ5Y9K","name":"smerity"},"action_ts":"1547031403.733548","message_ts":"1547031400.000200","attachment_id":"1","token":"FwydmeYg2VrS4vToSryWBkEK","is_app_unfurl":false,"original_message":{"type":"message","subtype":"bot_message","text":"Where are you locked out?","ts":"1547031400.000200","bot_id":"BF90RSZ17","attachments":[{"callback_id":"lockout_location","fallback":"If you can\'t select a location the helper will message you","text":"Choose a location","id":1,"actions":[{"id":"1","name":"location","text":"Main Building","type":"button","value":"main","style":""},{"id":"2","name":"location","text":"ABS","type":"button","value":"abs","style":""},{"id":"3","name":"location","text":"Women\'s College","type":"button","value":"womens","style":""},{"id":"4","name":"location","text":"SIT","type":"button","value":"sit","style":""}]}]},"response_url":"https:\\/\\/hooks.slack.com\\/actions\\/TEKDUUF5G\\/519975990261\\/QguWZ3Z2g7wM3mBe3Tbf6SPT","trigger_id":"519774931746.495470967186.c587a5aa20bd8fd19c692cce34ca20c3"}')])])
  # Less horrific version of this response is at https://api.slack.com/interactive-messages > Checking the action type
  ###
  # Your response must be a 200
  # Responding immediately with JSON will replace the current message
  # You can create a new message by setting replace_original to false
  ###
  # We'll assume there's only a single action
  # Honestly I don't know if there is anything where it replies with multiple
  # If it does I don't know how you respond with JSON
  payload = flask.request.values['payload']
  callback = payload['callback_id']
  if callback == 'lockout_location':
    actions = {}
    for action in payload.get('actions', []):
      name = action['name']
      value = action['value']
      actions[name] = value
    return f"Sending tutor to {actions['location']}"
  return ""

if __name__ == '__main__':
  app.run()
