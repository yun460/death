import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)


class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        # ============================================
        # TODO: Implement an event when block collides with a ball
        pass
        

class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        for block in blocks:
            if self.rect.colliderect(block.rect) and block.alive:
                # 블록의 collide() 호출하여 처리
                block.collide()
                block.alive = False

                # 충돌 방향 계산
                if (
                    abs(self.rect.bottom - block.rect.top) <= self.speed
                    or abs(self.rect.top - block.rect.bottom) <= self.speed
                ):
                    # 위아래 충돌 시 Y축 방향 반전
                    self.dir = 360 - self.dir
                elif (
                    abs(self.rect.right - block.rect.left) <= self.speed
                    or abs(self.rect.left - block.rect.right) <= self.speed
                ):
                    # 좌우 충돌 시 X축 방향 반전
                    self.dir = 180 - self.dir

                # 블록 하나와 충돌한 후에는 종료
                break

    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        # 좌우 벽 충돌: X축 진행 방향 반전
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir

        # 상단 벽 충돌: Y축 진행 방향 반전
        if self.rect.top <= 0:
            self.dir = 360 - self.dir
     
        
    
    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        #공이 화면 아래로 떨어졌는지 확인.
        #아래로 빠지면 False를 반환하고, 살아 있으면 True를 반환.
        if self.rect.top > config.display_dimension[1]:
            return False  # 공이 화면 아래로 떨어졌다면 False 반환
        return True  