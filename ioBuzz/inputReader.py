from ioBuzz.buzzIO import buzz, buzz_connected
from enum import Enum

keys = {'R':0, 'Y':1, 'G':2, 'O':3, 'B':4}

class Event(Enum):
	def __str__(self):
		return self.name

class Pressed(Event):
	P1_red_pressed    = 0
	P1_yellow_pressed = 1
	P1_green_pressed  = 2
	P1_orange_pressed = 3
	P1_blue_pressed   = 4

	P2_red_pressed    = 5
	P2_yellow_pressed = 6
	P2_green_pressed  = 7
	P2_orange_pressed = 8
	P2_blue_pressed   = 9

	P3_red_pressed    = 10
	P3_yellow_pressed = 11
	P3_green_pressed  = 12
	P3_orange_pressed = 13
	P3_blue_pressed   = 14
	
	P4_red_pressed    = 15
	P4_yellow_pressed = 16
	P4_green_pressed  = 17
	P4_orange_pressed = 18
	P4_blue_pressed   = 19

class Released(Event):
	P1_red_released    = 0
	P1_yellow_released = 1
	P1_green_released  = 2
	P1_orange_released = 3
	P1_blue_released   = 4

	P2_red_released    = 5
	P2_yellow_released = 6
	P2_green_released  = 7
	P2_orange_released = 8
	P2_blue_released   = 9

	P3_red_released    = 10
	P3_yellow_released = 11
	P3_green_released  = 12
	P3_orange_released = 13
	P3_blue_released   = 14
	
	P4_red_released    = 15
	P4_yellow_released = 16
	P4_green_released  = 17
	P4_orange_released = 18
	P4_blue_released   = 19

def reader_connected():
	return buzz_connected()

class buzzReader():
	def __init__(self):
		self.last_buttons = [{'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}, {'R':0, 'Y':0, 'G':0, 'O':0, 'B':0}]
		self.io = buzz()

	def read_io(self):
		buttons = self.io.getbuttons()
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

	def wait(self, event):
		pass

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
			if event.value//5 == player-1:
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

		
	