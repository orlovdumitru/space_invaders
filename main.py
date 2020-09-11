import pygame
import random
from pygame import mixer


MEDIA = 'media'

class SpaceInvaders(object):

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800

        self.game_running = True
       # player location
        self.playerX = self.screen_width // 2
        self.playerY = (self.screen_height // 5) * 4
        self.enemies = {}
        self.bullets = []
        self.explosions = []
        self.score = 0
        
        self.text_left = 20
        self.text_top = 20
        self.increase_score = 20
        self.bullet_speed = 5
        self.number_of_enemies = 4
        self.enemy_x_speed = 0.6
        self.enemy_y_speed = 0.5
        self.player_x_speed = 3
        self.player_y_speed = 2
        self.icon_size = 64
        self.enemy_conter = 0
        self.temp_lef_right = 0
        self.temp_up_down = 0

         # initialize pygame
        pygame.init()

        # define score font type and size
        # self.font = pygame.font.Font('freesansbold.ttf', 32) # default font
        # custom font (https://www.dafont.com/)
        self.font = pygame.font.Font(f'{MEDIA}/FIRESTARTER.TTF', 32)

        self.game_over_font = pygame.font.Font(f'{MEDIA}/FIRESTARTER.TTF', 60)

        # create a screen
        self.screen = pygame.display.set_mode( (self.screen_width, self.screen_height) )

        # background image
        self.background = pygame.image.load(f'{MEDIA}/bg.jpg')

        # background sound
        mixer.music.load(f'{MEDIA}/backgroun_sound_1.wav')
        mixer.music.play(-1)

        # title and game icon
        pygame.display.set_caption("Space invaders")
        icon = pygame.image.load(f'{MEDIA}/ship_small.png')
        pygame.display.set_icon(icon)

        # player
        self.playerImg = pygame.image.load(f'{MEDIA}/ship_medium.png')
    

    def check_collapse(self, enemy):
        if self.enemies[enemy]['positionY'] >= (self.screen_height - self.icon_size):
            return True
        if (((self.enemies[enemy]['positionY'] + self.icon_size) >= self.playerY) and (self.enemies[enemy]['positionY'] <= self.playerY + self.icon_size)) and (((self.enemies[enemy]['positionX'] + self.icon_size) >= self.playerX) and (self.enemies[enemy]['positionX'] <= self.playerX + self.icon_size)):
            return True
        return False


    def enemy_hit(self, bullet):
        for enemy in self.enemies:
            if ( bullet['y_coor'] <= (self.enemies[enemy]['positionY'] + self.icon_size) and (bullet['y_coor'] >= self.enemies[enemy]['positionY']) ) and ( (bullet['x_coor'] <= (self.enemies[enemy]['positionX'] + self.icon_size)) and ( bullet['x_coor'] >= self.enemies[enemy]['positionX'])):
                x_explo = self.enemies[enemy]['positionX']
                y_explo = self.enemies[enemy]['positionY']
                del self.enemies[enemy]

                # add shoot sound effect
                self.add_sound_effect('explosion.wav')
                
                self.add_enemy()
                self.create_explostion(x_explo, y_explo)
                self.score += self.increase_score
                return True


    # add sound effect
    def add_sound_effect(self, sound):
        sound_effect = mixer.Sound(f'{MEDIA}/{sound}')
        sound_effect.play()


    def add_bullet(self):
        # add shoot sound effect
        self.add_sound_effect('shoot.wav')

        new_bullet = {
            'x_coor': (self.playerX + 16),
            'y_coor': self.playerY,
            'bullet':  pygame.image.load(f'{MEDIA}/bullet.png')
        }
        self.bullets.append(new_bullet)
       

    def move_bullets(self):
        for bullet in self.bullets:
            bullet['y_coor'] -= self.bullet_speed
            self.screen.blit(bullet['bullet'], (bullet['x_coor'], bullet['y_coor']))

            hit_enem = self.enemy_hit(bullet)

            if bullet['y_coor'] < -10 or hit_enem:
                self.bullets.remove(bullet)

        

    def add_enemy(self):
        # add enemy to dict
        if len(self.enemies) < self.number_of_enemies:
            self.enemy_conter += 1
            random_enemy = random.randint(1, 3)
            enemyX = random.randint(1, 1150)
            enemyY = random.randint(-75, -10)
            enemy_move_direction = random.randint(0, 1)

            if enemy_move_direction == 0:
                enemy_move_direction = 'left'
            else:
                enemy_move_direction = 'right'

            new_enemy = pygame.image.load(f'{MEDIA}/enemy_{random_enemy}.png')
            enemy_name = f"enemy{self.enemy_conter}"
            
            self.enemies[enemy_name] = {}
            self.enemies[enemy_name]['move_direction'] = enemy_move_direction
            self.enemies[enemy_name]['image'] = new_enemy
            self.enemies[enemy_name]['positionX'] = enemyX
            self.enemies[enemy_name]['positionY'] = enemyY


    # position enemies on the screen
    def enemy_on_screen(self):
        self.add_enemy()

        # move enemy down
        for enemy in self.enemies:
            self.enemies[enemy]['positionY'] += self.enemy_y_speed

            # game lost check
            if self.check_collapse(enemy):
                self.game_running = False

            if self.enemies[enemy]['move_direction'] == 'left' and self.enemies[enemy]['positionX'] > 0:
                self.enemies[enemy]['positionX'] -= self.enemy_x_speed
            elif self.enemies[enemy]['move_direction'] == 'right' and self.enemies[enemy]['positionX'] < (self.screen_width - self.icon_size):
                self.enemies[enemy]['positionX'] += self.enemy_x_speed
            elif self.enemies[enemy]['move_direction'] == 'left' and self.enemies[enemy]['positionX'] <= 0:
                self.enemies[enemy]['move_direction'] = 'right'
                self.enemies[enemy]['positionX'] += self.enemy_x_speed
            elif self.enemies[enemy]['move_direction'] == 'right' and self.enemies[enemy]['positionX'] >= (self.screen_width - self.icon_size):
                self.enemies[enemy]['move_direction'] = 'left'
                self.enemies[enemy]['positionX'] -= self.enemy_x_speed

            self.screen.blit(self.enemies[enemy]['image'], (self.enemies[enemy]['positionX'], self.enemies[enemy]['positionY']))


    # position player image on the screen
    def player_on_screen(self, position_x, position_y):
        self.screen.blit(self.playerImg, (position_x, position_y) )


    def create_explostion(self, coor_x, coor_y):
        explosion = {
            'explosion':[
                pygame.image.load(f'{MEDIA}/explosion_0.png'),
                pygame.image.load(f'{MEDIA}/explosion_1.png'),
                pygame.image.load(f'{MEDIA}/explosion_2.png'),
            ],
            'x_coor': coor_x,
            'y_coor': coor_y
        }
        self.explosions.append(explosion)
        self.display_explosion()


    def display_explosion(self):
        for explosion in self.explosions:
            for image_explosion in explosion['explosion']:
                self.screen.blit(image_explosion, (explosion['x_coor'], explosion['y_coor']))
            # remove explosion from list
            self.explosions.remove(explosion)


    def game_score(self):
        score = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score, (self.text_left, self.text_top))

    
    def game_over_message(self):
        game_over = self.game_over_font.render(f"""GAME OVER YOUR SCORE: {self.score}""", True, (255, 255, 255))
        self.screen.blit(game_over, (100, self.screen_height//2 - 50))


    def run_game(self):
        # game running in a loop until close button is pressed
        
        while self.game_running:
            # set screen color
            self.screen.fill( (0, 0, 0) )
            # set background image below background color to stay on top of color
            self.screen.blit(self.background, (0, 0))

            # get events
            for event in pygame.event.get():
                # close the window 
                if event.type == pygame.QUIT:
                    self.game_running = False

                # left right arrow event
                if event.type == pygame.KEYDOWN:
                    # left arrow event
                    if event.key == pygame.K_LEFT:
                        self.temp_lef_right = -(self.player_x_speed)
                    # right arrow event
                    if event.key == pygame.K_RIGHT:
                        self.temp_lef_right = self.player_x_speed
                    # up arrow event
                    if event.key == pygame.K_UP:
                        self.temp_up_down = -(self.player_y_speed)
                    # down arrow event
                    if event.key == pygame.K_DOWN:
                        self.temp_up_down = self.player_y_speed
                    
                    if event.key == 32: #pygame.K_TAB
                        self.add_bullet()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                       self.temp_lef_right = 0
                       self.temp_up_down = 0
            
            # left right move
            if self.temp_lef_right < 0 and self.playerX >= 0:
                self.playerX += self.temp_lef_right
            if self.temp_lef_right > 0 and self.playerX < (self.screen_width - self.icon_size):
                self.playerX += self.temp_lef_right
            # up down move
            if self.temp_up_down > 0 and self.playerY < (self. screen_height -self.icon_size):
                self.playerY += self.temp_up_down
            if self.temp_up_down < 0 and self.playerY > ((self.screen_height // 5) * 3):
                self.playerY += self.temp_up_down

            # player must be after screen fill (reposition player)
            self.player_on_screen(self.playerX, self.playerY)

            # position enemy on the screen
            self.enemy_on_screen()

            # bullets on screen
            self.move_bullets()

            # display score
            self.game_score()

            # update game view
            pygame.display.update()
        
        end_game = True
        while end_game:
            self.game_over_message()
            
            # get events
            for event in pygame.event.get():
                # close the window 
                if event.type == pygame.QUIT:
                    end_game = False
            
            # update game view
            pygame.display.update()

    


game = SpaceInvaders()
game.run_game()
game.game_over