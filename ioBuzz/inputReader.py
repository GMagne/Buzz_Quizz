from ioBuzz.ioBuzz import Buzz
from ioBuzz.buzzEvents import Pressed, Released, keys

class BuzzReader():

	def __init__(self):
		self.last_buttons = [{'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}]
		self.io = Buzz()

	def read_io(self):
		buttons = self.io.get_buttons()
		ret = []
		for player, controller in enumerate(buttons):
			for key in controller:
				status = buttons[player][key]
				
				if status != self.last_buttons[player][key]:
					self.last_buttons[player][key] = status
					ret.append( self.event(player, key, status))
		return ret

	def event(self,player,key, status):
		if (status):
			return Pressed(player*5 + keys[key])
		else:
			return Released(player*5 + keys[key])


	def read_pressed(self, pressed):
		q = self.read_io()
		ret = []
		if pressed == 1 :
			for event in q:
				if isinstance(event, Pressed):
					ret.append(event)

		elif pressed == 0:
			for event in q:
				if isinstance(event, Released):
					ret.append(event)
		return ret


	def read_player(self, player):
		q = self.read_io()
		ret = []
		for event in q:
			if event.value//5 == player:
				ret.append(event)
		return ret

	def __del__(self):
		del self.io


if __name__ == '__main__':
	buzzConnected = False
	buzzInput = None
	while True :
		if buzzInput == None and buzz_connected():
			buzzInput = buzzReader()
			buzzConnected = True			
			print('connected')
		else:
			del buzzInput
			buzzConnected = False
			print('disconnected')
			time.sleep(1)

		while(buzzConnected):
			events = buzzInput.read_pressed(1)
			if len(events):
				for event in events:
					print(event,end='	')
				print()
