import copy
import random
import pygame
import sys
from pygame.locals import *

# importare imagini necesare pentru meniul principal cand se joaca cu computerul
TITLE = pygame.image.load('images/tile.png')
GAMEIMG = pygame.image.load('images/game.png')
BACKGROUND = pygame.image.load('images/bk.png')
STARTIMG = pygame.image.load('images/start.png')

EASYIMG = pygame.image.load('images/easy.png')
MEDIUMIMG = pygame.image.load('images/medium.png')
HARDIMG = pygame.image.load('images/hard.png')

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('4 In A Row')
screen = pygame.display.set_mode((950, 800), 0, 32)

window_width = 950  # lungimea ferestrei,in pixeli
window_height = 800  # inaltime fereastra in pixeli

pygame.display.set_icon(GAMEIMG)

display_surface = pygame.display.set_mode((window_width, window_height))

RED = 'red'
BLACK = 'black'

HUMAN1 = 'human1'
HUMAN2 = 'human2'
HUMAN = 'human'
COMPUTER = 'computer'

EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'

board_width = int(sys.argv[2])
board_height = int(sys.argv[3])

last_human_moves = {}
last_ai_moves = {}

human_name = ''

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.SysFont('Comic Sans MS', 20)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        """
        Constructorul pentru initializarea text box ului
        :param x: pozitia pe scara width
        :param y: pozitia pe scara height
        :param w: width ul box ului
        :param h: height ul box ului
        :param text: textul initial in casuta
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color(62, 152, 152)
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

            if self.active:
                self.color = pygame.Color((48, 90, 114))
            else:
                self.color = pygame.Color((62, 152, 152))
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def get_name(self):
        return self.text

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, display):
        # Blit the text.
        display.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(display, self.color, self.rect, 2)


class Button:
    def __init__(self, x, y, image, scale):
        """
        Constructor pentru butoane
        :param x: pozitia pe scara width
        :param y: pozitia pe scara height
        :param image: poza butonului
        :param scale: dimensiune
        """
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        """
        Afisez pe ecran butonul
        :return:
        """
        screen.blit(self.image, (self.rect.x, self.rect.y))


def draw_text(text, font, color, surface, x, y):
    """
    Metoda pentru a afisa scrris pe ecran
    :param text: textul de afisat
    :param font: fontul scrisului
    :param color: culoarea scrisului
    :param surface: unde sa se afiseze
    :param x: width
    :param y: height
    :return: scris
    """
    text_rend = font.render(text, 1, color)
    text_rect = text_rend.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_rend, text_rect)


def main_menu(oponent1, width, height, firstplayer):
    """
    Meniul principal pentru computer care contine butoanele pentru nivele
    :param oponent1: tipul oponentului
    :param width: dimensiunea tablei
    :param height: inaltimea tablei
    :param firstplayer: jucatorul care incepe jocul
    :return:
    """
    global click
    while True:
        assert width >= 4 and height >= 4, 'Board must be at least 4x4 to play 4 In A Row'

        display_surface.blit(BACKGROUND, (0, 0))
        mx, my = pygame.mouse.get_pos()

        x = window_width * 0.02 + 30
        y = window_height * 0.2 - 120

        display_surface.blit(TITLE, (x, y - 10))
        display_surface.blit(GAMEIMG, (x, y + 100))

        if oponent == COMPUTER:

            easy_button_rect = pygame.Rect(655, 230, 185, 50)
            medium_button_rect = pygame.Rect(655, 380, 185, 50)
            hard_button_rect = pygame.Rect(655, 520, 185, 50)

            easy_button = Button(600, 100, EASYIMG, 0.5)
            medium_button = Button(600, 250, MEDIUMIMG, 0.5)
            hard_button = Button(600, 400, HARDIMG, 0.5)
            pygame.draw.rect(screen, (255, 0, 0), easy_button_rect)
            pygame.draw.rect(screen, (255, 0, 0), medium_button_rect)
            pygame.draw.rect(screen, (254, 0, 0), hard_button_rect)
            easy_button.draw()
            medium_button.draw()
            hard_button.draw()

            if easy_button_rect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, EASY)
            if medium_button_rect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, MEDIUM)
            if hard_button_rect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, HARD)
        else:
            # VS Human
            menu_human(oponent1, firstplayer)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()

        mainClock.tick(60)


space_size = 50  # dimensiunea tokenurilor

# poziția de unde începe tabla
XMARGIN = int((window_width - board_width * space_size) / 2)
YMARGIN = int((window_height - board_height * space_size) / 2)


def init_game():
    global FPSCLOCK, display_surface_game, redpilerect, blackpilerect, FIRSTPLAYER, winnerrect, last_move_AI
    global blacktokenimg, redtokenimg, boardimg, humanwinnerimg, human1_winnerimg, human2_winnerimg, \
        computerwinnerimg, tieimg

    last_human_moves.clear()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    display_surface_game = pygame.display.set_mode((window_width, window_height))

    FIRSTPLAYER = sys.argv[4]

    # setarea bilelor langa tabla de joc(pe de o parte si de alta a ei), folosim rect pentru a putea apasa pe ele
    redpilerect = pygame.Rect(space_size, window_height - space_size * 2, space_size, space_size)
    blackpilerect = pygame.Rect(window_width - 2 * space_size, window_height - 2 * space_size,
                                space_size, space_size)
    humanwinnerimg = pygame.image.load('images/human_winner.png')
    human1_winnerimg = pygame.image.load('images/human1_winner.png')
    human2_winnerimg = pygame.image.load('images/human2_winner.png')
    computerwinnerimg = pygame.image.load('images/computer_winner.png')
    tieimg = pygame.image.load('images/tie.png')

    # modific imaginea la o dimensiune potrivita
    boardimg = pygame.image.load('images/board.png')
    boardimg = pygame.transform.smoothscale(boardimg, (space_size, space_size))
    redtokenimg = pygame.image.load('images/token_red.png')
    redtokenimg = pygame.transform.smoothscale(redtokenimg, (space_size, space_size))
    blacktokenimg = pygame.image.load('images/token_black.png')
    blacktokenimg = pygame.transform.smoothscale(blacktokenimg, (space_size, space_size))

    winnerrect = humanwinnerimg.get_rect()
    winnerrect.center = (int(window_width / 2), int(window_height / 2))


def re_init_menu():

    display_surface.blit(BACKGROUND, (0, 0))
    x = window_width * 0.02 + 30
    y = window_height * 0.2 - 120

    display_surface.blit(TITLE, (x, y - 10))
    display_surface.blit(GAMEIMG, (x, y + 100))

    draw_text('First Player Name:', pygame.font.SysFont('Comic Sans Ms', 28), (0, 0, 0), screen, 640, 200)
    draw_text('Second Player Name:', pygame.font.SysFont('Comic Sans Ms', 28), (0, 0, 0), screen, 640, 300)

    start_button_rect = pygame.Rect(670, 430, 185, 50)
    start_button = Button(615, 310, STARTIMG, 0.5)
    pygame.draw.rect(screen, (255, 0, 0), start_button_rect)
    start_button.draw()


def menu_human(oponent1, firstplayer):
    """
    Meniul pentru varianta Human VS Human, unde afisez imaginea de fundal, numele jocului, 2 casute input pentru
    jucatori sa isi introduca numele(Nu sunt obligati) si un buton de start joc
    :param oponent1: tipul oponentului
    :param firstplayer: cel care incepe jocul
    :return:
    """
    clock = pygame.time.Clock()
    display_surface.blit(BACKGROUND, (0, 0))
    x = window_width * 0.02 + 30
    y = window_height * 0.2 - 120

    display_surface.blit(TITLE, (x, y - 10))
    display_surface.blit(GAMEIMG, (x, y + 100))
    input_box1 = InputBox(655, 250, 140, 32)
    input_box2 = InputBox(655, 350, 140, 32)
    input_box = [input_box1, input_box2]
    draw_text('First Player Name:', pygame.font.SysFont('Comic Sans Ms', 28), (0, 0, 0), screen, 640, 200)
    draw_text('Second Player Name:', pygame.font.SysFont('Comic Sans Ms', 28), (0, 0, 0), screen, 640, 300)

    start_button_rect = pygame.Rect(670, 430, 185, 50)
    start_button = Button(615, 310, STARTIMG, 0.5)
    pygame.draw.rect(screen, (255, 0, 0), start_button_rect)
    start_button.draw()

    done = False
    while not done:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                done = True
            for box in input_box:
                box.handle_event(event)
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button_rect.collidepoint((mx, my)):
                        human_name1 = input_box[0].get_name()
                        human_name2 = input_box[1].get_name()
                        choose_mode_play(oponent1, firstplayer, None, human_name1, human_name2)

        for box in input_box:
            box.update()
        re_init_menu()

        for box in input_box:
            box.draw(display_surface)

        pygame.display.update()
        clock.tick(30)


def choose_mode_play(oponent_game, firstplayer, difficulty, human_name1=None, human_name2=None):
    """
    Aleg tipul jocului, pentru afisarea graficii
    :param oponent_game: jucatorul oponent
    :param firstplayer: cine incepe jocul
    :param difficulty: dificultateea pentru jocul cu calculatorul
    :param human_name1: numele primului jucator in Human VS Human
    :param human_name2: numele celuilalt jucator in Human VS Human
    :return:
    """
    init_game()
    while True:
        if oponent_game == COMPUTER:
            start_computer_play(firstplayer, difficulty)
        else:
            start_human_play(firstplayer, human_name1, human_name2)


def draw_board(board, turn, name, token_to_draw=None):
    """
    Desenez partea de joc ce contine tabla, teancurile de token uri, regulile, cat si numele jucatorilor
    :param board: tabla care trebuie construita
    :param turn: tura jucatorului, pentru cazul cu humans, spune ce nume va fi afisat
    :param name: numele jucatorilor humans
    :param token_to_draw: piese care trebuie colorata, este None cand desenez pentru prima data tabla sau nu pot muta
    poate fi RED sau BLACK
    :return: fereastra de joc
    """

    display_surface.blit(BACKGROUND, (0, 0))

    space_rect = pygame.Rect(0, 0, space_size, space_size)
    if turn == 1:
        draw_text(name, pygame.font.SysFont('Comic Sans MS', 28), (0, 0, 0), display_surface_game, space_size - 15,
                  window_height - space_size)
    elif turn == 2:
        if len(name) < 6:
            draw_text(name, pygame.font.SysFont('Comic Sans MS', 28), (0, 0, 0), display_surface_game,
                      window_width - 2 * space_size, window_height - space_size)
        else:
            space = len(name) / 2
            draw_text(name, pygame.font.SysFont('Comic Sans MS', 28), (0, 0, 0), display_surface_game,
                      window_width - (space - 2) * space_size, window_height - space_size)

    for x in range(board_width):
        for y in range(board_height):
            if board_height < 8:
                space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + (y * space_size))
            else:
                space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + ((y - 2) * space_size))

            if board[x][y] == RED:
                display_surface_game.blit(redtokenimg, space_rect)
            elif board[x][y] == BLACK:
                display_surface_game.blit(blacktokenimg, space_rect)

    if board_height > 7:
        position1 = YMARGIN + ((board_height - 2) * space_size + 10)
        position2 = YMARGIN + ((board_height - 1) * space_size + 10)
    else:
        position1 = YMARGIN + (board_height * space_size + space_size)
        position2 = YMARGIN + (board_height * space_size + 2 * space_size)

    draw_text('        How to Play Connect 4 | The Rules of Connect 4', pygame.font.SysFont('Comic Sans MS', 20),
              (0, 0, 0), display_surface_game, space_size * 5 - 30, position1)

    draw_text(' • Players must alternate turns, and only one disc can be dropped in each turn. ',
              pygame.font.SysFont('Comic Sans MS', 18),
              (0, 0, 0),
              display_surface_game, space_size * 3 - 20, position2)

    draw_text(' • Only one piece is played at a time.', pygame.font.SysFont('Comic Sans MS', 18), (0, 0, 0),
              display_surface_game, space_size * 3 - 20, position2 + 30)

    draw_text(' • On your turn, drop one of your colored discs from the top into any of the seven slots.',
              pygame.font.SysFont('Comic Sans MS', 18), (0, 0, 0),
              display_surface_game, space_size * 3 - 20, position2 + 60)

    draw_text(' • The game ends when there is a 4-in-a-row or a stalemate.', pygame.font.SysFont('Comic Sans MS', 18),
              (0, 0, 0), display_surface_game, space_size * 3 - 20, position2 + 85)

    if token_to_draw is not None:
        if token_to_draw['color'] == BLACK:
            display_surface_game.blit(blacktokenimg, (token_to_draw['x'], token_to_draw['y'], space_size, space_size))
        elif token_to_draw['color'] == RED:
            display_surface_game.blit(redtokenimg, (token_to_draw['x'], token_to_draw['y'], space_size, space_size))

    for x in range(board_width):
        for y in range(board_height):
            if board_height < 8:
                space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + (y * space_size))
            else:
                space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + ((y - 2) * space_size))

            display_surface_game.blit(boardimg, space_rect)

    display_surface_game.blit(redtokenimg, redpilerect)
    display_surface_game.blit(blacktokenimg, blackpilerect)


def start_human_play(firstplayer, human_name1, human_name2):
    if firstplayer == HUMAN1 or firstplayer == HUMAN:
        turn = HUMAN1
    else:
        turn = HUMAN2

    # Dupa ce un jucator castiga, cand va incepe din nou jocul prin apasarea oriunde pe fereastra,
    # FIRSTPLAYER ul nu se schimba, deci va incepe acelasi jucator
    # Daca vrea sa inceapa celalalt jucator va trebui sa ruleze din nou jocul cu ultimul parametru schimbat.

    # Construim noua tabla de joc
    main_board = build_new_board()

    while True:
        # loop-ul principal unde se decide ce se va face in functie de tura
        # Human1 primul jucator(RED), Human2 al doilea(BLACK)

        if turn == HUMAN1:
            print(human_name1)
            get_humans_move(main_board, human_name1, HUMAN1)

            # dupa fiecare mutare se verifica daca a castigat si se afiseaza imaginea corespunzatoare
            if is_winner(main_board, RED):
                winner_img = human1_winnerimg
                break
            # dupa ce face mutarea, tura se muta la celalalt jucator
            turn = HUMAN2

        else:  # al doilea jucator
            print(human_name2)
            get_humans_move(main_board, human_name2, HUMAN2)

            if is_winner(main_board, BLACK):
                winner_img = human2_winnerimg
                break

            turn = HUMAN1  # si revenim inapoi la primul jucator dupa mutare

        # daca ajungem in cazul in care nu mai avem unde muta inseamna
        # ca este remiza si se va afisa mesajul corespunzator
        if is_board_full(main_board):
            winner_img = tieimg
            break

    running = True
    # daca unul din castigatori a castigat actualizam tabla si afisam mesajul final pentru winner
    while running:
        if turn == HUMAN1:
            draw_board(main_board, 1, human_name1)
        else:
            draw_board(main_board, 2, human_name2)
        display_surface_game.blit(winner_img, winnerrect)

        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()
        mainClock.tick(60)


def start_computer_play(firstplayer, difficulty):
    if firstplayer == COMPUTER:
        turn = COMPUTER
    else:
        turn = HUMAN

        # Dupa terminarea jocului, jucatorul poate juca in continuare cu calculatorul
        # dar cel care a inceput prima data jocul trecut va incepe si acum
        # Pentru a schimba ordinea, va trebui sa fie din nou rulat codul cu ultimul parametru schimbat

        # Contruim noua tabla de joc
    main_board = build_new_board()

    while True:
        if turn == HUMAN:

            get_humans_move(main_board, '', HUMAN)

            if is_winner(main_board, RED):
                winner_img = humanwinnerimg
                break

            turn = COMPUTER
        else:
            # in move retinem mutarea computerului cu dificultatea aleasa de noi
            get_computer_move(main_board, difficulty)
            print(last_ai_moves)
            # verific daca este castigator
            if is_winner(main_board, BLACK):
                winner_img = computerwinnerimg
                break

            turn = HUMAN

        if is_board_full(main_board):
            winner_img = tieimg
            break

    while True:
        draw_board(main_board, 0, '')
        display_surface_game.blit(winner_img, winnerrect)
        FPSCLOCK.tick()

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()


def get_computer_move(board, difficulty):
    # final_move = 0
    potential_moves = []
    if difficulty == EASY:
        for moveComputer in range(board_width):
            if is_valid_move(board, moveComputer):
                potential_moves.append(moveComputer)

        final_move = random.choice(potential_moves)
    elif difficulty == MEDIUM:
        potential_moves = [0] * board_width

        for move in range(board_width):
            if is_valid_move(board, move):
                copy_board = copy.deepcopy(board)
                make_move(copy_board, BLACK, move)
                if not is_winner(copy_board, BLACK):
                    for red_move in range(board_width):
                        if not is_valid_move(copy_board, red_move):
                            continue
                        else:
                            copy_board_again = copy.deepcopy(copy_board)
                            make_move(copy_board_again, RED, red_move)
                            if is_winner(copy_board_again, RED):
                                potential_moves[move] = -1
                                break
                            else:
                                potential_moves[move] += potential_moves[move] / board_width
                else:
                    potential_moves[move] = 1
            else:
                continue
        best_new_choice = -1
        for i in range(board_width):
            if potential_moves[i] > best_new_choice and is_valid_move(board, i):
                best_new_choice = potential_moves[i]
        # find all potential moves that have this best fitness
        best_moves = []
        lenght = len(potential_moves)

        for i in range(lenght):
            if potential_moves[i] == best_new_choice and is_valid_move(board, i):
                best_moves.append(i)
        final_move = random.choice(best_moves)

    else:
        potential_moves = [0] * board_width
        iteration = 1
        color = BLACK
        oponent_color = RED
        while iteration < 4:

            for move in range(board_width):
                if not is_valid_move(board, move):
                    continue
                else:
                    copy_board = copy.deepcopy(board)
                    make_move(copy_board, color, move)
                    if not is_winner(copy_board, color):
                        for op_move in range(board_width):
                            if is_valid_move(board, op_move):
                                new_copy = copy.deepcopy(copy_board)
                                make_move(new_copy, oponent_color, op_move)
                                if is_winner(new_copy, oponent_color):
                                    potential_moves[move] = -1
                                else:
                                    potential_moves[move] += potential_moves[move] / board_width
                            else:
                                continue
                    else:
                        potential_moves[move] = 1
            swap_color = color
            color = oponent_color
            oponent_color = swap_color

        best_new_choice = -1
        for i in range(board_width):
            if potential_moves[i] > best_new_choice and is_valid_move(board, i):
                best_new_choice = potential_moves[i]
        # find all potential moves that have this best fitness
        best_moves = []
        lenght = len(potential_moves)

        for i in range(lenght):
            if potential_moves[i] == best_new_choice and is_valid_move(board, i):
                best_moves.append(i)
        final_move = random.choice(best_moves)

    # animam mutarea calculatorului si realizam mutarea
    animating_computer_move(board, final_move)


# mai intai in sus | si dupa la stanga -- pana la pozitia dorita
def animating_computer_move(board, position):
    # pozitia de unde pleaca bila computerului
    x = blackpilerect.left
    y = blackpilerect.top
    speed = 0.1

    if board_height < 8:
        max_position = YMARGIN - space_size
    else:
        max_position = YMARGIN - 3 * space_size
    # deplasam bila in sus
    while y > max_position:
        y -= int(speed)
        speed += 0.02
        draw_board(board, 0, '', {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # deplasam bila la stanga
    if board_height < 8:
        y = YMARGIN - space_size
    else:
        y = YMARGIN - 3 * space_size
    speed = 0.1
    while x > (XMARGIN + position * space_size):
        x -= int(speed)
        speed += 0.02
        draw_board(board, 0, '', {'x': x, 'y': y, 'color': BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # apelam functia pentru drop
    animation_dropping_token(board, position, BLACK)

    # dupa ce am mutat bila deasupra tablei facem mutarea
    make_move(board, BLACK, position)


def make_move(board, player, column):
    """
    Fac mutarea, initial retin pozitia -1, aceasta se va modifica la primul spatiu gol
    :param board: tabla de joc
    :param player: culoarea jucatorului care face mutarea
    :param column: coloana unde va face mutarea
    :return: tabla actualizata daca se gaseste vreun spatiu liber, altfel tabla neactualizata
    """
    lowest = -1

    for y in range(board_height - 1, -1, -1):  # start,stop,step
        if board[column][y] is None:
            lowest = y
            last_ai_moves.update({'row': y, 'column': column})
            break

    if lowest != -1:
        board[column][lowest] = player


def build_new_board():
    """
    Construiesc structura tablei de joc, unde voi sti unde sunt piesele formata din array uri initializate cu None
    Array urile adaugate reprezinta coloanele, deci pentru width= 5 height=4 voi avea:
    [None,None,None,None] <- de 5 ori
    :return:
    """
    board = []
    for x in range(board_width):
        board.append([None] * board_height)
    print(board)

    return board


def is_board_full(board):
    """
    Verific daca tabla este plina
    :param board: tabla de joc
    :return: True daca nu mai este vreun loc liber, False altfel
    """
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] is None:
                return False
    return True


def is_winner(board, color):
    """
    Metoda care verifica daca am 4 in linie(orizontal,vertical,diagonal
    :param board: tabla de joc
    :param color: culoarea pentru care verific cele 4 token uri in linie
    :return: False daca niciunul din cazuri nu returneaza True
    """
    for x in range(board_width - 3):
        for y in range(board_height):
            if board[x][y] == color and board[x + 1][y] == color and board[x + 2][y] == color and board[x + 3][y] \
                    == color:
                return True

    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] == color and board[x][y + 1] == color and board[x][y + 2] == color and board[x][y + 3] \
                    == color:
                return True

    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == color and board[x + 1][y - 1] == color and board[x + 2][y - 2] == color and \
                    board[x + 3][y - 3] == color:
                return True

    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == color and board[x + 1][y + 1] == color and board[x + 2][y + 2] == color and board[x + 3][
                y + 3] \
                    == color:
                return True

    return False


def get_humans_move(board, name, player):
    is_dragged = False
    tokenx, tokeny = None, None
    expression_to_test = None

    if player == HUMAN or player == HUMAN1:
        color_token = RED
        pile_color = redpilerect
    else:
        # next human
        color_token = BLACK
        pile_color = blackpilerect

    while True:
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # verific daca se apasa pe imaginea de unde trebuie sa iau bilele si memorez pozitia
            elif event.type == MOUSEBUTTONDOWN and not is_dragged and pile_color.collidepoint(event.pos):
                is_dragged = True
                tokenx, tokeny = event.pos

            # memorez pozitia actuala cand mouse ul se misca
            elif event.type == MOUSEMOTION and is_dragged:
                tokenx, tokeny = event.pos

            # dau drumul obiectului si verific daca are pozitia in intervalul corespunzator tablei
            elif event.type == MOUSEBUTTONUP and is_dragged:

                if player == HUMAN or player == HUMAN1:
                    if board_height > 7:
                        expression_to_test = tokeny < YMARGIN - 2 * space_size
                    else:
                        expression_to_test = tokeny < YMARGIN
                elif player == HUMAN2:
                    # next human
                    if board_height > 7:
                        expression_to_test = tokeny > (YMARGIN - 3 * space_size)
                    else:
                        expression_to_test = tokeny > (YMARGIN - space_size)

                # daca nu depaseste tabla, verific daca pot efectua miscare
                # si daca da apelez animatia si actualizez tabla si redesenez
                if expression_to_test and XMARGIN < tokenx < window_width - XMARGIN:
                    column = int((tokenx - XMARGIN) / space_size)

                    if is_valid_move(board, column):
                        animation_dropping_token(board, column, color_token)
                        row = get_lowest_empty_space_on_board(board, column)
                        board[column][row] = color_token
                        last_human_moves.update({'row': row, 'column': column})
                        if player == HUMAN1:
                            draw_board(board, 1, name)
                        else:
                            draw_board(board, 2, name)
                        pygame.display.update()
                        return
                    else:
                        print("Out of boundaries or not empty..Try again in another position!")

                #  sterg pozitiile memorate anterior pentru urmatoarea miscare
                tokenx, tokeny = None, None
                is_dragged = False

        # daca tokenx si tokeny raman goale atunci tabla ramane neschimbata, altfel o redesnez cu mutarea efectuata
        if tokenx is not None and tokeny is not None:
            if player == HUMAN1:
                draw_board(board, 1, name,
                           {'x': tokenx - int(space_size / 2), 'y': tokeny - int(space_size / 2), 'color': color_token})
            else:
                draw_board(board, 2, name,
                           {'x': tokenx - int(space_size / 2), 'y': tokeny - int(space_size / 2), 'color': color_token})
        else:
            if player == HUMAN1:
                draw_board(board, 1, name)
            else:
                draw_board(board, 2, name)

        pygame.display.update()
        FPSCLOCK.tick()


def print_board(board):
    for x in range(board_height):
        array = []
        for y in range(board_width):
            array.append(board[y][x])
            print(x)
        print(array)


def animation_dropping_token(board, column, color):
    """
    Metoda care face animatia pentru eliberarea token ului de deasupra tablei de joc
    :param board: tabla de joc
    :param column: coloana unde doresc sa dau drumul token ului
    :param color: culoarea token ului
    :return: oprire funtie
    """
    # calculez pozitia in pixeli pe tabla
    x = XMARGIN + column * space_size

    if board_height > 7:
        y = YMARGIN - 3 * space_size
    else:
        y = YMARGIN - space_size
    drop_speed = 0.1

    # decid unde voi pune bila(din cele mai joase locuri libere)
    lowest_empty_space = get_lowest_empty_space_on_board(board, column)

    while True:
        y += int(drop_speed)
        drop_speed += 0.02

        # cat timp nu ajung la pozitia unde vreau sa pun, bila cade.
        if board_height > 7:
            if int((y - YMARGIN + 3 * space_size) / space_size) >= lowest_empty_space:
                return
        else:
            if int((y - YMARGIN) / space_size) >= lowest_empty_space:
                return
        draw_board(board, 0, '', {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()


def is_valid_move(board, column):
    """
    Metoda pentru verificarea unei metode, daca este in interiorul tablei de joc
    :param board: Tabla unde sunt mutarile
    :param column: coloana pe care o vom verifica
    :return: True daca este posibila mutarea, False altfel
    """
    if column < 0 or column >= board_width or board[column][0] is not None:
        return False
    return True


def get_lowest_empty_space_on_board(board, column):
    """
    Metoda pentru a lua cel mai jos spatiu liber de pe coloana data ca parametru
    :param board: tabla de joc
    :param column: coloana de unde doresc sa iau primul spatiu liber
    :return: pozitia daca exista spatiu liber pe coloana data ca parametru, -1 in cazul in care coloana este plina
    """
    for y in range(board_height - 1, -1, -1):  # start,stop,step
        if board[column][y] is None:
            return y
    return -1


if __name__ == '__main__':
    oponent = sys.argv[1]
    board_width = int(sys.argv[2])
    board_height = int(sys.argv[3])
    first_player = sys.argv[4]
    main_menu(oponent, board_width, board_height, first_player)
