import pygame
import sys
import random
import cv2
import numpy as np
import PIL.Image as Image


class FlappyBird(object):

    def __init__(self, gravity, jump_power, floor_speed, pipe_speed):
        pygame.init()
        self.gravity = gravity
        self.jump_power = jump_power
        self.floor_speed = floor_speed
        self.pipe_speed = pipe_speed

        self.screen = pygame.display.set_mode((288, 512))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.bird_movement = 0
        self.game_active = True
        self.score = 0
        self.high_score = 0

        self.background_surface = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                                    'background-day.png').convert()

        self.floor_surface = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                               'base.png').convert()
        self.floor_x_position = 0

        self.bird_downflap = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                               'yellowbird-downflap.png').convert_alpha()
        self.bird_midflap = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                              'yellowbird-midflap.png').convert_alpha()
        self.bird_upflap = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                             'yellowbird-upflap.png').convert_alpha()
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(50, 256))
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)

        self.pipe_surface = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                              'pipe-green.png').convert()
        self.pipes = []
        self.pipe_heights = [400, 375, 350, 325, 300, 275, 250, 225, 200]
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

        self.game_over_message = pygame.image.load('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\'
                                                   'message.png').convert_alpha()
        self.game_over_rect = self.game_over_message.get_rect(center=(144, 256))

        self.flap_sound = pygame.mixer.Sound('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\audio\\wing.wav')
        self.death_sound = pygame.mixer.Sound('C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\audio\\hit.wav')
        self.score_sound = pygame.mixer.Sound(
            'C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\audio\\point.wav')
        self.score_sound_countdown = 200

        self.JUMP = pygame.USEREVENT + 2
        self.JUMPEVENT = pygame.event.Event(self.JUMP)

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird_movement = 0
                        self.bird_movement -= self.jump_power
                        self.flap_sound.play()
                    if event.key == pygame.K_SPACE and self.game_active is False:
                        self.reset()

                if event.type == self.SPAWNPIPE:
                    self.pipes.extend(self.create_pipe())
                if event.type == self.BIRDFLAP:
                    if self.bird_index < 2:
                        self.bird_index += 1
                    else:
                        self.bird_index = 0
                    self.bird_surface, self.bird_rect = self.bird_animation()

                if event.type == self.JUMP and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= self.jump_power
                    self.flap_sound.play()

                if self.check_bounds() is False or self.check_collision(self.pipes) is False:
                    self.game_active = False
                    self.pipes.clear()
                    self.death_sound.play()

            self.floor_x_position -= self.floor_speed

            self.screen.blit(self.background_surface, (0, 0))

            self.draw_floor()

            if self.game_active is True:
                # Bird
                self.bird_movement += self.gravity
                rotated_bird = self.rotate_bird(self.bird_surface)

                self.bird_rect.centery += self.bird_movement
                self.screen.blit(rotated_bird, self.bird_rect)

                # Pipes
                self.pipes = self.move_pipes(self.pipes)
                self.draw_pipes(pipes=self.pipes)

                self.score += 0.005
                self.score_display('main_game')
                self.score_sound_countdown -= 1
                if self.score_sound_countdown <= 0:
                    self.score_sound.play()
                    self.score_sound_countdown = 200
            else:
                self.screen.blit(self.game_over_message, self.game_over_rect)
                self.high_score = self.update_high_score()
                self.score_display('game_over')

            if self.floor_x_position <= -288:
                self.floor_x_position = 0

            pygame.display.update()
            self.clock.tick(120)

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_x_position, 450))
        self.screen.blit(self.floor_surface, (self.floor_x_position + 288, 450))

    def create_pipe(self):
        random_pipe_height = random.choice(self.pipe_heights)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(300, random_pipe_height))
        top_pipe = self.pipe_surface.get_rect(midbottom=(300, random_pipe_height - 175))
        return bottom_pipe, top_pipe

    def move_pipes(self, pipes):
        for pipe in pipes:
            pipe.centerx -= self.pipe_speed
        return pipes

    def draw_pipes(self, pipes):
        for pipe in pipes:
            if pipe.bottom >= 450:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def check_collision(self, pipes):
        flag = self.bird_rect.collidelist(pipes)
        if flag != -1:
            return False

    def check_bounds(self):
        if self.bird_rect.centery <= 0 or self.bird_rect.centery >= 512:
            return False

    def rotate_bird(self, bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 6, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(50, self.bird_rect.centery))
        return new_bird, new_bird_rect

    def score_display(self, game_state):
        if game_state == "main_game":
            score_surface = self.game_font.render(f"{str(int(self.score))}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(144, 50))
            self.screen.blit(score_surface, score_rect)
        if game_state == "game_over":
            score_surface = self.game_font.render(f"Score: {str(int(self.score))}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(144, 50))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f"High Score: {str(int(self.high_score))}", True,
                                                       (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(144, 430))
            self.screen.blit(high_score_surface, high_score_rect)

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
        return self.high_score

    def get_reward(self):
        return self.score

    def get_state(self):
        s = self.screen
        s.blit(self.rotate_bird(self.bird_surface), self.bird_rect)

        for pipe in self.pipes:
            if pipe.bottom >= 450:
                s.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                s.blit(flip_pipe, pipe)

        a = pygame.surfarray.array3d(s)
        na = np.fliplr(a)
        na = np.rot90(na)
        image = Image.fromarray(na)
        return image

    def reset(self):
        self.game_active = True
        self.score = 0
        self.high_score = 0
        self.bird_movement = 0
        self.score_sound_countdown = 200
        self.pipes.clear()
        self.bird_rect.center = (50, 256)
        self.screen.blit(self.bird_surface, self.bird_rect)

        return self.get_state()

    def step(self, action):
        if action == 1:
            pygame.event.post(self.JUMPEVENT)
        else:
            pass
        return self.get_state(), self.score, self.game_active


if __name__ == '__main__':
    Client = FlappyBird(gravity=0.075, jump_power=3.5, pipe_speed=2, floor_speed=1)
    Client.main()
