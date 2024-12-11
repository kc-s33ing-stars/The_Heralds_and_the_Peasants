import pygame
import sys
from data.scripts.peasant import Peasant
from data.scripts.lesser_peasant import LesserPeasant
from data.scripts.herald import Herald

class Game:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption('The Heralds and the Peasants')
        self.screen = pygame.display.set_mode((1280, 720))

        Herald.preload_images()
        LesserPeasant.preload_assets()

        self.clock = pygame.time.Clock()

        # Background
        self.background_img = pygame.image.load('data/images/clouds.png')

        # Peasant
        self.peasant_start_pos = [0, 600]
        self.peasant = Peasant('data/images/entities/peasant_1.png', self.peasant_start_pos)

        # Lesser Peasants
        self.lesser_peasants_array = []
        self.lesser_peasant_frame_counter = 0
        self.lesser_peasant_spawn_interval_frames = 300
        self.selected_peasant_type = 0

        # Heralds
        self.heralds_array = []
        self.herald_frame_counter = 0
        self.herald_spawn_interval_frames = 300

        # Church
        self.collision_area = pygame.Rect(900, 600, 300, 50)
        self.church_img = pygame.image.load('data/images/entities/Church.jpg')
        self.church_health = 100  

        # Buttons
        self.button_1 = pygame.Rect(20, 20, 200, 50)
        self.button_2 = pygame.Rect(20, 80, 200, 50)
        self.button_3 = pygame.Rect(20, 140, 200, 50)

        self.button_sounds = [
            pygame.mixer.Sound("data/sfx/MoreSPears.mp3"), 
            pygame.mixer.Sound("data/sfx/MoreShields.mp3"),
            pygame.mixer.Sound("data/sfx/MoreSwords.mp3") 
        ]

        self.endgame_sounds = [
            pygame.mixer.Sound("data/sfx/Victory.mp3"), 
            pygame.mixer.Sound("data/sfx/GameOver.mp3")
        ]

        self.music = [
            pygame.mixer.Sound("data/sfx/Music.wav")
        ]


    def run(self):

        self.music[0].play(loops=-1, maxtime=0, fade_ms=0)

        while True:

            # Background
            self.screen.blit(self.background_img, (0, 0))

            # Buttons
            self.draw_buttons()

            # Collision Area Health Bar
            img_r = pygame.Rect(self.peasant.peasant_img_pos[0], self.peasant.peasant_img_pos[1], self.peasant.peasant_img.get_width(), self.peasant.peasant_img.get_height())
            if img_r.colliderect(self.collision_area):
                self.church_health -= 0.05
                if self.church_health <= 0:
                    self.display_game_over_win()
                    break
            self.draw_collision_area_health()

            # Update peasant
            self.peasant.update_position()
            self.peasant.draw(self.screen)

            # Check collision with heralds
            if self.peasant.check_collision_with_herald(self.heralds_array):
                self.display_game_over()
                break

            # Update lesser peasants
            for lesser_peasant in self.lesser_peasants_array[:]:
                lesser_peasant.update_position()
                for herald in self.heralds_array[:]:
                    lesser_peasant_rect = pygame.Rect(lesser_peasant.peasant_img_pos[0], lesser_peasant.peasant_img_pos[1], 100, 100)
                    herald_rect = pygame.Rect(herald.herald_img_pos[0], herald.herald_img_pos[1], herald.herald_img.get_width(), herald.herald_img.get_height())
                    if lesser_peasant_rect.colliderect(herald_rect):
                        damage_to_herald = lesser_peasant.calculate_damage_to_herald(herald)
                        herald.health -= damage_to_herald
                        lesser_peasant.health -= 25
                        if herald.health <= 0:
                            self.heralds_array.remove(herald)
                        if lesser_peasant.health <= 0:
                            self.lesser_peasants_array.remove(lesser_peasant)
                else:
                    lesser_peasant.draw(self.screen)
            self.lesser_peasant_frame_counter += 1

            # Update heralds
            for herald in self.heralds_array[:]:
                herald.update_position()
                if herald.health <= 0:
                    self.heralds_array.remove(herald)
                else:
                    herald.draw(self.screen)
            self.herald_frame_counter += 1

            # Spawn lesser peasants
            if self.lesser_peasant_frame_counter >= self.lesser_peasant_spawn_interval_frames:
                self.spawn_lesser_peasant()
                self.lesser_peasant_frame_counter = 0

            # Spawn heralds
            if self.herald_frame_counter >= self.herald_spawn_interval_frames:
                self.spawn_herald()
                self.herald_frame_counter = 0

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_button_click(event.pos)
                self.peasant.handle_input(event)

            pygame.display.update()
            self.clock.tick(60)

    def draw_buttons(self):

        border_thickness = 3  
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_1.inflate(border_thickness * 2, border_thickness * 2), border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_2.inflate(border_thickness * 2, border_thickness * 2), border_radius=20)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_3.inflate(border_thickness * 2, border_thickness * 2), border_radius=20)

        pygame.draw.rect(self.screen, (100, 0, 50), self.button_1, border_radius=15)
        pygame.draw.rect(self.screen, (50, 200, 0), self.button_2, border_radius=15)
        pygame.draw.rect(self.screen, (0, 50, 150), self.button_3, border_radius=15)

        font = pygame.font.Font(None, 36)
        label_1 = font.render("Spear Peasant", True, (255, 255, 255))
        label_2 = font.render("Shield Peasant", True, (255, 255, 255))
        label_3 = font.render("Sword Peasant", True, (255, 255, 255))

        self.screen.blit(label_1, (self.button_1.x + 10, self.button_1.y + 15))
        self.screen.blit(label_2, (self.button_2.x + 10, self.button_2.y + 15))
        self.screen.blit(label_3, (self.button_3.x + 10, self.button_3.y + 15))

    def handle_button_click(self, pos):
        if self.button_1.collidepoint(pos):
            self.button_sounds[0].play()
            self.selected_peasant_type = 0
        elif self.button_2.collidepoint(pos):
            self.button_sounds[1].play()
            self.selected_peasant_type = 1
        elif self.button_3.collidepoint(pos):
            self.button_sounds[2].play()
            self.selected_peasant_type = 2

    def spawn_lesser_peasant(self):
        new_peasant = LesserPeasant(self.selected_peasant_type, [0, 540])
        self.lesser_peasants_array.append(new_peasant)

    def spawn_herald(self):
        new_herald = Herald(self.screen.get_width(), self.screen.get_height())
        self.heralds_array.append(new_herald)

    def draw_collision_area_health(self):
        health_width = self.collision_area.width
        health_height = 10
        health_percentage = self.church_health / 100
        pygame.draw.rect(self.screen, (255, 0, 0), (self.collision_area.x, self.collision_area.y - 320, health_width, health_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.collision_area.x, self.collision_area.y - 320, health_width * health_percentage, health_height))

        church_image = pygame.image.load('data/images/entities/Church.jpg')

        church_image.set_colorkey((255, 255, 255)) 
        church_width = self.collision_area.width
        church_height = int(church_image.get_height() * (church_width / church_image.get_width()))
        resized_church_image = pygame.transform.scale(church_image, (church_width, church_height))

        self.screen.blit(resized_church_image, (self.collision_area.x, 300))

    def display_game_over(self):
        font = pygame.font.Font(None, 100)
        text = font.render("Game Over!", True, (255, 0, 0))
        self.screen.blit(text, (375, 300))
        self.endgame_sounds[1].play()
        self.music[0].stop()
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    waiting = False

    def display_game_over_win(self):
        font = pygame.font.Font(None, 100)
        text = font.render("You Got Em!", True, (0, 255, 70))
        self.screen.blit(text, (375, 300))
        self.endgame_sounds[0].play()
        self.music[0].stop()
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    waiting = False

    def reset_game(self):
        self.peasant.health = 100
        self.peasant.peasant_img_pos = self.peasant_start_pos
        self.lesser_peasants_array.clear()
        self.heralds_array.clear()
        self.lesser_peasant_frame_counter = 0
        self.herald_frame_counter = 0
        self.church_health = 100  
        self.run()

Game().run()