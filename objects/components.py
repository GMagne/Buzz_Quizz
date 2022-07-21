import pygame
import pygame.gfxdraw

TOP_MARGIN_BTN = 4
SIDE_MARGIN_BTN = 4

DFLT_FNT = "Arial"

class Image:

    def __init__(self, image_path, pos = (None,None) ):
        self.x, self.y = None, None if pos==(None,None) else pos
        try:
            self.image = pygame.image.load(image_path) #imatge original
            self.size = self.image.get_size() #size de la imatge, passarà a size de la self.surface
            self.surface = -1  #imatge per fer screen.blit, -1 és no inicialitzat
            
        except FileNotFoundError:
            self.image = None
            self.surface = None


    def get_surface(self,scaled,x,y):
        if scaled and x>0 and y>0 and self.size[0]>0 and self.size[1]>0:
            if (self.size[0]/x > self.size[1]/y):
                self.size = (x, int(x*self.size[1]/self.size[0]))
                self.surface = pygame.transform.scale(self.image,self.size)
            else:
                self.size = ( int(y*self.size[0]/self.size[1]), y)
                self.surface = pygame.transform.scale(self.image,self.size)
        else:
            self.surface = self.image



    def show(self, screen, centered = False, scaled = True, last_show = True):

        x, y = screen.get_size()

        if self.surface == -1:
            self.get_surface(scaled,x,y)
            if centered or self.x == None or self.y == None:
                self.x, self.y = (int((x-self.size[0])/2), int((y-self.size[1])/2))
            self.rect = pygame.Rect( self.x, self.y, self.size[0], self.size[1])

        if self.surface == None:
            return 0
        else:
            screen.blit(self.surface, (self.x, self.y))



    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False


class Button:
 
    def __init__(self, text, font, color = "black",  pos = (None,None), border = False, bg="white", border_color = "black"):
        self.x, self.y = None, None if pos == (None,None) else pos
        self.font = pygame.font.SysFont(DFLT_FNT , font)
        self.color = color
        self.bg_color = bg
        self.border = border
        self.border_color = border_color
        self.change_text(text)

        if self.x != None or self.y != None :
            self.rect = pygame.Rect( self.x, self.y, self.size[0], self.size[1])

 
    def change_text(self, text):
        
        color = self.color
        bg = self.bg_color

        self.text = self.font.render(text, 1, color)
        self.size = self.text.get_size()
        
        if self.border:
            self.surface = pygame.Surface((self.size[0]+2*SIDE_MARGIN_BTN,self.size[1]+2*TOP_MARGIN_BTN))
            self.surface.fill(self.border_color)
            innerSurface = pygame.Surface(self.size)
            innerSurface.fill(bg)
            innerSurface.blit(self.text, (0, 0))
            self.surface.blit(innerSurface,(SIDE_MARGIN_BTN,SIDE_MARGIN_BTN))

        else:
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bg)
            self.surface.blit(self.text, (0, 0))
        


    def show(self, screen, centered = False):
        x, y = screen.get_size()

        if centered or self.x == None or self.y == None:
            self.x, self.y = (int((x-self.size[0])/2), int((y-self.size[1])/2))
            self.rect = pygame.Rect( self.x, self.y, self.size[0], self.size[1])


        screen.blit(self.surface, (self.x, self.y))
 

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    return True
        return False


class Text:

    def __init__(self, text, size, color = 'black', background_color = None, font = None):
        self.text = text 
        self.size = size 
        self.color = color
        self.font = DFLT_FNT if font == None else font
        self.background = background_color

        self.set_surface()


    def set_surface(self):
        text_render = pygame.font.SysFont(self.font, self.size).render(self.text, 1, self.color)
        self.s_size = text_render.get_size()
        self.surface = pygame.Surface(self.s_size, pygame.SRCALPHA)
        if self.background != None : 
            self.surface.fill(self.background_color)

        self.surface.blit(text_render, (0, 0))


    def show(self, screen, pos = (None,None)):
        x, y = screen.get_size()

        if (pos[0] == None) :
            pos = (int((x-self.s_size[0])/2), pos[1])
        elif (pos[1] == None) :
            pos = (pos[0], int((y-self.s_size[1])/2))

        screen.blit(self.surface, pos)


class Icon:

    def __init__(self, image_path, change_color = 'green', background_color = 'white'):

        self.change_color = pygame.Color(change_color)
        self.background_color = pygame.Color(background_color)
        self.connected = False
        self.refresh = True

        try:
            self.image = pygame.image.load(image_path) #imatge original
            self.surface = None
        except FileNotFoundError:
            self.image = None
            self.surface = None


    def set_surface(self, scaled, x, y):
        if self.image == None :
            return 0

        self.size = self.image.get_size()

        R = int(x/2) if x<y else int(y/2)

        self.surface = pygame.Surface( (2*R,2*R), pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(self.surface, R, R, R, self.background_color)
        pygame.gfxdraw.filled_circle(self.surface, R, R, R, self.background_color)


        if self.connected :
            r = int(9*R/10)
            pygame.gfxdraw.aacircle(self.surface, R, R, r, self.change_color)
            pygame.gfxdraw.filled_circle(self.surface, R, R, r, self.change_color)

        a = int(R/10)
        if scaled and self.size[0]>0 and self.size[1]>0:
            if (self.size[0] > self.size[1]):
                self.size = ( 2*R-2*a, int(2*(R-a)*self.size[1]/self.size[0]))
                img_surface = pygame.transform.scale(self.image,self.size)
            else:
                self.size = ( int(2*(R-a)*self.size[0]/self.size[1]), 2*R-2*a)
                img_surface = pygame.transform.scale(self.image,self.size)
        else:
            img_surface = self.image

        self.surface.blit(img_surface, (a,a) )


    def show(self, screen, h, pos = (0,None)):
        x, y = screen.get_size()
    
        if self.image == None:
            return 0
        elif self.refresh :
            self.refresh = False
            self.set_surface(True,x,y)

        R = int(x/2) if x<y else int(y/2)
        pos = (pos[0]+int(h/2)-R, pos[1])
        screen.blit(self.surface, pos)

    def connect(self, color = None, connected = True):
        self.connected = connected
        self.change_color = color if color != None else self.change_color
        self.refresh = True

