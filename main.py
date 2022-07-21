import pygame
import time #delete?
import json
from ioBuzz.inputReader import buzzReader, Pressed, Released, reader_connected
from objects.components import Button
from objects.quiz import Quiz , Slide

gameOn = True
buzzInput = None
quiz = None
DATA_PTH ='data.json'

BACKGROUND_COLOR = pygame.Color('BLACK')

pygame.init()
clock = pygame.time.Clock()
pauseButton = Button(
    " Buzz desconectat ",
    font = 50,
    color = pygame.Color('white'),
    border = True,
    bg = pygame.Color('navy'),
    border_color = pygame.Color('black'))

nojsonButton = Button(
    " NO data.json ",
    font = 50,
    color = pygame.Color('white'),
    border = True,
    bg = pygame.Color('navy'),
    border_color = pygame.Color('black'))

errorButton = Button(
    " ERROR ",
    font = 50,
    color = pygame.Color('white'),
    border = True,
    bg = pygame.Color('navy'),
    border_color = pygame.Color('black'))



if __name__ == '__main__':
	
	screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	screen.fill(BACKGROUND_COLOR)

	while quiz == None:
		#quiz = Quiz(DATA_PTH)
		try:
			quiz = Quiz(DATA_PTH)
		except NameError as err:
			if err == 'No data.json found':
				nojsonButton.show(screen, centered = True)
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT or nojsonButton.click(event):
						pygame.quit()
						exit()
			else:
				errorButton.show(screen, centered = True)
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT or errorButton.click(event):
						pygame.quit()
						exit()

		

	while gameOn:

		while not reader_connected():
			pauseButton.show(screen, centered = True)
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT or pauseButton.click(event):
					pygame.quit()
					exit()


		if buzzInput == None and reader_connected():
			buzzInput = buzzReader()

		quiz.check_events(pygame.event.get(),buzzInput.read_pressed(1))
		quiz.get_current_slide().show(screen, quiz)

		pygame.display.update()

		if quiz.get_ended():
			gameOn = False


	pygame.quit()

	

