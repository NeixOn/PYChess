import chess.engine as stock
from sys import platform
import chess
import math as M
"""if(platform == "linux" or platform == "linux2"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_linux_x64_avx2/stockfish_15_x64_avx2")
    pass
elif(platform == "darwin"):
    pass
elif(platform == "win32"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_x64_avx2.exe")
    pass
"""
class GameState():
    def __init__(self):

        self.board = {
            "a8": "r", "b8": "n", "c8": "b", "d8": "q", "e8": "k", "f8": "b", "g8": "n", "h8": "r",
            "a7": "p", "b7": "p", "c7": "p", "d7": "p", "e7": "p", "f7": "p", "g7": "p", "h7": "p",
            "a6": ".", "b6": ".", "c6": ".", "d6": ".", "e6": ".", "f6": ".", "g6": ".", "h6": ".",
            "a5": ".", "b5": ".", "c5": ".", "d5": ".", "e5": ".", "f5": ".", "g5": ".", "h5": ".",
            "a4": ".", "b4": ".", "c4": ".", "d4": ".", "e4": ".", "f4": ".", "g4": ".", "h4": ".",
            "a3": ".", "b3": ".", "c3": ".", "d3": ".", "e3": ".", "f3": ".", "g3": ".", "h3": ".",
            "a2": "P", "b2": "P", "c2": "P", "d2": "P", "e2": "P", "f2": "P", "g2": "P", "h2": "P",
            "a1": "R", "b1": "N", "c1": "B", "d1": "Q", "e1": "K", "f1": "B", "g1": "N", "h1": "R"
        }

        self.law = {
            18: "a8", 28: "b8", 38: "c8", 48: "d8", 58: "e8", 68: "f8", 78: "g8", 88: "h8",
            17: "a7", 27: "b7", 37: "c7", 47: "d7", 57: "e7", 67: "f7", 77: "g7", 87: "h7",
            16: "a6", 26: "b6", 36: "c6", 46: "d6", 56: "e6", 66: "f6", 76: "g6", 86: "h6",
            15: "a5", 25: "b5", 35: "c5", 45: "d5", 55: "e5", 65: "f5", 75: "g5", 85: "h5",
            14: "a4", 24: "b4", 34: "c4", 44: "d4", 54: "e4", 64: "f4", 74: "g4", 84: "h4",
            13: "a3", 23: "b3", 33: "c3", 43: "d3", 53: "e3", 63: "f3", 73: "g3", 83: "h3",
            12: "a2", 22: "b2", 32: "c2", 42: "d2", 52: "e2", 62: "f2", 72: "g2", 82: "h2",
            11: "a1", 21: "b1", 31: "c1", 41: "d1", 51: "e1", 61: "f1", 71: "g1", 81: "h1"
        }

        self.reverse_law = {
            "a8": 18, "b8": 28, "c8": 38, "d8": 48, "e8": 58, "f8": 68, "g8": 78, "h8": 88,
            "a7": 17, "b7": 27, "c7": 37, "d7": 47, "e7": 57, "f7": 67, "g7": 77, "h7": 87,
            "a6": 16, "b6": 26, "c6": 36, "d6": 46, "e6": 56, "f6": 66, "g6": 76, "h6": 86,
            "a5": 15, "b5": 25, "c5": 35, "d5": 45, "e5": 55, "f5": 65, "g5": 75, "h5": 85,
            "a4": 14, "b4": 24, "c4": 34, "d4": 44, "e4": 54, "f4": 64, "g4": 74, "h4": 84,
            "a3": 13, "b3": 23, "c3": 33, "d3": 43, "e3": 53, "f3": 63, "g3": 73, "h3": 83,
            "a2": 12, "b2": 22, "c2": 32, "d2": 42, "e2": 52, "f2": 62, "g2": 72, "h2": 82,
            "a1": 11, "b1": 21, "c1": 31, "d1": 41, "e1": 51, "f1": 61, "g1": 71, "h1": 81
        }


        self.boardReverse = {
            "a8": "R", "b8": "N", "c8": "B", "d8": "Q", "e8": "K", "f8": "B", "g8": "N", "h8": "R",
            "a7": "P", "b7": "P", "c7": "P", "d7": "P", "e7": "P", "f7": "P", "g7": "P", "h7": "P",
            "a6": ".", "b6": ".", "c6": ".", "d6": ".", "e6": ".", "f6": ".", "g6": ".", "h6": ".",
            "a5": ".", "b5": ".", "c5": ".", "d5": ".", "e5": ".", "f5": ".", "g5": ".", "h5": ".",
            "a4": ".", "b4": ".", "c4": ".", "d4": ".", "e4": ".", "f4": ".", "g4": ".", "h4": ".",
            "a3": ".", "b3": ".", "c3": ".", "d3": ".", "e3": ".", "f3": ".", "g3": ".", "h3": ".",
            "a2": "p", "b2": "p", "c2": "p", "d2": "p", "e2": "p", "f2": "p", "g2": "p", "h2": "p",
            "a1": "r", "b1": "n", "c1": "b", "d1": "q", "e1": "k", "f1": "b", "g1": "n", "h1": "r"
        }


        self.boardCBH = {
            "a8": "r1", "b8": "n1", "c8": "b1", "d8": "q1", "e8": "k", "f8": "b2", "g8": "n2", "h8": "r2",
            "a7": "p1", "b7": "p2", "c7": "p3", "d7": "p4", "e7": "p5", "f7": "p6", "g7": "p7", "h7": "p8",
            "a6": ".", "b6": ".", "c6": ".", "d6": ".", "e6": ".", "f6": ".", "g6": ".", "h6": ".",
            "a5": ".", "b5": ".", "c5": ".", "d5": ".", "e5": ".", "f5": ".", "g5": ".", "h5": ".",
            "a4": ".", "b4": ".", "c4": ".", "d4": ".", "e4": ".", "f4": ".", "g4": ".", "h4": ".",
            "a3": ".", "b3": ".", "c3": ".", "d3": ".", "e3": ".", "f3": ".", "g3": ".", "h3": ".",
            "a2": "P1", "b2": "P2", "c2": "P3", "d2": "P4", "e2": "P5", "f2": "P6", "g2": "P7", "h2": "P8",
            "a1": "R1", "b1": "N1", "c1": "B1", "d1": "Q1", "e1": "K", "f1": "B2", "g1": "N2", "h1": "R2"
        }




        self.figure_for_black = ["q", "k", "b", "n", "r", "p"] #список фигур черных
        self.figure_for_white = ["Q", "K", "B", "N", "R", "P"] #список фигур белых
        self.figure_for_move = ["Q", "K", "B", "N", "R", "P"]
        self.color = 1 # 1 - ход белых, 0 - ход черных
        self.whiteToMove = True
        self.movelog = []
        self.ruckingBlack = 1
        self.ruckingWhite = 1

    def output(self): # Вывод доски
        print("___________________")
        for i in range(8, 0, -1):
            for j in range(1, 9, 1):
                if(j == 1):
                    print("\n|", end=" ")
                print(self.translateNumberInPiece(j, i), end=" ")
                if(j == 8):
                    print("|", end="")
        print("\n___________________")


    def convertorMove(self, x, y, step): # Изменяет ход на x по оси OX и на y по оси OY
        return self.law[self.reverse_law[step[2:]] + x*10 + y]
    

    def copyBoard(self, copyboard):
        copyboard = str(copyboard)
        for i in range(1, 9, 1):
            for j in range(1, 9, 1):
                self.board[self.law[(j)*10 + 9-i]] = copyboard[((i-1)*8+j-1)*2]
        self.output()


    def move(self, step, figure, pName = None): # Ход - изменяет исходную доску
        step = str(step) # Ход типа e2e4

########### Взятие пешки на проходе ( Для оптимизации можно сравнивать буквы, если буква будет другая и дальше пусто то значит на проходе)
        if(figure == 'P'):
            print(self.reverse_law[step[:2]] - self.reverse_law[step[2:]])
            if(self.reverse_law[step[:2]] - self.reverse_law[step[2:]] == -11 and self.board[step[2:]] == '.'):
                self.board[self.convertorMove(0, -1, step)] = '.'
            elif(self.reverse_law[step[:2]] - self.reverse_law[step[2:]] == 9 and self.board[step[2:]] == '.'):
                self.board[self.convertorMove(0, -1, step)] = '.'
                
        if(figure == 'p'):
            print(self.reverse_law[step[:2]] - self.reverse_law[step[2:]])
            if(self.reverse_law[step[:2]] - self.reverse_law[step[2:]] == 11 and self.board[step[2:]] == '.'):
                self.board[self.convertorMove(0, 1, step)] = '.'
            elif(self.reverse_law[step[:2]] - self.reverse_law[step[2:]] == -9 and self.board[step[2:]] == '.'):
                self.board[self.convertorMove(0, 1, step)] = '.'


###########




        self.movelog.append(step)
        old = step[:2]
        new = step[2:]
        print("old = ",old)
        print("new = ",new)
        self.board[new] = figure
        self.board[old] = "."




###### Пешка дошла до 8 горизонтали или 1

        if(figure == 'P'):
            if(step[3] == '8'):
                self.board[new] = pName.title()
        elif(figure == 'p'):
            print("PFDJKLSJGLKSEDHJLGKESHJIOGHJSDIOLGHJ")
            if(step[3] == '1'):
                self.board[new] = pName
######
######### Ракировка
        if(figure == 'K' and self.ruckingWhite == 1):
            if(step == 'e1g1'):
                self.board['h1'] = '.'
                self.board['f1'] = 'R'
            elif(step == 'e1c1'):
                self.board['a1'] = '.'
                self.board['d1'] = 'R'
            else:
                self.ruckingWhite = 0

        if(figure == 'k' and self.ruckingBlack == 1):
            if(step == 'e8g8'):
                self.board['h8'] = '.'
                self.board['f8'] = 'r'
            elif(step == 'e8c8'):
                self.board['a8'] = '.'
                self.board['d8'] = 'r'
            else:
                self.ruckingBlack = 0
###########




        if(self.color == 1):
            self.color = 0
            self.figure_for_move = ["q", "k", "b", "n", "r", "p"]
        else:
            self.color = 1
            self.figure_for_move = ["Q", "K", "B", "N", "R", "P"]

    def translateNumberInPiece(self, posX, posY): # Перевод из позиции XY в фигуру стоящую на этом месте
        number = posX * 10 + posY
        q = self.law[number]
        return self.board[q]
    
    
    
    def translatePositionInMove(self, posX_UP, posY_UP, posX_DOWN, posY_DOWN): # Перевод из позиций XY в ход
        if(posX_UP > 8 or posX_UP < 1 and posY_UP > 8 or posY_UP < 1):
            return "not"
        move = self.law[posX_DOWN * 10 + posY_DOWN] + self.law[posX_UP * 10 + posY_UP]
        return move
    

    def deletePiece(self, posX, posY): # Удаление фигуры с доски
        number = posX * 10 + posY
        q = self.law[number]
        self.board[q] = "."


    def returnPiece(self, posX, posY, figure): # Возврат фигуры на доску
        number = posX * 10 + posY
        q = self.law[number]
        self.board[q] = figure

    def optionMove(self, figure): # Проверяет может ли ходить фигура определенного цвета сейчас
        if(figure in self.figure_for_move):
            return True
        else:
            return False
        


    def legalMovesFigure(self, posX, posY, all_moves): # Метод возвращает все поля, на которые может походить фигура стоящая на поле posX posY
        resultDict = dict()
        move_start = self.law[posX*10 + posY]
        for i in all_moves:
            if(move_start == i[:2]):
                if(self.board[i[2:4]] == '.'):
                    resultDict[i[2:4]] = 'green'
                else:
                    resultDict[i[2:4]] = 'red'
        return resultDict
    
    def returnBoard(self):
        self.board = {
            "a8": "r", "b8": "n", "c8": "b", "d8": "q", "e8": "k", "f8": "b", "g8": "n", "h8": "r",
            "a7": "p", "b7": "p", "c7": "p", "d7": "p", "e7": "p", "f7": "p", "g7": "p", "h7": "p",
            "a6": ".", "b6": ".", "c6": ".", "d6": ".", "e6": ".", "f6": ".", "g6": ".", "h6": ".",
            "a5": ".", "b5": ".", "c5": ".", "d5": ".", "e5": ".", "f5": ".", "g5": ".", "h5": ".",
            "a4": ".", "b4": ".", "c4": ".", "d4": ".", "e4": ".", "f4": ".", "g4": ".", "h4": ".",
            "a3": ".", "b3": ".", "c3": ".", "d3": ".", "e3": ".", "f3": ".", "g3": ".", "h3": ".",
            "a2": "P", "b2": "P", "c2": "P", "d2": "P", "e2": "P", "f2": "P", "g2": "P", "h2": "P",
            "a1": "R", "b1": "N", "c1": "B", "d1": "Q", "e1": "K", "f1": "B", "g1": "N", "h1": "R"
        }
        self.figure_for_black = ["q", "k", "b", "n", "r", "p"] #список фигур черных
        self.figure_for_white = ["Q", "K", "B", "N", "R", "P"] #список фигур белых
        self.figure_for_move = ["Q", "K", "B", "N", "R", "P"]
        self.color = 1 # 1 - ход белых, 0 - ход черных
        self.whiteToMove = True
        self.movelog = []
        self.ruckingBlack = 1
        self.ruckingWhite = 1
        return self.board
    
    def reverseBoard(self): # переворачивает доску
        pass
        

    

def Rucking(name_figure, move): # Ракировка
    pos = Translate_chess_in_position_x(move)
    move = str(move)
    if(name_figure == 'K'):
        if(move == 'e1g1'):
            return 'h1f1'
        elif(move == 'e1c1'):
            return 'a1d1'
    elif(name_figure == 'k'):
        if(move == 'e8g8'):
            return 'h8f8'
        elif(move == 'e8c8'):
            return 'a8d8'
    return '0'

def Pawn_asile(name_figure, move, board): # Взятие на проходе
    pos = Translate_chess_in_position_x(move)
    #print("move = ", move)
    #print("pos_new = ", pos[2], pos[3])
    #print("pos_x = ", pos[0], pos[2])
    #print("board = ", board[pos[3]][pos[2]])
    #print("________________________________")
    if(name_figure == 'p' and board[pos[3]][pos[2]] == '.' and pos[0] != pos[2]):
        return [pos[2], pos[3]-1]
    elif(name_figure == 'P' and board[pos[3]][pos[2]] == '.' and pos[0] != pos[2]):
        return [pos[2], pos[3]+1]
    else:
        return [0]
    
    




def Translate_move(x_old, y_old, x_new, y_new): #Перевод хода по типу откуда куда
    return chr(97+x_old) + str(8 - y_old) + chr(97+x_new) + str(8 - y_new)


def Translate_chess_in_position_x(move):
    moves = str(move)
    mas = list(moves)
    result = []
    result.append(ord(mas[0]) - 97)
    result.append(8 - int(mas[1]))
    result.append(ord(mas[2]) - 97)
    result.append(8 - int(mas[3]))
    return result


def Reurn_board(): # Приводит доску к начальному виду
    board = [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]]
    return board


def Check_position(board, steps, stock): #оценка позиции
    info = stock.analyse(board, chess.engine.Limit(depth=steps))
    return Translate_analise(info['score'], board)


def Translate_analise(analise, board): #перевод из оценки позиции chess в нормальную оценку позиции
    result = str('')
    analise = str(analise)
    counter = 0
    for i in analise:
        if(i == '+' or i == '-'):
            counter = 1
        if(counter == 1):
            if(i == ')'):
                counter = 0
                break
            result += i
    if(result == ''):
        result = 0
    else:
        result = float(result) / 100
    if(board.turn):
        return result
    else:
        return -result

def Saves(game):
    f = open("game/new_party.PGN", "w")
    string_ = '[Event "?"]\n[Site "?"]\n[Date "????.??.??"]\n[Round "?"]\n[White "?"]\n[Black "?"]\n[Result "*"]\n\n'
    f.write(string_)
    for infomation in game:
        information = str(infomation)
        f.write(information)
        f.close
   # print(123123123123)


def Close_engine(): #выключение движка
    stock.quit()