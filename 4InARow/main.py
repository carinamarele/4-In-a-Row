import copy
import random
import pygame
import sys
from pygame.locals import *

# importare imagini necesare pentru meniul principal cand se joaca cu computerul
TITLE = pygame.image.load('images/tile.png')
GAMEIMG = pygame.image.load('images/game.png')
BACKGROUND = pygame.image.load('images/bk.png')

EASYIMG = pygame.image.load('images/easy.png')
MEDIUMIMG = pygame.image.load('images/medium.png')
HARDIMG = pygame.image.load('images/hard.png')

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('4 In A Row')
screen = pygame.display.set_mode((950, 800), 0, 32)

font = pygame.font.SysFont('Comic Sans MS', 50)

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
last_ai_moves={}

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def main_menu(oponent1, width, height, firstplayer):
    while True:

        # Daca tabla nu e de dimensiunea 4x4 atunci vom arunca o exceptia si programul nu va porni
        assert width >= 4 and height >= 4, 'Board must be at least 4x4 to play 4 In A Row'

        display_surface.blit(BACKGROUND, (0, 0))
        mx, my = pygame.mouse.get_pos()

        x = window_width*0.02+30
        y = window_height*0.2-120

        display_surface.blit(TITLE, (x, y - 10))
        display_surface.blit(GAMEIMG, (x, y + 100))

        # se va alege dificultatea cand se joaca impotriva calculatorului
        if oponent == COMPUTER:

            easyButtonRect = pygame.Rect(655, 230, 185, 50)
            mediumButtonRect = pygame.Rect(655, 380, 185, 50)
            hardButtonRect = pygame.Rect(655, 520, 185, 50)

            easy_button = Button(600, 100, EASYIMG, 0.5)
            medium_button = Button(600, 250, MEDIUMIMG, 0.5)
            hard_button = Button(600, 400, HARDIMG, 0.5)
            pygame.draw.rect(screen, (255, 0, 0), easyButtonRect)
            pygame.draw.rect(screen, (255, 0, 0), mediumButtonRect)
            pygame.draw.rect(screen, (254, 0, 0), hardButtonRect)
            easy_button.draw()
            medium_button.draw()
            hard_button.draw()

            if easyButtonRect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, EASY)
            if mediumButtonRect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, MEDIUM)
            if hardButtonRect.collidepoint((mx, my)):
                if click:
                    choose_mode_play(oponent1, firstplayer, HARD)
        else:
            # VS Human
            choose_mode_play(oponent1, firstplayer, None)

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



space_size = 50   # dimensiunea tokenurilor

# poziția de unde începe tabla
XMARGIN = int((window_width - board_width * space_size) / 2)
YMARGIN = int((window_height - board_height * space_size) / 2)


def init_game():
    global FPSCLOCK, display_surface_game, redpilerect, blackpilerect, FIRSTPLAYER, winnerrect, last_move_AI
    global blacktokenimg, redtokenimg, boardimg, humanwinnerimg, human1_winnerimg, human2_winnerimg, computerwinnerimg, tieimg

    last_human_moves.clear()
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    display_surface_game = pygame.display.set_mode((window_width, window_height))

    FIRSTPLAYER = sys.argv[4]

    # setarea bilelor langa tabla de joc(pe de o parte si de alta a ei), folosim rect pentru a putea apasa pe ele
    redpilerect = pygame.Rect(int(space_size / 2), window_height - int(space_size * 3 / 2), space_size, space_size)
    blackpilerect = pygame.Rect(window_width - int(3 * space_size / 2), window_height - int(3 * space_size / 2), space_size, space_size)
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


def choose_mode_play(oponent_game, firstplayer, difficulty):

    init_game()
    while True:
        if oponent_game == COMPUTER:
            start_computer_play(firstplayer,  difficulty)
        else:
            start_human_play(firstplayer)


# desenez tabla, extraToken reprezinta locul unde va fi pusa bila,mereu se actualizeaza
def draw_board(board, token_to_draw=None):

    # initial pun extraToken=none pentru cand desenez tabla la inceperea jocului, inainte de vreo mutare
    display_surface.blit(BACKGROUND, (0, 0))

    # desenez tokenurile,verificand daca in structura tablei am RED sau BLACK
    space_rect = pygame.Rect(0, 0, space_size, space_size)

    for x in range(board_width):
        for y in range(board_height):
            space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + (y * space_size))

            if board[x][y] == RED:  # afișez imaginea corespunzătoare
                display_surface_game.blit(redtokenimg, space_rect)
            elif board[x][y] == BLACK:
                display_surface_game.blit(blacktokenimg, space_rect)

    # daca nu sunt la initializare atunci variabila va contine pozitia si culoarea tokenului de desenat
    if token_to_draw is not None:
        if token_to_draw['color'] == BLACK:
            display_surface_game.blit(blacktokenimg, (token_to_draw['x'], token_to_draw['y'], space_size, space_size))
        elif token_to_draw['color'] == RED:
            display_surface_game.blit(redtokenimg, (token_to_draw['x'], token_to_draw['y'], space_size, space_size))

    # afisez fiecare bucata de tabla, construindu-i si un rect pentru a putea interactiona
    for x in range(board_width):
        for y in range(board_height):
            space_rect.topleft = (XMARGIN + (x * space_size), YMARGIN + (y * space_size))
            display_surface_game.blit(boardimg, space_rect)

    # afisez imaginile pentru locul de unde iau tokenurile ffolosindu-ma de recturile initializate
    display_surface_game.blit(redtokenimg, redpilerect) # red on the left
    display_surface_game.blit(blacktokenimg, blackpilerect) # black on the right


def start_human_play(firstplayer):

    if firstplayer == HUMAN1 or firstplayer == HUMAN:
        turn = HUMAN1
    else:
        turn = HUMAN2

    # Dupa ce un jucator castiga, cand va incepe din nou jocul prin apasarea oriunde pe fereastra,
    # FIRSTPLAYER ul nu se schimba, deci va incepe acelasi jucator
    # Daca vrea sa inceapa celalalt jucator va trebui sa ruleze din nou jocul cu ultimul parametru schimbat.

    # Construim noua tabla de joc
    mainBoard = build_new_board()

    while True:
        # loop-ul principal unde se decide ce se va face in functie de tura
        # Human1 primul jucator(RED), Human2 al doilea(BLACK)

        if turn == HUMAN1:

            get_humans_move(mainBoard, HUMAN1)

            # dupa fiecare mutare se verifica daca a castigat si se afiseaza imaginea corespunzatoare
            if is_winner(mainBoard, RED):
                winnerImg = human1_winnerimg
                break
            # dupa ce face mutarea, tura se muta la celalalt jucator
            turn = HUMAN2

        else:  # al doilea jucator

            get_humans_move(mainBoard, HUMAN2)

            if is_winner(mainBoard, BLACK):
                winnerImg = human2_winnerimg
                break

            turn = HUMAN1  # si revenim inapoi la primul jucator dupa mutare

        # daca ajungem in cazul in care nu mai avem unde muta inseamna ca este remiza si se va afisa mesajul corespunzator
        if is_board_full(mainBoard):
            winnerImg = tieimg
            break

    running = True
    # daca unul din castigatori a castigat actualizam tabla si afisam mesajul final pentru winner
    while running:
        draw_board(mainBoard)
        display_surface_game.blit(winnerImg, winnerrect)

        FPSCLOCK.tick()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)


def start_computer_play(firstplayer,difficulty):

    if firstplayer == COMPUTER:
        turn = COMPUTER
    else:
        turn = HUMAN

        # Dupa terminarea jocului, jucatorul poate juca in continuare cu calculatorul
        # dar cel care a inceput prima data jocul trecut va incepe si acum
        # Pentru a schimba ordinea, va trebui sa fie din nou rulat codul cu ultimul parametru schimbat

        # Contruim noua tabla de joc
    mainBoard = build_new_board()

    while True:
        if turn == HUMAN:

            get_humans_move(mainBoard, HUMAN)

            if is_winner(mainBoard, RED):
                winnerImg = humanwinnerimg
                break

            turn = COMPUTER
        else:
            # in move retinem mutarea computerului cu dificultatea aleasa de noi
            get_computer_move(mainBoard, difficulty)
            print(last_ai_moves)
            # verific daca este castigator
            if is_winner(mainBoard, BLACK):
                winnerImg = computerwinnerimg
                break

            turn = HUMAN

        if is_board_full(mainBoard):
            winnerImg = tieimg
            break

    while True:
        draw_board(mainBoard)
        display_surface_game.blit(winnerImg, winnerrect)
        FPSCLOCK.tick()

        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                return

        pygame.display.update()

def get_computer_move(board,difficulty):
    final_move = 0
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
                makeMove(copy_board, BLACK, move)
                if not is_winner(copy_board, BLACK):
                    for red_move in range(board_width):
                        if not is_valid_move(copy_board, red_move):
                            continue
                        else:
                            copy_board_again = copy.deepcopy(copy_board)
                            makeMove(copy_board_again, RED, red_move)
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
        bestMoves = []
        lenght=len(potential_moves)

        for i in range(lenght):
            if potential_moves[i] == best_new_choice and is_valid_move(board, i):
                bestMoves.append(i)
        final_move= random.choice(bestMoves)

    else:
        potential_moves=[0]*board_width
        iteration=1
        color=BLACK
        oponent_color=RED
        while iteration < 4:

            for move in range(board_width):
                if not is_valid_move(board,move):
                    continue
                else:
                    copy_board=copy.deepcopy(board)
                    makeMove(copy_board,color,move)
                    if not is_winner(copy_board,color):
                        for op_move in range(board_width):
                            if is_valid_move(board,op_move):
                                new_copy=copy.deepcopy(copy_board)
                                makeMove(new_copy,oponent_color,op_move)
                                if is_winner(new_copy,oponent_color):
                                    potential_moves[move]=-1
                                else:
                                    potential_moves[move]+=potential_moves[move]/board_width
                            else: continue
                    else:
                        potential_moves[move]=1
            swap_color=color
            color=oponent_color
            oponent_color=swap_color

        best_new_choice = -1
        for i in range(board_width):
            if potential_moves[i] > best_new_choice and is_valid_move(board, i):
                best_new_choice = potential_moves[i]
        # find all potential moves that have this best fitness
        bestMoves = []
        lenght = len(potential_moves)

        for i in range(lenght):
            if potential_moves[i] == best_new_choice and is_valid_move(board, i):
                bestMoves.append(i)
        final_move = random.choice(bestMoves)



    # animam mutarea calculatorului si realizam mutarea
    animating_computer_move(board, final_move)


# mai intai in sus | si dupa la stanga -- pana la pozitia dorita
def animating_computer_move(board, position):

    # pozitia de unde pleaca bila computerului
    x = blackpilerect.left
    y = blackpilerect.top
    speed = 0.1

    # deplasam bila in sus
    while y > (YMARGIN - space_size):
        y -= int(speed)
        speed += 0.02
        draw_board(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # deplasam bila la stanga
    y = YMARGIN - space_size
    speed = 0.1
    while x > (XMARGIN + position * space_size):
        x -= int(speed)
        speed += 0.02
        draw_board(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # apelam functia pentru drop
    animation_dropping_token(board, position, BLACK)

    # dupa ce am mutat bila deasupra tablei facem mutarea
    makeMove(board, BLACK, position)


# pozitionez bila pentru un player pe coloana dorita si pe cel mai jos rand
def makeMove(board, player, column):
    lowest = -1

    for y in range(board_height-1, -1, -1):  # start,stop,step
        if board[column][y] == None:
            lowest = y
            last_ai_moves.update({'row': y, 'column': column})
            break

    if lowest is not -1:
        board[column][lowest] = player




# construiesc tabla intr-un array de array uri(structura tablei)
def build_new_board():
    board = []
    for x in range(board_width):
        # umplu array ul cu None-uri pe coloane, transformându-l astfel intr-o matrice [None,None,....]
        board.append([None] * board_height)
    print(board)

    return board


# verific daca mai este vreun loc liber
def is_board_full(board):

    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] == None:
                return False
    return True


# iau pe cazuri, tile={RED,BLACK}
def is_winner(board, color):
    # verific orizontal
    for x in range(board_width - 3):
        for y in range(board_height):
            if board[x][y] == color and board[x+1][y] == color and board[x+2][y] == color and board[x+3][y] == color:
                return True
    # verific vertical
    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] == color and board[x][y+1] == color and board[x][y+2] == color and board[x][y+3] == color:
                return True
    # verific diagonal(\)
    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == color and board[x+1][y-1] == color and board[x+2][y-2] == color and board[x+3][y-3] == color:
                return True
    # verific diagonal(/)
    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == color and board[x+1][y+1] == color and board[x+2][y+2] == color and board[x+3][y+3] == color:
                return True

    # daca nu sunt valide variantele de mai sus returnez fals
    return False


def get_humans_move(board, player):
    is_dragged = False
    tokenx, tokeny = None, None

    if player == HUMAN or player == HUMAN1:
        color_token = RED
        pile_color = redpilerect
    else:
        # next human
        color_token = BLACK
        pile_color = blackpilerect

    while True:
        for event in pygame.event.get(): # event handling loop
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
                    expressionToTest = tokeny < YMARGIN
                elif player == HUMAN2:
                    # next human
                    expressionToTest = tokeny > (YMARGIN - space_size)

                # daca nu depaseste tabla, verific daca pot efectua miscare
                # si daca da apelez animatia si actualizez tabla si redesenez
                if expressionToTest and XMARGIN < tokenx < window_width - XMARGIN:
                    column = int((tokenx - XMARGIN) / space_size)

                    if is_valid_move(board, column):
                        animation_dropping_token(board, column, color_token)
                        row = get_lowest_empty_space_on_board(board, column)
                        board[column][row] = color_token
                        last_human_moves.update({'row': row, 'column': column})
                        draw_board(board)
                        pygame.display.update()
                        return
                    else:
                        print("Out of boundaries or not empty..Try again in another position!")

                #  sterg pozitiile memorate anterior pentru urmatoarea miscare
                tokenx, tokeny = None, None
                is_dragged = False

        # daca tokenx si tokeny raman goale atunci tabla ramane neschimbata, altfel o redesnez cu mutarea efectuata
        if tokenx is not None and tokeny is not None:
            draw_board(board, {'x': tokenx - int(space_size / 2), 'y': tokeny - int(space_size / 2), 'color': color_token})
        else:
            draw_board(board)

        pygame.display.update()
        FPSCLOCK.tick()


def print_board(board):

    for x in range(board_height):
        array = []
        for y in range(board_width):
            array.append(board[y][x])
            print(x)
        print(array)


# animatia pentru mutare, am nevoie de tabla cu pozitiile ocupate,
# de pozitia(din lungime) unde vreau sa fac mutarea si culoarea tokenului
def animation_dropping_token(board, column, color):

    # calculez pozitia in pixeli pe tabla
    x = XMARGIN + column * space_size
    y = YMARGIN - space_size

    dropSpeed = 0.1

    # decid unde voi pune bila(din cele mai joase locuri libere)
    lowest_empty_space = get_lowest_empty_space_on_board(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.02

        # cat timp nu ajung la pozitia unde vreau sa pun, bila cade.
        if int((y - YMARGIN) / space_size) >= lowest_empty_space:
            return
        draw_board(board, {'x': x, 'y': y, 'color': color})
        pygame.display.update()
        FPSCLOCK.tick()


# verific daca a depasit bordura tablei sau daca locul unde vreau sa pun e ocupat
def is_valid_move(board, column):
    if column < 0 or column >= board_width or board[column][0] is not None:
        return False
    return True


# returnez indicele randului pentru cel mai jos spatiu liber de pe coloana data
# daca nu mai este loc va returna -1
def get_lowest_empty_space_on_board(board, column):
    for y in range(board_height-1, -1, -1):  # start,stop,step
        if board[column][y] == None:
            return y
    return -1


if __name__ == '__main__':
    oponent = sys.argv[1]
    board_width = int(sys.argv[2])
    board_height = int(sys.argv[3])
    first_player = sys.argv[4]
    main_menu(oponent, board_width, board_height, first_player)
