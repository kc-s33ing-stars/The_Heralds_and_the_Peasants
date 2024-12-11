import pygame
import random

class Herald:
    def __init__(self, screen_width, screen_height):
        self.herald_images = [
            pygame.image.load('data/images/entities/herald_1.png'),
            pygame.image.load('data/images/entities/herald_2.png'),
            pygame.image.load('data/images/entities/herald_3.png')
        ]

        self.herald_type = random.choice([0, 1, 2])  
        self.herald_img = self.herald_images[self.herald_type]
        self.herald_img.set_colorkey((255, 255, 255))  
        self.herald_img_pos = [1200, (screen_height - self.herald_img.get_height()) - 75]
        self.speed = 1
        self.health = 100  

    def update_position(self):
        self.herald_img_pos[0] -= self.speed

    def draw(self, screen):
        screen.blit(self.herald_img, self.herald_img_pos)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_width = 50
        health_height = 8
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.herald_img_pos[0], self.herald_img_pos[1] - 10, health_width, health_height))  
        pygame.draw.rect(screen, (0, 255, 0), (self.herald_img_pos[0], self.herald_img_pos[1] - 10, health_width * health_percentage, health_height))  

    def check_collision_with_peasants(self, peasants):
        herald_rect = pygame.Rect(self.herald_img_pos[0], self.herald_img_pos[1], self.herald_img.get_width(), self.herald_img.get_height())
        for peasant in peasants[:]:
            peasant_rect = pygame.Rect(peasant.peasant_img_pos[0], peasant.peasant_img_pos[1], peasant.peasant_img.get_width(), peasant.peasant_img.get_height())
            if herald_rect.colliderect(peasant_rect):
                damage_to_peasant = self.calculate_damage_to_peasant(peasant)
                peasant.health -= damage_to_peasant
                if peasant.health <= 0:
                    peasants.remove(peasant)  # Remove peasant if health is zero
                return True
        return False

    def calculate_damage_to_peasant(self, peasant):
        print(self.herald_type)
        base_damage = 100  # Default damage value
        if self.herald_type == 0 and peasant.peasant_type == 2:
            return base_damage / 8  # Half damage to type 3 Lesser Peasant
        elif self.herald_type == 1 and peasant.peasant_type == 0:
            return base_damage / 8  # Half damage to type 1 Lesser Peasant
        elif self.herald_type == 2 and peasant.peasant_type == 1:
            return base_damage / 8  # Half damage to type 1 Lesser Peasant
        return base_damage  # Full damage otherwise