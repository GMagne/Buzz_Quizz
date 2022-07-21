class BuzzWriter():
	
	def __init__(self, buzzInput):
		self.io = buzzInput.io

	def change_light_player(self, player):
		lights = self.io.get_lights().copy()
		if type(player) == list:
			for p in player:
				lights[p] = 0x00 if lights[p] == 0xFF else 0xFF
		else:
			lights[player] = 0x00 if lights[player] == 0xFF else 0xFF
		
		if lights != self.io.get_lights():
			self.io.set_lights(lights)
			self.io.write_lights()

	def off_light_player(self, player):
		lights = self.io.get_lights().copy()
		if type(player) == list:
			for p in player:
				lights[p] = 0x00 
		else:
			lights[player] = 0x00 
		
		if lights != self.io.get_lights():
			self.io.set_lights(lights)
			self.io.write_lights()

	def on_light_player(self, player):
		lights = self.io.get_lights().copy()
		if type(player) == list:
			for p in player:
				lights[p] = 0xFF
		else:
			lights[player] = 0xFF 
		
		if lights != self.io.get_lights():
			self.io.set_lights(lights)
			self.io.write_lights()

