import pygame
import random
import math

class Peasant:
    def __init__(self, image_path, start_pos):
        self.peasant_img = pygame.image.load(image_path)
        self.peasant_img.set_colorkey((255, 255, 255)) 
        self.original_peasant_img = self.peasant_img.copy() 
        self.peasant_img_pos = start_pos
        self.peasant_movement = [False, False]

        self.sounds = [
            pygame.mixer.Sound("data/sfx/Hit1.mp3"),
            pygame.mixer.Sound("data/sfx/Hit2.mp3"),
            pygame.mixer.Sound("data/sfx/Hit3.mp3"),
            pygame.mixer.Sound("data/sfx/Hit4.mp3"),
            pygame.mixer.Sound("data/sfx/Hit5.mp3"),
            pygame.mixer.Sound("data/sfx/Hit6.mp3"),
            pygame.mixer.Sound("data/sfx/Hit7.mp3"),
            pygame.mixer.Sound("data/sfx/Hit8.mp3"),
            pygame.mixer.Sound("data/sfx/Hit9.mp3"),
            pygame.mixer.Sound("data/sfx/Hit10.mp3"),
            pygame.mixer.Sound("data/sfx/Hit11.mp3"),
            pygame.mixer.Sound("data/sfx/Hit12.mp3")
        ]

        self.health = 100 

        # Bobbing
        self.bobbing_amplitude = 1.5 
        self.bobbing_frequency = 0.25  
        self.time_offset = 0  

    def update_position(self):
     
        if self.peasant_movement[0]:
            new_x = self.peasant_img_pos[0] + 1.5
            if new_x + self.peasant_img.get_width() <= 1280:
                self.peasant_img_pos[0] = new_x
            self.peasant_img = self.original_peasant_img

        elif self.peasant_movement[1]:
            new_x = self.peasant_img_pos[0] - 1.5
            if new_x >= 0:
                self.peasant_img_pos[0] = new_x
            # Flip the sprit
            self.peasant_img = pygame.transform.flip(self.original_peasant_img, True, False)

        if self.peasant_movement[0] or self.peasant_movement[1]:  # Only oscillate if moving
            self.time_offset += 1
            vertical_offset = int(self.bobbing_amplitude * math.sin(self.time_offset * self.bobbing_frequency))
            self.peasant_img_pos[1] += vertical_offset

    def handle_input(self, event):
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
        screen.blit(self.peasant_img, self.peasant_img_pos)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_width = 50
        health_height = 8
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.peasant_img_pos[0], self.peasant_img_pos[1] - 10, health_width, health_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.peasant_img_pos[0], self.peasant_img_pos[1] - 10, health_width * health_percentage, health_height))

    def take_damage(self, damage, attacker_type):
        if self.health <= 0:
            return True
        self.health -= damage
        if self.health <= 20:
            return False
        return False

    def check_collision_with_herald(self, heralds):
        for herald in heralds[:]: 
            peasant_rect = pygame.Rect(self.peasant_img_pos[0], self.peasant_img_pos[1], self.peasant_img.get_width(), self.peasant_img.get_height())
            herald_rect = pygame.Rect(herald.herald_img_pos[0], herald.herald_img_pos[1], herald.herald_img.get_width(), herald.herald_img.get_height())
            if peasant_rect.colliderect(herald_rect):

                sound_to_play = random.choice(self.sounds)
                sound_to_play.play()

                self.health -= 20 
                heralds.remove(herald) 
                if self.health <= 0:
                    return True  
        return False