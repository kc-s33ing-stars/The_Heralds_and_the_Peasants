import pygame
import random

class LesserPeasant:
    preloaded_images = {}
    preloaded_sounds = []

    def preload_assets():
        for peasant_type in range(3):
            LesserPeasant.preloaded_images[peasant_type] = [
                LesserPeasant.load_image(LesserPeasant.get_image_for_type(peasant_type, 0)),
                LesserPeasant.load_image(LesserPeasant.get_image_for_type(peasant_type, 1))
            ]
        LesserPeasant.preloaded_sounds = [
            pygame.mixer.Sound(f"data/sfx/Hit{i}.mp3") for i in range(1, 13)
        ]

    def __init__(self, peasant_type, start_pos):
        self.peasant_type = peasant_type
        self.frame = 0 
        self.peasant_images = LesserPeasant.preloaded_images[peasant_type]
        
        self.peasant_images = [self.resize_image(img, 125) for img in self.peasant_images]

        self.peasant_img_pos = start_pos
        self.speed = 1
        self.sounds = LesserPeasant.preloaded_sounds

        self.health = 100

    def load_image(image_path):
        img = pygame.image.load(image_path).convert_alpha() 
        img = LesserPeasant.make_off_white_transparent(img)
        return img

    def make_off_white_transparent(img):
        width, height = img.get_width(), img.get_height()
        tolerance = 30
        for y in range(height):
            for x in range(width):
                r, g, b, a = img.get_at((x, y))
                if (r >= 255 - tolerance and g >= 255 - tolerance and b >= 255 - tolerance):
                    img.set_at((x, y), pygame.Color(0, 0, 0, 0)) 
        return img

    def get_image_for_type(peasant_type, frame):
        if peasant_type == 0:
            return f'data/images/entities/Spear{frame + 1}.jpg'
        elif peasant_type == 1:
            return f'data/images/entities/Shield{frame + 1}.jpg'
        elif peasant_type == 2:
            return f'data/images/entities/Sword{frame + 1}.jpg'
        return 'data/images/entities/peasant_1.png'

    def resize_image(self, img, width):
        aspect_ratio = img.get_height() / img.get_width()
        height = int(width * aspect_ratio)
        return pygame.transform.scale(img, (width, height))

    def update_position(self):
        self.peasant_img_pos[0] += (1 * self.speed)
        self.frame += 1
        if self.frame >= 30: 
            self.frame = 0

    def draw(self, screen):
        screen.blit(self.peasant_images[self.frame // 15], self.peasant_img_pos)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_width = 50
        health_height = 8
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.peasant_img_pos[0] + 35, self.peasant_img_pos[1] - 20, health_width, health_height))  
        pygame.draw.rect(screen, (0, 255, 0), (self.peasant_img_pos[0] + 35, self.peasant_img_pos[1] - 20, health_width * health_percentage, health_height))

    def calculate_damage_to_herald(self, herald):
        sound_to_play = random.choice(self.sounds)
        sound_to_play.play()

        base_damage = 50 
        if self.peasant_type == 0 and herald.herald_type == 2:
            return base_damage / 8 
        elif self.peasant_type == 1 and herald.herald_type == 0:
            return base_damage / 8 
        elif self.peasant_type == 2 and herald.herald_type == 1:
            return base_damage / 8 
        return base_damage 