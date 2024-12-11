import pygame
import random
import math

class Herald:
    herald_images = []

    def preload_images():
        herald_images_paths = [
            'data/images/entities/SpearHerald.jpg',
            'data/images/entities/ShieldHerald.jpg',
            'data/images/entities/SwordHerald.jpg'
        ]

        target_width = 150
        Herald.herald_images = [
            Herald.resize_image(Herald.make_off_white_transparent(pygame.image.load(img_path)), target_width)
            for img_path in herald_images_paths
        ]

    def __init__(self, screen_width, screen_height):
        # Randomly select
        self.herald_type = random.choice([0, 1, 2])
        self.herald_img = Herald.herald_images[self.herald_type]

        # Set initial position
        self.herald_img_pos = [1200, (screen_height - self.herald_img.get_height()) - 55]
        self.speed = 1
        self.health = 100

        # Bobbing
        self.bobbing_amplitude = 1.2  
        self.bobbing_frequency = 0.25 
        self.time_offset = 0 

    def resize_image(img, width):
        aspect_ratio = img.get_height() / img.get_width()
        height = int(width * aspect_ratio)
        return pygame.transform.scale(img, (width, height))

    def make_off_white_transparent(img):
        img = img.convert_alpha()

        width, height = img.get_width(), img.get_height()

        tolerance = 30

        for y in range(height):
            for x in range(width):
                r, g, b, a = img.get_at((x, y))

                if (r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance):
                    img.set_at((x, y), pygame.Color(0, 0, 0, 0))
        return img

    def update_position(self):
        self.herald_img_pos[0] -= self.speed

        self.time_offset += 1 
        vertical_offset = int(self.bobbing_amplitude * math.sin(self.time_offset * self.bobbing_frequency))
        self.herald_img_pos[1] += vertical_offset

    def draw(self, screen):
        screen.blit(self.herald_img, self.herald_img_pos)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_width = 50
        health_height = 8
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.herald_img_pos[0] + 40, self.herald_img_pos[1] - 20, health_width, health_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.herald_img_pos[0] + 40, self.herald_img_pos[1] - 20, health_width * health_percentage, health_height))

    def check_collision_with_peasants(self, peasants):
        herald_rect = pygame.Rect(self.herald_img_pos[0], self.herald_img_pos[1], self.herald_img.get_width(), self.herald_img.get_height())
        for peasant in peasants[:]:
            peasant_rect = pygame.Rect(peasant.peasant_img_pos[0], peasant.peasant_img_pos[1], peasant.peasant_img.get_width(), peasant.peasant_img.get_height())
            if herald_rect.colliderect(peasant_rect):
                damage_to_peasant = self.calculate_damage_to_peasant(peasant)
                peasant.health -= damage_to_peasant
                if peasant.health <= 0:
                    peasants.remove(peasant)
                return True
        return False

    def calculate_damage_to_peasant(self, peasant):
        base_damage = 100 
        if self.herald_type == 0 and peasant.peasant_type == 2:
            return base_damage / 8  
        elif self.herald_type == 1 and peasant.peasant_type == 0:
            return base_damage / 8 
        elif self.herald_type == 2 and peasant.peasant_type == 1:
            return base_damage / 8  
        return base_damage 