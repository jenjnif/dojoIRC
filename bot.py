import pyjokes
import datetime

class Bot:
	def public(self, channel, sender, msg):
		if msg.lower() == 'hi':
			return f'hello {sender}'
		if "joke" in msg.lower():
			return pyjokes.get_joke()
		if "date" in msg.lower() or "day" in msg.lower():
			d = datetime.datetime.now()
			weekday = d.strftime('%A')
			return week_days[weekday]

	def private(self, sender, msg):
		response = self.public('', sender, msg)
		if not response:
			return "I'm hungry"
		else:
			return f'just between me and you {response}'

week_days = {'Monday': "Have a marvelous Monday", 'Tuesday': "Have a terrific Tuesday",
'Wednesday': 'Have a wonderful Wednesday', 'Thursday': 'Have a Thabulous Thursday', 
'Friday': 'Have a fantastic Friday', 'Saturday': 'Have a super Saturday',
'Sunday': 'Have a sleepy Sunday'}

def main():
	bot = Bot()
	msg = bot.public('ldnpydojo', 'Gautier', 'Hi')
	if msg:
		print(msg)
	msg = bot.public('ldnpydojo', 'Gautier', 'tell me a joke')
	if msg:
		print(msg)
	msg = bot.public('ldnpydojo', 'Gautier', 'what day is it?')
	if msg:
		print(msg)


if __name__ == '__main__':
	main()
