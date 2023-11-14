from ntpath import join
from turtle import Screen
import pygame as pyg
from pygame.locals import *
from pygame import mixer
import random
from tkinter import *
from utlis import Calibrate as cam
from Ml import Object
import cv2
import numpy as np
import time

fps = 60
pyg.init()
pyg.display.set_caption("GolTrainer")
mixer.init()
mixer.music.load("resources/backgroundMusic.mp3")
mixer.music.play(loops=-1)
mixer.music.set_volume(0.1)


info = pyg.display.Info()
print(info)
display = Tk()
targetWidth, targetHeight = 150, 150
winInWidth, winInHeight = (
    display.winfo_screenwidth() - 200,
    display.winfo_screenheight() - 200,
)
postWidth, postHeight = 400, 130
window = pyg.display.set_mode((winInWidth, winInHeight), pyg.RESIZABLE)
background = pyg.image.load(join("resources", "background2.jpeg")).convert()
background = pyg.transform.smoothscale(background, window.get_size())
targetImg = pyg.image.load(join("resources", "png-image.png")).convert_alpha()
targetImg = pyg.transform.scale(targetImg, [targetWidth, targetHeight])
postImg = pyg.image.load(join("resources", "football_goal_PNG10.png")).convert_alpha()
highscore = 0
startGame = True
stop_game = False


def display_text(text, window, x, y, size=36, color=(0, 0, 0)):
    font = pyg.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)


class Target:
    def __init__(self, window, img, post):
        self.post = post
        self.window = window
        self.img = img
        self.width = targetWidth
        self.height = targetHeight
        self.x = random.randrange(
            int(self.post.posX), int(self.post.width + self.post.posX - self.width - 50)
        )
        self.y = random.randrange(
            int(self.post.posY),
            int(self.post.height + self.post.posY - self.height - 50),
        )
        self.rect = pyg.Rect(self.x, self.y, self.width, self.height)
        self.score = 0

    def draw(self):
        self.window.blit(self.img, self.rect)
        score = "Score : " + str(self.score)
        display_text(score, self.window, 150, 100, 56, (255, 255, 255))
        print(self.score)

    def update(self, hit):
        if hit:
            self.x = random.randrange(
                int(self.post.posX + 50),
                int(self.post.width + self.post.posX - self.width - 50),
            )
            self.y = random.randrange(
                int(self.post.posY + 50),
                int(self.post.height + self.post.posY - self.height - 50),
            )
            self.rect = pyg.Rect(self.x, self.y, self.width, self.height)
            self.score += 1
        else:
            pass


class Post:
    def __init__(self, window, img):
        self.window = window
        self.height = (self.window.get_height() * 0.5) + postHeight
        self.width = (self.window.get_width() * 0.5) + postWidth
        self.posX = (self.window.get_width() - self.width) / 2
        self.posY = (self.window.get_height() - self.height) - 100
        self.rect = pyg.Rect(self.posX, self.posY, self.width, self.height)
        self.img = img

    def update(self):
        self.posX = (self.window.get_width() - self.width) / 2
        self.posY = (self.window.get_height() - self.height) - 100
        self.height = (self.window.get_height() * 0.5) + postHeight
        self.width = (self.window.get_width() * 0.5) + postWidth
        self.rect = pyg.Rect(self.posX, self.posY, self.width, self.height)
        self.img = pyg.transform.smoothscale(self.img, [self.width, self.height])

    def draw(self):
        self.window.blit(self.img, self.rect)


class lifeSystem:
    def __init__(self, window):
        self.window = window
        self.hartimg = pyg.image.load(
            join("resources", "png-image.png")
        ).convert_alpha()

    def draw(self, x, y):
        rect = pyg.Rect(x, y, 1, 1)
        self.hartimg = pyg.transform.scale(self.hartimg, (50, 50))
        # self.window.blit(self.hartimg, rect)


class GameEngine:
    def __init__(self, window):
        self.window = window
        self.post = Post(self.window, postImg)
        self.cam = 0
        self.hit = False
        self.target = Target(self.window, targetImg, self.post)
        self.list = [lifeSystem(window), lifeSystem(window), lifeSystem(window)]
        self.camera = cam(0, 0, self.cam, "object")
        self.camera.setup()
        self.model_path = "resources/model.tflite"
        self.ball = Object(self.model_path, 0.5)
        # self.start_time = 0
        self.delay_duration = 100000

    def upddate(self):
        global highscore, stop_game
        self.camera.loop()
        self.post.update()
        self.start_time = pyg.time.get_ticks()
        if not self.camera.is_selecting:
            frame = self.camera.imageWarped
            height, width, channel = frame.shape
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ballX, ballY, width_b, height_h, image = self.ball.Track_Objecte(frame)

            mapedX = np.interp(ballX, (0, width), (0, self.window.get_width()))
            mapedY = np.interp(ballY, (0, height), (0, self.window.get_height()))

            ball = pyg.Rect(mapedX, mapedY,width_b,height_h)

            # print(self.target.rect.colliderect(ball))


                # self.target.rect.collidepoint(
                #     mapedX + (self.target.width / 4) + 20,
                #     mapedY + (self.target.height / 4) + 20,
                # )





            if ( self.target.rect.colliderect(ball)
                and stop_game != True
            ):
                if not self.hit:
                    self.start_time = pyg.time.get_ticks()
                    self.hit = True
                self.target.update(True)

            else:
                self.hit = False

            # else:
            #     self.target.update(False)
            #     if len(self.list) > 0 and stop_game != True:
            #         # self.list.remove(self.list[len(self.list) - 1])
            #         #
            #         previous = self.target.score
            #         if previous >= highscore:
            #             highscore = self.target.score
            #             self.target.score = 0

            cv2.imshow("Custom Object Detection", image)

    def render(self):
        global highscore, startGame, stop_game
        bgImg = pyg.transform.smoothscale(background, window.get_size())
        self.window.blit(bgImg, [0, 0])
        highs = "High Score : " + str(highscore)
        display_text(
            highs, window, (window.get_width() - 200), 100, 56, (255, 255, 255)
        )

        if self.hit:
            current_time = pyg.time.get_ticks()
            elapsed_time = current_time - self.start_time

            if elapsed_time < self.delay_duration:
                display_text(
                    "Goal!!",
                    window,
                    (window.get_width() / 2),
                    (window.get_height() / 2),
                    200,
                    (0, 255, 0),
                )

            else:
                self.hit = False

        for index in range(len(self.list)):
            self.list[index].draw((index * 60) + window.get_width() - 300, 20)

        self.post.draw()
        self.target.draw()

        if len(self.list) == 0:
            previous = self.target.score
            if previous >= highscore:
                highscore = self.target.score
            game_over = "Game Over"
            display_text(
                game_over,
                self.window,
                (self.window.get_width() / 2),
                (self.window.get_height() / 2),
                100,
                (255, 0, 0),
            )
            stop_game = True
            self.target.score = 0
        pyg.display.update()


def main(window):
    clock = pyg.time.Clock()
    global highscore, startGame, stop_game
    game = GameEngine(window)
    while startGame:
        clock.tick(fps)
        print(fps)
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                startGame = False
                break

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_ESCAPE:
                    game.list = [
                        lifeSystem(window),
                        lifeSystem(window),
                        lifeSystem(window),
                    ]
                    stop_game = False
                    previous = game.target.score
                    if previous >= highscore:
                        highscore = game.target.score
                    game.target.score = 0

                if event.key == pyg.K_SPACE and game.target.score != 0:
                    game.target.score -= 1

        game.upddate()
        game.render()
        # print(stop_game)
    game.camera.cap.release()
    cv2.destroyAllWindows()
    pyg.display.flip()
    pyg.quit()
    quit()


if __name__ == "__main__":
    main(window)
