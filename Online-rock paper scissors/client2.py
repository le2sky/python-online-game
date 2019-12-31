import pygame
from network import Network
import socket
import pickle
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from gameinfo import GameInfo
from pygame.locals import *
import time
hostname = None
def getHostName():
    def getValue():
        global hostname
        hostname =str(hostname_entry.get())
        win.destroy()


    win = Tk()
    win.title("WELLCOME TO SKYGAME!")
    win.resizable(False, False)
    win.geometry("400x400+600+150")
    image = tkinter.PhotoImage(file="img/logo.png")
    label = tkinter.Label(win, image=image)
    label.pack()
    progressbar = tkinter.ttk.Progressbar(win, maximum=100, mode="indeterminate",length=250)
    progressbar.pack()
    progressbar.start(10)
    hostname_text = tkinter.Label(win, text="호스트 IP 설정 : ")
    hostname_text.place(x= 70, y= 255)
    hostname_entry = tkinter.Entry(win)
    hostname_entry.place(x=180 , y= 255)
    button = tkinter.Button(win, text="게임시작!", width=35,height=2, command=getValue, fg="white", bg="skyblue")
    button.place(x=70, y=290)

    infotext = tkinter.Label(win, text="20180709 컴퓨터소프트웨어공학과 이하늘 2019-1 파이썬 프로젝트")
    infotext.pack(side="bottom")

    win.mainloop()



getHostName()

pygame.font.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client2")
wait_sound = pygame.mixer.Sound("music/wait.wav")
waiting_img = pygame.image.load('img/wating.png')
you_img =pygame.image.load("img/you.png")
gameback = pygame.image.load("img/gamebackground.png")
p1_Score = 0
p2_Score = 0

Score_font = pygame.font.SysFont("comicsans", 40)
vsfont = pygame.font.SysFont("comicsans", 80)
vstext = vsfont.render("VS", 1, (255, 0, 0))
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((hostname,1234))
gameInfo = pickle.loads(s.recv(1024))
s.close()
gameround = int(gameInfo.game_round)
p1_id = gameInfo.p1_id
p2_id = gameInfo.p2_id
myChr =""
atChr = ""
playerMyChr = ""
playerAtChr = ""
backgroundmusic = gameInfo.music
pygame.mixer.music.load(backgroundmusic)

n = None
finalwinner ="0"




def getChrUrl(chr1,chr2, p):
    global playerAtChr, playerMyChr
    if p == 0:
        if chr1 =="dora":
            playerMyChr = "img/doraemon0.png"
        elif chr1 =="na":
            playerMyChr = "img/naruto0.png"
        elif chr1 =="son":
            playerMyChr = "img/goku0.png"
        elif chr1 =="be":
            playerMyChr ="img/begi0.png"

        if chr2 == "dora":
            playerAtChr = "img/doraemon1.png"
        elif chr2 == "na":
            playerAtChr = "img/naruto1.png"
        elif chr2 == "son":
            playerAtChr = "img/goku1.png"
        elif chr2 == "be":
            playerAtChr = "img/begi1.png"

    elif p == 1:
        if chr2 == "dora":
            playerMyChr = "img/doraemon0.png"
        elif chr2 == "na":
            playerMyChr = "img/naruto0.png"
        elif chr2 == "son":
            playerMyChr = "img/goku0.png"
        elif chr2 == "be":
            playerMyChr = "img/begi0.png"

        if chr1 == "dora":
            playerAtChr = "img/doraemon1.png"
        elif chr1 == "na":
            playerAtChr = "img/naruto1.png"
        elif chr1 == "son":
            playerAtChr = "img/goku1.png"
        elif chr1 == "be":
            playerAtChr = "img/begi1.png"


def getScore(result):
    # 만약 player가 0이라면 p1
    # 1이면 p2
    global p1_Score
    global p2_Score
    if result == 0:
        p1_Score += 1
    if result == 1:
        p2_Score += 1


def drawScore(p):
    if p == 0:
        Score_string1 = p1_id + " score :" + str(p1_Score)
        Score_text1 = Score_font.render(Score_string1, 1, (0, 0, 0))
        win.blit(Score_text1, (20, 0))
        Score_string2 = p2_id +" score :" + str(p2_Score)
        Score_text2 = Score_font.render(Score_string2, 1, (0, 0, 0))
        win.blit(Score_text2, (445, 0))

    if p == 1:
        Score_string1 = p2_id + " score :" + str(p2_Score)
        Score_text1 = Score_font.render(Score_string1, 1, (0, 0, 0))
        win.blit(Score_text1, (0, 0))
        Score_string2 = p1_id + " score :" + str(p1_Score)
        Score_text2 = Score_font.render(Score_string2, 1, (0, 0, 0))
        win.blit(Score_text2, (445, 0))


def isEndGame(player):
    global finalwinner
    # 만약 너가 p1 이야 ==> player == 0 이면
    # if p1 score == round :
    # print("게임에서 승리하셨습니다.")
    # elif p2 score == round :
    # print("게임에서 패배했습니다")

    # 만약 너가 p2 이야 ==> player == 1 이면
    # if p2 score == round :
    # print("게임에서 승리하셨습니다.")
    # elif p1 score == round :
    # print("게임에서 패배했습니다")

    if p1_Score == gameround or p2_Score == gameround:

        win.fill((255, 255, 255))
        end_font = pygame.font.SysFont("comicsans", 60)
        end_font2 = pygame.font.SysFont("comicsans", 30)
        end_string1 = "You were defeated in the game"
        end_string2 = "You won the game"
        if player == 0:
            if p1_Score == gameround : #player1 승리
                text = end_font.render(end_string2, 1, (0, 0, 0))
                win.blit(text, (150,330))
                pygame.display.update()
                finalwinner = "1"

            elif p2_Score == gameround : #player2 승리
                text = end_font.render(end_string1, 1, (0, 0, 0))
                win.blit(text, (50, 330))
                pygame.display.update()
                finalwinner = "2"

        if player == 1:
            if p2_Score == gameround:
                text = end_font.render(end_string2, 1, (0, 0, 0))
                win.blit(text, (150, 330))
                pygame.display.update()


            elif p1_Score == gameround:
                text = end_font.render(end_string1, 1, (0, 0, 0))
                win.blit(text, (50, 330))
                pygame.display.update()

        if finalwinner == "1" or finalwinner == "2":
            n.send(finalwinner)

        text = end_font2.render("The game will be  end after 5 seconds.",1, (255,0,0))
        win.blit(text, (150, 380))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):

    win.blit(gameback,(0,0))
    #win.blit(background, (0, 0))
    win.blit(myChr, (60,150))
    win.blit(atChr, (400,150))
    win.blit(vstext, (300,230))
    win.blit(you_img, (280,80))
    if not (game.connected()):
        # font = pygame.font.SysFont("comicsans", 80)
        # text = font.render("Waiting for Player...", 1, (255,0,0), True)
        # win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        win.blit(waiting_img, (0, 0))

    else:
        pygame.mixer.music.unpause()
        font = pygame.font.SysFont("comicsans", 60)


        if p == 0:
            text = font.render(p1_id, 1, (79, 139, 254))
            win.blit(text, (60, 70))

            text = font.render(p2_id, 1, (79, 139, 254))
            win.blit(text, (400, 70))

        elif p == 1:
            text = font.render(p2_id, 1, (79, 139, 254))
            win.blit(text, (60, 70))

            text = font.render(p1_id, 1, (79, 139, 254))
            win.blit(text, (400, 70))

        drawScore(p)

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)

        if game.bothWent():
            text1 = font.render(move1, 1, (255,255,255))
            text2 = font.render(move2, 1, (255,255,255))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (255,255,255))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (255,255,255))
            else:
                text1 = font.render("Waiting...", 1, (255,255,255))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (255,255,255))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (255,255,255))
            else:
                text2 = font.render("Waiting...", 1, (255,255,255))

        if p == 1:
            win.blit(text2, (100, 400))
            win.blit(text1, (400, 400))
        else:
            win.blit(text1, (100, 400))
            win.blit(text2, (400, 400))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (1, 193, 239)), Button("Scissors", 250, 500, (1, 193, 239)),
        Button("Paper", 450, 500, (1, 193, 239))]


def main():
    global myChr, atChr, finalwinner, n
    run = True
    clock = pygame.time.Clock()
    n = Network(hostname)
    player = int(n.getP())
    print("You are player", player)
    getChrUrl(gameInfo.p1_chr,gameInfo.p2_chr, player)
    myChr = pygame.image.load(playerMyChr)
    atChr = pygame.image.load(playerAtChr)
    while run:

        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Win!", 1, (255, 0, 0))
                result = game.winner()
                getScore(result)

            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0))
            else:
                text = font.render("You Lose...", 1, (255, 0, 0))
                result = game.winner()
                getScore(result)

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(3000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)
        ##
        isEndGame(player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()
    background = pygame.image.load('img/background.png')
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        win.blit(background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.pause()
                pygame.mixer.Sound.play(wait_sound)
                run = False

    main()


while True:
    menu_screen()








