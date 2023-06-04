import pygame as p
import engine
import chess
import chess.pgn
import chess.engine as stock
import string
import open_file as op
from sys import platform
p.init()
p.font.init()
if(platform == "linux" or platform == "linux2"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_linux_x64_avx2/stockfish_15_x64_avx2")
    pass
elif(platform == "darwin"):
    pass
elif(platform == "win32"):
    stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_x64_avx2.exe")
    pass


WIDTH = HEIGHT = 640
DIMENSION = 8
SQ_SIZE = 64 #В данный момент 64
MAX_FPS = 60
IMAGES = {}

#mode = 0 - обычный режим игры друг с другом
#mode = 1 - считывание партии
#mode = 2 - игра против компьютера?

image_for_black = p.image.load("black.png")
image_for_white = p.image.load("white.png")
image_arrow = p.image.load("arrow.png")
image_arrow = p.transform.scale(image_arrow, (256,64))
image_open = p.image.load("open_party.png")
image_output = p.image.load("Output_field.png")
image_position = p.image.load(("Evaluation_position.png"))
image_usually = p.image.load("usually.png")
image_computer = p.image.load("computer.png")
image_save_files = p.image.load("save_files.png")





def loadImages(): #  Загрузка изображений в списки
    pieces = ['P', 'R', 'N', 'B', 'K', 'Q', 'p', 'r', 'n', 'b', 'k', 'q']
    piece_b =['p', 'r', 'n', 'b', 'k', 'q']
    piece_w = ['P', 'R', 'N', 'B', 'K', 'Q']
    for piece in piece_w:
        IMAGES[piece] = p.image.load("images_w/" + piece + ".png")
    for piece in piece_b:
        IMAGES[piece] = p.image.load("images_b/" + piece + ".png")



def legal_moves_for_figure(x, y, new_x, new_y, board): # функция проверки легальности ходов конкретной фигуры
    move = chess.Move.from_uci(engine.Translate_move(x, y, new_x, new_y))
    legal_moves_str = []
    for i in board.legal_moves:
        legal_moves_str.append(i)
    if (move in legal_moves_str):
        return True
    else:
        return False



def main():
    change_P = 0
    change_p = 0
    ruck_choice_white = 1 # возможность ракировки у белых
    ruck_choice_back = 1 # возможность ракировки у черных
    fontObj = p.font.Font('freesansbold.ttf', 20)
    textSurfaceObj = fontObj.render('', True, 'black')
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (576, 576)
    mode = 0
    stack_death = []#Символы умерших фигур
    stack_death_step = []#ходы на которых умирали фигуры и stack_death соответственно
    global_step_move = int(0)# текущий ход
    stack_me_move = [] #Совершенные ходы в партии
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE) # Задаем размер
    current_size = screen.get_size()
    virtual_surface = p.Surface((WIDTH, HEIGHT)) #Создаем виртуальную поверхность, чтобы могли растягивать и картинки
    clock = p.time.Clock()
    virtual_surface.fill(p.Color("white"))
    gs = engine.GameState()
    loadImages()
    choice_figure, position_x, position_y = 0, 0, 0
    board_game0 = chess.Board()
    game0 = chess.pgn.Game()
    game2 = chess.pgn.Game()
    counter = 0


    running = True
    while running:
        for i in p.event.get():
            if i.type == p.VIDEORESIZE:
                current_size = i.size

            if i.type == p.QUIT:
                running = False
                engine.Close_engine()
                stock.quit()
                quit()

            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 64: #Выбор файла и создание новой доски
                app = op.App()
                open_party = app.choose_file()
                if(open_party):
                    stack_death = []  # Символы умерших фигур
                    stack_death_step = []  # ходы на которых умирали фигуры и stack_death соответственно
                    global_step_move = int(0)  # текущий ход
                    mode = 1
                    pgn1 = open(open_party)
                    game1 = chess.pgn.read_game(pgn1)
                    board_game1 = game1.board()
                    move_game1 = []
                    len_move_game1 = 0
                    for move in game1.mainline_moves():  # формируем удобный список ходов в партии
                        move_game1.append(move)
                        len_move_game1 = len_move_game1 + 1
                    gs.board = engine.Reurn_board()

            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 384 and p.mouse.get_pos()[1] < 448:  # обычный режим и создание новой доски
                mode = 0
                gs.board = engine.Reurn_board()
                board_game0 = chess.Board()
                game0 = chess.pgn.Game()
                counter = 0

            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 320 and p.mouse.get_pos()[1] < 384:  # режим игры против компьютера
                mode = 2
                gs.board = engine.Reurn_board()
                board_game2 = chess.Board()
                game2 = chess.pgn.Game()
                counter = 0

            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 64 and p.mouse.get_pos()[1] < 128:# Сохранение файла

                if(mode == 0):
                    engine.Saves(game0)
                elif(mode == 1):
                    engine.Saves(game1)
                elif(mode == 2):
                    engine.Saves(game2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
            if(mode == 0):
                output = str(engine.Check_position(board_game0, 10, stock))
                textSurfaceObj = fontObj.render(output, True, 'black')
                textRectObj = textSurfaceObj.get_rect()
                textRectObj.center = (576, 576)
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448:
                    pass
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 512 and p.mouse.get_pos()[1] < 512: # ходьба при помощи мышки
                    location = p.mouse.get_pos() # Позиция полседнего клика мыши
                    print(location)
                    position_x = location[0]//SQ_SIZE #Позиция по оси Ox
                    position_y = location[1]//SQ_SIZE #Позиция по оси Oy
                    print("x = ", position_x)
                    print("y = ", position_y)
                    print("__________________")
                    if(choice_figure == 1 and (position_y != position_old_figure_y or position_x != position_old_figure_x)):# Проверка была ли выбрана фигура, и проверка, что человек 2 раз не нажал на ту же фигуру
                        move = chess.Move.from_uci(engine.Translate_move(position_old_figure_x, position_old_figure_y, position_x, position_y))

                        if(name_figure == 'P'): # Смены пешки на Королеву за белых
                            if(str(move)[3] == "8"):
                                str_legal_moves = []
                                move_P = str(move)
                                move_P = move_P + 'q'
                                #print("move_P_res = ", move_P)
                                for i in board_game0.legal_moves:
                                    #print(str(i))
                                    if(str(i) == move_P):
                                        move = i
                                        change_P = 1
                                        #print(move)

                        if(name_figure == 'p'): # Смены пешки на Королеву
                            if(str(move)[3] == "1"):
                                str_legal_moves = []
                                move_P = str(move)
                                move_P = move_P + 'q'
                                #print("move_P_res = ", move_P)
                                for i in board_game0.legal_moves:
                                    #print(str(i))
                                    if(str(i) == move_P):
                                        move = i
                                        change_p = 1
                                        #print(move)
                    
                        #print(move)
                        #print(name_figure)
                        #print("legal = ")
                        new_legal = []
                        for i in board_game0.legal_moves:
                            #print(i, end=' ')
                            pass
                        #print("legal = ", board_game0.legal_moves)
                        if(move in board_game0.legal_moves):
                            asile = engine.Pawn_asile(name_figure, move, gs.board)
                            gs.board[position_y][position_x] = name_figure
                            if(change_P == 1):
                                gs.board[position_y][position_x] = 'Q'
                                change_P = 0
                            if(change_p == 1):
                                gs.board[position_y][position_x] = 'q'
                                change_p = 0
                            gs.board[position_old_figure_y][position_old_figure_x] = "."

                            '''for i in range(8):
                                print(gs.board[i])
                            print("\n_____________________________________________")'''
                            #print('asile = ', asile)
                            if(len(asile) == 2):
                                gs.board[asile[1]][asile[0]] = "."

                            if(name_figure == 'k' and ruck_choice_back == 1): # Проверка на ракировку
                                ruck = engine.Rucking(name_figure, move)
                                if(ruck != '0'):
                                    ruck_step = engine.Translate_chess_in_position_x(ruck)
                                    print(ruck_step)
                                    gs.board[ruck_step[1]][ruck_step[2]] = 'r'
                                    gs.board[ruck_step[3]][ruck_step[0]] = "."
                            if(name_figure == 'K' and ruck_choice_white == 1):
                                ruck = engine.Rucking(name_figure, move)
                                if(ruck != '0'):
                                    ruck_step = engine.Translate_chess_in_position_x(ruck)
                                    print(ruck_step)
                                    gs.board[ruck_step[1]][ruck_step[2]] = 'R'
                                    gs.board[ruck_step[3]][ruck_step[0]] = "."
                            
                            board_game0.push(move)
                            stack_me_move.append(engine.Translate_move(position_old_figure_x, position_old_figure_y, position_x, position_y))
                            if(counter == 0):
                                node = game0.add_variation(move)
                                counter = 1
                            else:
                                node = node.add_variation(move)
                        choice_figure = 0
                    if(gs.board[position_y][position_x] != "."): # Случай, когда была выбрана фигура
                        qhqh = 8
                        for i in gs.board:
                            #print(qhqh, i)
                            qhqh-= 1
                        #for i in range(8):
                            #print("    ", chr(97 + i),  end = '', sep='')
                        #print()
                        #gs.legal_moves_counting(stack_me_move)
                        #print("gs.legal_moves", gs.legal_moves)
                        #print("stack_me_move", stack_me_move)
                        #print("stack_me_move[:-1]", stack_me_move[::-1])
                        #for i in stack_me_move:
                            #print("i = ", engine.Translate_chess_in_position_x(i))
                        choice_figure = 1
                        name_figure = gs.board[position_y][position_x]
                        position_old_figure_x = position_x
                        position_old_figure_y = position_y
                    else:
                        choice_figure = 0
                picture(virtual_surface, gs, choice_figure, position_x, position_y, current_size, MAX_FPS, screen, clock, board_game0, textRectObj, textSurfaceObj)
#--------------------------------------------------------------------------------------------------------------------------------------------------------

            if(mode == 1):
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448:
                    output = str(engine.Check_position(board_game0, 20))
                    textSurfaceObj = fontObj.render(output, True, 'black')
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (576, 576)
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 256 and p.mouse.get_pos()[1] > 512 and p.mouse.get_pos()[0] <384:
                    if (global_step_move != len_move_game1):#Случай промотки вперед
                        board_game1.push(move_game1[global_step_move])
                        buff = gs.board[-(move_game1[global_step_move].from_square // 8) - 1][(move_game1[global_step_move].from_square % 8)]
                        if(gs.board[-(move_game1[global_step_move].to_square // 8) - 1][(move_game1[global_step_move].to_square % 8)] != "."): #Записываем кто умер и на каком ходе, чтобы потом возвратить их
                            stack_death.append(gs.board[-(move_game1[global_step_move].to_square // 8) - 1][(move_game1[global_step_move].to_square % 8)])
                            stack_death_step.append(global_step_move)
                        gs.board[-(move_game1[global_step_move].to_square // 8) - 1][(move_game1[global_step_move].to_square % 8)] = buff #Перемещаем фигуру на новое место
                        gs.board[-(move_game1[global_step_move].from_square // 8) - 1][(move_game1[global_step_move].from_square % 8)] = "." # На старое место ставим точку
                        global_step_move += 1
                        #print("_________", global_step_move, "_________")
                        #print(board_game1)
                elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 256 and p.mouse.get_pos()[1] > 512 and p.mouse.get_pos()[0] >128: #Случай промотки назад
                    if (global_step_move != 0): # Проверка был ли совершен хоть один ход, если нет то проматывать некуда, поэтому ничего не делаем
                        board_game1.pop()
                        buff = gs.board[-(move_game1[global_step_move-1].to_square // 8) - 1][(move_game1[global_step_move-1].to_square % 8)]#запоминаем куда пришла фигура, ходившая на прошлом ходе
                        gs.board[-(move_game1[global_step_move-1].from_square // 8) - 1][(move_game1[global_step_move-1].from_square % 8)] = buff#присваиваем месту откуда ходила фигура символ этой фигуры
                        gs.board[-(move_game1[global_step_move-1].to_square // 8) - 1][(move_game1[global_step_move-1].to_square % 8)] = "." #На место куда ходила фигура ставим точку
                        for i in stack_death_step:
                            if(i == global_step_move-1): #Если ход на котором кто-то умер совпадает с данным ходом, то нужно вернуть умершую фигуру на свое место
                                gs.board[-(move_game1[global_step_move-1].to_square // 8) - 1][(move_game1[global_step_move-1].to_square % 8)] = stack_death[-1]
                                stack_death.pop(len(stack_death) - 1)
                                stack_death_step.pop(len(stack_death_step) - 1)
                                break

                        global_step_move -= 1
                        #print("_________", global_step_move, "_________")
                        #print(board_game1)
                picture(virtual_surface, gs, choice_figure, position_x, position_y, current_size, MAX_FPS, screen, clock, board_game1, textRectObj, textSurfaceObj)
            if (mode == 2):
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448:
                    output = str(engine.Check_position(board_game2, 20))
                    textSurfaceObj = fontObj.render(output, True, 'black')
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (576, 576)
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 512 and p.mouse.get_pos()[1] < 512:  # ходьба при помощи мышки
                    location = p.mouse.get_pos()  # Позиция полседнего клика мыши
                    position_x = location[0] // SQ_SIZE  # Позиция по оси Ox
                    position_y = location[1] // SQ_SIZE  # Позиция по оси Oy
                    if (choice_figure == 1 and (position_y != position_old_figure_y or position_x != position_old_figure_x)):
                        move = chess.Move.from_uci(engine.Translate_move(position_old_figure_x, position_old_figure_y, position_x, position_y))
                        if (move in board_game2.legal_moves):
                            gs.board[position_y][position_x] = name_figure
                            gs.board[position_old_figure_y][position_old_figure_x] = "."
                            board_game2.push(move)
                            if (counter == 0):
                                node = game2.add_variation(move)
                                counter = 1
                            else:
                                node = node.add_variation(move)
                            result = stock.play(board_game2, chess.engine.Limit(time=0.3))
                            board_game2.push(result.move)
                            posotion_old_and_new = engine.Translate_chess_in_position_x(result.move)
                            name_figure = gs.board[posotion_old_and_new[1]][posotion_old_and_new[0]]
                            gs.board[posotion_old_and_new[3]][posotion_old_and_new[2]] = name_figure
                            gs.board[posotion_old_and_new[1]][posotion_old_and_new[0]] = "."
                            if (counter == 0):
                                node = game2.add_variation(result.move)
                                counter = 1
                            else:
                                node = node.add_variation(result.move)
                        choice_figure = 0
                    elif (gs.board[position_y][position_x] != "."):  # Случай, когда была выбрана фигура
                        choice_figure = 1
                        name_figure = gs.board[position_y][position_x]
                        position_old_figure_x = position_x
                        position_old_figure_y = position_y
                    else:
                        choice_figure = 0
                picture(virtual_surface, gs, choice_figure, position_x, position_y, current_size, MAX_FPS, screen, clock, board_game0, textRectObj, textSurfaceObj)
                #picture(virtual_surface, gs, choice_figure, position_x, position_y, current_size, MAX_FPS, screen, clock, board)

def picture(virtual_surface, gs, choice_figure, position_x, position_y, current_size, MAX_FPS, screen, clock, board, textRectObj, textSurfaceObj):
    drawGameState(virtual_surface, gs, choice_figure, position_x, position_y, board, textRectObj, textSurfaceObj)
    scaled_surface = p.transform.scale(virtual_surface, current_size)
    screen.blit(scaled_surface, (0, 0))
    clock.tick(MAX_FPS)
    p.display.flip()

def drawGameState(virtual_surface, gs, choice_figure, position_x, position_y, board, textRectObj, textSurfaceObj):
    drawBoard(virtual_surface, choice_figure, position_x, position_y, board)
    drawPieces(virtual_surface, gs.board, textRectObj, textSurfaceObj)

'''Рисует квадраты на доске(верхний левый квадрат всегда белый)'''
def drawBoard(virtual_surface, choice_figure, position_x, position_y, board):
    colors = [p.Color("#eedab8"), p.Color("#b18a66")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[(i+j) % 2]
            if(j == position_x and i == position_y and choice_figure == 1):
                color = "#859666a8"
            p.draw.rect(virtual_surface, color, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if(choice_figure == 1 and i != position_y):
                if (legal_moves_for_figure(position_x, position_y, j, i,board)):
                    if((i+j) % 2 == 0):
                        virtual_surface.blit(image_for_white, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    else:
                       virtual_surface.blit(image_for_black, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    i = 8
    for j in range(9):
        p.draw.rect(virtual_surface, "#c37742", p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    i = 9
    for j in range(9):
        p.draw.rect(virtual_surface, "#c37742", p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    j = 8
    for i in range(8):
        p.draw.rect(virtual_surface, "#c37742", p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    j = 9
    for i in range(9):
        p.draw.rect(virtual_surface, "#c37742", p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


    p.draw.rect(virtual_surface, "black", p.Rect(512, 0, 4, 516))
    p.draw.rect(virtual_surface, "black", p.Rect(0, 512, 516, 4))
    p.draw.rect(virtual_surface, "black", p.Rect(0, 516, 4, 128))
    p.draw.rect(virtual_surface, "black", p.Rect(0, 636, 640, 4))
    p.draw.rect(virtual_surface, "black", p.Rect(636, 0, 4, 640))


'''Рисует фигуры на доске'''
def drawPieces(virtual_surface, board, textRectObj, textSurfaceObj):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != ".":
                virtual_surface.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_arrow, p.Rect(2*SQ_SIZE, 8*SQ_SIZE+32, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_open, p.Rect(8 * SQ_SIZE, 0 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_output, p.Rect(8 * SQ_SIZE, 8 * SQ_SIZE, SQ_SIZE*2, SQ_SIZE*2))
    virtual_surface.blit(image_position, p.Rect(8 * SQ_SIZE, 7 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_usually, p.Rect(8 * SQ_SIZE, 6 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_computer, p.Rect(8 * SQ_SIZE, 5 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(image_save_files, p.Rect(8 * SQ_SIZE, 1 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    virtual_surface.blit(textSurfaceObj, textRectObj)


main()
