
import pygame

class Peasant:
    def __init__(self, image_path, start_pos):
        self.peasant_img = pygame.image.load(image_path)
        self.peasant_img.set_colorkey((255, 255, 255))  # Remove white color
        self.peasant_img_pos = start_pos
        self.peasant_movement = [False, False]  # Movement: [right, left]
    
    def update_position(self):
        # Update the peasant's horizontal position based on the movement flags
        self.peasant_img_pos[0] += self.peasant_movement[0] - self.peasant_movement[1]
    
    def handle_input(self, event):
        # Handle key events for peasant movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.peasant_movement[0] = True
            if event.key == pygame.K_LEFT:
                self.peasant_movement[1] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.peasant_movement[0] = False
            if event.key == pygame.K_LEFT:
                self.peasant_movement[1] = False
    
    def draw(self, screen):
        # Draw the peasant image on the screen
        screen.blit(self.peasant_img, self.peasant_img_pos)