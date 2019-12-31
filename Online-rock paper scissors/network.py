import socket
import pickle

class Network:
    def __init__(self, hostname):
        #생성자 ,
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #생성한 객체에 대한, 소켓  객체를 선언
        self.server = hostname # 호스트 네임 _  프로그램 실행중에 매개변수로 받아온다.
        self.port = 5555 #포트번호
        self.addr = (self.server, self.port) #서버의 호스트이름과, 포트번호를 튜플로 묶는다.
        self.p = self.connect() #해당 객체에 connect method 를 실행해 리턴값을 p에 대입한다
        #self.p는 getP 함수 (플레이어 번호를 리턴하는 함수 추후에 게임을 하는 중 이 값을 통해 진행한다.

    def getP(self): # 플레이어 번호를 리턴하는 함수
        return self.p

    def connect(self): #현 클래스로 선언된 객체의 소켓 객체의 connect 함수를 사용 (아까 만들었던 튜플에)
        # 해당 소켓객체는 해당 주소에 연결된다.
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode() ## 소켓에서 player번호 받아오기
        except:
            pass

    def send(self, data): #값을 전달하는 함수
        try:
            self.client.send(str.encode(data)) #data를 인코딩해서 소켓객체의 send함수로  전달한다.
            print(data)
            return pickle.loads(self.client.recv(2048*2)) # 갹체를 전달하기 위해 pickle 모듈을 사용해
                                                         # 직렬화(dump 함수)한 것을 받기위해 역직렬화한다.
        except socket.error as e:
            print(e)