import flask
app = flask.Flask(__name__)

state = []

@app.route('/')
def hello_world():
  return 'Hello World v0.1'

@app.route('/slack/slash/zah', methods=['POST'])
def slash_zah():
  print(flask.request.form)
  # https://api.slack.com/slash-commands
  # -> Sending an immediate response
  # You can reply with plain text
  return '... butzah!'
  # or with a JSON response

if __name__ == '__main__':
  app.run()
