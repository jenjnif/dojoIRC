import pyjokes

class Bot:
	def public(self, channel, sender, msg):
		if msg.lower() == 'hi':
			return f'hello {sender}'
		if "joke" in msg.lower():
			return pyjokes.get_joke()


	def private(self, sender, msg):
		pass



bot = Bot()
msg = bot.public('ldnpydojo', 'Gautier', 'Hi')
if msg:
	print(msg)
msg = bot.public('ldnpydojo', 'Gautier', 'tell me a joke')
if msg:
	print(msg)
