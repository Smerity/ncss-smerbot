import random
import re

TUTORS = ['Tim', 'Nicky', 'Kenni', 'Ben', 'Smerity']

# Returns are STATE, OUTPUT

# The NO QUERY state
def no_query_on_enter_state(data):
	print('I am Lockout helper bot. How can I help you?')

def no_query_on_input(text, data):
	match = re.match('I am locked out( in (?P<location>.*))?', text)
	if match:
		location = match.group('location')
		if location:
			return 'LOCKED OUT LOCATION', location
		else:
			return 'LOCKED OUT', None
	else:
		return 'END', None

# The LOCKED OUT state
def locked_out_on_enter_state(data):
	print('Where are you locked out?')

def locked_out_on_input(text, data):
	return 'LOCKED OUT LOCATION', text

# The LOCKED OUT LOCATION state
def locked_out_location_on_enter_state(data):
	location = data
	tutor = random.choice(TUTORS)
	print(f'{tutor} will be at {location} right away!')

def locked_out_location_on_input(text, data):
	return 'END', None

# What to do when we enter a state
def on_enter_state(state, data):
	if state == 'NO QUERY':
		return no_query_on_enter_state(data)
	elif state == 'LOCKED OUT':
		return locked_out_on_enter_state(data)
	elif state == 'LOCKED OUT LOCATION':
		return locked_out_location_on_enter_state(data)

# What to do when we receive input while in a state
def on_input(state, text, data):
	if state == 'NO QUERY':
		return no_query_on_input(text, data)
	elif state == 'LOCKED OUT':
		return locked_out_on_input(text, data)
	elif state == 'LOCKED OUT LOCATION':
		return locked_out_location_on_input(text, data)

# Set the initial state and data
state = 'NO QUERY'
data = None

# Until we reach the end state...
while state != 'END':
	# Do the action for the current state
	on_enter_state(state, data)

	# Then get input and transition to the next state
	text = input('> ')
	state, data = on_input(state, text, data)
