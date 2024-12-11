import pygame

class LesserPeasant:
    def __init__(self, peasant_type, start_pos):
        self.peasant_type = peasant_type
        self.peasant_img = pygame.image.load(self.get_image_for_type(peasant_type))
        self.peasant_img.set_colorkey((255, 255, 255))
        self.peasant_img_pos = start_pos
        self.speed = 1
        self.health = 100

    def get_image_for_type(self, peasant_type):
        if peasant_type == 0:
            return 'data/images/entities/peasant_1.png'
        elif peasant_type == 1: 
            return 'data/images/entities/peasant_2.png'
        elif peasant_type == 2: 
            return 'data/images/entities/peasant_3.png'
        return 'data/images/entities/peasant_1.png'

    def update_position(self):
        self.peasant_img_pos[0] += (1 * self.speed)

    def draw(self, screen):
        screen.blit(self.peasant_img, self.peasant_img_pos)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        health_width = 50
        health_height = 8
        health_percentage = self.health / 100
        pygame.draw.rect(screen, (255, 0, 0), (self.peasant_img_pos[0], self.peasant_img_pos[1] - 10, health_width, health_height))  
        pygame.draw.rect(screen, (0, 255, 0), (self.peasant_img_pos[0], self.peasant_img_pos[1] - 10, health_width * health_percentage, health_height))

    def calculate_damage_to_herald(self, herald):
        print(self.peasant_type)
        base_damage = 50  # Default damage value
        if self.peasant_type == 0 and herald.herald_type == 2:
            return base_damage / 8  # Half damage to type 2 Herald
        elif self.peasant_type == 1 and herald.herald_type == 0:
            return base_damage / 8  # Half damage to type 3 Herald
        elif self.peasant_type == 2 and herald.herald_type == 1:
            return base_damage / 8  # Half damage to type 1 Herald
        print(self.peasant_type)
        return base_damage 