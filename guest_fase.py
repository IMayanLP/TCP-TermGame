import pygame
import sys


class Guest_screen():
    def __init__(self, id, string_len, screen):
        self.base_font = pygame.font.Font(None, 32)
        self.logo = pygame.image.load("logo.jpg").convert()
        self.logo = pygame.transform.scale(self.logo, (292, 90))
        self.user_input = ''
        self.id = id

        self.color = pygame.Color('white')
        self.color_second = pygame.Color(200, 200, 200)
        self.color_active = pygame.Color(180, 180, 180)
        self.color_active_second = pygame.Color(150, 150, 150)

        self.color_yellow = pygame.Color(255, 255, 150)
        self.color_yellow_second = pygame.Color(200, 200, 150)
        self.color_green = pygame.Color(100, 255, 100)
        self.color_green_second = pygame.Color(100, 200, 100)

        self.left_anchor = screen.get_width() / 2 - ((64) * string_len / 2) if string_len % 2 == 0 \
            else screen.get_width() / 2 - (((64) * string_len / 2) + 30)

        self.guest_rect = []
        self.guest_colors = []
        self.guests = []

        self.round = 0
        self.max_round = 6

        self.message = "Esperando outro jogador..."

        for i in range(self.max_round):
            line_colors = []
            line_rects = []
            for j in range(string_len):
                line_rects.append(pygame.Rect((j * 64) + self.left_anchor, (i * 78) + 100, 48, 64))
                line_colors.append({
                    "primary": self.color,
                    "second": self.color_second})
            self.guest_colors.append(line_colors)
            self.guest_rect.append(line_rects)

    def checkGuest(self, con):
        con.send(str(self.user_input).encode())
        string_code = con.recv(1024)
        status_code = str(string_code).split("'")[1]

        if(status_code == '3'):
            self.user_input = ''
            return

        for i in range(len(string_code)):
            if string_code[i] == 1:
                self.guest_colors[self.round][i]["primary"] = self.color_green
                self.guest_colors[self.round][i]["second"] = self.color_green_second
            elif string_code[i] == 2:
                self.guest_colors[self.round][i]["primary"] = self.color_yellow
                self.guest_colors[self.round][i]["second"] = self.color_yellow_second

        self.guests.append(self.user_input)
        self.user_input = ''
        self.round += 1

    def render(self, screen):
        for i in range(self.max_round):
            for j in range(len(self.guest_rect[i])):
                rect_color = self.color_active if (j == len(self.user_input) and i == self.round) \
                    else self.guest_colors[i][j]["primary"]
                react_second_color = self.color_active_second if (j == len(self.user_input) and i == self.round) \
                    else self.guest_colors[i][j]["second"]

                pygame.draw.rect(screen, rect_color, self.guest_rect[i][j])
                pygame.draw.rect(screen, react_second_color,
                                 (self.guest_rect[i][j].x, self.guest_rect[i][j].y + self.guest_rect[i][j].h - 12,
                                  self.guest_rect[i][j].w, 12))

        if self.round < self.max_round:
            for i in range(len(self.user_input)):
                text_surface = self.base_font.render(self.user_input[i], True, (0, 0, 0))
                screen.blit(text_surface, (self.guest_rect[self.round][i].x + 18, self.guest_rect[self.round][i].y + 15))

        for i in range(len(self.guests)):
            for j in range(len(self.guests[i])):
                text_surface = self.base_font.render(self.guests[i][j], True, (0, 0, 0))
                screen.blit(text_surface, (self.guest_rect[i][j].x + 18, self.guest_rect[i][j].y + 15))

        self.base_font = pygame.font.Font(None, 24)
        text = self.base_font.render("Status: " + self.message, True, (255, 255, 255))
        screen.blit(text, (50, screen.get_height() - 30))
        self.base_font = pygame.font.Font(None, 32)

        screen.blit(self.logo, (screen.get_width()/2 - 142, 10))

    def tick(self, string_len, con):
        con.send('status'.encode())
        msg = con.recv(1024)
        msg = str(msg).split("'")[1]

        if (msg == "vez do 1" and self.id == 1) or (msg == "vez do 2" and self.id == 2):
            self.message = "Sua vez de jogar..."
        elif (msg == "1 ganhou" and self.id == 1) or msg == "2 ganhou" and self.id == 2:
            self.message = "Você venceu!!!"
        elif (msg == "1 ganhou" and self.id == 2) or msg == "2 ganhou" and self.id == 1:
            self.message = "O adversario acertou a palavra :("
        elif msg == "waiting":
            self.message = "Esperando outro jogador..."
        else:
            self.message = "Esperando a vez do adversario..."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN
                    and self.round < self.max_round
                    and self.message != "Esperando outro jogador..."):
                if self.message != "Você venceu!!!" and self.message != "O adversario acertou a palavra :(":
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]
                    else:
                        if len(self.user_input) < string_len:
                            newString = self.user_input + event.unicode
                            if newString.isalpha():
                                self.user_input = newString
                        else:
                            if event.key == pygame.K_RETURN:
                                self.checkGuest(con)
