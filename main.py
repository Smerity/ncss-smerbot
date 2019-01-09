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
  print(flask.request.form)
  # For https://api.slack.com/slash-commands "Sending an immediate response"
  # You can reply with plain text
  return '... butzah!'
  # or with a JSON response
  attachments = [{'text': 'Zah butzah is a game from when NCSS ran on Z80 CPUs'}]
  return flask.jsonify({'text': '... butzah!', 'attachments': attachments})

if __name__ == '__main__':
  app.run()
