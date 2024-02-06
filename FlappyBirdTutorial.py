import pygame
import sys
import random


class FlappyBird(object):

    def __init__(self, gravity, jump_power, floor_speed, pipe_speed):
        pygame.init()
        self.gravity = gravity
        self.jump_power = jump_power
        self.floor_speed = floor_speed
        self.pipe_speed = pipe_speed

        self.screen = pygame.display.set_mode((288, 512))
        self.clock = pygame.time.Clock()

        self.background_surface = pygame.image.load("C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\"
                                                    "background-night.png").convert()
        self.floor_surface = pygame.image.load("C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\"
                                               "base.png").convert()
        self.floor_position = 0

        self.pipe_surface = pygame.image.load(
            "C:\\Users\\Thomas\\PycharmProjects\\FlappyBird\\assets\\images\\pipe-red.png").convert()

        self.pipe_heights = [400, 375, 350, 325, 300, 275, 250, 225, 200]
        self.pipes = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

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
        file = ''

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.SPAWNPIPE:
                    self.pipes.extend(self.create_pipe())
                if event.type == self.BIRDFLAP:
                    if self.bird_index < 2:
                        self.bird_index += 1
                    else:
                        self.bird_index = 0
                    print(self.bird_index)

            self.floor_position -= 1

            if self.floor_position <= -288:
                self.floor_position = 0

            self.screen.blit(self.background_surface, (0, 0))
            self.draw_floors()

            # Pipes
            self.pipes = self.move_pipes(self.pipes)
            self.draw_pipes(pipes=self.pipes)

            self.bird_surface = self.bird_frames[self.bird_index]
            self.screen.blit(self.bird_surface, self.bird_rect)

            pygame.display.update()
            self.clock.tick(120)

    def draw_floors(self):
        self.screen.blit(self.floor_surface, (self.floor_position, 450))
        self.screen.blit(self.floor_surface, (self.floor_position + 288, 450))

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
            if pipe.bottom > 450:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)


if __name__ == "__main__":
    Bird = FlappyBird(0, 0, 1, 2)
    Bird.main()
