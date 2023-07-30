import pygame

pygame.init()

WIDTH = 800
HEIGHT = 750
ORANGE = (255, 165, 0)
ORANGE_DARK = (220, 130, 0)

font = pygame.font.Font("./Poppins-Regular.ttf", 24)
title_font = pygame.font.Font("./Orbitron-Regular.ttf", 48)
end_font = pygame.font.Font("./Poppins-Regular.ttf", 40)


def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**0.5


class Circle:
    radius = 30

    def __init__(self, val, x, y):
        self.val = val
        self.x = x
        self.y = y
        self.posx = 160 + self.x * 80
        self.posy = 90 + self.y * 80

    def draw(self, surface):
        if distance(*pygame.mouse.get_pos(), self.posx, self.posy) <= Circle.radius:
            color = (192, 192, 192)
        else:
            color = "white"

        if self.val != -1:
            pygame.draw.circle(surface, color, (self.posx, self.posy), Circle.radius)


class Marble:
    radius = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.posx = 160+self.x*80
        self.posy = 90+self.y*80
        self.clicked = False

    def draw(self, board, surface):
        color = (0, 150, 255)

        if self.clicked:
            color = (0, 128, 128)

        if board[self.x][self.y].val == 1:
            pygame.draw.circle(surface, color, (self.posx, self.posy), Marble.radius)


class Button:
    def __init__(self, width, height, y, text):
        self.button = pygame.Rect(0, 0, width, height)
        self.button.center = (WIDTH//2, y)
        self.txt = font.render(text, True, "white")
        self.txt_rect = self.txt.get_rect()
        self.txt_rect.center = self.button.center

    def draw(self, surface, color1, color2):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, color1, self.button, border_radius=3)
        else:
            pygame.draw.rect(surface, color2, self.button, border_radius=3)

        screen.blit(self.txt, self.txt_rect)


def initialize_board():
    x = -1
    board = [
        [x, x, 1, 1, 1, x, x],
        [x, x, 1, 1, 1, x, x],
        [1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1],
        [x, x, 1, 1, 1, x, x],
        [x, x, 1, 1, 1, x, x]
    ]
    marbles = [[0 for _ in range(7)] for _ in range(7)]

    for i in range(7):
        for j in range(7):
            board[i][j] = Circle(board[i][j], i, j)
            marbles[i][j] = Marble(i, j)

    return board, marbles


def count_moves(board, i, j):
    cnt = 0
    if board[i][j].val == 1:
        if i-2 >= 0 and board[i-1][j].val == 1 and board[i-2][j].val == 0:
            cnt += 1
        if i+2 < 7 and board[i+1][j].val == 1 and board[i+2][j].val == 0:
            cnt += 1
        if j-2 >= 0 and board[i][j-1].val == 1 and board[i][j-2].val == 0:
            cnt += 1
        if j+2 < 7 and board[i][j+1].val == 1 and board[i][j+2].val == 0:
            cnt += 1
    return cnt


def total_moves(board):
    total = 0
    for i in range(7):
        for j in range(7):
            total += count_moves(board, i, j)
    return total


def make_move(board, i1, j1, i2, j2):
    success = False
    if i1 == i2 and j1+2 == j2:
        if board[i1][j1].val == 1 and board[i1][j1+1].val == 1 and board[i1][j1+2].val == 0:
            board[i1][j1].val = 0
            board[i1][j1+1].val = 0
            board[i1][j1+2].val = 1
            success = True
    if i1 == i2 and j1-2 == j2:
        if board[i1][j1].val == 1 and board[i1][j1-1].val == 1 and board[i1][j1-2].val == 0:
            board[i1][j1].val = 0
            board[i1][j1-1].val = 0
            board[i1][j1-2].val = 1
            success = True
    if j1 == j2 and i1+2 == i2:
        if board[i1][j1].val == 1 and board[i1+1][j1].val == 1 and board[i1+2][j1].val == 0:
            board[i1][j1].val = 0
            board[i1+1][j1].val = 0
            board[i1+2][j1].val = 1
            success = True
    if j1 == j2 and i1-2 == i2:
        if board[i1][j1].val == 1 and board[i1-1][j1].val == 1 and board[i1-2][j1].val == 0:
            board[i1][j1].val = 0
            board[i1-1][j1].val = 0
            board[i1-2][j1].val = 1
            success = True

    return success


def display_board(board):
    for i in range(7):
        for j in range(7):
            if board[i][j].val == -1:
                print("X", end=" ")
            else:
                print(board[i][j].val, end=" ")
        print()
    print()


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Brainvita")
    brainvita_board, brainvita_marbles = initialize_board()

    title = title_font.render("Brainvita", True, "white")
    title_rect = title.get_rect()
    title_rect.center = (WIDTH // 2, 120)

    win = end_font.render("You Win!", True, "green")
    win_rect = title.get_rect()
    win_rect.center = (WIDTH//2 + 20, 120)

    loss = end_font.render("You Lost!", True, "red")
    loss_rect = title.get_rect()
    loss_rect.center = (WIDTH//2 + 20, 120)

    start_button = Button(200, 50, 400, "New Game")
    quit_button = Button(200, 50, 700, "Quit")
    play_again_button = Button(200, 50, 400, "Play Again")

    running = True
    clicked = False
    start = True
    end = False
    wait = False
    start_pos = (0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start:
                    if start_button.button.collidepoint(pos):
                        start = False
                        brainvita_board, brainvita_marbles = initialize_board()
                elif end:
                    if play_again_button.button.collidepoint(pos):
                        start = True
                        end = False
                else:
                    if quit_button.button.collidepoint(pos):
                        start = True

                    for a in range(7):
                        for b in range(7):
                            if distance(*pos, brainvita_marbles[a][b].posx, brainvita_marbles[a][b].posy) <= Marble.radius:
                                if clicked:
                                    if (a, b) == start_pos:
                                        brainvita_marbles[a][b].clicked = False
                                        clicked = False
                                    else:
                                        moved = make_move(brainvita_board, *start_pos, a, b)
                                        if moved:
                                            brainvita_marbles[a][b].clicked = False
                                            clicked = False
                                            if total_moves(brainvita_board) == 0:
                                                end = True
                                                wait = True
                                else:
                                    brainvita_marbles[a][b].clicked = True
                                    start_pos = (a, b)
                                    clicked = True
                                    break

        screen.fill("black")

        if start:
            start_button.draw(screen, ORANGE, ORANGE_DARK)
            screen.blit(title, title_rect)
        elif end and not wait:
            if sum([sum([1 if b.val == 1 else 0 for b in a]) for a in brainvita_board]) == 1:
                screen.blit(win, win_rect)
            else:
                screen.blit(loss, loss_rect)
            play_again_button.draw(screen, ORANGE, ORANGE_DARK)
        else:
            pygame.draw.circle(screen, "red", (400, 330), 300)

            for a in range(7):
                for b in range(7):
                    brainvita_board[a][b].draw(screen)
                    brainvita_marbles[a][b].draw(brainvita_board, screen)

            quit_button.draw(screen, ORANGE, ORANGE_DARK)

        pygame.display.flip()

        if wait:
            pygame.time.wait(500)
            wait = False

    pygame.quit()
