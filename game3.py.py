import pygame
import random
import time
# Initialize Pygame
pygame.init()
 
# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

 
class Game:
    def __init__(self):
        # Initialize game state variables
        self.running = True
        self.spaceship = Spaceship()
        self.enemies=[]
        self.asteroids=[]
        self.bullets=[]
        self.specialboxes=[]
        self.bombs = []
        self.lasers = []
        self.enemy_bullets = []
        self.current_time = pygame.time.get_ticks()
        self.current_time_asteroid = pygame.time.get_ticks()
        self.current_time_specialbox = pygame.time.get_ticks()
        self.current_time_enemy_bullet = pygame.time.get_ticks()
        self.score = 0
        self.firing_rate = 1000
        self.last_shot_time = 0 
        self.clock = pygame.time.Clock()
 
    def create_asteroid(self):
        # Get the elapsed time for asteroid
        elapsed_time_asteroid = pygame.time.get_ticks()-self.current_time_asteroid
        # Every 1 second, create a new enemy spaceship
        if elapsed_time_asteroid > 5000:
            self.asteroids.append(Asteroid())
            # Reset the current time
            self.current_time_asteroid = pygame.time.get_ticks()
 
    def move_asteroids(self):
        for asteroid in self.asteroids:
            # Move the asteroid spaceship down
            asteroid.move()
 
        if self.spaceship.check_collision(self.asteroids):
            self.running = False
 
            # Destroy the asteroid spaceship
            asteroid.destroy_yourself(self.asteroids)
 
    def create_specialbox(self):
        # Get the elapsed time for asteroid
        elapsed_time_specialbox = pygame.time.get_ticks()-self.current_time_specialbox
        # Every 1 second, create a new enemy spaceship
        if elapsed_time_specialbox > 10000:
            self.specialboxes.append(SpecialBox())
            # Reset the current time
            self.current_time_specialbox = pygame.time.get_ticks()
 
    def move_specialboxes(self):
        for specialbox in self.specialboxes:
            # Move the specialbox spaceship down
            specialbox.move()
            
        if self.spaceship.check_collision(self.specialboxes):
            specialbox.destroy_yourself(self.specialboxes)
            self.spaceship.use_special_box()
            
    
    def create_enemies(self):
        # Get the elapsed time
        elapsed_time = pygame.time.get_ticks() - self.current_time
 
        # Every 1 second, create a new enemy spaceship
        if elapsed_time > 3000:
            self.enemies.append(EnemySpaceship())
            # Reset the current time
            self.current_time = pygame.time.get_ticks()
   
    def move_enemies(self):
        for enemy in self.enemies:
            # Move the enemy spaceship down
            enemy.move()
 
        if self.spaceship.check_collision(self.enemies):
            self.running = False
 
            # Destroy the enemy spaceship
            enemy.destroy_yourself(self.enemies)
 
 
    def move_right(self):
        # Check if the right arrow key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            # Check the location of the spaceship and move right if within screen boundaries
            self.spaceship.check_location(self.spaceship.move_right_to_spaceship)
 
    def move_left(self):
        # Check if the left arrow key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Check the location of the spaceship and move left if within screen boundaries
            self.spaceship.check_location(self.spaceship.move_left_to_spaceship)
       
    def create_bullet(self):
        # Create a new bullet at the middle of the spaceship's position
        x = self.spaceship.rect.x + self.spaceship.rect.width // 2
        y = self.spaceship.rect.y
        self.bullets.append(Bullet(x, y))
    
    def create_enemy_bullet(self):
        for enemy in self.enemies:
            random_number = random.randint(0,1000)
            if random_number < 4:
                # Create a new bullet at the middle of the spaceship's position               
                self.enemy_bullets.append(EnemyBullet(enemy.get_bullet_position_x(), enemy.get_bullet_position_y()))

    def move_enemy_bullet(self):
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.move()

        if self.spaceship.check_collision_with_bullet(self.enemy_bullets):
            self.spaceship.take_damage()

    def move_bullets(self):
        for bullet in self.bullets:
            # Move the bullet
            bullet.move()
    def create_laser(self):
        # Create a new bullet at the middle of the spaceship's position
        x = self.spaceship.rect.x + self.spaceship.rect.width // 2
        y = self.spaceship.rect.y
        self.lasers.append(Laser(x, y))
        self.spaceship.has_laser -= 1
        if self.spaceship.has_laser == 0 :
            self.spaceship.weapon_type = "bullet"
            self.spaceship.has_laser = 5
 
    def move_laser(self):
        for laser in self.lasers:
            # Move the bullet
            laser.move()

    def create_bomb(self):
        # Create a new bullet at the middle of the spaceship's position
        x = self.spaceship.rect.x + self.spaceship.rect.width // 2
        y = self.spaceship.rect.y
        self.bombs.append(Bomb(x, y))
        self.spaceship.has_bomb = False
        self.spaceship.weapon_type = "bullet"
        
 
    def move_bombs(self):
        for bomb in self.bombs:
            # Move the bullet
            bomb.move()
   
    def check_collisions(self):
        # Check if any bullets have collided with any enemies
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    # Destroy the enemy and remove the bullet
                    # Increase score by 2 points
                    self.score += 2
                    enemy.destroy_yourself(self.enemies)
                    bullet.destroy_yourself(self.bullets)        
                            # Check if any bullets have collided with any enemies
        for laser in self.lasers:
            for enemy in self.enemies:
                if laser.rect.colliderect(enemy.rect):
                    # Destroy the enemy and remove the bullet
                    # Increase score by 2 points
                    self.score += 2
                    enemy.destroy_yourself(self.enemies)

        for bomb in self.bombs:
            for enemy in self.enemies:
                if bomb.rect.colliderect(enemy.rect):
                    # Destroy the enemy and remove the bullet
                    # Increase score by 2 points
                    self.score += 2
                    self.enemies = []
                    self.asteroids = []
                    bomb.destroy_yourself(self.bombs)
       
         # Check if any bullets have collided with any asteroids
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if bullet.rect.colliderect(asteroid.rect):
                    # Destroy the asteroid and remove the bullet
                    # Increase score by 3 points
                    self.score += 3
                    asteroid.destroy_yourself(self.asteroids)
                    bullet.destroy_yourself(self.bullets)
         # Check if any bullets have collided with any asteroids
        for laser in self.lasers:
            for asteroid in self.asteroids:
                if laser.rect.colliderect(asteroid.rect):
                    # Destroy the asteroid and remove the bullet
                    # Increase score by 3 points
                    self.score += 3
                    asteroid.destroy_yourself(self.asteroids)
                    

         # Check if any bullets have collided with any asteroids
        for bomb in self.bombs:
            for asteroid in self.asteroids:
                if bomb.rect.colliderect(asteroid.rect):
                    # Destroy the asteroid and remove the bullet
                    # Increase score by 3 points
                    self.score += 3
                    self.asteroids = []
                    self.enemies = []
                    bomb.destroy_yourself(self.bombs)

    def draw_score(self):
        # Set the font and size
        font = pygame.font.Font(None, 36)
        # Render the text
        text = font.render("Score: {}".format(self.score), True, (255, 255, 255))
        # Draw the text on the screen
        screen.blit(text, (10, 10))

    def draw_health(self):
        self.spaceship.draw_health()
    
    def draw_weapon_type(self):
        self.spaceship.draw_weapon_type()


    def check_if_out_of_screen(self):
        for enemy in self.enemies:
            enemy.check_if_out_of_screen()
    
    def pause_game(self):
    # Check if the P key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.paused = True

            # Display the "Please Press R Button To Continue" message on the screen
            font = pygame.font.Font(None, 36)
            text = font.render("Please Press R Button To Continue", 1, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
            screen.blit(text, text_rect)
            pygame.display.flip()

            # Wait for the R key to be pressed
            while self.paused:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.paused = False

                    

   
    def run_game(self):
        # Set the initial time
        current_time = pygame.time.get_ticks()
 
        # Main game loop
        while self.running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_time_for_firing = pygame.time.get_ticks()
                        if current_time_for_firing - self.last_shot_time > self.firing_rate:

                            if self.spaceship.weapon_type == "bullet":
                                self.create_bullet()
                            elif self.spaceship.weapon_type == "bomb":
                                self.create_bomb()
                            elif self.spaceship.weapon_type == "laser":
                                self.create_laser ()
                            self.last_shot_time = current_time_for_firing
            
            self.pause_game()
                    
                   


                            
            self.clock.tick(60)
 
            # Clear the screen
            screen.fill((0, 0, 0))
 
            # Update game state
            self.move_left()
            self.move_right()
            self.create_enemies()
            self.move_enemies()
            self.create_asteroid()
            self.move_asteroids()
            self.move_bullets()
            self.move_laser()
            self.move_bombs()
            self.check_collisions()
            self.create_specialbox()
            self.move_specialboxes()
            self.draw_score()
            self.draw_health()
            self.draw_weapon_type()
            self.check_if_out_of_screen()
            self.create_enemy_bullet()
            self.move_enemy_bullet()

 
 
              # Draw to screen
            self.spaceship.create_spaceship()
            for enemy in self.enemies:
                enemy.create_enemy_spaceship()
           
            for asteroid in self.asteroids:
                asteroid.create_asteroid()
           
            for specialbox in self.specialboxes:
                specialbox.create_specialbox()
           
            for bullet in self.bullets:
                bullet.create_our_bullet()
            for laser in self.lasers:
                laser.create_laser()
            for bomb in self.bombs:
                bomb.create_bomb()

            for enemy_bullet in self.enemy_bullets:
                enemy_bullet.create_enemy_bullet()

               
           
            pygame.display.update()
           # pygame.time.delay(3)

 
 
class Spaceship:
    def __init__(self):
        # Load the spaceship image
        self.image = pygame.image.load("player_spaceship.png")
 
        # Get the rect of the spaceship image
        self.rect = self.image.get_rect()
 
        # Scale the spaceship image to 10% of the screen size
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.1), int(screen_height * 0.1)))
 
        # Get the new rect of the spaceship image after scaling
        self.rect = self.image.get_rect()
 
        # Set the position of the spaceship at the bottom of the screen
        self.rect.x = screen_width / 2
        self.rect.y = screen_height - self.rect.height

        self.health = 100
        self.weapon_type = "bullet"  
        self.has_bomb = False    
        self.has_laser = 5  

 
    def create_spaceship(self):
        # Draw the spaceship image to the screen
        screen.blit(self.image, self.rect)
   
    def check_location(self, move_function):
        # Call the provided function to move the spaceship
        move_function()
 
        # Check if the spaceship has moved beyond the screen boundaries
        if self.rect.left < 0:
            # If beyond the left edge, move the spaceship to the edge
            self.rect.left = 0
        elif self.rect.right > screen_width:
            # If beyond the right edge, move the spaceship to the edge
            self.rect.right = screen_width
 
    def move_left_to_spaceship(self):
        # Only move the spaceship if it is not already at the left edge of the screen
        if self.rect.left > 0:
            # Move the spaceship left
            self.rect.x -= 6
 
    def move_right_to_spaceship(self):
        if self.rect.right < screen_width:
            # Move the spaceship right
            self.rect.x += 6
    def check_collision_with_bullet(self, enemy_bullets):
        for enemy_bullet in enemy_bullets:
            if enemy_bullet.is_collide(self.rect):
                self.health -= 30
                enemy_bullet.destroy_yourself(enemy_bullets)
                print(self.health)
                if self.health<= 0:
                    game.running = False
 
    def check_collision(self, enemies):
        for enemy in enemies:
            if enemy.is_collide(self.rect):
                # Collision detected, end the game
                return True
        return False
    def draw_weapon_type(self):
        # Set the font and size
        font = pygame.font.Font(None, 36)
        # Render the text
        text = font.render("Weapon: {}".format(self.weapon_type), True, (255, 255, 255))
        # Draw the text on the screen
        screen.blit(text, (612, 40))

    def draw_health(self):
        # Set the font and size
        font = pygame.font.Font(None, 36)
        # Render the text
        text = font.render("Health: {}".format(self.health), True, (255, 255, 255))
        # Draw the text on the screen
        screen.blit(text, (657, 10))

    def use_special_box(self):

            # Generate a random integer from 1 to 3
            specail_box_type = random.randint(1, 3)
            if specail_box_type == 1:
                #self.spaceship.change_weapon_to_laser()
                self.weapon_type = "laser"
                

            if specail_box_type == 2:
                self.has_bomb = True
                #self.spaceship.change_weapon_to_bomb()
                self.weapon_type = "bomb"


            if specail_box_type == 3:
                #self.spaceship.repair()
                self.health +=40
                if self.health > 100:
                    self.health = 100
            

class EnemySpaceship:
    def __init__(self):
        # Load the enemy spaceship image
        self.image = pygame.image.load("enemyspaceship.png")
 
        # Get the rect of the enemy spaceship image
        self.rect = self.image.get_rect()
 
        # Scale the enemy spaceship image to 10% of the screen size
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.1), int(screen_height * 0.1)))
 
        # Get the new rect of the enemy spaceship image after scaling
        self.rect = self.image.get_rect()
 
        # Set the initial position of the enemy spaceship at the top of the screen
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -80
        self.x = 0
        self.y = 0

    
    def check_if_out_of_screen(self):
        if self.rect.y >1000:
            self.destroy_yourself(game.enemies)
            
    def get_bullet_position_x(self):
            x = self.rect.x + self.rect.width // 2
            
            return x
    def get_bullet_position_y(self):
        
            y = self.rect.y

            return y
 
    def create_enemy_spaceship(self):
        # Draw the enemy spaceship image to the screen
        screen.blit(self.image, self.rect)
 
    def is_collide(self, spaceship_rect):
        return self.rect.colliderect(spaceship_rect)

    def destroy_yourself(self, enemies):
     # Remove the enemy spaceship from the list of enemies
        enemies.remove(self)
    def move(self):
        self.rect.y += 2
 
 
class Asteroid:
    def __init__(self):
        # Load the enemy spaceship image
        self.image = pygame.image.load("asteroid.png")
 
        # Get the rect of the enemy spaceship image
        self.rect = self.image.get_rect()
 
        # Scale the enemy spaceship image to 10% of the screen size
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.1), int(screen_height * 0.1)))
 
        # Get the new rect of the enemy spaceship image after scaling
        self.rect = self.image.get_rect()
 
        # Set the initial position of the enemy spaceship at the top of the screen
        self.rect.x = random.randint(0, screen_width - self.rect.width)
       
        self.rect.y = float(-80) 

    def check_if_out_of_screen(self):
        if self.rect.y >1000:
            self.destroy_yourself(game.asteroids) 
   
    def create_asteroid(self):
        # Draw the enemy spaceship image to the screen
        screen.blit(self.image, self.rect)
 
    def is_collide(self, spaceship_rect):
        return self.rect.colliderect(spaceship_rect)
 
    def destroy_yourself(self, asteroids):
     # Remove the enemy spaceship from the list of enemies
        asteroids.remove(self)
    def move(self):
        self.rect.y += 4
 
class SpecialBox:
    def __init__(self):
        # Load the enemy spaceship image
        self.image = pygame.image.load("specialbox.jpg")
 
        # Get the rect of the enemy spaceship image
        self.rect = self.image.get_rect()
 
        # Scale the enemy spaceship image to 10% of the screen size
        self.image = pygame.transform.scale(self.image, (int(screen_width * 0.1), int(screen_height * 0.1)))
 
        # Get the new rect of the enemy spaceship image after scaling
        self.rect = self.image.get_rect()
 
        # Set the initial position of the enemy spaceship at the top of the screen
        self.rect.x = random.randint(0, screen_width - self.rect.width)
       
        self.rect.y = float(-80)  
   
    def check_if_out_of_screen(self):
        if self.rect.y >1000:
            self.destroy_yourself(game.specialboxes)
 
    def create_specialbox(self):
        # Draw the enemy spaceship image to the screen
        screen.blit(self.image, self.rect)
 
    def is_collide(self, spaceship_rect):
        return self.rect.colliderect(spaceship_rect)
 
    def destroy_yourself(self, specialboxes):
     # Remove the enemy spaceship from the list of enemies
        specialboxes.remove(self)
    def move(self):
        self.rect.y += 5
 
class Guns:
    def destroy_yourself(self, bullets):
        bullets.remove(self)

    def check_if_out_of_screen(self):
        if self.rect.y < -300:
            self.destroy_yourself(game.bullets)
        

class Bomb(Guns):
    def __init__(self, x, y):
        # Load the bomb image
        self.image = pygame.image.load("Bomb.png")

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Get the rect of the bomb image
        self.rect = self.image.get_rect()

        # Set the initial position of the bomb
        self.rect.x = x
        self.rect.y = y

    def move(self):
        # Move the bomb upward
        self.rect.y -= 5

    def create_bomb(self):
        screen.blit(self.image, self.rect)

    def destroy_yourself(self, bombs):
        bombs.remove(self)
        
class Laser(Guns):
    def __init__(self, x, y):
        # Load the laser image
        self.image = pygame.image.load("laser.png")

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Get the rect of the laser image
        self.rect = self.image.get_rect()

        # Set the initial position of the bullet
        self.rect.x = x
        self.rect.y = y

    def move(self):
        # Move the bullet upward
        self.rect.y -= 5

    def create_laser(self):
        screen.blit(self.image, self.rect)

    def destroy_yourself(self, lasers):
        lasers.remove(self)

    def check_if_out_of_screen(self):
        if self.rect.y < -300:
            self.destroy_yourself(game.lasers)


class Bullet(Guns):
    def __init__(self, x, y):
        # Load the bullet image
        self.image = pygame.image.load("OurBullet.png")

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Get the rect of the bullet image
        self.rect = self.image.get_rect()

        # Set the initial position of the bullet
        self.rect.x = x
        self.rect.y = y

    def move(self):
        # Move the bullet upward
        self.rect.y -= 5

    def create_our_bullet(self):
        screen.blit(self.image, self.rect)

class EnemyBullet(Guns):
    def __init__(self, x, y):
        # Load the bullet image
        self.image = pygame.image.load("EnemyBullet.png")

        # Scale the image to the desired size
        self.image = pygame.transform.scale(self.image, (40, 40))

        # Get the rect of the bullet image
        self.rect = self.image.get_rect()

        # Set the initial position of the bullet
        self.rect.x = x
        self.rect.y = y

    def create_enemy_bullet(self):
        screen.blit(self.image, self.rect)

    def check_if_out_of_screen(self):
        if self.rect.y > 1000:
            self.destroy_yourself(game.enemy_bullets)

    def move(self):
        # Move the bullet upward
        self.rect.y += 5

    def is_collide(self, spaceship_rect):
        return self.rect.colliderect(spaceship_rect)


# Set the window title
pygame.display.set_caption("Press Enter to Start")

# Set the font and font size
font = pygame.font.Font(None, 36)

# Render the text
text = font.render("Press Enter to Start", True, (255, 255, 255))

# Get the rectangle for the text
text_rect = text.get_rect()

# Center the rectangle
text_rect.center = (screen_width // 2, screen_height // 2)

# Set the background color
screen.fill((0, 0, 0))

# Draw the text on the screen
screen.blit(text, text_rect)

# Update the display
pygame.display.flip()

# Wait for the Enter key to be pressed
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False


game = Game()
game.run_game()