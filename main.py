import pygame
import sys
import random
from pygame.locals import *

pygame.init()

width = 600
height = 499
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")
game_image = {}
framespersec = 32
pipeimage = 'assets/pipe.jpeg'
backgroundimage = 'assets/bg.png'
birdimage = 'assets/spirit.png'
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)
game_image['bird'] = pygame.image.load(birdimage).convert_alpha()
game_image['background'] = pygame.image.load(backgroundimage).convert_alpha()
game_image['pipe'] = (
    pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
    pygame.image.load(pipeimage).convert_alpha(),
)
score_images = [pygame.image.load(f'assets/{i}.png').convert_alpha() for i in range(10)]
game_image['score'] = {str(i): score_images[i] for i in range(10)}

def frontScene():
    font = pygame.font.Font(None, 36)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_DELETE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return

        window.fill((255, 255, 255))

        title_text = font.render("Flappy Bird", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(width / 2, height / 3))
        window.blit(title_text, title_rect)

        instructions_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        instructions_rect = instructions_text.get_rect(center=(width / 2, height / 2))
        window.blit(instructions_text, instructions_rect)

        pygame.display.update()
        framespersec_clock.tick(framespersec)

def startGame():
    score = 0
    horizontal = int(width / 5)
    vertical = int((height - game_image['bird'].get_height()) / 2)

    first_pipe = createPipes()
    second_pipe = createPipes()

    down_pipe = [
        {'x': width + 300,
         'y': first_pipe[1]['y']},
        {'x': width + 300 + (width / 2),
         'y': second_pipe[1]['y']}
    ]

    up_pipe = [
        {'x': width + 300,
         'y': first_pipe[0]['y']},
        {'x': width + 200 + (width / 2),
         'y': second_pipe[0]['y']}
    ]

    pipeVelx = -4

    bird_speed = -9
    bird_max_speed = 10
    bird_acceleration = 1
    bird_flap_speed = -8
    bird_flapped = False
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_DELETE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE):
                if vertical > 0:
                    bird_speed = bird_flap_speed
                    bird_flapped = True

        lost = gameOver(horizontal, vertical, up_pipe, down_pipe)
        if lost:
            finalScreen(score)
            return

        if vertical >= height:
            playing = False

        playerMidPos = horizontal + game_image['bird'].get_width() / 2
        for pipe in up_pipe:
            pipeMidPos = pipe['x'] + game_image['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"You Scored {score} Points")
        if bird_speed < bird_max_speed and not bird_flapped:
            bird_speed += bird_acceleration
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_image['bird'].get_height()
        vertical += min(bird_speed, height - vertical)

        for upperpipe, lowerpipe in zip(up_pipe, down_pipe):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx

        if 0 < up_pipe[0]['x'] < 5:
            newpipe = createPipes()
            up_pipe.append(newpipe[0])
            down_pipe.append(newpipe[1])

        if up_pipe[0]['x'] < -game_image['pipe'][0].get_width():
            up_pipe.pop(0)
            down_pipe.pop(0)

        window.blit(game_image['background'], (0, 0))
        for upperpipe, lowerpipe in zip(up_pipe, down_pipe):
            window.blit(game_image['pipe'][0], (upperpipe['x'], upperpipe['y']))
            window.blit(game_image['pipe'][1], (lowerpipe['x'], lowerpipe['y']))
        window.blit(game_image['bird'], (horizontal, vertical))

        numbers = [int(x) for x in list(str(score))]
        widths = 0
        for num in numbers:
            widths += game_image['score'][str(num)].get_width()
        offset = (width - widths) / 1.1

        for num in numbers:
            window.blit(game_image['score'][str(num)], (offset, height * 0.02))
            offset += game_image['score'][str(num)].get_width()

        pygame.display.update()
        framespersec_clock.tick(framespersec)
        
def gameOver(horizontal, vertical, up_pipe, down_pipe):
    if vertical <= 0 or vertical >= height:
        return True
    for pipe in up_pipe:
        pipeheight = game_image['pipe'][0].get_height()
        if (vertical < pipeheight + pipe['y'] and abs(horizontal - pipe['x']) < game_image['pipe'][0].get_width()):
            return True
    for pipe in down_pipe:
        if (vertical + game_image['bird'].get_height() > pipe['y'] and abs(horizontal - pipe['x']) < game_image['pipe'][0].get_width()):
            return True
    return False

def finalScreen(score):
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_DELETE):
                pygame.quit()
                sys.exit()
            elif event.type == QUIT or (event.type == KEYDOWN and event.key == K_SPACE):
                startGame()
                return

        window.fill((255, 255, 255))

        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(width / 2, height / 3))
        window.blit(game_over_text, game_over_rect)

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(width / 2, height / 2))
        window.blit(score_text, score_rect)

        instructions_text = font.render("Press SPACE to Play Again", True, (0, 0, 0))
        instructions_rect = instructions_text.get_rect(center=(width / 2, 2 * height / 3))
        window.blit(instructions_text, instructions_rect)
        

        pygame.display.update()
        framespersec_clock.tick(framespersec)

def createPipes():
    offset = height / 3
    pipeheight = game_image['pipe'][0].get_height()
    
    gap_position = random.randint(0, int(height - 1.3 * offset))

    y1 = gap_position - pipeheight
    y2 = gap_position + offset

    pipeX = width + 10
    
    pipe = [
        {'x': pipeX, 'y': y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

framespersec_clock = pygame.time.Clock()

frontScene()

while True:
    horizontal = int(width / 5)
    vertical = int((height - game_image['bird'].get_height()) / 2)

    while True:
        startGame()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_DELETE):
                pygame.quit()
                sys.exit()
        else:
            window.blit(game_image['background'], (0, 0))
            window.blit(game_image['bird'], (horizontal, vertical))

        pygame.display.update()
        framespersec_clock.tick(framespersec)
