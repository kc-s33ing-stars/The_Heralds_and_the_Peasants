import pygame

class Peasant:
    def __init__(self, image_path, start_pos):
        self.peasant_img = pygame.image.load(image_path)
        self.peasant_img.set_colorkey((255, 255, 255))  # Remove white bg
        self.peasant_img_pos = start_pos
        self.peasant_movement = [False, False]
        self.health = 100  # Starting health

    def update_position(self):
        self.peasant_img_pos[0] += self.peasant_movement[0] - self.peasant_movement[1]

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
        if self.health <= 20:  # Last 1/5th of health
            return False
        return False

    # Check collision with a Herald and take 1/5th of health
    def check_collision_with_herald(self, heralds):
        for herald in heralds[:]:  # Use a copy of the list for safe removal
            peasant_rect = pygame.Rect(self.peasant_img_pos[0], self.peasant_img_pos[1], self.peasant_img.get_width(), self.peasant_img.get_height())
            herald_rect = pygame.Rect(herald.herald_img_pos[0], herald.herald_img_pos[1], herald.herald_img.get_width(), herald.herald_img.get_height())
            if peasant_rect.colliderect(herald_rect):
                self.health -= 20  # Take 1/5th of health
                heralds.remove(herald)  # Remove Herald after collision
                if self.health <= 0:
                    return True  
        return False