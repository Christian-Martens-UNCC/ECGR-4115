import pygame.math
import pygame_screen_recorder
import sys
import numpy
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.finder.breadth_first import BreadthFirstFinder
from pathfinding.finder.dijkstra import DijkstraFinder
from pygame.math import Vector2
from settings import *
import time
import random
import csv

class Fruit:
    def __init__(self):
        self.x = 2
        self.y = 2
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self, screen):
        fruit_circ = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.ellipse(screen, (255, 0, 0), fruit_circ)

class Snake:
    def __init__(self):
        self.body = [Vector2(0, 0), Vector2(1, 0), Vector2(2, 0)]
        self.direction = Vector2(1, 0)
        self.add_block = False
        self.text_font = pygame.font.SysFont("calibri", FONT_SIZE)

    def draw_snake(self, screen):
        for n, block in enumerate(self.body):
            snake_rect = pygame.Rect(int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            if block != self.body[-1]:
                pygame.draw.rect(screen, (0, 175, 0), snake_rect)
            else:
                pygame.draw.rect(screen, (0, 255, 0), snake_rect)
            # /// used for debugging/checking snake size easily
            # text_x = int(block.x * CELL_SIZE)
            # text_y = int(block.y * CELL_SIZE)
            # text_surface = self.text_font.render(str(n+1), True, (255, 100, 0))
            # text_rect = text_surface.get_rect(topleft=(text_x, text_y))
            # screen.blit(text_surface, text_rect)

    def move_snake(self):
        body_copy = self.body[:]
        if self.add_block:
            self.body.append(self.body[-1] + self.direction)
            self.add_block = False
        else:
            for i in range(len(body_copy)-1):
                body_copy[i] = self.body[i + 1]
            body_copy[-1] = self.body[-1] + self.direction
            self.body = body_copy[:]

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.text_font = pygame.font.SysFont("calibri", FONT_SIZE)
        self.path_chosen = True
        self.follow_tail = False
        self.path = []
        self.path_moves = 0
        self.total_moves = 0
        self.attempt_moves = 0
        self.timer = 0
        self.phantom_fruit = Vector2(0, 0)
        self.restart_count = 1
        self.master_csv = open(DATASET_18, 'a', newline='')
        self.csv_writer = csv.writer(self.master_csv)
        self.data = []

    def update(self):
        if ALGO_PICK == 0:
            self.a_star_algo()
        elif ALGO_PICK == 1:
            self.bfs_algo()
        elif ALGO_PICK == 2:
            self.dij_algo()
        if self.path_chosen:
            self.total_moves += 1
            self.attempt_moves += 1
            self.path_moves += 1
            self.snake.direction = Vector2(self.path[1]) - Vector2(self.path[0])
            self.snake.move_snake()
            self.eat_fruit_check()
            self.check_fail()

    def a_star_algo(self):
        self.path_chosen = True
        s, e, g = self.create_matrix()
        self.path, t = self.a_star(s, e, g)
        self.timer += t
        if self.path == []:
            s, e, g = self.create_tail_mat()
            self.path, self.timer = self.a_star(s, e, g)
            self.phantom_fruit = Vector2(self.snake.body[0])
            if self.path == []:
                self.restart()
                self.path_chosen = False

    def bfs_algo(self):
        self.path_chosen = True
        s, e, g = self.create_matrix()
        self.path, t = self.bfs(s, e, g)
        self.timer += t
        if self.path == []:
            s, e, g = self.create_tail_mat()
            self.path, self.timer = self.bfs(s, e, g)
            self.phantom_fruit = Vector2(self.snake.body[0])
            if self.path == []:
                self.restart()
                self.path_chosen = False

    def dij_algo(self):
        self.path_chosen = True
        s, e, g = self.create_matrix()
        self.path, t = self.dijkstra(s, e, g)
        self.timer += t
        if self.path == []:
            s, e, g = self.create_tail_mat()
            self.path, self.timer = self.dijkstra(s, e, g)
            self.phantom_fruit = Vector2(self.snake.body[0])
            if self.path == []:
                self.restart()
                self.path_chosen = False

    def draw_elem(self, screen):
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake(screen)
        self.draw_info(screen)

    def create_matrix(self):
        matrix = numpy.ones([CELL_NUMBER + 2, CELL_NUMBER + 2]) # Creates a grid with a space for boundaries
        for n in range(CELL_NUMBER + 2):
            for m in range(CELL_NUMBER + 2):
                if n == 0 or n == CELL_NUMBER + 1:
                    matrix[n][m] = 0
                elif m == 0 or m == CELL_NUMBER + 1:
                    matrix[n][m] = 0
        for block in self.snake.body[:-1]:
            matrix[int(block.y + 1)][int(block.x + 1)] = 0
        grid = Grid(matrix=matrix)
        start_vec = self.snake.body[-1] + Vector2(1, 1)
        end_vec = self.fruit.pos + Vector2(1, 1)
        start_loc = grid.node(int(start_vec.x), int(start_vec.y))
        end_loc = grid.node(int(end_vec.x), int(end_vec.y))
        return start_loc, end_loc, grid

    def create_tail_mat(self):
        matrix = numpy.ones([CELL_NUMBER + 2, CELL_NUMBER + 2]) # Creates a grid with a space for boundaries
        for n in range(CELL_NUMBER + 2):
            for m in range(CELL_NUMBER + 2):
                if n == 0 or n == CELL_NUMBER + 1:
                    matrix[n][m] = 0
                elif m == 0 or m == CELL_NUMBER + 1:
                    matrix[n][m] = 0
        for block in self.snake.body[1:-1]:
            matrix[int(block.y + 1)][int(block.x + 1)] = 0
        grid = Grid(matrix=matrix)
        start_vec = self.snake.body[-1] + Vector2(1, 1)
        end_vec = self.snake.body[0] + Vector2(1, 1)
        start_loc = grid.node(int(start_vec.x), int(start_vec.y))
        end_loc = grid.node(int(end_vec.x), int(end_vec.y))
        return start_loc, end_loc, grid

    def a_star(self, start_loc, end_loc, grid):
        finder = AStarFinder()
        tic = time.perf_counter()
        path, _ = finder.find_path(start_loc, end_loc, grid)
        toc = time.perf_counter()
        return path, round(toc - tic, 5)

    def bfs(self, start_loc, end_loc, grid):
        finder = BreadthFirstFinder()
        tic = time.perf_counter()
        path, _ = finder.find_path(start_loc, end_loc, grid)
        toc = time.perf_counter()
        return path, round(toc - tic, 5)

    def dijkstra(self, start_loc, end_loc, grid):
        finder = DijkstraFinder()
        tic = time.perf_counter()
        path, _ = finder.find_path(start_loc, end_loc, grid)
        toc = time.perf_counter()
        return path, round(toc - tic, 5)

    def eat_fruit_check(self):
        if self.fruit.pos == self.snake.body[-1]:
            self.path_chosen = False
            fruit_placement = False
            self.path_moves = 0
            if WRITING_CSV:
                self.data.append([self.restart_count, ALGO_NAMES[ALGO_PICK],
                                              len(self.snake.body), self.timer])
            self.timer = 0
            while not fruit_placement:
                self.fruit.x = random.randint(0, CELL_NUMBER - 1)
                self.fruit.y = random.randint(0, CELL_NUMBER - 1)
                self.fruit.pos = Vector2(self.fruit.x, self.fruit.y)
                if self.fruit.pos not in self.snake.body[:]:
                    fruit_placement = True
            self.snake.add_block = True

    def game_over(self):
        if WRITING_CSV:
            self.csv_writer.writerows(self.data)
            self.master_csv.close()
        pygame.quit()
        sys.exit()

    def restart(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.path_chosen = False
        self.follow_tail = False
        self.phantom_fruit = Vector2(0, 0)
        self.attempt_moves = 0
        self.restart_count += 1

    def check_fail(self):
        if not 0 <= self.snake.body[-1].x < CELL_NUMBER or not 0 <= self.snake.body[-1].y < CELL_NUMBER:
            self.restart()
        if self.snake.body[-1] in self.snake.body[:-2]:
            self.restart()

    def draw_info(self, screen):
        snake_len = len(self.snake.body)
        info_surface_1 = self.text_font.render(
            f"Algorithm = {ALGO_NAMES[ALGO_PICK]}, Length = {str(snake_len)}, Attempt = {str(self.restart_count)}, "
            f"Time = {str(round(self.timer, 6))}",
            True, (255, 255, 255))
        info_surface_2 = self.text_font.render(
            f"Total Moves = {str(self.total_moves)}, "
            f"Moves this Attempt = {str(self.attempt_moves)} "
            f"Move this Fruit = {str(self.path_moves)}",
            True, (255, 255, 255))

        info_x = 10
        info_y_1 = int(CELL_NUMBER * CELL_SIZE + 5)
        info_y_2 = int(CELL_NUMBER * CELL_SIZE + 15 + FONT_SIZE)
        info_rect_1 = info_surface_1.get_rect(topleft=(info_x, info_y_1))
        info_rect_2 = info_surface_2.get_rect(topleft=(info_x, info_y_2))
        screen.blit(info_surface_1, info_rect_1)
        screen.blit(info_surface_2, info_rect_2)

    def data_to_csv(self):
        self.data = self.data.append([self.restart_count, ALGO_NAMES[ALGO_PICK], len(self.snake.body), 1])