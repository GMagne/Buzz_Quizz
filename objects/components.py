import pygame
import pygame.gfxdraw
import random
from math import ceil
from imageManager import imageDict, Image
from objects.constants import TOP_MARGIN_BTN, SIDE_MARGIN_BTN, DFLT_FONT, OPTION_FNT, DFLT_TXT_COLOR,\
DFLT_BG_COLOR, DFLT_BRDR_COLOR, DFLT_FEEDBACK_COLOR, DFLT_SCR_SIZE, colorDict, OPTION_BG_COLOR, OPTION_MRGN_p100, \
TIMER_FONT_SIZE


class Draw:

    def __init__(self, image, size):
        self.image = image
        x, y = size
        self.set_surface(x,y)
        self.refresh = False


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if self.refresh:
            self.set_surface(x, y)
            self.refresh = False

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        if self.surface != None:
            screen.blit(self.surface, pos)


    def set_surface(self, x, y):
        self.surface,  self.s_size = self.image.get_surface(True, x, y)

    def get_surface(self):
        return self.surface

    def get_surface_size(self):
        return self.s_size



class Text:

    def __init__(self, text, size, color = None ,\
                font = None, background_color = None):
        self.text = text 
        self.size = size 
        self.color = DFLT_TXT_COLOR if color == None else color
        self.font = DFLT_FONT if font == None else font
        self.background = background_color

        self.set_surface()

    def get_text(self):
        return self.text


    def set_surface(self):
        font = pygame.font.SysFont(self.font, self.size, bold = True)
        line_renders = []
        line_sizes = []
        self.s_size = (0,0)

        for line in self.text.splitlines():
            line_renders.append(font.render( line, 1, self.color))
            line_size = line_renders[-1].get_size()
            line_sizes.append(line_size)
            if line_size[0]>self.s_size[0]:
                self.s_size = (line_size[0], self.s_size[1])
            self.s_size = (self.s_size[0], self.s_size[1]+line_size[1])

        self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)
        if self.background != None:
                self.surface.fill(self.background)
        posy = 0
        for i, render in enumerate(line_renders):
            line_size = line_sizes[i]

            self.surface.blit(render, ( int((self.s_size[0]-line_size[0])/2), posy ))
            
            posy = posy+line_size[1]


    def change(self, text = None, size = None, color = None, font = None, background_color = None):
        self.text = self.text if text == None else text
        self.size = self.size if size == None else size
        self.color = self.color if color == None else color
        self.font = self.font if font == None else font
        self.background = self.background if background_color == None else background_color

        self.set_surface()


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        screen.blit(self.surface, pos)

    def get_surface(self):
        return self.surface

    def get_surface_size(self):
        return self.s_size


class Button:
 
    def __init__(self, text, tamany, font = DFLT_FONT , color = DFLT_TXT_COLOR,\
         bg = DFLT_BG_COLOR, border_color = DFLT_BRDR_COLOR ):
        self.text = Text(text, tamany, color = color, background_color = bg, font = font)
        self.border_color = border_color # pygame.color
        self.set_surface()


    def set_surface(self):
        text_surface = self.text.get_surface()
        txt_sur_size = self.text.get_surface_size()

        if self.border_color != None:
            self.s_size = (txt_sur_size[0]+2*SIDE_MARGIN_BTN, txt_sur_size[1]+2*TOP_MARGIN_BTN)
            self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)
            self.surface.fill(self.border_color)
            self.surface.blit(text_surface, (SIDE_MARGIN_BTN, SIDE_MARGIN_BTN) )

        else:
            self.s_size = txt_sur_size
            self.surface = text_surface


    def show(self, screen, pos = (None, None)):
        x, y = screen.get_size()

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        self.rect = pygame.Rect( pos[0], pos[1], self.s_size[0], self.s_size[1])
        screen.blit(self.surface, pos)
 

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False



class Icon:

    def __init__(self, image_path, feedback_color = DFLT_FEEDBACK_COLOR,\
            background_color = DFLT_BG_COLOR):

        self.feedback = False
        self.feedback_color = feedback_color
        self.background_color = background_color
        self.refresh = True

        self.image = imageDict[image_path] if image_path in imageDict.keys() else imageDict['blank'] #imatge original
        self.surface = None


    def set_surface(self, scaled, x, y):

        self.s_size = self.image.get_size()

        R = int(x/2) if x<y else int(y/2)

        self.surface = pygame.Surface( (2*R,2*R), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.surface, R, R, R, self.background_color)
        pygame.gfxdraw.aacircle(self.surface, R, R, R-1, self.background_color)
        pygame.gfxdraw.filled_circle(self.surface, R, R, R, self.background_color)


        if self.feedback :
            r = int(0.9*R)
            pygame.gfxdraw.aacircle(self.surface, R, R, r, self.feedback_color)
            pygame.gfxdraw.filled_circle(self.surface, R, R, r, self.feedback_color)

        a = int(R/10)
        if scaled and self.s_size[0]>0 and self.s_size[1]>0:
            if (self.s_size[0] > self.s_size[1]):
                self.s_size = ( 2*R-2*a, int(2*(R-a)*self.s_size[1]/self.s_size[0]))
                img_surface = pygame.transform.scale(self.image.get_image(), self.s_size)
            else:
                self.s_size = ( int(2*(R-a)*self.s_size[0]/self.s_size[1]), 2*R-2*a)
                img_surface = pygame.transform.scale(self.image.get_image(), self.s_size)
        else:
            img_surface = self.image

        self.surface.blit(img_surface, (a,a) )


    def show(self, screen, pos):
        x, y = screen.get_size()
    
        if self.refresh :
            self.refresh = False
            self.set_surface(True,x,y)

        screen.blit(self.surface, pos)


    def set_feedback(self, feedback, color = None):
        if feedback != self.feedback:
            self.feedback = feedback
            self.feedback_color = color if color != None else self.feedback_color
            self.refresh = True


class IconBar:

    def __init__(self, list_image_path, n, size):
        self.n = n
        self.s_size = size
        self.icon_player =[]
        self.refresh = False
        
        for i in range(n):
            self.icon_player.append(Icon(list_image_path[i]))

        self.set_surface(size[0],size[1])


    def set_surface(self, x, y):
        self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)
        if x>y :
            R = int(y/2)
            h = int(x/self.n)
            h2 = int(h/2)
            for i in range(self.n):
                self.icon_player[i].show(self.surface, (i*h+h2-R, 0))
        else:
            R = int(x/2)
            h = int(y/self.n)
            h2 = int(h/2)
            for i in range(self.n):
                self.icon_player[i].show(self.surface, (0, i*h+h2-R))


    def set_feedback(self, player, feedback, color = None):
        self.icon_player[player].set_feedback(feedback, color)
        self.refresh = True


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if self.refresh :
            a, b = self.s_size
            self.set_surface(a, b)
            self.refresh = False

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        screen.blit(self.surface, pos)


class ScoreBar:

    def __init__(self, n, size):
        self.n = n
        self.s_size = size
        self.refresh = False
        self.score_number = [0 for _ in range(n)]

        self.score = []
        for i in range(n):
            self.score.append(Text('0', DFLT_SCR_SIZE))

        self.set_surface(size[0],size[1])

    def get_score(self):
        return self.score_number

    def change_score(self, score):
        for i in range(len(self.score_number)):
            self.score_number[i] = score[i]
        self.refresh = True 
        for i, text in enumerate(self.score):
            text.change(text = str(score[i]))


    def set_surface(self, x, y):
        self.s_size = (x,y)
        self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)
        if x>y :
            h = int(x/self.n)
            for i in range(self.n):
                a, b = self.score[i].get_surface_size()
                self.score[i].show(self.surface, (i*h+int((h-a)/2), None))
        else:
            h = int(y/self.n)
            h2 = int(h/2)
            for i in range(self.n):
                a, b = self.score[i].get_surface_size()
                self.score[i].show(self.surface, (None, i*h+int((h-b)/2)))


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if self.refresh :
            a, b = self.s_size
            self.set_surface(a, b)
            self.refresh = False

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        screen.blit(self.surface, pos)


class OptionsBar:

    def __init__(self, data, size):
        self.opcions =  data["text"]
        self.correcte = data["correcte"]  
        self.random = data["posicio_aleatoria"]
        self.size = data["tamany_lletra"]
        self.color = colorDict[data["color"]] if data["color"] in colorDict.keys() else None

        self.set_surface(size[0], size[1])

    def get_text(self):
        ret = []
        for text in self.text:
            ret.append(text.get_text())
        return ret

    def get_correct(self):
        return self.correcte

    def set_text(self):
        self.text = []
        for i in range(len(self.opcions)):
            t = Text(self.opcions[i], self.size, color = self.color , font = OPTION_FNT, background_color = OPTION_BG_COLOR)
            self.text.append(t)
        
        if self.random:
            random.shuffle(self.text)

    def set_surface(self, x, y):
        self.s_size = (x,y)
        self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)

        self.set_text()
        n = len(self.text)

        if n==1:
            self.text[0].show(self.surface)

        elif n==2:
            mini_s_size = (int(x/2), y)
            s0 = pygame.Surface(mini_s_size, pygame.SRCALPHA)
            self.text[0].show(s0, (int(x*OPTION_MRGN_p100/2),None))
            self.text[1].show(s1, (int(x*OPTION_MRGN_p100/2),None))

            self.surface.blit(s0,(0,0))
            self.surface.blit(s1,(mini_s_size[0],0))

        elif n>2:
            m = int(ceil(n/2))
            mini_s0_size = (int(x/m), int(y/2))

            for i in range(m):
                s0 = pygame.Surface(mini_s0_size, pygame.SRCALPHA)
                self.text[i].show(s0, (int(mini_s0_size[0]*OPTION_MRGN_p100),None))
                self.surface.blit(s0,(mini_s0_size[0]*i,0))

            mini_s1_size = (int(x/(n-m)), mini_s0_size[1])
            for i in range(m,n):

                s1 = pygame.Surface(mini_s1_size, pygame.SRCALPHA)
                self.text[i].show(s1, (int(mini_s1_size[0]*OPTION_MRGN_p100),None))
                self.surface.blit(s1,(mini_s1_size[0]*(i-m), mini_s1_size[1]))


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        screen.blit(self.surface, pos)

class Timer:

    def __init__(self, inicial_time):
        self.clock = pygame.time.Clock()
        self.inicial_time = inicial_time
        self.time = inicial_time
        self.running = False

        self.set_surface()

    def get_surface_size(self):
        return self.surface.get_size()

    def get_surface(self):
        return self.surface

    def set_surface(self):
        text = Text(str(int(round(self.time,0))), TIMER_FONT_SIZE)
        self.surface = text.get_surface()

    def set_running(self, running):
        if self.time<=0 and running:
            self.restart()

        self.clock.tick()
        self.running = running

    def change_running(self):
        if self.running:
            self.set_running(0)
        else:
            self.set_running(1)

    def restart(self):
        self.time = self.inicial_time
        self.set_surface()

    def get_time(self):
        return self.time

    def show(self, screen, pos = (None, None)):
        x, y = screen.get_size()

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        if (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        if self.running:
            self.time -= self.clock.tick()/1000
            if self.time <= 0:
                self.time = 0
                self.running = False
            self.set_surface()

        a, b = self.get_surface_size()
        screen.blit(self.surface, (pos[0]-a, pos[1]-b))