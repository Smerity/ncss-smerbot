# NCSS SmerBot example

Features:
- Environment variable pulled in from `os.environ`
- Going to the URL `/poke` sends a simple message to a channel using `send_message`
- Going to the URL `/flightexample` sends a message with attachments using `send_message`
- Typing in Slack `/zah` will reply with "... butzah!" and optionally replies with your text
- Typing in Slack `/smerlock` will parse the message for a location and if not found will respond by adding buttons [Main, Langley, Williams, Reid]
- When a button is clicked the `lockout_location` is intercepted at `/slack/action-endpoint`, a message is sent saying a student is locked out at location, and we tell the student a tutor is coming

What's not handled:
- Security to ensure it's Slack sending the message
