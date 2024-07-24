import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.radius = 30
        self.color = (0, 0, 0)
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.speed = 5
        self.target_radius = self.radius
        self.growth_rate = 0.1  # Growth rate per frame

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def set_target_radius(self, amount):
        # Set the target radius to grow towards
        self.target_radius = max(self.target_radius, self.radius + amount)

    def update_growth(self):
        # Incrementally grow the player towards the target radius
        if self.radius < self.target_radius:
            self.radius += self.growth_rate
            if self.radius > self.target_radius:
                self.radius = self.target_radius

    def reset(self):
        self.radius = 30
        self.target_radius = self.radius
        self.x, self.y = WIDTH // 2, HEIGHT // 2

class GameObject:
    def __init__(self):
        self.radius = random.randint(20, 50)  # Objects are larger than the player
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.dx = 0
        self.dy = 0
        self.speed = random.uniform(0.5, 2)  # Speed can vary

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self, player, delta_time):
        # Calculate distance from the player
        dx_to_player = player.x - self.x
        dy_to_player = player.y - self.y
        distance = math.hypot(dx_to_player, dy_to_player)

        if self.radius > player.radius:
            # Chase the player if the object is larger
            self.chase(dx_to_player, dy_to_player, distance)
        else:
            # Escape from the player if the object is smaller
            self.escape(dx_to_player, dy_to_player, distance)

        # Update position based on velocity and delta_time
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time

        # Bounce off the edges
        self.handle_edges()

    def chase(self, dx_to_player, dy_to_player, distance):
        chase_speed = 2.0  # Adjust this value to control chase speed
        if distance < 200:  # Threshold distance to start chasing
            if distance != 0:
                chase_dx = dx_to_player / distance
                chase_dy = dy_to_player / distance
                # Gradually update dx and dy for smoother chasing
                self.dx = chase_dx * chase_speed
                self.dy = chase_dy * chase_speed
        else:
            # Move in the current direction
            self.dx *= self.speed
            self.dy *= self.speed

    def escape(self, dx_to_player, dy_to_player, distance):
        escape_speed = 2.0  # Adjust this value to control escape speed
        if distance < 200:  # Threshold distance to start escaping
            if distance != 0:
                escape_dx = -dx_to_player / distance
                escape_dy = -dy_to_player / distance
                # Gradually update dx and dy for smoother escaping
                self.dx = escape_dx * escape_speed
                self.dy = escape_dy * escape_speed
        else:
            # Move in the current direction
            self.dx *= self.speed
            self.dy *= self.speed

    def handle_edges(self):
        # Bounce off the edges
        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx = abs(self.dx)
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -abs(self.dx)
        
        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy = abs(self.dy)
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy = -abs(self.dy)

    def check_collision(self, player):
        # Check if the player is inside this object
        distance = math.hypot(player.x - self.x, player.y - self.y)
        return distance < (self.radius + player.radius)

def game_over():
    print("Game Over!")
    pygame.quit()
    sys.exit()

def restart_game():
    global player, objects
    player.reset()
    objects = [GameObject() for _ in range(20)]  # Recreate objects

# Create the player and objects
player = Player()
objects = [GameObject() for _ in range(20)]

# Main game loop
while True:
    delta_time = clock.tick(60) / 1000.0  # Time in seconds since the last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get key states
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -1
    if keys[pygame.K_RIGHT]:
        dx = 1
    if keys[pygame.K_UP]:
        dy = -1
    if keys[pygame.K_DOWN]:
        dy = 1

    # Move the player
    player.move(dx, dy)
    player.update_growth()  # Update player growth

    # Check for collisions and handle objects
    for obj in objects[:]:
        obj.move(player, delta_time)
        if obj.check_collision(player):
            # If the object is larger, game over
            if obj.radius > player.radius:
                game_over()
            else:
                # Set growth target for the player
                player.set_target_radius(obj.radius // 2)
                objects.remove(obj)  # Remove the object from the game

    # Game over condition (example: no objects left)
    if not objects:
        restart_game()

    # Fill the screen with a color (white in this case)
    screen.fill((255, 255, 255))

    # Draw the player
    player.draw(screen)

    # Draw the objects
    for obj in objects:
        obj.draw(screen)

    # Update the display
    pygame.display.flip()
