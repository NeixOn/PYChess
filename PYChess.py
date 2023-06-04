import pygame as p
import engine
import copy_engine
import chess
import chess.pgn
import chess.engine as stock
import string
import open_file as op
from sys import platform
if(platform == "linux" or platform == "linux2"):
    stock = chess.engine.SimpleEngine.popen_uci(r"AVX2/stockfish_15_x64_avx2")
    pass
elif(platform == "darwin"):
    pass
elif(platform == "win32"):
    #stock = chess.engine.SimpleEngine.popen_uci(r"stockfish_15_x64_avx2.exe")
    stock = chess.engine.SimpleEngine.popen_uci(r"winPOPCNT/stockfish-windows-2022-x86-64-modern.exe")
    pass


WIDTH = HEIGHT = 640
DIMENSION = 8
SQ_SIZE = 64 #В данный момент 64
MAX_FPS = 120
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
image_choice_figure_black = p.image.load("choice_figure_black.png")
image_choice_figure_white = p.image.load("choice_figure_white.png")
image_final_black = p.image.load("final_black.png")
image_final_white = p.image.load("final_white.png")
image_point_green = p.image.load("greenPoint.png")
image_point_red = p.image.load("redPoint.png")
image_choice_color = p.image.load("blackORwhite.png")
all = p.image.load("all.png")
BoardPNG = p.image.load("onlyBoard.png")




game_state = copy_engine.GameState()





def loadImages(): #  Загрузка изображений фигур в списки 
    pieces = ['P', 'R', 'N', 'B', 'K', 'Q', 'p', 'r', 'n', 'b', 'k', 'q']
    piece_b =['p', 'r', 'n', 'b', 'k', 'q']
    piece_w = ['P', 'R', 'N', 'B', 'K', 'Q']
    for piece in piece_w:
        IMAGES[piece] = p.image.load("images_w/" + piece + ".png")
    for piece in piece_b:
        IMAGES[piece] = p.image.load("images_b/" + piece + ".png")






p.init()
p.font.init()

depth = 10 # Глубина оценки

final = 0 # Окончание партии (1 - партия закочена, поставлен мат)
OneTick = 0    



def main():
    global final
    ### Игра против компьютера
    color_choice = ''
    ###
    step_move_counter = 0
    change_P = 0 # Режим выбора фигуры за белых
    change_p = 0 # Режим выбора фигуры за черных
    ruck_choice_white = 1 # возможность ракировки у белых
    ruck_choice_back = 1 # возможность ракировки у черных
    fontObj = p.font.SysFont('arial', 20)
    #fontObj = p.font.Font('Arial', 14)
    mode = 0
    stack_death = []#Символы умерших фигур
    stack_death_step = []#ходы на которых умирали фигуры и stack_death соответственно
    global_step_move = int(0)# текущий ход
    stack_me_move = [] #Совершенные ходы в партии
    screen = p.display.set_mode((936, 604), p.RESIZABLE) # Задаем размер
    
    clock = p.time.Clock()
    gs = engine.GameState()
    loadImages()
    choice_figure, posX_Down, posY_Down = 0, 0, 0
    mode_choice = 0 # Превращение пешки во что-то другое
    figure_maybe_move = [] # Куда может походить выбранная фигура
    ########Удалять надо
    position_x, position_y = 0, 0
    textSurfaceObj = fontObj.render('', True, 'black')
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (700, 576)

    ########
    board_game0 = chess.Board()
    game0 = chess.pgn.Game()
    game1 = chess.pgn.Game()
    game2 = chess.pgn.Game()
    counter = 0
    chessMoveStr = []
    name_choice_figure = '.'
    screen.blit(all, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = game_state.translateNumberInPiece(j + 1, 8 - i)
            if piece != ".":
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE + 3, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    textSurfaceOb = fontObj.render('', True, 'black')
    textRectob = textSurfaceOb.get_rect()
    textRectob = (520, 130)
    


    running = True
    while running:
        for i in p.event.get():

            if i.type == p.QUIT:
                running = False
                engine.Close_engine()
                stock.quit()
                quit()
####### Выбор режима игры

           

########################
            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 384 and p.mouse.get_pos()[1] < 448:  # обычный режим и создание новой доски
                mode = 0
                final = 0
                step_move_counter = 0
                game_state.returnBoard()
                board_game0 = chess.Board()
                game0 = chess.pgn.Game()
                counter = 0
                final = 0
                Update(screen, textRectObj, textSurfaceObj, clock)

            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 320 and p.mouse.get_pos()[1] < 384:  # режим игры против компьютера
                mode = 2
                final = 0
                step_move_counter
                game_state.returnBoard()
                board_game2 = chess.Board()
                game2 = chess.pgn.Game()
                counter = 0
                color_choice = ''
                final = 0

            
            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 64: #Выбор файла и создание новой доски
                final = 0
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



            if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] > 64 and p.mouse.get_pos()[1] < 128:

                if(mode == 0):
                    print(game0, file=open("game/new_party.PGN", "w"), end = "\n\n")
                    #copy_engine.Saves(game0)
                elif(mode == 1):
                    print("game2 = ", game2)
                    print(game1, file=open("game/new_party.PGN", "w"), end = "\n\n")
                    #copy_engine.Saves(game1)
                elif(mode == 2):
                    print("game2 = ", game2)
                    print(game2, file=open("game/new_party.PGN", "w"), end = "\n\n")
                    #copy_engine.Saves(game2)
#--------------------------------------------------------------------------------------------------------------------------------------------------------
            if(mode == 0): # Режим разбора партии, либо же игры против друг друга
                if(board_game0.is_checkmate()):
                    #global final
                    final = 1
                    # is_checkmate()  Проверяет является ли позиция мат
                    # is_stalemate() Проверяет является ли позиция патовой
                if(board_game0.is_stalemate()):
                    final = 2
                    # is_checkmate()  Проверяет является ли позиция мат
                    # is_stalemate() Проверяет является ли позиция патовой


                if mode_choice == 1: # Выбор фигуры в которую превратится пешка
                    print(p.mouse.get_pos()[0], p.mouse.get_pos()[1])

                    if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 0 and p.mouse.get_pos()[0] <= 127 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор коня
                        game_state.move(move, name_choice_figure, 'n')
                        move = move + 'n'
                        mode_choice = 0
                        board_game0.push(chess.Move.from_uci(move))
                        Text(game0, fontObj, screen, clock)
                        node = node.add_variation(chess.Move.from_uci(move))
                    if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 128 and p.mouse.get_pos()[0] <= 255 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор слона
                        game_state.move(move, name_choice_figure, 'b')
                        move = move + 'b'
                        mode_choice = 0
                        board_game0.push(chess.Move.from_uci(move))
                        Text(game0, fontObj, screen, clock)
                        node = node.add_variation(chess.Move.from_uci(move))
                    if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 256 and p.mouse.get_pos()[0] <= 383 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ладьи
                        game_state.move(move, name_choice_figure, 'r')
                        move = move + 'r'
                        mode_choice = 0
                        board_game0.push(chess.Move.from_uci(move))
                        Text(game0, fontObj, screen, clock)
                        node = node.add_variation(chess.Move.from_uci(move))
                    if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 384 and p.mouse.get_pos()[0] <= 512 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ферзя
                        game_state.move(move, name_choice_figure, 'q')
                        move = move + 'q'
                        board_game0.push(chess.Move.from_uci(move))
                        Text(game0, fontObj, screen, clock)
                        node = node.add_variation(chess.Move.from_uci(move))
                        mode_choice = 0


                elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448: # Нажатие кнопки оценить позицию
                    output = str(engine.Check_position(board_game0, depth, stock))
                    output = 'Оценка: ' + output + '; Глубина: ' + str(depth)
                    textSurfaceObj = fontObj.render(output, True, 'black')
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (700, 576)
                    
                elif i.type == p.MOUSEBUTTONUP and choice_figure == 1:
                    choice_figure = 0
                    location = p.mouse.get_pos() #Позиция полседнего клика мыши
                    posX_UP = location[0]//SQ_SIZE + 1 #Позиция по оси Ox
                    posY_UP = 8 - location[1]//SQ_SIZE #Позиция по оси Oy
                    move = game_state.translatePositionInMove(posX_UP, posY_UP, posX_Down, posY_Down)
                    
                        #print(k, end = ' ')
                    #print("\nmove - ", move, 'in ', chessMoveStr,"\nresult = ", move in chessMoveStr)
                    if(move in chessMoveStr): # Если такой ход возможен, то походить
                        game_state.move(move, name_choice_figure)
                        board_game0.push(chess.Move.from_uci(move))
                        
                        Update(screen, textRectob, textSurfaceOb, clock)
                        Text(game0, fontObj, screen, clock)
                        if(step_move_counter == 0):
                            node = game0.add_variation(chess.Move.from_uci(move))
                            step_move_counter += 1
                        else:
                            node = node.add_variation(chess.Move.from_uci(move))
                        print(move)
                        print('good')
                    elif(name_choice_figure == 'P' and posY_UP == 8 and posY_Down == 7):
                        for k in chessMoveStr:
                            if(str(move) == k[:4]):
                                mode_choice = 1
                                '''game_state.move(move, name_choice_figure)
                                move = move + 'q'
                                board_game0.push(chess.Move.from_uci(move))'''
                                
                    elif(name_choice_figure == 'p' and posY_UP == 1 and posY_Down == 2):
                        for k in chessMoveStr:
                            if(str(move) == k[:4]):
                                mode_choice = 1
                                '''game_state.move(move, name_choice_figure)
                                move = move + 'q'
                                board_game0.push(chess.Move.from_uci(move))'''
                    else:
                        game_state.returnPiece(posX_Down, posY_Down, name_choice_figure)
                    chessMoveStr = []

                elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 512 and p.mouse.get_pos()[1] < 512 and i.button == 1:  # ходьба при помощи мышки
                    Update(screen, textRectob, textSurfaceOb, clock)
                    location = p.mouse.get_pos()
                    print("position: ", location)
                    posX_Down = location[0]//SQ_SIZE + 1
                    posY_Down = 8 - location[1]//SQ_SIZE
                    choice = game_state.translateNumberInPiece(posX_Down, posY_Down)
                    if(choice != "." and game_state.optionMove(choice)):
                        name_choice_figure = game_state.translateNumberInPiece(posX_Down, posY_Down)
                        game_state.deletePiece(posX_Down, posY_Down)
                        choice_figure = 1
                        for k in board_game0.legal_moves: # Формирование списка возможных ходов
                            chessMoveStr.append(str(k))
                        figure_maybe_move = game_state.legalMovesFigure(posX_Down, posY_Down, chessMoveStr)
                    else:
                        choice_figure = 0
                    #game_state.output()







                    
                    
                picture(screen, choice_figure, MAX_FPS, clock, board_game0, textRectObj, textSurfaceObj, name_choice_figure, p.mouse.get_pos(), game_state, mode_choice, figure_maybe_move)
#--------------------------------------------------------------------------------------------------------------------------------------------------------

            if(mode == 2): # Режим игры против компьютера
                if(board_game2.is_checkmate()):
                    final = 1
                    # is_checkmate()  Проверяет является ли позиция мат
                    # is_stalemate() Проверяет является ли позиция патовой
                if(board_game2.is_stalemate()):
                    final = 2
                    # is_checkmate()  Проверяет является ли позиция мат
                    # is_stalemate() Проверяет является ли позиция патовой


                    
            

                


                if(color_choice == 'white'): # Игра за белых
                    if(game_state.color == 1):
                        if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448: # Нажатие кнопки оценить позицию
                            output = str(engine.Check_position(board_game2, depth, stock))
                            output = 'Оценка: ' + output + '; Глубина: ' + str(depth)
                            textSurfaceObj = fontObj.render(output, True, 'black')
                            textRectObj = textSurfaceObj.get_rect()
                            textRectObj.center = (700, 576)
                            Update(screen, textRectObj, textSurfaceObj, clock)


                        if mode_choice == 1: # Выбор фигуры в которую превратится пешка
                            print(p.mouse.get_pos()[0], p.mouse.get_pos()[1])

                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 0 and p.mouse.get_pos()[0] <= 127 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор коня
                                game_state.move(move, name_choice_figure, 'n')
                                move = move + 'n'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node = node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 128 and p.mouse.get_pos()[0] <= 255 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор слона
                                game_state.move(move, name_choice_figure, 'b')
                                move = move + 'b'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node = node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 256 and p.mouse.get_pos()[0] <= 383 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ладьи
                                game_state.move(move, name_choice_figure, 'r')
                                move = move + 'r'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node = node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 384 and p.mouse.get_pos()[0] <= 512 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ферзя
                                game_state.move(move, name_choice_figure, 'q')
                                move = move + 'q'
                                board_game2.push(chess.Move.from_uci(move))
                                node = node.add_variation(chess.Move.from_uci(move))
                                mode_choice = 0


                        elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448: # Нажатие кнопки оценить позицию
                            pass
                        elif i.type == p.MOUSEBUTTONUP and choice_figure == 1:
                            choice_figure = 0
                            location = p.mouse.get_pos() #Позиция полседнего клика мыши
                            posX_UP = location[0]//SQ_SIZE + 1 #Позиция по оси Ox
                            posY_UP = 8 - location[1]//SQ_SIZE #Позиция по оси Oy
                            move = game_state.translatePositionInMove(posX_UP, posY_UP, posX_Down, posY_Down)
                            
                                #print(k, end = ' ')
                            #print("\nmove - ", move, 'in ', chessMoveStr,"\nresult = ", move in chessMoveStr)
                            if(move in chessMoveStr): # Если такой ход возможен, то походить
                                game_state.move(move, name_choice_figure)
                                board_game2.push(chess.Move.from_uci(move))
                                if(step_move_counter == 0):
                                    node = game2.add_variation(chess.Move.from_uci(move))
                                    step_move_counter += 1
                                else:
                                    node = node.add_variation(chess.Move.from_uci(move))
            
                            elif(name_choice_figure == 'P' and posY_UP == 8 and posY_Down == 7):
                                for k in chessMoveStr:
                                    if(str(move) == k[:4]):
                                        mode_choice = 1
                                        '''game_state.move(move, name_choice_figure)
                                        move = move + 'q'
                                        board_game2.push(chess.Move.from_uci(move))'''
                                        
                            elif(name_choice_figure == 'p' and posY_UP == 1 and posY_Down == 2):
                                for k in chessMoveStr:
                                    if(str(move) == k[:4]):
                                        mode_choice = 1
                                        '''game_state.move(move, name_choice_figure)
                                        move = move + 'q'
                                        board_game2.push(chess.Move.from_uci(move))'''
                            else:
                                game_state.returnPiece(posX_Down, posY_Down, name_choice_figure)
                            chessMoveStr = []
                            game_state.output()

                        elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 512 and p.mouse.get_pos()[1] < 512 and i.button == 1:  # ходьба при помощи мышки
                            location = p.mouse.get_pos()
                            print("position: ", location)
                            posX_Down = location[0]//SQ_SIZE + 1
                            posY_Down = 8 - location[1]//SQ_SIZE
                            choice = game_state.translateNumberInPiece(posX_Down, posY_Down)
                            if(choice != "." and game_state.optionMove(choice)):
                                name_choice_figure = game_state.translateNumberInPiece(posX_Down, posY_Down)
                                game_state.deletePiece(posX_Down, posY_Down)
                                choice_figure = 1
                                for k in board_game2.legal_moves: # Формирование списка возможных ходов
                                    chessMoveStr.append(str(k))
                                figure_maybe_move = game_state.legalMovesFigure(posX_Down, posY_Down, chessMoveStr)
                            else:
                                choice_figure = 0
                            #game_state.output()







                            
                            
                        picture(screen, choice_figure, MAX_FPS, clock, board_game2, textRectObj, textSurfaceObj, name_choice_figure, p.mouse.get_pos(), game_state, mode_choice, figure_maybe_move)                   
                                    


                        
                elif(color_choice == 'black'): # Игра за черных
                    if(game_state.color == 0):
                        if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448: # Нажатие кнопки оценить позицию
                            output = str(engine.Check_position(board_game2, depth, stock))
                            output = 'Оценка: ' + output + '; Глубина: ' + str(depth)
                            textSurfaceObj = fontObj.render(output, True, 'black')
                            textRectObj = textSurfaceObj.get_rect()
                            textRectObj.center = (700, 576)
                            UpdateReverse(screen, textRectObj, textSurfaceObj, clock)


                        if mode_choice == 1: # Выбор фигуры в которую превратится пешка
                            print(p.mouse.get_pos()[0], p.mouse.get_pos()[1])

                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 0 and p.mouse.get_pos()[0] <= 127 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор коня
                                game_state.move(move, name_choice_figure, 'n')
                                move = move + 'n'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 128 and p.mouse.get_pos()[0] <= 255 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор слона
                                game_state.move(move, name_choice_figure, 'b')
                                move = move + 'b'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 256 and p.mouse.get_pos()[0] <= 383 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ладьи
                                game_state.move(move, name_choice_figure, 'r')
                                move = move + 'r'
                                mode_choice = 0
                                board_game2.push(chess.Move.from_uci(move))
                                node.add_variation(chess.Move.from_uci(move))
                            if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 384 and p.mouse.get_pos()[0] <= 512 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор ферзя
                                game_state.move(move, name_choice_figure, 'q')
                                move = move + 'q'
                                board_game2.push(chess.Move.from_uci(move))
                                node.add_variation(chess.Move.from_uci(move))
                                mode_choice = 0


                        elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448: # Нажатие кнопки оценить позицию
                            pass
                        elif i.type == p.MOUSEBUTTONUP and choice_figure == 1:
                            choice_figure = 0
                            location = p.mouse.get_pos() #Позиция полседнего клика мыши
                            posX_UP = 8 - location[0]//SQ_SIZE #Позиция по оси Ox
                            posY_UP = location[1]//SQ_SIZE + 1 #Позиция по оси Oy
                            print('posX, posY = ', posX_UP, posY_UP)
                            move = game_state.translatePositionInMove(posX_UP, posY_UP, posX_Down, posY_Down)
                            
                                #print(k, end = ' ')
                            #print("\nmove - ", move, 'in ', chessMoveStr,"\nresult = ", move in chessMoveStr)
                            if(move in chessMoveStr): # Если такой ход возможен, то походить
                                game_state.move(move, name_choice_figure)
                                board_game2.push(chess.Move.from_uci(move))
                                if(step_move_counter == 0):
                                    node = game2.add_variation(chess.Move.from_uci(move))
                                    step_move_counter += 1
                                else:
                                    node = node.add_variation(chess.Move.from_uci(move))
                            elif(name_choice_figure == 'P' and posY_UP == 8 and posY_Down == 7):
                                for k in chessMoveStr:
                                    if(str(move) == k[:4]):
                                        mode_choice = 1
                                        '''game_state.move(move, name_choice_figure)
                                        move = move + 'q'
                                        board_game2.push(chess.Move.from_uci(move))'''
                                        
                            elif(name_choice_figure == 'p' and posY_UP == 1 and posY_Down == 2):
                                for k in chessMoveStr:
                                    if(str(move) == k[:4]):
                                        mode_choice = 1
                                        '''game_state.move(move, name_choice_figure)
                                        move = move + 'q'
                                        board_game2.push(chess.Move.from_uci(move))'''
                            else:
                                game_state.returnPiece(posX_Down, posY_Down, name_choice_figure)
                            chessMoveStr = []
                            game_state.output()

                        elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 512 and p.mouse.get_pos()[1] < 512 and i.button == 1:  # ходьба при помощи мышки
                            location = p.mouse.get_pos()
                            print("position: ", location)
                            posX_Down = 8-location[0]//SQ_SIZE
                            posY_Down = location[1]//SQ_SIZE + 1
                            choice = game_state.translateNumberInPiece(posX_Down, posY_Down)
                            if(choice != "." and game_state.optionMove(choice)):
                                name_choice_figure = game_state.translateNumberInPiece(posX_Down, posY_Down)
                                game_state.deletePiece(posX_Down, posY_Down)
                                choice_figure = 1
                                for k in board_game2.legal_moves: # Формирование списка возможных ходов
                                    chessMoveStr.append(str(k))
                                figure_maybe_move = game_state.legalMovesFigure(posX_Down, posY_Down, chessMoveStr)
                            else:
                                choice_figure = 0
                            #game_state.output()







                            
                            
                        picture_reverse(screen, choice_figure, MAX_FPS, clock, board_game2, textRectObj, textSurfaceObj, name_choice_figure, p.mouse.get_pos(), game_state, mode_choice, figure_maybe_move)                   
                
                
                
                
                
                
                
                else: # Отрисовка вариантов выбора цвета
                    pictureChoiceColor(screen, clock)
                    if(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 0 and p.mouse.get_pos()[0] <= 256 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор коня
                        color_choice = 'white'
                        Update(screen, textRectObj, textSurfaceObj, clock)
                    elif(i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] >= 257 and p.mouse.get_pos()[0] <= 512 and p.mouse.get_pos()[1] >= 190 and p.mouse.get_pos()[1] <= 320): # Выбор коня
                        color_choice = 'black'
                        UpdateReverse(screen, textRectObj, textSurfaceObj, clock)

            
            
            if(mode == 2): # Находится здесь, так как не должно зависить от событий, компьютер находит ходы за черных
                if(color_choice == 'white'):
                    if(game_state.color == 0):
                        result = stock.play(board_game2, chess.engine.Limit(time=0.01))
                        print("result_move = ",result.move)
                        board_game2.push(result.move)
                        
                        if(step_move_counter == 0):
                            node = game2.add_variation(result.move)
                            step_move_counter += 1
                        else:
                            node = node.add_variation(result.move)
                        str_move = str(result.move)
                        if(len(str_move) <= 4):
                            game_state.move(str_move[:4], game_state.board[str_move[:2]])
                        else:
                            game_state.move(str_move[:4], game_state.board[str_move[:2]], str_move[4])
                        picture(screen, choice_figure, MAX_FPS, clock, board_game2, textRectObj, textSurfaceObj, name_choice_figure, p.mouse.get_pos(), game_state, mode_choice, figure_maybe_move)
                        Update(screen, textRectObj, textSurfaceObj, clock)

            if(mode == 2): # Находится здесь, так как не должно зависить от событий, компьютер находит ходы за черных
                if(color_choice == 'black'):
                    if(game_state.color == 1):
                        result = stock.play(board_game2, chess.engine.Limit(time=0.01))
                        print("result_move = ",result.move)
                        board_game2.push(result.move)
                        
                        if(step_move_counter == 0):
                            node = game2.add_variation(result.move)
                            step_move_counter += 1
                        else:
                            node = node.add_variation(result.move)
                        str_move = str(result.move)
                        if(len(str_move) <= 4):
                            game_state.move(str_move[:4], game_state.board[str_move[:2]])
                        else:
                            game_state.move(str_move[:4], game_state.board[str_move[:2]], str_move[4])
                        picture_reverse(screen, choice_figure, MAX_FPS, clock, board_game2, textRectObj, textSurfaceObj, name_choice_figure, p.mouse.get_pos(), game_state, mode_choice, figure_maybe_move)
                        UpdateReverse(screen, textRectObj, textSurfaceObj, clock)

            if(mode == 1):
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 512 and p.mouse.get_pos()[1] < 512 and p.mouse.get_pos()[1] > 448:
                    output = str(copy_engine.Check_position(board_game1, depth, stock))
                    output = 'Оценка: ' + output + '; Глубина: ' + str(depth)
                    textSurfaceObj = fontObj.render(output, True, 'black')
                    textRectObj = textSurfaceObj.get_rect()
                    textRectObj.center = (700, 576)
                if i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] > 256 and p.mouse.get_pos()[1] > 512 and p.mouse.get_pos()[0] <384:
                    if (global_step_move != len_move_game1):#Случай промотки вперед
                        board_game1.push(move_game1[global_step_move])
                        game_state.copyBoard(board_game1)
                        global_step_move += 1
                elif i.type == p.MOUSEBUTTONDOWN and p.mouse.get_pos()[0] < 256 and p.mouse.get_pos()[1] > 512 and p.mouse.get_pos()[0] >128: #Случай промотки назад
                    if (global_step_move != 0): # Проверка был ли совершен хоть один ход, если нет то проматывать некуда, поэтому ничего не делаем
                        board_game1.pop()
                        game_state.copyBoard(board_game1)

                        global_step_move -= 1
                picture(screen, choice_figure, MAX_FPS, clock, board_game1, textRectObj, textSurfaceObj, 'p', 0, game_state, 0, [])









def Update(screen, textRectObj, textSurfaceObj, clock):
    screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    drawPieces(screen, textRectObj, textSurfaceObj)
    clock.tick(MAX_FPS)
    p.display.flip()

def UpdateText(screen, textRectObj, textSurfaceObj, clock):
    screen.blit(all, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    screen.blit(textSurfaceObj, textRectObj)
    clock.tick(MAX_FPS)
    p.display.flip()


def UpdateReverse(screen, textRectObj, textSurfaceObj, clock):
    screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    drawPieces_reverse(screen, textRectObj, textSurfaceObj)
    clock.tick(MAX_FPS)
    p.display.flip()




def picture(screen, choice_figure, MAX_FPS, clock, board, textRectObj, textSurfaceObj, figure, position_mouse, game_state, mode_choice, figure_maybe_move):
    
    global OneTick
    if(choice_figure == 1):
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces(screen, textRectObj, textSurfaceObj)
        picture_move(screen, choice_figure, figure_maybe_move)
        drawPieceMouse(screen, figure, position_mouse)
        OneTick = 1
    elif(OneTick == 1):
        OneTick = 0
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces(screen, textRectObj, textSurfaceObj)
    if(mode_choice == 1):
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces(screen, textRectObj, textSurfaceObj)
        picture_choice_figure(game_state.color, screen)
        OneTick = 1
        
        
    if(final == 1):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if(game_state.translateNumberInPiece(i+1, j+1) == 'k' and game_state.color == 0):
                    screen.blit(image_final_black, p.Rect(i * SQ_SIZE, (8-j-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                if(game_state.translateNumberInPiece(i+1, j+1) == 'K' and game_state.color == 1):
                    screen.blit(image_final_white, p.Rect(i * SQ_SIZE, (8-j-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    clock.tick(MAX_FPS)
    p.display.flip()

    

'''Рисует фигуры на доске'''
def drawPieces(screen, textRectObj, textSurfaceObj):
    
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = game_state.translateNumberInPiece(j + 1, 8 - i)
            if piece != ".":
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE + 3, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    screen.blit(textSurfaceObj, textRectObj)


def drawPieceMouse(screen, figure, position): #Функция рисования фигуры перемещающейся за мышкой
    screen.blit(IMAGES[figure], p.Rect(position[0] - 32, position[1] - 32, SQ_SIZE, SQ_SIZE))
    


def picture_choice_figure(color, screen):
        if(color == 1):
            screen.blit(image_choice_figure_white, p.Rect(0 * SQ_SIZE, 3 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        if(color == 0):
            screen.blit(image_choice_figure_black, p.Rect(0 * SQ_SIZE, 3 * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def picture_move(screen, choice_figure, figure_maybe_move):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if(choice_figure == 1):
                if (game_state.law[(j+1)*10 + i+1] in figure_maybe_move):
                    if(figure_maybe_move[game_state.law[(j+1)*10 + i+1]] == 'green'):
                        screen.blit(image_point_green, p.Rect(j * SQ_SIZE + 2, (8-i-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    else:
                        screen.blit(image_point_red, p.Rect(j * SQ_SIZE + 2, (8-i-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    



def pictureChoiceColor(screen, clock): # Зарисовка выбора цвета
    screen.blit(image_choice_color, p.Rect(0 * SQ_SIZE, 3 * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    clock.tick(MAX_FPS)
    p.display.flip()


def picture_move_reverse(screen, choice_figure, figure_maybe_move):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            if(choice_figure == 1):
                if (game_state.law[(j+1)*10 + i+1] in figure_maybe_move):
                    if(figure_maybe_move[game_state.law[(j+1)*10 + i+1]] == 'green'):
                        screen.blit(image_point_green, p.Rect((8-j-1) * SQ_SIZE + 2, i * SQ_SIZE, SQ_SIZE, SQ_SIZE)) # j, 8-i-1
                    else:
                        screen.blit(image_point_red, p.Rect((8-j-1) * SQ_SIZE + 2, i * SQ_SIZE, SQ_SIZE, SQ_SIZE)) # j, 8-i-1


def Text(game, fontObj, screen, clock):
    
    out = str(game)[93:]
    result = ''
    counter = 0
    for i in out:
        if(counter % 10 == 0):
            result += out[counter:counter+10] + '\n'
        counter += 1
    textSurfaceOb = fontObj.render(result, True, 'black')
    print("asdfasdfsadf", type(textSurfaceOb))
    textRectob = textSurfaceOb.get_rect()
    textRectob = (520, 130)
    UpdateText(screen, textRectob, textSurfaceOb, clock)


def drawPieces_reverse(screen, textRectObj, textSurfaceObj):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = game_state.translateNumberInPiece(8-j, i+1) # j+1, 8 - i
            if piece != ".":
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE + 3, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    screen.blit(textSurfaceObj, textRectObj)

def picture_reverse(screen, choice_figure, MAX_FPS, clock, board, textRectObj, textSurfaceObj, figure, position_mouse, game_state, mode_choice, figure_maybe_move):
    global OneTick
    if(choice_figure == 1):
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces_reverse(screen, textRectObj, textSurfaceObj)
        picture_move_reverse(screen, choice_figure, figure_maybe_move)
        drawPieceMouse(screen, figure, position_mouse)
        OneTick = 1
    elif(OneTick == 1):
        OneTick = 0
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces_reverse(screen, textRectObj, textSurfaceObj)
    if(mode_choice == 1):
        screen.blit(BoardPNG, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        drawPieces_reverse(screen, textRectObj, textSurfaceObj)
        picture_choice_figure(game_state.color, screen)
        OneTick = 1
        
        
    if(final == 1):
        for i in range(DIMENSION):
            for j in range(DIMENSION):
                if(game_state.translateNumberInPiece(i+1, j+1) == 'k' and game_state.color == 0):
                    screen.blit(image_final_black, p.Rect(i * SQ_SIZE, (8-j-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                if(game_state.translateNumberInPiece(i+1, j+1) == 'K' and game_state.color == 1):
                    screen.blit(image_final_white, p.Rect(i * SQ_SIZE, (8-j-1) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    clock.tick(MAX_FPS)
    p.display.flip()






main()
