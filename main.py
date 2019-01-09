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
  # For https://api.slack.com/slash-commands "Sending an immediate response"
  # You can reply with plain text
  #return '... butzah!'
  # or with a JSON response
  resp = {'text': '... butzah!'}
  # If you want to see the command as well as the reply, set the response type
  resp['response_type'] = 'in_channel'
  # You can also add attachments
  attachments = [{'text': 'Zah butzah is a game from when NCSS ran on Z80 CPUs'}]
  if 'text' in flask.request.values:
    attachments.append(f"... and you said {flask.request.values['text']}")
  resp['attachments'] = attachments
  print(resp)
  return flask.jsonify(resp)

if __name__ == '__main__':
  app.run()
