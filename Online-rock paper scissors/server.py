import socket
from _thread import *
import pickle
from game import Game
from gameinfo import GameInfo
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime
DBcount = 0
Lostindex = 0;
hostname =""
gameround = ""
player1_id = ""
player2_id = ""
player1_chr = ""
player2_chr =""
bgm = ""
winner = ""
now = datetime.now()

def getToday(nowObj): #오늘의 날짜를 20190614 형식으로  바꾸는 함수
    y = str(nowObj.year)
    m = nowObj.month
    d = nowObj.day
    if m < 10:
        m = "0" + str(m)

    if d < 10:
        d = "0" + str(d)

    today = str(y) + str(m)  + str(d)
    return str(today)


todaydate = getToday(now)
print ("오늘의 날짜 :" , todaydate)




def getSave(): #데이터를 저장하는 함수이다.
    con = sqlite3.connect("sqlite/gameDB")
    cur = con.cursor()
    data1 = player1_id
    data2 = player2_id
    player2chr_temp = player2_chr
    player1chr_temp = player1_chr

    if player1chr_temp == "dora":
        data3 = "도라에몽"
    elif player1chr_temp == "na":
        data3 = "나루토"
    elif player1chr_temp == "son":
        data3 = "손오공"
    elif player1chr_temp == "be":
        data3 = "베지터"

    if player2chr_temp == "dora":
        data4 = "도라에몽"
    elif player2chr_temp == "na":
        data4 = "나루토"
    elif player2chr_temp == "son":
        data4 = "손오공"
    elif player2chr_temp == "be":
        data4 = "베지터"

    data5 = gameround


    if winner == "player1 is winner":
        data6  = player1_id
    if winner == "player2 is winner":
        data6 = player2_id
    data7 = todaydate

    sql = "INSERT INTO gameData VALUES ('"+ data1 + "', '" + data2 + "', '" + data3 + "','" + data4 + "','" +data5 + "','" + data6 + "'," +data7+")"
    cur.execute(sql)
    con.commit()
    con.close()

win = None
def serverBoard(): #서버 보드를 실행하는 함수이다.
    if win == None:
        pass
    else :
        win.destroy()

    global hostname, gameround, player1_id, player2_id, player1_chr, player2_chr, bgm
    #--내부함수
    def getVersion(): # 버전 확인 함수
        version  = "버전 정보 : v1.3\n최종 수정일 : 2019/06/11 01:58 AM\n" \
                   "1.0 : 기본 가위바위보 형식 및 라운드 설정 구현\n" \
                   "1.1 : 캐릭터, 배경음악, 사용자 아이디 설정 가능, 서버 설정 유저 인터페이스 추가\n" \
                   "1.2 : DB연동 및 조회 기능 추가\n" \
                   "1.3 : 리더보드 인터페이스 구현, 사용자 접속 인터페이스 구현"
        messagebox.showinfo("버전 정보", version)

    def skytemp(): #데이터를 조회하는 함수이다.
        window.destroy()
        global  DBcount,win
        #messagebox.showinfo("notice", "개발중입니다.")
        con = sqlite3.connect("sqlite/gameDB")
        cur = con.cursor()
        cur.execute("select * from gameData")
        win = Tk()
        win.title("reader board")
        win.resizable(False, False)

        image = tkinter.PhotoImage(file="img/logo.png")
        label = tkinter.Label(win, image=image)
        label.pack()
        but1 = tkinter.Button(win, text="뒤로가기", width=15, command=serverBoard, fg ='white', bg ='skyblue')
        but2 = tkinter.Button(win, text="종료", width=15, command=win.destroy,fg ='white', bg ='skyblue')

        but1.place(x= 450, y= 150)
        but2.place(x=450, y=180)
        #(1, 193, 239)배경
        #(0,0,0)


        text = tkinter.Label(win, text="|  player1 id  |   player2 id  |   player1 chr   |  player2 chr  | GameRound |      winner     |      date      |")
        listbox1 = tkinter.Listbox(win, selectmode='extended', height=30, width=10)
        listbox2 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        listbox3 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        listbox4 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        listbox5 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        listbox6 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        listbox7 = tkinter.Listbox(win, selectmode='extended', height=20, width=10)
        while True:
            row = cur.fetchone()
            if row == None:
                break
            data1 = row[0]
            data2 = row[1]
            data3 = row[2]
            data4 = row[3]
            data5 = str(row[4])
            data6 = row[5]
            data7 = str(row[6])

            listbox1.insert(DBcount, data1)
            listbox2.insert(DBcount, data2)
            listbox3.insert(DBcount, data3)
            listbox4.insert(DBcount, data4)
            listbox5.insert(DBcount, data5)
            listbox6.insert(DBcount, data6)
            listbox7.insert(DBcount, data7)

            DBcount+=1
        con.close()
        text.place(x=10, y= 240)
        listbox1.place(x=10 , y= 260)
        listbox2.place(x=90 , y=260)
        listbox3.place(x=170, y=260)
        listbox4.place(x=250, y=260)
        listbox5.place(x=330, y=260)
        listbox6.place(x=410, y=260)
        listbox7.place(x=490, y=260)
        win.geometry("600x600+600+150")
        win.mainloop()
    def getValue(): # 게임정보에 대한 값을 서버보드에 입력된 값으로부터 받아오는 역할을 한다.
        global hostname, gameround, player1_id, player2_id, player1_chr, player2_chr, bgm
        hostname = str(hostname_entry.get())
        gameround = str(round_entry.get())
        player1_id = p1_entry.get()
        player2_id = p2_entry.get()
        bgmtemp = music1.get()
        if bgmtemp =="이정희-가위바위보":
            bgm = "music/background_music1.mp3"

        elif bgmtemp == "별의커비 테마 음악":
            bgm = "music/background_music2.mp3"

        elif bgmtemp == "어벤져스 테마 음악":
            bgm = "music/background_music3.mp3"

        elif bgmtemp == "Sub Urban - Cradles":
            bgm = "music/background_music4.mp3"
        chr1temp = cr1.get()
        chr2temp = cr2.get()
#player 1
        if chr1temp == "도라에몽":
            player1_chr ="dora"
        elif chr1temp =="손오공":
            player1_chr ="son"
        elif chr1temp == "나루토":
            player1_chr = "na"
        elif chr1temp == "베지터":
            player1_chr = "be"
#player 2
        if chr2temp == "도라에몽":
            player2_chr = "dora"
        elif chr2temp == "손오공":
            player2_chr = "son"
        elif chr2temp == "나루토":
            player2_chr = "na"
        elif chr2temp == "베지터":
            player2_chr = "be"
        window.destroy()
#--내부함수

    window = tkinter.Tk()
    window.title("server board")
    window.geometry("400x400+600+150")
    window.resizable(False, False)

    gamesettext= tkinter.Label(window, text="게임 설정")
    gamesettext.pack(side ="top")

    hostname_text = tkinter.Label(window, text="호스트 IP 설정 : ")
    hostname_text.place(x= 70, y= 30)
    hostname_entry = tkinter.Entry(window)
    hostname_entry.place(x=180 , y= 30)

    round_text = tkinter.Label(window, text="게임 승리 점수 설정 : ")
    round_text.place(x=40, y=60)
    round_entry = tkinter.Entry(window)
    round_entry.place(x=180, y=60)

    notice_text = tkinter.Label(window, text= "플레이어 이름은 영문자(1~8 글자)로 설정해주세요.")
    notice_text.place(x=50,y=100)
    p1_text = tkinter.Label(window, text ="플레이어1 이름 설정 :")
    p1_text.place(x = 30,y= 140)
    p1_entry = tkinter.Entry(window)
    p1_entry.place(x= 20, y= 160)

    vs_text = tkinter.Label(window, text="VS")
    vs_text.place(x =183,y=150)

    p2_text = tkinter.Label(window, text="플레이어2 이름 설정 :")
    p2_text.place(x=230, y=140)
    p2_entry = tkinter.Entry(window)
    p2_entry.place(x=220, y=160)

    cr1_text = tkinter.Label(window, text="< 플레이어1 캐릭터 설정 >")
    cr1_text.place(x= 15, y= 190)

    cr2_text = tkinter.Label(window, text="< 플레이어2 캐릭터 설정 >")
    cr2_text.place(x=215, y=190)

    cr1 = StringVar()
    crbox1 = ttk.Combobox(textvariable = cr1, width= 15)
    crbox1['value'] = ('도라에몽','손오공','나루토','베지터')
    crbox1.place(x= 28, y= 220)

    cr2 = StringVar()
    crbox2 = ttk.Combobox(textvariable=cr2, width=15)
    crbox2['value'] = ('도라에몽', '손오공', '나루토', '베지터')
    crbox2.place(x=224, y=220)


    music_text = Label(window, text ="배경음악(BGM) 설정 : ")
    music_text.place(x= 30 ,y= 260)
    music1 = StringVar()
    musicbox = ttk.Combobox(textvariable = music1 , width =30)
    musicbox['value'] =('이정희-가위바위보','별의커비 테마 음악','어벤져스 테마 음악','Sub Urban - Cradles')
    musicbox.place(x=32, y= 280)




    button = tkinter.Button(window, text="서버실행", width=50, command=getValue)
    button2 = tkinter.Button(window, text="리더 보드 확인", width=50, command=skytemp)
    button3 = tkinter.Button(window, text="버전 정보 확인", width=50, command=getVersion)
    button.pack(side = "bottom")
    button2.pack(side="bottom")
    button3.pack(side="bottom")
    window.mainloop()

    gameinfo = GameInfo(gameround, player1_id, player2_id, player1_chr, player2_chr, bgm) #게임인포의 객체를 생성

    test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 객체 생성 //게임정보를 클라이언트에게 전달할 용도이다.
    try:
        test.bind((hostname, port2))
        # 호스트 이름과 포트번호를 튜플로 감싸서 전달한다. (바인딩 행위)
        # 바인드는 프로그램 인터페이스인 소켓과 네트워크 자원인 포트를 연결하는 행위이다.
    except socket.error as e:
        str(e)
        # socket error 을 catch 하는 부분이다.
    test.listen(2)
    # 클라이언트가 바인드된 포트로 연결을 할 때까지 기다리는 블럭킹 함수이다.
    # 블럭킹 함수 : 자신의 수행결과가 끝날 때까지 제어권을 가진다.
    # temp  = bytearray(gameInfo,'utf-8')
    index = 0
    while index != 2:  # 두명의 접속만 허용
        c, ad = test.accept()
        c.sendall(pickle.dumps(gameinfo))
        index += 1
    c.close()
    return gameinfo


#소켓은 응용 프로그램에서 TCP/IP를 이용하는 창구 역할을 하며
# 응용 프로그램과 소켓 사이의 인터페이스를 소켓 인터페이스라고 한다.
#hostname = "192.168.0.144" #서버 ip주소
port = 5555 # 포트번호
port2=1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #소켓 객체 생성
# 인자 1 = 패밀리, 인자 2 = 타입
# 소켓의 패밀리란, “택배상자에 쓰는 주소 체계가 어떻게 되어 있느나”에 관한 것
# AF_INET = IPv4 에서 사용
# 타입은 소켓의 타입이다. raw소켓, 스트림소켓, 데이터그램 소켓 등 있다.
# 보통 스트림과 데이터그램 소켓이 많이 사용된다.
# 동작 과정
# 1. 소켓 객체 생성
# 2. 소켓을 포트에 맵핑, 상대측 포트에 연결
# (1) 서버는 소켓을 만들고 포트에 맵핑한 다음 *소켓을 포트에 맵핑하는 행위 => 바인딩
# (2) 클라이언트가 접속하기를 기다린다.


gameInfo = serverBoard()





try:
    s.bind((hostname, port))
    # 호스트 이름과 포트번호를 튜플로 감싸서 전달한다. (바인딩 행위)
    # 바인드는 프로그램 인터페이스인 소켓과 네트워크 자원인 포트를 연결하는 행위이다.
except socket.error as e:
    str(e)
    # socket error 을 catch 하는 부분이다.

s.listen(2)

print("서버 실행 : 클라이언트를 기다리는 중입니다.")


games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    # 인자 : conn : 소켓객체
    # p =1
    # gameId= 0
    global idCount, winner, Lostindex
    #접속자 수
    conn.send(str.encode(str(p)))
    # p를 스트링으로 변환한 후 인코딩하여 소켓에 전달
    # send 메소드는 반환값이 존재 => 실제 전송된 바이트 수
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            # 소켓으로부터 데이터 읽어오되, 문자열이라면 디코딩 행위를 해줘야함
            #
            if gameId in games:
                game = games[gameId]

                if not data: #데이터가 없으면  break
                    print(data)
                    break
                else: #데이터가 있으면
                    if data == "reset": #데이터가 리셋이면
                        print(data)
                        game.resetWent() #리셋원트함수
                    elif data == "1": #승리자정보를 소켓으로 부터 읽어와서 최종 우승자를 서버에 저장한다.
                        winner = "player1 is winner"
                        print(winner)
                    elif data =="2":
                        winner = "player2 is winner"
                        print(winner)
                    elif data != "get":
                        print(data)
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    Lostindex +=1
    if Lostindex == 2:
        print("데이터를 저장합니다.")
        getSave()
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:

    conn, addr = s.accept() # 서버의 리스닝 행위에 대한 클라이언트의 해당 연결을 받아들이기 위함
    # accept() 함수는 (소켓, 주소정보)로 구성되는 튜플을 리턴한다.
    # 처음에 생성된 소켓과는 별개의 객체로 클라이언트와 연결이 구성되어 실제로 데이터를 주고 받을 수 있는
    # 창구가 된다.
    print("Connected to:", addr)
    # 접속된 클라이언트 정보
    idCount += 1 # 접속 유저


    p = 0

    gameId = (idCount - 1)//2
    # 게임 번호
    if idCount % 2 == 1:
        #player가 한명이라면
        games[gameId] = Game(gameId) #
        #print("idCount =", idCount)
        #print("gameId =", gameId)
        print("Creating a new game...")
        print(conn)
        print(addr)
        print(p)
    else:
        print("start game")
        #print("idCount =", idCount)
        #print("gameId =", gameId)
        games[gameId].ready = True
        p = 1
        print(conn) # 소켓 객체
        print(addr)
        print(p)
    start_new_thread(threaded_client, (conn, p, gameId))

