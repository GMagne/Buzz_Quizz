import pygame
from ioBuzz.ioBuzz import Buzz
from ioBuzz.inputReader import BuzzReader
from ioBuzz.outputWriter import BuzzWriter
from ioBuzz.buzzEvents import Pressed, Released
from objects.components import Button
from objects.quiz import Quiz
from objects.slide import Slide
from objects.constants import BLACK, WHITE, NAVY, DATA_PTH, BACKGROUND_COLOR


gameOn = True
buzzInput = None
buzzOutput = None
quiz = None
clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()

pauseButton = Button(
    " Buzz desconectat ",
    50,
    color = WHITE,
    bg = NAVY,
    border_color = BLACK
	)

nojsonButton = Button(
    " NO data.json ",
    50,
    color = WHITE,
    bg = NAVY,
    border_color = BLACK
	)

errorButton = Button(
    " ERROR ",
    50,
    color = WHITE,
    bg = NAVY,
    border_color = BLACK
	)



if __name__ == '__main__':

	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	screen.fill(BACKGROUND_COLOR)

	while quiz == None:
		#quiz = Quiz(DATA_PTH, screen.get_size())
		try:
			quiz = Quiz(DATA_PTH, screen.get_size())
		except NameError as err:
			if err == 'No data.json found':
				nojsonButton.show(screen)
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT or nojsonButton.click(event):
						pygame.quit()
						exit()
			else:
				errorButton.show(screen)
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT or errorButton.click(event):
						pygame.quit()
						exit()
		except:
			errorButton.show(screen)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT or errorButton.click(event):
					pygame.quit()
					exit()


	while gameOn:

		while not Buzz.connected():
			pauseButton.show(screen)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT or pauseButton.click(event):
					pygame.quit()
					exit()

		if buzzInput == None and Buzz.connected():
			buzzInput = BuzzReader()
		if buzzInput != None and Buzz.connected():
			buzzOutput = BuzzWriter(buzzInput)
			quiz.get_writer(buzzOutput)

		if quiz.check_events(pygame.event.get()):
			quiz.check_buzz_events(buzzInput.read_io())
		#clock.tick(80)
		quiz.get_current_slide().show(screen, quiz)
		pygame.display.update()

		if quiz.get_ended():
			gameOn = False

	pygame.quit()