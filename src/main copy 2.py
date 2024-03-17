# Pygame template.
# This game is not complete yet, it should represent an easy but addictive game that is quite fast with the aim to get a highscore
# There are some mistakes still
# The Game Speed is to fast
# After a certain amount of points there should be a rewarding message (keep up the motivation), however this seems to crash the game right now, i think is due to time.delay function. Right now i dont know how to solve it
# The monsters should end the Game when collide with player, the idea is that monsters are like level 2 enemies that move in x-direction 
# towards player position but otherwise just fall like obstacle
# The game should become increasingly difficult the more points the player has
# i want to add the robot figure as boss fight when points reach 3000 the robot can be hit by obstacles couple of times, but he wants to push the player around
# the robot moves towards player, once reached, the player is moving in a random direction a certain amount without beeing able to move 
# this makes it more likely to collide with obstacle


# Well, this is where i stand right now. If i find time, i will try to continue this. Thanks for everything, this was a fun course!!

# Import standard modules.
import sys
import pygame
import random
from pygame.locals import *
import pygame.image
import math

class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

def display_congratulations(screen, score):
    font = pygame.font.Font(None, 36)
    congrats_text = font.render("Congratulations! Score: " + str(score), True, (0, 0, 0))
    screen.blit(congrats_text, (width // 2 - congrats_text.get_width() // 2, height // 2 - congrats_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the message for 3000 milliseconds (3 seconds)

def update(dt, player, items, special_items, obstacles, score, special_timer, obstacle_speed, game_over, screen):
    """
    Update game. Called once per frame.
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Handle player input
        keys = pygame.key.get_pressed()
        player_speed = 7 if keys[K_LSHIFT] or keys[K_RSHIFT] else 5
        if keys[K_LEFT] and player.rect.left > 0:
            player.rect.x -= player_speed
        if keys[K_RIGHT] and player.rect.right < width:
            player.rect.x += player_speed
        if keys[K_UP] and player.rect.top > 0:
            player.rect.y -= player_speed
        if keys[K_DOWN] and player.rect.bottom < height:
            player.rect.y += player_speed

        # Update items
        for item in items:
            if player.rect.colliderect(item):
                items.remove(item)
                score += 10

        # Update special items
        if random.random() < 0.01:
            special_items.append(pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20))

        for special_item in special_items:
            if player.rect.colliderect(special_item):
                special_items.remove(special_item)
                score += 50

        # Update obstacles
        for obstacle in obstacles:
            obstacle.y += int(obstacle_speed)
            if obstacle.top > height:
                obstacle.y = 0
                obstacle.x = random.randint(0, width - obstacle.width)

            if player.rect.colliderect(obstacle):
                game_over = True

        # Update special item timer
        special_timer -= dt
        if special_timer <= 0:
            special_timer = 5.0

        # Change player color after gaining 500 points
        # Increase obstacle speed with collected points
        if score >= 500:
            rainbow_color = (255, 0, 0)
            if score >= 500:
                rainbow_color = (255, 125, 0)
                obstacle_speed = 6.0
                display_congratulations(screen, score)
            if score >= 1000:
                rainbow_color = (255, 255, 0)
                obstacle_speed = 7.0
                display_congratulations(screen, score)
            if score >= 1500:
                rainbow_color = (0, 255, 0)
                obstacle_speed = 8.0
                display_congratulations(screen, score)
            if score >= 2000:
                rainbow_color = (0, 125,  255)
                obstacle_speed = 9.0
                display_congratulations(screen, score)
            if score >= 2500:
                rainbow_color = (0, 0,  255)
                obstacle_speed = 10.0
                display_congratulations(screen, score)
            player.color = tuple(map(int, rainbow_color))

    return score, special_timer, obstacle_speed, game_over

def update_special_monster_items(dt, special_monster_items, player, game_over):
    for item in special_monster_items:
        direction_x = player.rect.centerx - item['rect'].centerx
        direction_y = player.rect.centery - item['rect'].centery
        distance = math.sqrt(direction_x**2 + direction_y**2)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        item['rect'].x += int(direction_x * item['x_speed'] * dt)
        item['rect'].y += int(direction_y * item['fall_speed'] * dt)

        if item['rect'].top > height or item['rect'].left < 0 or item['rect'].right > width:
            special_monster_items.remove(item)

        if player.rect.colliderect(item['rect']):
            game_over = True

    return game_over

def draw(screen, player, items, special_items, obstacles, score, game_over, coin_image, monster_image, special_monster_items):
    screen.fill((255, 255, 255))

    if not game_over:
        pygame.draw.rect(screen, player.color, player.rect)

        for item in items:
            pygame.draw.rect(screen, (0, 255, 0), item)

        for special_item in special_items:
            screen.blit(coin_image, special_item)

        for item in special_monster_items:
            screen.blit(monster_image, item['rect'])

        for obstacle in obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)

        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (10, 10))
    else:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

        font = pygame.font.Font(None, 36)
        restart_text = font.render("Press 'R' to restart", True, (0, 0, 0))
        quit_text = font.render("Press 'Q' to quit", True, (0, 0, 0))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))
        screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 100))

    pygame.display.flip()

def run_pygame():
    pygame.init()
    coin_image = pygame.image.load('coin.png')
    coin_image = pygame.transform.scale(coin_image, (20, 20))

    monster_image = pygame.image.load('monster.png')
    monster_image = pygame.transform.scale(monster_image, (30, 30))

    special_monster_items = []

    fps = 60.0
    fps_clock = pygame.time.Clock()

    global width, height
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    player = Player(width // 2 - 25, height - 60, 50, 50, (255, 0, 0))
    items = [pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20) for _ in range(12)]
    special_items = []
    obstacles = [pygame.Rect(random.randint(0, width - 30), random.randint(0, height - 30), 30, 30) for _ in range(5)]

    special_timer = 5.0
    obstacle_speed = 5.0
    game_over = False
    dt = fps_clock.tick(fps) / 1000.0

    score = 0

    while True:
        score, special_timer, obstacle_speed, game_over = update(dt, player, items, special_items, obstacles, score, special_timer, obstacle_speed, game_over, screen)

        if random.random() < 0.005 + 0.00002 * int(score):
            special_monster_items.append({
                'rect': pygame.Rect(random.randint(0, width - 30), 0, 30, 30),
                'fall_speed': random.randint(5, 9),
                'x_speed': random.uniform(-1.5, 1.5) * 2.0
            })

        draw(screen, player, items, special_items, obstacles, score, game_over, coin_image, monster_image, special_monster_items)

        keys = pygame.key.get_pressed()
        if game_over:
            if keys[K_r]:
                player = Player(width // 2 - 25, height - 60, 50, 50, (255, 0, 0))
                items = [pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20) for _ in range(10)]
                special_items = []
                obstacles = [pygame.Rect(random.randint(0, width - 30), random.randint(0, height - 30), 30, 30) for _ in range(5)]

                special_timer = 5.0
                obstacle_speed = 5.0
                game_over = False
                score = 0
            elif keys[K_q]:
                pygame.quit()
                sys.exit()

        score, special_timer, obstacle_speed, game_over = update(dt, player, items, special_items, obstacles, score, special_timer, obstacle_speed, game_over, screen)
        update_special_monster_items(dt, special_monster_items, player, game_over)
        draw(screen, player, items, special_items, obstacles, score, game_over, coin_image, monster_image, special_monster_items)

        for i in range(len(items)):
            if random.random() < 0.01:
                items[i] = pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20)

        dt = fps_clock.tick(fps) / 100  # Update dt inside the loop

if __name__ == "__main__":
    run_pygame()
