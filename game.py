import pygame

import sys


class Game:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption('The Heralds and the Peasants')
        self.screen = pygame.display.set_mode((1280, 720))

        self.clock = pygame.time.Clock()

        #BACKGROUND
        self.background_img= pygame.image.load('data\images\clouds.png')


        #PEASANT
        self.peasant_img = pygame.image.load('data\images\entities\peasant.png')
        self.peasant_img.set_colorkey((255,255,255))
        self.peasant_img_pos = [0, 600]
        self.peasant_movement = [False, False]

        #CHURCH
        self.collision_area = pygame.Rect(0,200,300,50)
        self.church_img = pygame.image.load('data\images\entities\Church.png')

    def run(self):
        while True:

            #Background is in back
            self.screen.blit(self.background_img, (0,0))




            #Collision Area
            img_r = pygame.Rect(self.peasant_img_pos[0], self.peasant_img_pos[1], self.peasant_img.get_width(), self.peasant_img.get_height())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
            

            #Update Screen And Process Movement
            self.peasant_img_pos[1] += self.peasant_movement[1] - self.peasant_movement[0]
            self.screen.blit(self.peasant_img, self.peasant_img_pos)




            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.peasant_movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.peasant_movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.peasant_movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.peasant_movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()