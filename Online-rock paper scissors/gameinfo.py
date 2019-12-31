class GameInfo :
    def __init__(self, round , p1, p2, p1chr, p2chr, bgm):
        self.game_round = round
        self.p1_id  = p1
        self.p2_id  = p2
        self.p1_chr = p1chr
        self.p2_chr = p2chr
        self.music = bgm