from flask import Flask
app = Flask(__name__)

state = []

@app.route('/')
def hello_world():
  return 'Hello World v0.1'

@app.route('/slack/slash/zah', methods=['POST'])
def slash_zah():
  print(request.form)

if __name__ == '__main__':
  app.run()
