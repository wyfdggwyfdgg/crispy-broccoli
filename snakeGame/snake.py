 #-*- coding: utf-8 -*-
"""
Created on Thu Jun 15 18:39:38 2023

@author: 25626
"""

import pygame
import sys
import random
from pygame.locals import *
import os

 # 初始化 pygame 库
pygame.init()         

#导入背景音乐                   
pygame.mixer.music.load(os.path.join( "background_music.mp3"))
pygame.mixer.music.play(-1)

def game():
    # 初始化
    #pygame.init()

    # 设置游戏窗口大小
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('贪吃蛇游戏')
    
    # 加载资源文件
    bg_image = pygame.image.load('background.png')
    snake_body_img = pygame.image.load('snake_head.png')
    food_img = pygame.image.load('food.png')
    font = pygame.font.Font(None, 28)

    # 控制游戏帧率
    fps = pygame.time.Clock()

    # 定义重新开始和退出游戏的函数
    def game_over(score):
        # 在游戏结束时，显示Game Over文字和分数提示
        font_large = pygame.font.Font(None, 48)
        text_game_over = font_large.render('Game Over', True, (0, 0, 0))
        text_game_over_rect = text_game_over.get_rect()
        text_game_over_rect.center = (screen_width // 2, screen_height // 2 - 20)
        screen.blit(bg_image, (0, 0))
        screen.blit(text_game_over, text_game_over_rect)

        # 提示重新开始或退出游戏操作
        text_restart = font.render('R: restart  Q: quit', True, (0, 0, 0))
        text_restart_rect = text_restart.get_rect()
        text_restart_rect.center = (screen_width // 2, screen_height // 2 + 30)
        screen.blit(text_restart, text_restart_rect)
        
        # 显示最后得分
        text_score = font.render(f'Scores: {score}', True, (0, 0, 0))
        text_score_rect = text_score.get_rect()
        text_score_rect.center = (screen_width // 2, screen_height // 2 + 80)
        screen.blit(text_score, text_score_rect)

        pygame.display.flip()

         # 检测用户输入操作以重新开始或退出游戏
        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_q or event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_r:
                    game()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

    # 初始蛇位置
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    score = 0  # 记录得分
    
    def generate_food_pos():
        return [random.randrange(1, screen_width // 10) * 10, random.randrange(1, screen_height // 10) * 10]

    # 初始食物位置
    food_pos = generate_food_pos()

    # 游戏主循环
    while True:
        # 监听用户输入操作
        for event in pygame.event.get():
            if event.type == QUIT: # 退出游戏
                pygame.quit()
                sys.exit()

            # 检测方向键
            if event.type == KEYDOWN:
                if event.key == K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # 更新蛇头位置
        if direction == "UP":
            snake_pos[1] -= 10
        elif direction == "DOWN":
            snake_pos[1] += 10
        elif direction == "LEFT":
            snake_pos[0] -= 10
        elif direction == "RIGHT":
            snake_pos[0] += 10

        # 更新蛇的位置
        snake_body.insert(0, list(snake_pos))

         # 绘制游戏画面
        screen.blit(bg_image, (0, 0))
        for pos in snake_body:
            screen.blit(snake_body_img, (pos[0], pos[1]))

        screen.blit(food_img, (food_pos[0], food_pos[1]))

          # 处理蛇吃到食物的情况
        if snake_pos == food_pos:
            score += 10
            food_pos = generate_food_pos()# 重新生成食
        else:
            snake_body.pop()# 移除蛇尾

        # 显示分数
        text_score = font.render(f'Scores: {score}', True, (0, 0, 0))
        screen.blit(text_score, (10, 10))
        pygame.display.flip()

        # 判断蛇是否撞墙
        if not 0 <= snake_pos[0] < screen_width or not 0 <= snake_pos[1] < screen_height:
            game_over(score)

        # 判断蛇是否撞到自己
        for section in snake_body[1:]:
            if section == snake_pos:
                game_over(score)
           # 控制帧率
        fps.tick(15)

# 运行游戏
game()