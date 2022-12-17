import pygame

# Parameters
CELL_SIZE = 35 # number of pixels each side of the cell is
CELL_NUMBER = 18 # number of cells each side of the game screen is, must be >= 5
FRAMERATE = 60 # number of frames per second the game screen updates at
CALC_TIME = 10 # number of milliseconds the game will wait between updates for.
FONT_SIZE = 20 # font size of the text
ALGO_PICK = 3 # 0: A* Algorithm, 1: BFS Algorithm, 2: Dijkstra Algorithm, 3: Mixed System
ACC_CONST = 0.8 # Desired Minimum Accuracy
WRITING_CSV = False # Allows for writing new data to the datasheet

# Constants
SCREEN_UPDATE = pygame.USEREVENT
ALGO_NAMES = ["A*", "BFS", "Dijkstra", "Mixed"]
DATASET_6 = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_6.csv"
DATASET_9 = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_9.csv"
DATASET_12 = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_12.csv"
DATASET_15 = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_15.csv"
DATASET_18 = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_18.csv"
DATASET_6D = r"C:\Users\ccm51\Documents\Snake_Game_Pathfinder\master_dataset_6_dummy.csv"
