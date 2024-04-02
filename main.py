import pygame
import socket
from guest_fase import Guest_screen

HOST = '127.0.0.1'
PORT = 5000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

id = int(tcp.recv(1024))

if id < 0:
    print("A partida está lotada... :(")
    exit(1)

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([800, 600])

tcp.send("get_size".encode())
string_len = int(tcp.recv(1024))

guest_screen = Guest_screen(id, string_len, screen)

while True:
    guest_screen.tick(string_len, tcp)

    screen.fill((50, 50, 90))

    guest_screen.render(screen)

    pygame.display.flip()

    clock.tick(60)
