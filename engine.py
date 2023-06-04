import chess.engine as stock
from sys import platform
import chess
import math as M
if(platform == "linux" or platform == "linux2"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_linux_x64_avx2/stockfish_15_x64_avx2")
    pass
elif(platform == "darwin"):
    pass
elif(platform == "win32"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_x64_avx2.exe")
    pass

class GameState():
    def __init__(self):

        self.board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]]
        self.figure_for_black = ["q", "k", "b", "n", "r", "p"] #список фигур черных
        self.figure_for_white = ["Q", "K", "B", "N", "R", "P"] #список фигур белых
        self.whiteToMove = True
        self.movelog = []

    def move(self, step):
        pass


    def legal_moves_counting(self, moves):
        self.legal_moves = []
        counter = 0
        for i in range(8):#Строка
            for j in range(8):#Столбец
                #_____________________________________________________________________ПЕШКА
                if(self.board[i][j] == "p"):
                    if(self.board[i+1][j] == "."):
                        self.legal_moves.append(Translate_move(j, i, j, i+1))
                    if(j != 7 and self.board[i+1][j+1] in self.figure_for_white):
                        self.legal_moves.append(Translate_move(j, i, j+1, i+1))
                    if(j!= 0 and self.board[i+1][j-1] in self.figure_for_white):
                        self.legal_moves.append(Translate_move(j, i, j-1, i+1))
                if(self.board[i][j] == "P"):
                    if(self.board[i-1][j] == "."):
                        self.legal_moves.append(Translate_move(j, i, j, i - 1))
                    if( j != 7 and self.board[i-1][j+1] in self.figure_for_black):
                        self.legal_moves.append(Translate_move(j, i, j + 1, i - 1))
                    if(j!= 0 and self.board[i-1][j-1] in self.figure_for_black):
                        self.legal_moves.append(Translate_move(j, i, j - 1, i - 1))
                if(i == 1 and self.board[i+2][j] == "." and self.board[1][j] == "p"):
                    self.legal_moves.append(Translate_move(j, 1, j, 3))
                if(i == 6 and self.board[i-2][j] == "." and self.board[6][j] == "P"):
                    self.legal_moves.append(Translate_move(j, 6, j, 4))
                #_________________________________________________________________________Взятие на проходе
        for i in range(3, 5, 1):
            for j in range(7):
                #print("-------", self.board[i][j], self.board[i][j+1])
                if((self.board[i][j] == "p" and self.board[i][j+1] == "P") or (self.board[i][j] == "P" and self.board[i][j+1] == "p")):
                    #print("havehavehave")
                    for k in moves:
                        if (Translate_chess_in_position_x(k)[2] == j and Translate_chess_in_position_x(k)[3] == i):
                            #print(k)
                            counter = 1
                            #print("counter = ", counter)
                            break
                        if(Translate_chess_in_position_x(k)[2] == j+1 and Translate_chess_in_position_x(k)[3] == i):
                           # print(k)
                            counter = 2
                            #print("counter = ", counter)
                            break
                    if(counter == 1):
                        for k in moves[::-1]:
                            if(Translate_chess_in_position_x(k)[2] == j+1 and Translate_chess_in_position_x(k)[3] == i):
                                #print("Проверка, что был совершен двойной ход")
                                y1_y2 = Translate_chess_in_position_x(k)[1] - Translate_chess_in_position_x(k)[3]
                                #print(k)
                                #print(y1_y2)
                                if(M.fabs(y1_y2) == 2):
                                    if(y1_y2 > 0):
                                        if(self.board[i+1][j+1] == "."):
                                            self.legal_moves.append(Translate_move(j, i, j+1, i+1))
                                    if(y1_y2 < 0):
                                        if(self.board[i-1][j+1] == "."):
                                            self.legal_moves.append(Translate_move(j, i, j+1, i-1))
                    
                    if(counter == 2):
                        for k in moves[::-1]:
                            if(Translate_chess_in_position_x(k)[2] == j and Translate_chess_in_position_x(k)[3] == i):
                                #print("Проверка, что был совершен двойной ход")
                                y1_y2 = Translate_chess_in_position_x(k)[1] - Translate_chess_in_position_x(k)[3]
                                #print(k)
                                #print(y1_y2)
                                if(M.fabs(y1_y2) == 2):
                                    if(y1_y2 > 0):
                                        if(self.board[i+1][j] == "."):
                                            self.legal_moves.append(Translate_move(j+1, i, j, i+1))
                                    if(y1_y2 < 0):
                                        if(self.board[i-1][j] == "."):
                                            self.legal_moves.append(Translate_move(j+1, i, j, i-1))
        #__________________________________________________________________________________________________________СЛОН
        buff = 0
        for i in range(8):
            for j in range(8):
                if(self.board[i][j] == "b"): #По диагонгали вверх вправо!!!Надо тоже работать через 2 переменные, а не через одну k
                    for k in range(j+1, 8, 1):
                        if(self.board[k][k] in self.figure_for_black):
                            #print("break без ничего", self.board[k][k])
                            break
                        elif(self.board[k][k] in self.figure_for_white):
                            #print("break с добавлением", self.board[k][k])
                            self.legal_moves.append(Translate_move(j, i, k, k))
                            break
                        else:
                           # print('ksks - ', Translate_move(j, i, k, k))
                            #print(j, i, k, k)
                            self.legal_moves.append(Translate_move(j, i, k, k))
                if(self.board[i][j] == "b"): #По диагонгали вниз влево
                    for k in range(j-1, -1, -1):
                        if(self.board[k][k] in self.figure_for_black):
                            break
                        elif(self.board[k][k] in self.figure_for_white):
                            self.legal_moves.append(Translate_move(j, i, k, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, k, k))
                if(self.board[i][j] == "b"): #По диагонгали вниз вправо
                    buff = i + 1
                    for k in range(j-1, -1, -1):
                        if(buff > 7):
                            break
                        if(self.board[k][buff] in self.figure_for_black):
                            break
                        elif(self.board[k][buff] in self.figure_for_white):
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                        buff += 1
                if(self.board[i][j] == "b"): #По диагонгали вверх влево
                    buff = i - 1
                    for k in range(j+1, 8, 1):
                        if(buff < 0):
                            break
                        if(self.board[k][buff] in self.figure_for_black):
                            break
                        elif(self.board[k][buff] in self.figure_for_white):
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                        buff -= 1
                #Для белых
                if(self.board[i][j] == "B"): #По диагонгали вверх вправо
                    for k in range(i+1, 8, 1):
                        if(self.board[k][k] in self.figure_for_white):
                            break
                        elif(self.board[k][k] in self.figure_for_black):
                            self.legal_moves.append(Translate_move(j, i, k, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, k, k))
                if(self.board[i][j] == "B"): #По диагонгали вниз влево
                    for k in range(i-1, -1, -1):
                        if(self.board[k][k] in self.figure_for_white):
                            break
                        elif(self.board[k][k] in self.figure_for_black):
                            self.legal_moves.append(Translate_move(j, i, k, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, k, k))
                if(self.board[i][j] == "B"): #По диагонгали вниз вправо
                    buff = i + 1
                    for k in range(i-1, -1, -1):
                        if(buff > 7):
                            break
                        if(self.board[k][buff] in self.figure_for_white):
                            break
                        elif(self.board[k][buff] in self.figure_for_black):
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                        buff += 1
                if(self.board[i][j] == "B"): #По диагонгали вверх влево
                    buff = i - 1
                    for k in range(i+1, 8, 1):
                        if(buff < 0):
                            break
                        if(self.board[k][buff] in self.figure_for_white):
                            break
                        elif(self.board[k][buff] in self.figure_for_black):
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                            break
                        else:
                            self.legal_moves.append(Translate_move(j, i, buff, k))
                        buff -= 1



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