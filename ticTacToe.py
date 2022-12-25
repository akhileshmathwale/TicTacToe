import pygame as pg,sys
from pygame.locals import *
import time

#initialize global variables
XO = 'x'
winner = None
draw = False

#screen= pg.display.set_mode((height,width))
white = (255, 255, 255)
line_color = (10,10,10)

#TicTacToe 3x3 board
TTT = [[None]*3,[None]*3,[None]*3]

pg.init()
fps = 3000
CLOCK = pg.time.Clock()
width= pg.display.get_desktop_sizes()[0][0]
height= pg.display.get_desktop_sizes()[0][1]
screen = pg.display.set_mode((width, height))
pg.display.set_caption("Tic Tac Toe")



#loading the images
opening = pg.image.load('TicTacToe.png')
x_img = pg.image.load('x.png')
o_img = pg.image.load('o.png')

#resizing images
x_img = pg.transform.scale(x_img, (80,80))
o_img = pg.transform.scale(o_img, (80,80))
opening = pg.transform.scale(opening, (width,height))

def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(2.5)
    screen.fill(white)

    # Drawing vertical lines
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height*7/8),7)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height*7/8),7)
    # Drawing horizontal lines
    pg.draw.line(screen,line_color,(0,height*7/24),(width, height*7/24),7)
    pg.draw.line(screen,line_color,(0,height*14/24),(width, height*14/24),7)
    draw_status()
    
def draw_status():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game Draw!'

    font = pg.font.Font(None, 72)
    text = font.render(message, 1, (0, 255, 255))
    # copy the rendered message onto the board
    screen.fill ((0, 0, 0), (0, height*7/8, width,height*7/8))
    text_rect = text.get_rect(center=(width/2, height*15/16))
    screen.blit(text, text_rect)
    pg.display.update()
    
def check_win():
    global TTT, winner,draw

    # check for winning rows
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            pg.draw.line(screen, (255,0,0), (0, (2*row +1)*height*7/48),(width, (2*row + 1)*height*7/48), 4)
            break

    # check for winning columns
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            #draw winning line
            pg.draw.line (screen, (250,0,0),((col + 1)* width/3 - width/6, 0),\
                          ((col + 1)* width/3 - width/6, height), 4)
            break

    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pg.draw.line (screen, (250,70,70), (0, 0), (width,height*7/8), 4)

    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pg.draw.line (screen, (250,70,70), (width, 00), (0, height*7/8), 4)

    if(all([all(row) for row in TTT]) and winner is None ):
        draw = True
    draw_status()
    
def drawXO1(row,col):
    global TTT,XO
    if col==1:
        posy = width/6
    if col==2:
        posy = width/2
    if col==3:
        posy = width*5/6

    if row==1:
        posx = height*7/48
    if row==2:
        posx = height*21/48
    if row==3:
        posx = height*35/48
    TTT[row-1][col-1] = XO
    if(XO == 'x'):
        img_rect= x_img.get_rect(center=(posy,posx))
        screen.blit(x_img,img_rect)
        XO= 'o'
    else:
        img_rect= o_img.get_rect(center=(posy,posx))
        screen.blit(o_img,img_rect)
        XO= 'x'
    pg.display.update()
    #print(posx,posy)
    #print(TTT)
    
def userClick():
        x,y = pg.mouse.get_pos()
        if(x<width/3):
            col = 1
        elif (x<width/3*2):
            col = 2
        elif(x<width):
            col = 3
        else:
            col = None

    #get row of mouse click (1-3)
        if(y<height/3):
            row = 1
        elif (y<height/3*2):
            row = 2
        elif(y<height):
            row = 3
        else:
            row = None
    #print(row,col)

        if(row and col and TTT[row-1][col-1] is None):
            global XO1

        #draw the x or o on screen
            drawXO1(row,col)
            check_win()
        
def reset_game():
            global TTT, winner,XO, draw
            time.sleep(3)
            XO1 = 'x'
            draw = False
            game_opening()
            winner=None
            TTT = [[None]*3,[None]*3,[None]*3]
            
game_opening()

# run the game loop forever
while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            userClick()
            if(winner or draw):
                reset_game()

    pg.display.update()
    CLOCK.tick(fps)