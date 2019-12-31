class Game:
    def __init__(self, id):
        self.p1Went = False  #p1 game flag
        self.p2Went = False #p2 game flag
        self.ready = False
        self.id = id # 0번
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p): #player 가 선택한 값(가위,바위,보)를 리턴
        """
        :param p: [0,1]
        :return: Move
        """
        return self.moves[p]

    def play(self, player, move): #플레이어가 값을 입력하면 Went 값이 true 로 바뀐다.
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self): #통신에 접속되어 준비가 된 상태인지에 대한 상태값을 리턴하는 함수다.
        return self.ready

    def bothWent(self): # 모든 플레이어가 값(가위,바위,보)를  입력했는지에 대한 판단
        return self.p1Went and self.p2Went

    def winner(self): # 승리자를 판단한다. game객체의 moves 배열에 양쪽 클라이언트에 대한 값을 저장한다.

        p1 = self.moves[0].upper()[0] # 앞글자를 따와 대문자로 변경
        p2 = self.moves[1].upper()[0] # 예컨데 rock 이 저장되어있으면 p2 = "R" 이다
        winner = -1 #winner 초기값
        if p1 == "R" and p2 == "S":
            winner = 0 # 플레이어 1 승리
        elif p1 == "S" and p2 == "R":
            winner = 1 # 플레이어 2 승리
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1
        return winner
    def resetWent(self): #한판 끝나면 went 값 초기화
        self.p1Went = False
        self.p2Went = False