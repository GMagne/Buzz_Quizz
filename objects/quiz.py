import pygame
import json
from objects.slide import Slide

class Quiz():

	def __init__(self, path, screen_size):
		try:
			f = open(path, encoding='utf-8')
		except:
			raise NameError('No data.json found')

		data = json.load(f)
		f.close()

		self.n = data['nombre_de_jugadors']
		self.score_player = [ 0 for _ in range(self.n)]
		self.current_slide = 0 
		self.create_slides(data['diapositives'], self.n, screen_size)
		self.number_slides = len(self.slides)
		self.ended = False
		self.buzzOutput = None

	def get_writer(self, buzzOutput):
		self.buzzOutput = buzzOutput

	def create_slides(self, data, n, screen_size):
		self.slides = []
		if len(data)>0:
			for i, slide_data in enumerate(data):
				self.slides.append(Slide(slide_data, n, screen_size, i))


	def change_score(self, player, points):
		if player<self.n :
			self.score_player[player]+= points
			return True
		else:
			return False


	def check_events(self, queue):
		ret = 1
		retT = 1
		#keyboard and mouse
		for event in queue:
			if event.type == pygame.KEYDOWN:
				cs = self.get_current_slide()
				if event.key == pygame.K_1:
					self.change_score(0,1)
					retT = False
				elif event.key == pygame.K_2:
					self.change_score(1,1)
					retT = False
				elif event.key == pygame.K_3:
					self.change_score(2,1)
					retT = False
				elif event.key == pygame.K_4:
					self.change_score(3,1)
					retT = False
				if event.key == pygame.K_q:
					self.change_score(0,-1)
					retT = False
				elif event.key == pygame.K_w:
					self.change_score(1,-1)
					retT = False
				elif event.key == pygame.K_e:
					self.change_score(2,-1)
					retT = False
				elif event.key == pygame.K_r:
					self.change_score(3,-1)
					retT = False
				elif event.key == pygame.K_p and pygame.mixer.get_busy():
					pygame.mixer.pause()
				elif event.key == pygame.K_o and pygame.mixer.get_busy():
					pygame.mixer.unpause()
					retT = False
				elif event.key == pygame.K_0 and cs.music[0] != None:
					pygame.mixer.stop()
					cs.music[0].play(-1)
					retT = False
				elif event.key == pygame.K_UP and cs.music[0] != None:
					cs.music[0].set_volume(cs.music[0].get_volume()+0.1)
				elif event.key == pygame.K_DOWN and cs.music[0] != None:
					cs.music[0].set_volume(cs.music[0].get_volume()-0.1)
				elif event.key == pygame.K_RIGHT:
					self.next_slide()
					retT = False
				elif event.key == pygame.K_LEFT:
					self.previous_slide()
					retT = False
				elif event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
				else:
					retT = self.get_current_slide().action(event, self.score_player, self.buzzOutput)

			elif event.type == pygame.QUIT:
				pygame.quit()
				exit()
			
			if retT:
				pass
			else:
				ret = retT

		return ret


	def check_buzz_events(self, buzzevents):
		for buzzevent in buzzevents:
			self.get_current_slide().buzz_action(buzzevent, self.buzzOutput)


	def get_score(self):
		return self.score_player


	def get_current_slide(self):
		if len(self.slides)>0 :
			return self.slides[self.current_slide]
		else:
			return Slide(data_empty_slide)


	def next_slide(self):
		# change to the next slide. Return True if there is a next slide, else return False.
		if (self.current_slide + 1 < self.number_slides):
			self.buzzOutput.off_light_player([i for i, _ in enumerate(self.score_player)])
			cs = self.get_current_slide()
			if cs.timer != None: 
				cs.timer.set_running(0)
			if cs.music[0] != None:
				pygame.mixer.stop()
				cs.music[1] = False


			self.current_slide += 1
			
			cs = self.get_current_slide()
			if cs.timer != None and cs.tipus != 9: 
				cs.timer.set_running(1)
			if cs.music[0] != None:
				cs.music[0].play(-1)

			return True
		else:
			return False


	def previous_slide(self):
		# change to the next slide. Return True if there is a next slide, else return False.
		if (self.current_slide - 1 >= 0):
			self.buzzOutput.off_light_player([i for i, _ in enumerate(self.score_player)])
			cs = self.get_current_slide()
			if cs.timer != None: 
				cs.timer.set_running(0)
			if cs.music[0] != None:
				pygame.mixer.stop()

			self.current_slide -= 1
			
			cs = self.get_current_slide()
			if cs.timer != None and cs.tipus != 9: 
				cs.timer.set_running(1)
			if cs.music[0] != None:
				cs.music[0].play(-1)

			return True
		else:
			return False


	def get_ended(self):
		return self.ended


if __name__ == '__main__':
	Quiz()