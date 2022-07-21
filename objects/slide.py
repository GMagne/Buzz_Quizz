import pygame
from objects.components import Draw, Text, Button, Icon, IconBar, ScoreBar, OptionsBar, Timer
from imageManager import imageDict
from musicManager import musicDict
from objects.constants import colorDict, valueDict, SLIDE_TYPE_LIST, DFLT_FEEDBACK_COLOR, RED, YELLOW,\
GREEN, ORANGE, BLUE, DFLT_FONT, INDEX_FONT_SIZE, INDEX_MRGN_Y, INDEX_MRGN_X, TIMER_RLTV_POS
from ioBuzz.buzzEvents import Pressed, Released

class Slide():

	def __init__(self, data, n, screen_size, index):
		self.tipus = data['tipus']
		self.index = Text(str(index+1), INDEX_FONT_SIZE)
		self.background = Draw(imageDict[data['imatge_de_fons']], screen_size)

		if 'temporitzador' in data.keys() and data['temporitzador']>0:
			self.timer = Timer(data['temporitzador'])
			
		else:
			self.timer = None
		
		if 'musica' in data.keys() and data['musica'] in musicDict.keys():
			self.music = [musicDict[data['musica']], False]
		else:
			self.music = [None, None]

		bg_size = self.background.get_surface_size()
		size = screen_size if bg_size == (0,0) else bg_size

		if self.tipus in SLIDE_TYPE_LIST:
			Slide.init_func[self.tipus](self, data, n, size)
		else:
			Slide.init_func[0](self, data, n, size)
#####################################################################################

	def show(self, screen, quiz):

		bg_surface = self.background.get_surface().copy()

		if bg_surface == None :
			bg_surface = screen
			x, y = screen.get_size()
		else:
			x, y = self.background.get_surface_size()


		a, b = self.index.get_surface_size()
		self.index.show(bg_surface, (x -a -INDEX_MRGN_X, y -b -INDEX_MRGN_Y ))

		if self.timer != None:
			self.timer.show(bg_surface, (int(x*TIMER_RLTV_POS[0]), int(y*TIMER_RLTV_POS[1])) )
			t =self.timer.get_time()
			if t<1.5 and self.music[0]!=None and not self.music[1] :
				pygame.mixer.fadeout(1300)
				self.music[1] = True
			if t==0 and self.music[0]!=None and self.music[1]:
				self.music[1] = False

		if self.tipus == 0:
			pass

		elif self.tipus == 1:
			imatgeSurface = pygame.Surface((x,y), pygame.SRCALPHA)
			self.draw.show(imatgeSurface)
			bg_surface.blit(imatgeSurface, (0,0))

		elif self.tipus == 2:
			self.title.show(bg_surface, (None, int(y/7)))
			self.iconBar.show(bg_surface, (0, int(y*19/30)) )

		elif self.tipus == 3:
			imatgeSurface = pygame.Surface((x,int(y*0.65)), pygame.SRCALPHA)
			self.draw.show(imatgeSurface)
			bg_surface.blit(imatgeSurface, (0,int(y/40)))
			self.iconBar.show(bg_surface, (0, int(y*0.72)) )

		elif self.tipus == 4:
			self.title.show(bg_surface, (None, int(y/20)))
			self.optionsBar.show(bg_surface, (0, int(y*0.5)) )
			self.iconBar.show(bg_surface, (0,int(y*0.84)))

		elif self.tipus == 5:
			imatgeSurface = pygame.Surface((x,int(y*0.48)), pygame.SRCALPHA)
			self.draw.show(imatgeSurface)
			bg_surface.blit(imatgeSurface, (0,int(y/40)))
			self.optionsBar.show(bg_surface, (0, int(y*0.5)) )
			self.iconBar.show(bg_surface, (0,int(y*0.84)))

		elif self.tipus == 6:
			self.title.show(bg_surface, (None, int(y/7)))
			self.iconBar.show(bg_surface, (0, int(y*19/30)) )

		elif self.tipus == 7:
			imatgeSurface = pygame.Surface((x,int(y*0.65)), pygame.SRCALPHA)
			self.draw.show(imatgeSurface)
			bg_surface.blit(imatgeSurface, (0,int(y/40)))
			self.iconBar.show(bg_surface, (0, int(y*0.72)) )

		elif self.tipus == 8:
			self.iconBar.show(bg_surface, (0,int(y/4)))
			if self.scoreBar.get_score() != quiz.score_player:
				self.scoreBar.change_score( quiz.score_player)
			self.scoreBar.show(bg_surface, (0,int(y*0.57)))

		elif self.tipus == 9:
			imatgeSurface = pygame.Surface((x,int(y*0.65)), pygame.SRCALPHA)
			self.draw.show(imatgeSurface)
			bg_surface.blit(imatgeSurface, (0,int(y/40)))
			self.iconBar.show(bg_surface, (0, int(y*0.72)) )

		a, b = screen.get_size()
		screen.blit( bg_surface, (int( (a-x)/2 ),int(  (b-y)/2 )) )

#####################################################################################
	
	def action(self, event, score, buzzOutput):			
		if (self.tipus == 4 or self.tipus == 5) and (event.key == pygame.K_RETURN):
			buzzOutput.off_light_player([0,1,2,3])
			pygame.mixer.fadeout(1000)
			if self.timer != None and self.timer.running:
				self.timer.change_running()
			self.solved = True
			sols = self.optionsBar.get_correct()
			for k in self.choice.keys():
				choice = self.choice[k]
				if choice == None:
					self.iconBar.set_feedback( k , False, color = DFLT_FEEDBACK_COLOR)
				else:
					self.iconBar.set_feedback( k , False, color = choice[1])
					self.iconBar.set_feedback( k , True, color = choice[1])
					if choice[0] in sols:
						score[k] +=1
						buzzOutput.on_light_player(k)

		elif (self.tipus == 6 or self.tipus == 7) and event.key == pygame.K_BACKSPACE and self.first:
			buzzOutput.off_light_player([0,1,2,3])
			for k in range(len(self.iconBar.icon_player)):
				self.iconBar.set_feedback( k, False, color = DFLT_FEEDBACK_COLOR)
			self.first = False
			pygame.mixer.unpause()

		elif event.key == pygame.K_BACKSPACE and self.tipus == 9 and self.player_on != None:
			buzzOutput.off_light_player(self.player_on)
			self.iconBar.set_feedback( self.player_on, False, color = DFLT_FEEDBACK_COLOR)
			self.player_on = (self.player_on+1)%len(score)
			buzzOutput.on_light_player(self.player_on )
			self.iconBar.set_feedback( self.player_on, True, color = RED)


		elif event.key == pygame.K_RETURN and self.tipus == 9:
			if self.timer != None: 
				self.timer.set_running(1)
			if self.player_on == None:
				print(True)
				self.player_on = 0
			else:
				self.iconBar.set_feedback( self.player_on, False, color = DFLT_FEEDBACK_COLOR)
				buzzOutput.off_light_player(self.player_on)
				score[self.player_on] +=1
				self.player_on = (self.player_on+1)%len(score)
				
			buzzOutput.on_light_player(self.player_on)
			self.iconBar.set_feedback( self.player_on, True, color = RED)


		elif self.timer != None:
			if event.key == pygame.K_t:
				self.timer.change_running()
			elif event.key == pygame.K_y:
				self.timer.restart()
		else:
			return True

		return False

			

		



	def buzz_action(self, buzzevent, buzzOutput):
		if self.tipus == 0:
			pass

		elif self.tipus == 1:
			pass

		elif self.tipus == 2 or self.tipus == 3:
			self.iconBarActionRed(buzzevent, buzzOutput)				

		elif (self.tipus == 4 or self.tipus == 5):
			if self.timer == None:
				self.iconBarActionChoose(buzzevent, buzzOutput)
			elif self.timer.get_time()>0 :
				self.iconBarActionChoose(buzzevent, buzzOutput)


		elif self.tipus == 6 or self.tipus == 7:			
			if self.iconBarAction1stRed(buzzevent, buzzOutput) and self.music[0]!=None:
				pygame.mixer.pause()

		elif self.tipus == 8:
			self.iconBarActionColor(buzzevent, buzzOutput)



	def iconBarActionChoose(self, buzzevent, buzzOutput):
		if isinstance(buzzevent, Pressed):
			b = buzzevent.value
			text_opcions = self.optionsBar.get_text()
			if b%5 != 0 and 4-b%5 < len(text_opcions) and self.choice[b//5]==None and not self.solved:
				self.choice[b//5] = (text_opcions[4-b%5], valueDict[b%5])
				self.iconBar.set_feedback( b//5 , True, color = DFLT_FEEDBACK_COLOR)
				buzzOutput.on_light_player(b//5)

				#self.iconBar.set_feedback( 0, True, color = DFLT_FEEDBACK_COLOR)


	def iconBarActionRed(self, buzzevent, buzzOutput):
		if buzzevent is Pressed.P1_red:
			self.iconBar.set_feedback( 0, True)
			buzzOutput.on_light_player(0)
		elif buzzevent is Pressed.P2_red:
			self.iconBar.set_feedback( 1, True)
			buzzOutput.on_light_player(1)
		elif buzzevent is Pressed.P3_red:
			self.iconBar.set_feedback( 2, True)
			buzzOutput.on_light_player(2)
		elif buzzevent is Pressed.P4_red:
			self.iconBar.set_feedback( 3, True)
			buzzOutput.on_light_player(3)

	def iconBarAction1stRed(self, buzzevent, buzzOutput):
		if not self.first :
			if buzzevent is Pressed.P1_red and 0 in self.players_allowed:
				self.iconBar.set_feedback( 0, True, color = RED)
				self.players_allowed.remove(0)
				buzzOutput.on_light_player(0)
				self.first = True
				return True
			elif buzzevent is Pressed.P2_red and 1 in self.players_allowed:
				self.iconBar.set_feedback( 1, True, color = RED)
				self.players_allowed.remove(1)
				buzzOutput.on_light_player(1)
				self.first = True
				return True
			elif buzzevent is Pressed.P3_red and 2 in self.players_allowed:
				self.iconBar.set_feedback( 2, True, color = RED)
				self.players_allowed.remove(2)
				buzzOutput.on_light_player(2)
				self.first = True
				return True
			elif buzzevent is Pressed.P4_red and 3 in self.players_allowed:
				self.iconBar.set_feedback( 3, True, color = RED)
				self.players_allowed.remove(3)
				buzzOutput.on_light_player(3)
				self.first = True
				return True
		return False

	def iconBarActionColor(self, buzzevent, buzzOutput):
		if isinstance(buzzevent, Pressed):
			b = buzzevent.value
			self.iconBar.set_feedback( b//5 , False)
			self.iconBar.set_feedback( b//5 , True, color = valueDict[b%5] )
			self.pressed[b//5].append(valueDict[b%5])
			if b%5==0:
				buzzOutput.on_light_player(b//5)


		elif isinstance(buzzevent, Released) :
			b = buzzevent.value
			self.pressed[b//5].remove(valueDict[b%5])
			if len(self.pressed[b//5]) ==0:
				self.iconBar.set_feedback( b//5 , False, color = DFLT_FEEDBACK_COLOR )
			else:
				self.iconBar.set_feedback( b//5 , False)
				self.iconBar.set_feedback( b//5 , True, color = self.pressed[b//5][0] )
			
			if not RED in self.pressed[b//5]:
				buzzOutput.off_light_player(b//5) 


	def iconBarAction1stColor(self, buzzevent):
		if isinstance(buzzevent, Pressed) and (not self.first):
			b = buzzevent.value
			if b%5 != 0 :
				self.first = True
				self.iconBar.set_feedback( b//5 , True, color = valueDict[b%5] )
		
#####################################################################################

	def init0(self, data, n, screen_size): # blank slide
		pass
		

	def init1(self, data, n, screen_size): # 1 imatge central, foto slide
		x, y = screen_size
		image = imageDict[data['imatge_1']] if data['imatge_1'] in imageDict.keys() else imageDict['blank']
		self.draw = Draw(image, (int(x*0.9),int(y*0.9)) )


	def init2(self, data, n, screen_size): # Títol + iconBar, title connect
		color_str = data['pregunta_o_titol']['color']
		color = colorDict[color_str] if color_str in colorDict.keys() else None
		self.title = Text(data['pregunta_o_titol']['text'], data['pregunta_o_titol']['tamany_lletra'], color = color )
		
		x, y = screen_size
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y/3)) )


	def init3(self, data, n, screen_size): # Imatge + iconBar, title-foto connect
		x, y = screen_size
		image = imageDict[data['imatge_1']] if data['imatge_1'] in imageDict.keys() else imageDict['blank']	
		self.draw = Draw(image, (x,int(y*0.65)))
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y*0.25)) )


	def init4(self, data, n, screen_size): # 4-opcions choose
		color_str = data['pregunta_o_titol']['color']
		color = colorDict[color_str] if color_str in colorDict.keys() else None
		self.title = Text(data['pregunta_o_titol']['text'], data['pregunta_o_titol']['tamany_lletra'], color = color )

		x, y = screen_size
		self.optionsBar = OptionsBar( data["opcions"], (x,int(y*0.35)))
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y/8)) )
		self.solved = False
		self.choice = {}
		for k in range(n):
			self.choice[k] = None


	def init5(self, data, n, screen_size): #4opcions-foto choose
		x, y = screen_size
		image = imageDict[data['imatge_1']] if data['imatge_1'] in imageDict.keys() else imageDict['blank']	
		self.optionsBar = OptionsBar( data["opcions"], (x,int(y*0.35)))
		self.draw = Draw(image, (x,int(y*0.48)))
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y/8)) )
		self.solved = False
		self.choice = {}
		for k in range(n):
			self.choice[k] = None


	def init6(self, data, n, screen_size): # Títol + iconBar, title first
		self.first = False
		self.players_allowed = [i for i in range(n)]
		color_str = data['pregunta_o_titol']['color']
		color = colorDict[color_str] if color_str in colorDict.keys() else None
		self.title = Text(data['pregunta_o_titol']['text'], data['pregunta_o_titol']['tamany_lletra'], color = color )
		
		x, y = screen_size
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y/3)) )



	def init7(self, data, n, screen_size): # Imatge + iconBar, title-foto first
		x, y = screen_size
		self.first = False
		self.players_allowed = [i for i in range(n)]
		image = imageDict[data['imatge_1']] if data['imatge_1'] in imageDict.keys() else imageDict['blank']	
		self.draw = Draw(image, (x,int(y*0.65)))
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y*0.25)) )



	def init8(self, data, n, screen_size): #Score slide
		x, y = screen_size
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y*2/7)) )
		self.scoreBar = ScoreBar( n, (x, int(y/4)) )
		self.pressed = {0: [], 1: [], 2: [], 3:[]}


	def init9(self, data, n, screen_size): # Imatge + iconBar, title-foto connect
		x, y = screen_size
		image = imageDict[data['imatge_1']] if data['imatge_1'] in imageDict.keys() else imageDict['blank']	
		self.draw = Draw(image, (x,int(y*0.65)))
		self.iconBar = IconBar(data['logo_jugador'], n, (x, int(y*0.25)) )
		self.player_on = None



	init_func = {
		0: init0,
		1: init1,
		2: init2,
		3: init3,
		4: init4,
		5: init5,
		6: init6,
		7: init7,
		8: init8,
		9: init9
	}

