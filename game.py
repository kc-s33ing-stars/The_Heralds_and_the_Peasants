
import pygame
import sys
from data.peasant import Peasant 

class Game:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption('The Heralds and the Peasants')
        self.screen = pygame.display.set_mode((1280, 720))

        self.clock = pygame.time.Clock()

        # Background
        self.background_img = pygame.image.load('data/images/clouds.png')

        # Initialize Peasant object
        self.peasant = Peasant('data/images/entities/peasant.png', [0, 600])

        # Church and collision area
        self.collision_area = pygame.Rect(700, 500, 300, 50)
        self.church_img = pygame.image.load('data/images/entities/Church.png')

    def run(self):
        while True:
            # Background is in back
            self.screen.blit(self.background_img, (0, 0))

            # Collision Area
            img_r = pygame.Rect(self.peasant.peasant_img_pos[0], self.peasant.peasant_img_pos[1], self.peasant.peasant_img.get_width(), self.peasant.peasant_img.get_height())
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            # Update peasant position and draw it
            self.peasant.update_position()
            self.peasant.draw(self.screen)

            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle peasant movement based on key events
                self.peasant.handle_input(event)

            pygame.display.update()
            self.clock.tick(60)

# Run the game
Game().run()