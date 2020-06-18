import pygame as pg
import random
import os

pg.init()
pg.mixer.init()
clock = pg.time.Clock()

# Colors
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 50)
orange = (255, 140, 0)
cyan = (0, 255, 200)
blue = (0, 50, 255)

# Define Resolution and create window
screen_width = 900
screen_height = 600
gameWindow = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Snakes With Saptarshi')
pg.display.update()
font = pg.font.SysFont('gabriola', 40)
font2 = pg.font.SysFont('Sans', 16)

# Background Image
bgimg1 = pg.image.load('snk.jpg')
bgimg1 = pg.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

bgimg2 = pg.image.load('bg.jpg')
bgimg2 = pg.transform.scale(bgimg2, (screen_width, screen_height)).convert_alpha()


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def text_screen1(text, color, x, y):
    screen_text = font2.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snake_list, snake_size):
    for x, y in snake_list:
        pg.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    if not os.path.exists("highscore"):
        with open("highscore", "w") as f:
            f.write("0")
    sound = pg.mixer.Sound("sound\\explosion1.ogg")
    sound.play()
    exit_game = False
    with open("highscore", "r") as f:
        hs = f.read()
    while not exit_game:
        gameWindow.fill(yellow)
        gameWindow.blit(bgimg1, (0, 0))
        text_screen1("© Saptarshi Roy", cyan, 20, 20)
        text_screen("Welcome to Snake!", blue, 350, 220)
        text_screen("Press SpaceBar to Play...", red, 330, 260)
        text_screen("Your Highest Score: " + hs, black, 330, 300)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    gameloop()
        pg.display.update()
        clock.tick(60)


def gameloop():
    music = pg.mixer.Sound("sound\\snake.ogg")
    music.play(loops=-1)
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 12
    food_size = 12
    fps = 60
    velocity_x = 0
    velocity_y = 0
    food_x = random.randint(0, screen_width / 2)
    food_y = random.randint(0, screen_height / 2)
    score = 0
    init_vel = 4
    snake_list = []
    snake_length = 1
    with open('highscore', "r") as f:
        hs = int(f.read())
    while not exit_game:
        if game_over:
            with open("highscore", "w") as f:
                f.write(str(hs))
            gameWindow.fill(orange)
            text_screen("Game Over! Press Enter to Continue.", green, 250, 220)
            text_screen("Your Final Score: " + str(score * 10), red, 340, 260)
            text_screen("Your Highest Score: " + str(hs), yellow, 330, 300)
            text_screen("Press 'Q' to Reset Highscore", black, 310, 340)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        fl.stop()
                        gameloop()
                    if event.key == pg.K_q:
                        hs = str(0)
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        velocity_x = init_vel
                        velocity_y = 0
                    if event.key == pg.K_LEFT:
                        velocity_x = -init_vel
                        velocity_y = 0
                    if event.key == pg.K_UP:
                        velocity_y = -init_vel
                        velocity_x = 0
                    if event.key == pg.K_DOWN:
                        velocity_y = init_vel
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 1
                food_x = random.randint(0, screen_width / 2)
                food_y = random.randint(0, screen_height / 2)
                snake_length += 5
                if score * 10 > hs:
                    hs = score * 10

            gameWindow.fill(blue)
            gameWindow.blit(bgimg2, (0, 0))
            text_screen("Score: " + str(score * 10) + " | Highscore: " + str(hs), green, 5, 5)
            pg.draw.rect(gameWindow, yellow, [food_x, food_y, food_size, food_size])

            head = list()
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                music.stop()
                fl = pg.mixer.Sound("sound\\over.ogg")
                fl.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                music.stop()
                fl = pg.mixer.Sound("sound\\over.ogg")
                fl.play()

            plot_snake(gameWindow, red, snake_list, snake_size)
        pg.display.update()
        clock.tick(fps)
    pg.quit()
    os._exit(1)


welcome()
