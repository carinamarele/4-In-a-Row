import random
import pygame
import sys
from pygame.locals import *

# importare imagini necesare pentru meniul principal cand se joaca cu computerul
TITLE = pygame.image.load('tile.png')
GAMEIMG = pygame.image.load('game.png')
BACKGROUND = pygame.image.load('bk.png')

EASYIMG = pygame.image.load('easy.png')
MEDIUMIMG = pygame.image.load('medium.png')
HARDIMG = pygame.image.load('hard.png')

# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('4 In A Row')
screen = pygame.display.set_mode((950, 800), 0, 32)

font = pygame.font.SysFont('Comic Sans MS', 50)

WINDOWWIDTH = 950  # lungimea ferestrei,in pixeli
WINDOWHEIGHT = 800  # inaltime fereastra in pixeli
BOARDWIDTH = int(sys.argv[2])  # cat de lunga este tabla
BOARDHEIGHT = int(sys.argv[3])  # cat de inalta este tabla

pygame.display.set_icon(GAMEIMG)

display_surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

RED = 'red'
BLACK = 'black'

HUMAN1 = 'human1'
HUMAN2 = 'human2'
HUMAN = 'human'
COMPUTER = 'computer'

EMPTY = None
EASY = 'easy'
MEDIUM = 'medium'
HARD = 'hard'


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def main_menu(oponent):
    while True:

        # Daca tabla nu e de dimensiunea 4x4 atunci vom arunca o exceptia si programul nu va porni
        assert BOARDWIDTH >= 4 and BOARDHEIGHT >= 4, 'Board must be at least 4x4 to play 4 In A Row'

        display_surface.blit(BACKGROUND, (0, 0))
        mx, my = pygame.mouse.get_pos()

        x = WINDOWWIDTH*0.02+30
        y = WINDOWHEIGHT*0.2-120

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
                   startGame(oponent, EASY)
            if mediumButtonRect.collidepoint((mx, my)):
                if click:
                   startGame(oponent, MEDIUM)
            if hardButtonRect.collidepoint((mx, my)):
                if click:
                   startGame(oponent, HARD)
        else:
            # VS Human
            startGame(oponent, EMPTY)

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


SPACESIZE = 50   # dimensiunea tokenurilor

FPS = 30  # frames per second to update the screen

# poziția de unde începe tabla
XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * SPACESIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - BOARDHEIGHT * SPACESIZE) / 2)


def startGame(oponent, difficulty):
    global FPSCLOCK, SHOWSURFACE, REDPILERECT, BLACKPILERECT, FIRSTPLAYER, WINNERRECT
    global BLACKTOKENIMG, REDTOKENIMG, BOARDIMG, HUMANWINNERIMG, HUMAN1WINNERIMG, HUMAN2WINNERIMG, COMPUTERWINNERIMG, TIEIMG

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    SHOWSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    FIRSTPLAYER=sys.argv[4]

    # setarea bilelor langa tabla de joc(pe de o parte si de alta a ei), folosim rect pentru a putea apasa pe ele
    REDPILERECT = pygame.Rect(int(SPACESIZE / 2), WINDOWHEIGHT - int(SPACESIZE * 3 / 2), SPACESIZE, SPACESIZE)
    BLACKPILERECT = pygame.Rect(WINDOWWIDTH - int(3 * SPACESIZE / 2), WINDOWHEIGHT - int(3 * SPACESIZE / 2), SPACESIZE,
                                SPACESIZE)

    # modific imaginea la o dimensiune potrivita
    BOARDIMG = pygame.image.load('board.png')
    BOARDIMG = pygame.transform.smoothscale(BOARDIMG, (SPACESIZE, SPACESIZE))
    REDTOKENIMG = pygame.image.load('token_red.png')
    REDTOKENIMG = pygame.transform.smoothscale(REDTOKENIMG, (SPACESIZE, SPACESIZE))
    BLACKTOKENIMG = pygame.image.load('token_black.png')
    BLACKTOKENIMG = pygame.transform.smoothscale(BLACKTOKENIMG, (SPACESIZE, SPACESIZE))

    HUMANWINNERIMG = pygame.image.load('human_winner.png')
    HUMAN1WINNERIMG = pygame.image.load('human1_winner.png')
    HUMAN2WINNERIMG = pygame.image.load('human2_winner.png')
    COMPUTERWINNERIMG = pygame.image.load('computer_winner.png')
    TIEIMG = pygame.image.load('tie.png')

    WINNERRECT = HUMANWINNERIMG.get_rect()
    WINNERRECT.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))


    while True:
        if oponent == 'computer':
          playComputerGame(difficulty)

        else:
            #Human VS Human
            playHumansGame()


def playHumansGame():

    if FIRSTPLAYER == HUMAN1 or FIRSTPLAYER == HUMAN:
        turn = HUMAN1
    else:
        turn = HUMAN2

    # Dupa ce un jucator castiga, cand va incepe din nou jocul prin apasarea oriunde pe fereastra,
    # FIRSTPLAYER ul nu se schimba, deci va incepe acelasi jucator
    # Daca vrea sa inceapa celalalt jucator va trebui sa ruleze din nou jocul cu ultimul parametru schimbat.

    # Construim noua tabla de joc
    mainBoard = buildNewBoard()

    while True:
        # loop-ul principal unde se decide ce se va face in functie de tura
        # Human1 primul jucator(RED), Human2 al doilea(BLACK)

        if turn == HUMAN1:
            getHumanMove(mainBoard, HUMAN1)

            # dupa fiecare mutare se verifica daca a castigat si se afiseaza imaginea corespunzatoare
            if isWinner(mainBoard, RED):
                winnerImg = HUMAN1WINNERIMG
                break
            # dupa ce face mutarea, tura se muta la celalalt jucator
            turn = HUMAN2

        else:  # al doilea jucator

            getHumanMove(mainBoard, HUMAN2)

            if isWinner(mainBoard, BLACK):
                winnerImg = HUMAN2WINNERIMG
                break

            turn = HUMAN1 # si revenim inapoi la primul jucator dupa mutare

       # daca ajungem in cazul in care nu mai avem unde muta inseamna ca este remiza si se va afisa mesajul corespunzator
        if isBoardFull(mainBoard):
            winnerImg = TIEIMG
            break

    running=True
    # daca unul din castigatori a castigat actualizam tabla si afisam mesajul final pentru winner
    while running:
        drawBoard(mainBoard)
        SHOWSURFACE.blit(winnerImg, WINNERRECT)

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


def playComputerGame(difficulty):

    if FIRSTPLAYER == COMPUTER:
        turn = COMPUTER
    else:
        turn = HUMAN

    # Dupa terminarea jocului, jucatorul poate juca in continuare cu calculatorul
    # dar cel care a inceput prima data jocul trecut va incepe si acum
    # Pentru a schimba ordinea, va trebui sa fie din nou rulat codul cu ultimul parametru schimbat

    # Contruim noua tabla de joc
    mainBoard = buildNewBoard()

    while True:
        if turn == HUMAN:

            getHumanMove(mainBoard,HUMAN)

            if isWinner(mainBoard, RED):
                winnerImg = HUMANWINNERIMG
                break


            turn = COMPUTER
        else:
            # in move retinem mutarea computerului cu dificultatea aleasa de noi
            getComputerMove(mainBoard, difficulty)

            # verific daca este castigator
            if isWinner(mainBoard, BLACK):
                winnerImg = COMPUTERWINNERIMG
                break

            turn = HUMAN

        if isBoardFull(mainBoard):
            winnerImg = TIEIMG
            break

    while True:
            drawBoard(mainBoard)
            SHOWSURFACE.blit(winnerImg, WINNERRECT)
            FPSCLOCK.tick()

            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    return

            pygame.display.update()

def getComputerMove(board,difficulty):

    potentialMoves = []
    if difficulty == EASY:
        for moveComputer in range(BOARDWIDTH):
            if isValidMove(board, moveComputer):
                potentialMoves.append(moveComputer)

        finalMove = random.choice(potentialMoves)

    # animam mutarea calculatorului si realizam mutarea
    animateComputerMoving(board, finalMove)


def animateComputerMoving(board, position):

    # pozitia de unde pleaca bila computerului
    x = BLACKPILERECT.left
    y = BLACKPILERECT.top
    speed = 0.1

    # deplasam bila in sus
    while y > (YMARGIN - SPACESIZE):
        y -= int(speed)
        speed += 0.02
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # deplasam bila la stanga
    y = YMARGIN - SPACESIZE
    speed = 0.1
    while x > (XMARGIN + position * SPACESIZE):
        x -= int(speed)
        speed += 0.02
        drawBoard(board, {'x':x, 'y':y, 'color':BLACK})
        pygame.display.update()
        FPSCLOCK.tick()

    # apelam functia pentru drop
    dropToken(board, position, BLACK)

    # dupa ce am mutat bila deasupra tablei facem mutarea
    makeMove(board, BLACK, position)


# pozitionez bila pentru un player pe coloana dorita si pe cel mai jos rand
def makeMove(board, player, column):
    lowest = -1

    for y in range(BOARDHEIGHT-1, -1, -1):  # start,stop,step
        if board[column][y] == EMPTY:
            lowest = y
            break

    if lowest != -1:
        board[column][lowest] = player

# desenez tabla, extraToken reprezinta locul unde va fi pusa bila
def drawBoard(board, extraToken=None):

    # initial pun extraToken=none pentru cand desenez tabla la inceperea jocului, inainte de vreo mutare
    display_surface.blit(BACKGROUND, (0, 0))

    # desenez tokenurile,verificand daca in board am RED sau BLACK
    spaceRect = pygame.Rect(0, 0, SPACESIZE, SPACESIZE)

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))

            if board[x][y] == RED:  # afisez imaginea corespunzatoare
                SHOWSURFACE.blit(REDTOKENIMG, spaceRect)

            elif board[x][y] == BLACK:
                SHOWSURFACE.blit(BLACKTOKENIMG, spaceRect)

    # desenez tokenul pe care il vreau sa il pun, adica cand fac mutare
    if extraToken != None:
        if extraToken['color'] == RED:
            SHOWSURFACE.blit(REDTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))
        elif extraToken['color'] == BLACK:
            SHOWSURFACE.blit(BLACKTOKENIMG, (extraToken['x'], extraToken['y'], SPACESIZE, SPACESIZE))

    # desenez imaginea pentru tabla
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            spaceRect.topleft = (XMARGIN + (x * SPACESIZE), YMARGIN + (y * SPACESIZE))
            SHOWSURFACE.blit(BOARDIMG, spaceRect)

    # desenez locul de unde iau bilele
    SHOWSURFACE.blit(REDTOKENIMG, REDPILERECT) # red on the left
    SHOWSURFACE.blit(BLACKTOKENIMG, BLACKPILERECT) # black on the right

# construiesc tabla intr-un array(structura tablei)
def buildNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        # umplu array ul cu None-uri pe coloane, transformându-l astfel intr-o matrice
        board.append([EMPTY] * BOARDHEIGHT)
    return board

# returnez indicele randului pentru cel mai jos spatiu liber de pe coloana data
# daca nu mai este loc va returna -1
def getLowestEmptySpace(board, column):
    for y in range(BOARDHEIGHT-1, -1, -1):# start,stop,step
        if board[column][y] == EMPTY:
            return y
    return -1

def getHumanMove(board, player):
    draggingToken = False
    tokenx, tokeny = None, None

    if player == HUMAN or player == HUMAN1:
        colorToken = RED
        pileColor = REDPILERECT
    else:
        # next human
        colorToken = BLACK
        pileColor = BLACKPILERECT

    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # verific daca se apasa pe imaginea de unde trebuie sa iau bilele si memorez pozitia
            elif event.type == MOUSEBUTTONDOWN and not draggingToken and pileColor.collidepoint(event.pos):
                draggingToken = True
                tokenx, tokeny = event.pos

            # memorez pozitia actuala cand mouse ul se misca
            elif event.type == MOUSEMOTION and draggingToken:
                tokenx, tokeny = event.pos

            # dau drumul obiectului si verific daca are pozitia in intervalul corespunzator tablei
            elif event.type == MOUSEBUTTONUP and draggingToken:

                if player == HUMAN or player == HUMAN1:
                    expressionToTest = tokeny < YMARGIN
                elif player == HUMAN2:
                    # next human
                    expressionToTest = tokeny > (YMARGIN - SPACESIZE)

                # daca nu depaseste tabla, verific daca pot efectua miscare
                # si daca da apelez animatia si actualizez tabla si redesenez
                if expressionToTest and XMARGIN < tokenx < WINDOWWIDTH - XMARGIN:
                    column = int((tokenx - XMARGIN) / SPACESIZE)

                    if isValidMove(board, column):
                        dropToken(board, column, colorToken)
                        board[column][getLowestEmptySpace(board, column)] = colorToken
                        drawBoard(board)
                        pygame.display.update()
                        return

                #sterg pozitiile memorate anterior pentru urmatoarea miscare
                tokenx, tokeny = None, None
                draggingToken = False

        # daca tokenx si tokeny raman goale atunci tabla ramane neschimbata, altfel o redesnez cu mutarea efectuata
        if tokenx != None and tokeny != None:
            drawBoard(board, {'x': tokenx - int(SPACESIZE / 2), 'y': tokeny - int(SPACESIZE / 2), 'color': colorToken})
        else:
            drawBoard(board)

        pygame.display.update()
        FPSCLOCK.tick()


# verific daca a depasit bordura tablei sau daca locul unde vreau sa pun e ocupat
def isValidMove(board, column):
    if column < 0 or column >= BOARDWIDTH or board[column][0] != EMPTY:
        return False
    return True


# animatia pentru mutare, am nevoie de tabla cu pozitiile ocupate,
# de pozitia(din lungime) unde vreau sa fac mutarea si culoarea tokenului
def dropToken(board, column, color):

    # calculez pozitia in pixeli pe tabla
    x = XMARGIN + column * SPACESIZE
    y = YMARGIN - SPACESIZE

    dropSpeed = 0.1

    # decid unde voi pune bila(din cele mai joase locuri libere)
    lowestEmptySpace = getLowestEmptySpace(board, column)

    while True:
        y += int(dropSpeed)
        dropSpeed += 0.02

        # cat timp nu ajung la pozitia unde vreau sa pun, bila cade.
        if int((y - YMARGIN) / SPACESIZE) >= lowestEmptySpace:
            return
        drawBoard(board, {'x':x, 'y':y, 'color':color})
        pygame.display.update()
        FPSCLOCK.tick()


# verific daca a depasit bordura tablei sau daca locul unde vreau sa pun e ocupat
def isValidMove(board, column):
    if column < 0 or column >= BOARDWIDTH or board[column][0] != EMPTY:
        return False
    return True


# verific daca mai este vreun loc liber
def isBoardFull(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == EMPTY:
                return False
    return True


# iau pe cazuri, tile={RED,BLACK}
def isWinner(board, color):
    # verific orizontal
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT):
            if board[x][y] == color and board[x+1][y] == color and board[x+2][y] == color and board[x+3][y] == color:
                return True
    # verific vertical
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == color and board[x][y+1] == color and board[x][y+2] == color and board[x][y+3] == color:
                return True
    # verific diagonal(\)
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == color and board[x+1][y-1] == color and board[x+2][y-2] == color and board[x+3][y-3] == color:
                return True
    # verific diagonal(/)
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == color and board[x+1][y+1] == color and board[x+2][y+2] == color and board[x+3][y+3] == color:
                return True

    # daca nu sunt valide variantele de mai sus returnez fals
    return False


if __name__ == "__main__":

    OPONENT = sys.argv[1]
    WIDTH = int(sys.argv[2])
    LENGHT= int(sys.argv[3])
    main_menu(OPONENT)
