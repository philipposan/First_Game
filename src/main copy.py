import sys
import pygame
import random
from pygame.locals import *

class Player:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

class Monster:
    def __init__(self, x, y, width, height, fall_speed, x_speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.fall_speed = fall_speed
        self.x_speed = x_speed

def display_congratulations(screen, score):
    font = pygame.font.Font(None, 36)
    congrats_text = font.render(f"Congratulations! Score: {score}", True, (0, 0, 0))
    screen.blit(congrats_text, (width // 2 - congrats_text.get_width() // 2, height // 2 - congrats_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(3000)  # Display the message for 3000 milliseconds (3 seconds)

def handle_player_input(player, keys):
    player_speed = 7 if keys[K_LSHIFT] or keys[K_RSHIFT] else 5
    if keys[K_LEFT] and player.rect.left > 0:
        player.rect.x -= player_speed
    if keys[K_RIGHT] and player.rect.right < width:
        player.rect.x += player_speed
    if keys[K_UP] and player.rect.top > 0:
        player.rect.y -= player_speed
    if keys[K_DOWN] and player.rect.bottom < height:
        player.rect.y += player_speed

def update_items(player, items, special_items, monsters, obstacles, score, special_timer, obstacle_speed, game_over):
    for item in items:
        if player.rect.colliderect(item):
            items.remove(item)
            score += 10

    if random.random() < 0.01:
        special_items.append(pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20))

    for special_item in special_items:
        if player.rect.colliderect(special_item):
            special_items.remove(special_item)
            score += 50

    # Update monsters
    monster_y_speed = 5 * 0.0001 * score  # Adjust this value based on the desired speed
    for monster in monsters:
        monster.rect.y += int(monster_y_speed)  # Use constant speed in y-direction

        if monster.rect.top > height:
            monsters.remove(monster)

        if player.rect.colliderect(monster.rect):
            game_over = True

    for obstacle in obstacles:
        obstacle.y += int(obstacle_speed)
        if obstacle.top > height:
            obstacle.y = 0
            obstacle.x = random.randint(0, width - obstacle.width)

        if player.rect.colliderect(obstacle):
            game_over = True

    return score, game_over

def update_special_timer(special_timer):
    special_timer -= 1
    if special_timer <= 0:
        special_timer = 5.0
    return special_timer

def update_player_color(player, score):
    if score >= 500:
        color_mapping = [
            (500, (255, 125, 0)),
            (1000, (255, 255, 0)),
            (1500, (0, 255, 0)),
            (2000, (0, 125, 255)),
            (2500, (0, 0, 255))
        ]
        for threshold, rainbow_color in color_mapping:
            if score >= threshold:
                player.color = tuple(map(int, rainbow_color))
    return player

def update_monsters(monsters, game_over, score):
    monster_y_speed = 5 * 0.0001 * score  # Adjust this value based on the desired speed

    for monster in monsters:
        monster.rect.y += int(monster_y_speed)  # Use constant speed in y-direction

        if monster.rect.top > height:
            monsters.remove(monster)

    return game_over

def draw_game_screen(screen, player, items, special_items, monsters, obstacles, score, coin_image, monster_image):
    screen.fill((255, 255, 255))

    pygame.draw.rect(screen, player.color, player.rect)

    for item in items:
        pygame.draw.rect(screen, (0, 255, 0), item)

    for special_item in special_items:
        screen.blit(coin_image, special_item)

    for monster in monsters:
        screen.blit(monster_image, monster.rect)

    for obstacle in obstacles:
        pygame.draw.rect(screen, (255, 0, 0), obstacle)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()

def draw_game_over_screen(screen, width, height, game_over_text, restart_text, quit_text):
    font = pygame.font.Font(None, 72)
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2))

    font = pygame.font.Font(None, 36)
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, height // 2 + 100))

    pygame.display.flip()


def run_pygame():
    pygame.init()
    coin_image = pygame.image.load('coin.png')
    coin_image = pygame.transform.scale(coin_image, (20, 20))

    monster_image = pygame.image.load('monster.png')
    monster_image = pygame.transform.scale(monster_image, (30, 30))

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

    score = 0
    monsters = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over:
            handle_player_input(player, keys)
            score, game_over = update_items(player, items, special_items, monsters, obstacles, score, special_timer, obstacle_speed, game_over)

            if random.random() < 0.005 + 0.00002 * int(score):
                monsters.append(Monster(random.randint(0, width - 30), 0, 30, 30, random.randint(5, 9), random.uniform(-1.5, 1.5) * 2.0))

            special_timer = update_special_timer(special_timer)
            player = update_player_color(player, score)

        draw_game_screen(screen, player, items, special_items, monsters, obstacles, score, coin_image, monster_image)

        if game_over:
            game_over_text = pygame.font.Font(None, 72).render("Game Over", True, (255, 0, 0))
            restart_text = pygame.font.Font(None, 36).render("Press 'R' to restart", True, (0, 0, 0))
            quit_text = pygame.font.Font(None, 36).render("Press 'Q' to quit", True, (0, 0, 0))

            draw_game_over_screen(screen, width, height, game_over_text, restart_text, quit_text)

            if keys[K_r]:
                player = Player(width // 2 - 25, height - 60, 50, 50, (255, 0, 0))
                items = [pygame.Rect(random.randint(0, width - 20), random.randint(0, height - 20), 20, 20) for _ in range(10)]
                special_items = []
                obstacles = [pygame.Rect(random.randint(0, width - 30), random.randint(0, height - 30), 30, 30) for _ in range(5)]

                special_timer = 5.0
                obstacle_speed = 5.0
                game_over = False
                score = 0
                monsters = []
            elif keys[K_q]:
                pygame.quit()
                sys.exit()

        update_monsters(monsters, game_over, score)

        fps_clock.tick(fps)  # Removed dt from the tick call

if __name__ == "__main__":
    run_pygame()
