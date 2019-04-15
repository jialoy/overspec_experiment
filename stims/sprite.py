import pygame
import sys

class LoadSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(LoadSprite, self).__init__()
        self.images = []
        self.images.extend([pygame.image.load('loading{}.png'.format(i)) for i in range(1,5)])

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(0, 0, 300, 300)

    def update(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0      # reset index to 0 if we're at the last image of our sprite
        self.image = self.images[self.index]

def loading_screen():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    screen.fill((255, 255, 255))

    loadingImage = LoadSprite()
    loadingImageGroup = pygame.sprite.Group(loadingImage)
    
    clock = pygame.time.Clock()
    t0 = pygame.time.get_ticks()
    
    while True:
        
        tt = pygame.time.get_ticks() - t0
        
        event = pygame.event.poll()

        # Calling the 'my_group.update' function calls the 'update' function of all 
        # its member sprites. Calling the 'my_group.draw' function uses the 'image'
        # and 'rect' attributes of its member sprites to draw the sprite.
        loadingImageGroup.update()
        loadingImageGroup.draw(screen)
        pygame.display.update()
        clock.tick(1)
        
        if tt > 15000:
            break

loading_screen()