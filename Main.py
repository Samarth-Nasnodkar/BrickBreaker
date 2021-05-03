#!/usr/bin/env python3

import pygame
import os
import random
from libs.Vectors import Vector2D


def mod(x):
    return x if x >= 0 else -1 * x


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.display.set_caption('Brick Breaker')
        self.icon = pygame.image.load('sprites/Icons/Icon.png')
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)
        self.width = 720
        self.height = 720
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.ballSprite = pygame.image.load('sprites/Bullets/ball.png')
        self.ballSprite = pygame.transform.scale(self.ballSprite, (30, 30))
        self.playerSprite = pygame.image.load('sprites/Player/main_player.png')
        self.playerSprite = pygame.transform.scale(
            self.playerSprite, (114, 30))
        self.playerPosition = Vector2D(self.width/2 - 57, self.height - 30)
        self.ballPosition = self.playerPosition + Vector2D(42, -30)
        self.ballLaunched = False
        self.ballVelocity = Vector2D(0, -1*self.height/60)
        self.playerVelocity = Vector2D(self.width/60, 0)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.blit(self.playerSprite, self.playerPosition.toTuple)
        self.screen.blit(self.ballSprite, self.ballPosition.toTuple)
        self.loadText(text='Press SPACE to start', coords=(
            self.width/3 - 10, self.height/2))
        self.brickWidth = 0
        self.brickHeight = 0
        self.running = True
        self.bricks = []
        self.generateBricks()
        while True:
            self.eventLoop()
            self.startNewSession()

    def generateBricks(self):
        sprites = os.listdir('sprites/Bricks/Mint')
        currentSprite = random.choice(sprites)
        brickSprite = pygame.image.load(f'sprites/Bricks/Mint/{currentSprite}')
        brokenSprite = pygame.image.load(
            f'sprites/Bricks/Broken/{currentSprite}')
        brickAspectRatio = brickSprite.get_height() / brickSprite.get_width()
        bricksPerLine = 7
        self.brickWidth, self.brickHeight = int(
            self.width / bricksPerLine), int(self.width * brickAspectRatio / bricksPerLine)
        brickSprite = pygame.transform.scale(
            brickSprite, (self.brickWidth, self.brickHeight))
        brokenSprite = pygame.transform.scale(
            brokenSprite, (self.brickWidth, self.brickHeight))
        current_width, current_height = 0, 0
        for i in range(3):
            current_width = 0
            for j in range(bricksPerLine):
                self.screen.blit(brickSprite, (current_width, current_height))
                brick = {
                    'position': (current_width, current_height),
                    'sprite': brickSprite,
                    'spriteName': currentSprite,
                    'broken': False,
                    'brokenSprite': brokenSprite
                }
                self.bricks.append(brick)
                current_width += self.brickWidth
                currentSprite = random.choice(sprites)
                brickSprite = pygame.image.load(
                    f'sprites/Bricks/Mint/{currentSprite}')
                brokenSprite = pygame.image.load(
                    f'sprites/Bricks/Broken/{currentSprite}')
                brickSprite = pygame.transform.scale(
                    brickSprite, (self.brickWidth, self.brickHeight))
                brokenSprite = pygame.transform.scale(
                    brokenSprite, (self.brickWidth, self.brickHeight))
            current_height += self.brickHeight
        pygame.display.update()

    def refresh(self):
        self.screen.fill((0, 0, 0))
        for brick in self.bricks:
            if not brick['broken']:
                self.screen.blit(brick['sprite'], brick['position'])
            else:
                self.screen.blit(brick['brokenSprite'], brick['position'])

        if not self.ballLaunched:
            self.loadText(text='Press SPACE to start',
                          coords=(self.width/3 - 10, self.height/2))
        self.screen.blit(self.playerSprite, self.playerPosition.toTuple)
        self.screen.blit(self.ballSprite, self.ballPosition.toTuple)
        pygame.display.update()

    def startNewSession(self):
        self.bricks = []
        self.playerPosition = Vector2D(self.width/2 - 57, self.height - 30)
        self.ballPosition = self.playerPosition + Vector2D(42, -30)
        self.ballLaunched = False
        self.ballVelocity = Vector2D(0, -1*self.height/60)
        self.running = True
        self.generateBricks()
        self.refresh()

    def loadText(self, text: str, coords: tuple = None):
        if coords is None:
            coords = (self.width/2, self.height/2)
        Text = self.font.render(text, False, (255, 255, 255))
        self.screen.blit(Text, coords)

    def eventLoop(self):
        keep_updating = False
        update_vel = Vector2D(0, 0)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        update_vel = self.playerVelocity
                        keep_updating = True
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        update_vel = self.playerVelocity * -1
                        keep_updating = True
                    elif event.key == pygame.K_SPACE:
                        if not self.ballLaunched:
                            self.ballVelocity += update_vel
                            self.ballLaunched = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        keep_updating = False
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        keep_updating = False

            if keep_updating or self.ballLaunched:
                if keep_updating:
                    self.playerPosition += update_vel
                    if self.playerPosition.x >= self.width - 114:
                        self.playerPosition.x = self.width - 114
                    if self.playerPosition.x <= 0:
                        self.playerPosition.x = 0
                if not self.ballLaunched:
                    self.ballPosition = Vector2D(
                        self.playerPosition.x + 42, self.playerPosition.y - 30)
                else:
                    if mod(self.ballVelocity.x) >= self.width/60:
                        self.ballVelocity.x = self.width / \
                            60 if self.ballVelocity.x > 0 else -1 * self.width/60
                    self.ballPosition += self.ballVelocity
                    if self.ballPosition.x >= self.width - 30 or self.ballPosition.x <= 0:
                        self.ballVelocity.x *= -1
                        if self.ballPosition.x >= self.width - 30:
                            self.ballPosition.x = self.width - 30
                        else:
                            self.ballPosition.x = 0
                    if self.height >= self.ballPosition.y >= self.height - 60 and self.playerPosition.x <= self.ballPosition.x + 15 <= self.playerPosition.x + 114:
                        self.ballVelocity.y *= -1
                        self.ballVelocity.x += update_vel.x
                    if self.ballPosition.y <= 0:
                        self.ballVelocity.y *= -1
                    else:
                        for i in range(len(self.bricks)):
                            brickPos = self.bricks[i]['position']
                            if brickPos[0] <= self.ballPosition.x + 15 <= brickPos[0] + self.brickWidth and self.ballPosition.y <= brickPos[1] + self.brickHeight:
                                self.ballVelocity.y *= -1
                                if self.bricks[i]['broken']:
                                    self.bricks.pop(i)
                                else:
                                    self.bricks[i]['broken'] = True

                                break

                self.refresh()

            if self.ballPosition.y >= self.height - 15:
                self.running = False
            self.clock.tick(self.fps)


game = Game()
