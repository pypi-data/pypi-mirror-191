import pygame
from car import car
from microphones import Microphones
from src.tudelft_pycar.settings import settings

pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_SIZE, settings.SCREEN_SIZE))
clock = pygame.time.Clock()

pygame.display.set_caption("Virtual KITT")
pygame.display.set_icon(pygame.image.load('img/window-icon.png'))

microphones = Microphones(settings.pyaudio_handle)

window_closed = False
while not window_closed:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_closed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            car.reset(event.pos)

    car.act()
    microphones.act()

    screen.fill(0x303440)
    microphones.draw(screen)
    car.draw(screen)
    pygame.display.flip()

pygame.quit()
