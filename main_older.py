import pygame
import random

pygame.init()
screen = pygame.display.set_mode()

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Score:', True, (200, 200, 0))

screen.blit(text, (0, 0))

pygame.display.flip()