import pygame
import json
from objects.components import Button, Image, Text, Icon
from ioBuzz.inputReader import Pressed, Released

data_empty_slide = {
		"tipus": 0,

		"pregunta_o_titol": {
			"text": "No troba cap diapositiva",
			"tamany_lletra": 18,
			"color": "white"
		},

		"imatge_de_fons": "",

		"imatge_1": "",

		"musica": ""

	},

############################################################################

class Quiz():

	def __init__(self,path):
		try:
			f = open(path)
		except:
			raise NameError('No data.json found')

		data = json.load(f)
		f.close()

		self.n = data['nombre_de_jugadors']
		self.score_player = [ 0 for _ in range(self.n)]
		self.current_slide = 0 
		self.create_slides(data['diapositives'])
		self.number_slides = len(self.slides)
		self.ended = False

		

	def create_slides(self, data):
		self.slides = []
		if len(data)>0:
			for slide in data:
				s = Slide(slide)
				self.slides.append(s)

	def change_score(self,player, points):
		if player<self.n :
			self.score_player[player]+= points
			return True
		else:
			return False

	def check_events(self, queue, buzzevents):
		#keyboard and mouse
		for event in queue:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					self.change_score(0,1)
				elif event.key == pygame.K_2:
					self.change_score(1,1)
				elif event.key == pygame.K_3:
					self.change_score(2,1)
				elif event.key == pygame.K_4:
					self.change_score(3,1)
				elif event.key == pygame.K_RIGHT:
					self.next_slide()
				elif event.key == pygame.K_LEFT:
					self.previous_slide()

			elif event.type == pygame.QUIT:
				pygame.quit()
				exit()

		for buzzevent in buzzevents:
			self.get_current_slide().action(buzzevent)
		


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
			self.current_slide += 1
			return True
		else:
			return False

	def previous_slide(self):
		# change to the next slide. Return True if there is a next slide, else return False.
		if (self.current_slide - 1 >= 0):
			self.current_slide -= 1
			return True
		else:
			return False

	def get_ended(self):
		return self.ended	


############################################################################

class Slide():

	def __init__(self, data):
		self.tipus = data['tipus']
		self.imatge = Image(data['imatge_1'])
		self.background = Image(data['imatge_de_fons'])
		self.title = Text(data['pregunta_o_titol']["text"], data['pregunta_o_titol']["tamany_lletra"], data['pregunta_o_titol']["color"])
		self.music = data['musica']
		self.icon_player = []
		for path in data['logo_jugador']:
			self.icon_player.append(Icon(path))


	def show(self, screen, quiz):
		x, y = screen.get_size()
		self.background.show(screen)

		if self.tipus == 0:
			self.title.show(screen, (None,int(y/4)))
			try:
				bx, by = self.background.surface.get_size()
			except:
				bx, by = screen.get_size()

			iconSurface = pygame.Surface((bx,int(by/3)), pygame.SRCALPHA)

			h = int(bx/quiz.n)
			for i in range(quiz.n):
				self.icon_player[i].show(iconSurface, h, (i*h,0) )

			screen.blit(iconSurface, (int((x-bx)/2),int(1.9*by/3)) )


		elif self.tipus == 1:
			imatgeSurface = pygame.Surface((x,int(y/2)), pygame.SRCALPHA)
			self.imatge.show(imatgeSurface)
			screen.blit(imatgeSurface, (0,int(y/40)))


	def action(self, buzzevent):
		if self.tipus == 0:
			if buzzevent is Pressed.P1_red_pressed:
				self.icon_player[0].connect()
			elif buzzevent is Pressed.P2_red_pressed:
				self.icon_player[1].connect()
			elif buzzevent is Pressed.P3_red_pressed:
				self.icon_player[2].connect()
			elif buzzevent is Pressed.P4_red_pressed:
				self.icon_player[3].connect()



############################################################################




if __name__ == '__main__':
	q = Quiz()
