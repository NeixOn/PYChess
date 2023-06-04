"""filele=1234563
f=open('CBH/chess/CBH/q.cbh','rb')
if(f.closed):
  print('file not open!')
else:
  print("file open!")
"""

import pygame as p
import open_file
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









def loadImages(): #  Загрузка изображений фигур в списки 
    pieces = ['P', 'R', 'N', 'B', 'K', 'Q', 'p', 'r', 'n', 'b', 'k', 'q']
    piece_b =['p', 'r', 'n', 'b', 'k', 'q']
    piece_w = ['P', 'R', 'N', 'B', 'K', 'Q']
    for piece in piece_w:
        IMAGES[piece] = p.image.load("images_w/" + piece + ".png")
    for piece in piece_b:
        IMAGES[piece] = p.image.load("images_b/" + piece + ".png")


loadImages()



#p.init()
#p.font.init()



final = 0 # Окончание партии (1 - партия закочена, поставлен мат)
OneTick = 0    

#fontObj = p.font.Font('freesansbold.ttf', 20)
#screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE) # Задаем размер
#clock = p.time.Clock()
#textSurfaceObj = fontObj.render('', True, 'black')
#textRectObj = textSurfaceObj.get_rect()
#textRectObj.center = (576, 576)
posFigure = {
        "r1": 18, "n1": 28, "b1": 38, "q1": 48, "k": 58, "b2": 68, "n2": 78, "r2": 88,
        "p1": 17, "p2": 27, "p3": 37, "p4": 47, "p5": 57, "p6": 67, "p7": 77, "p8": 87,
        "P1": 12, "P2": 22, "P3": 32, "P4": 42, "P5": 52, "P6": 62, "P7": 72, "P8": 82,
        "R1": 11, "N1": 21, "B1": 31, "Q1": 41, "K": 51, "B2": 61, "N2": 71, "R2": 81,
        "r3": 0, "n3": 0, "b3": 0, "q2": 0, "q3": 0,
        "R3": 0, "N3": 0, "B3": 0, "Q2": 0, "Q3": 0
}




def Update(screen, textRectObj, textSurfaceObj, clock):
    bo = {
            18: "..", 28: "..", 38: "..", 48: "..", 58: "..", 68: "..", 78: "..", 88: "..",
            17: "..", 27: "..", 37: "..", 47: "..", 57: "..", 67: "..", 77: "..", 87: "..",
            16: "..", 26: "..", 36: "..", 46: "..", 56: "..", 66: "..", 76: "..", 86: "..",
            15: "..", 25: "..", 35: "..", 45: "..", 55: "..", 65: "..", 75: "..", 85: "..",
            14: "..", 24: "..", 34: "..", 44: "..", 54: "..", 64: "..", 74: "..", 84: "..",
            13: "..", 23: "..", 33: "..", 43: "..", 53: "..", 63: "..", 73: "..", 83: "..",
            12: "..", 22: "..", 32: "..", 42: "..", 52: "..", 62: "..", 72: "..", 82: "..",
            11: "..", 21: "..", 31: "..", 41: "..", 51: "..", 61: "..", 71: "..", 81: "..",
        }
    screen = p.display.set_mode((WIDTH, HEIGHT), p.RESIZABLE) # Задаем размер
    screen.blit(all, p.Rect(0*SQ_SIZE, 0*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    for i in posFigure:
        if(posFigure[i] == 0):
            pass
        else:
            bo[posFigure[i]] = i

    for i in range(1, 9, 1):
        for j in range(1, 9, 1):
            if(bo[j*10 + (9 - i)] == 'K'):
                piece = 'K'
            elif(bo[j*10 + (9 - i)] == 'k'):
                piece = 'k'
            else:
                piece = bo[j*10 + (9 - i)]
            if piece != "..":
                screen.blit(IMAGES[piece[0]], p.Rect((j-1)*SQ_SIZE, (i-1)*SQ_SIZE, SQ_SIZE, SQ_SIZE))

    clock.tick(MAX_FPS)
    p.display.flip()

#Update(screen, textRectObj, textSurfaceObj, clock)




count_party = 0 # Количество партий
count_party_two = 0 # Количество партий 2 вариант
partyNow = 0

CBH_Decode = [
	162,149,67,245,193,61,74,108,83,131,204,124,255,174,104,173,
	209,146,139,141,53,129,94,116,38,142,171,202,253,154,243,160,
	165,21,252,177,30,237,48,234,34,235,167,205,78,111,46,36,
	50,148,65,140,110,88,130,80,187,2,138,216,250,96,222,82,
	186,70,172,41,157,215,223,8,33,1,102,163,241,25,39,181,
	145,213,66,14,180,76,217,24,95,188,37,166,150,4,86,106,
	170,51,28,43,115,240,221,164,55,211,197,16,191,90,35,52,
	117,91,184,85,210,107,9,58,87,18,179,119,72,133,155,15,
	158,199,200,161,127,122,192,189,49,109,246,62,195,17,113,206,
	125,218,168,84,144,151,31,68,64,22,201,227,44,203,132,236,
	159,63,92,230,118,11,60,32,183,54,0,220,231,249,79,247,
	175,6,7,224,26,10,169,75,12,214,99,135,137,29,19,27,
	228,112,5,71,103,123,47,238,226,232,152,13,239,207,196,244,
	251,176,23,153,100,242,212,42,3,77,120,198,254,101,134,136,
	121,69,59,229,73,143,45,185,190,98,147,20,233,208,56,156,
	178,194,89,93,182,114,81,248,40,126,97,57,225,219,105,128]

partyOrText = [] # Список содержащий 0 и 1 и 2, 0 - значит сопроводительный текст, 1 - значит описание партии, 2 - блок был удален
posCBG = [] # Позиция в файле CBG, где описываются последовательности ходов в партии
posCBA = [] # Позиция в файле CBA, откуда ничанается описание комментариев к партии
posCBPWhite = [] # Номер блока в файле CBP для игрока белыми
posCBPBlack = [] # Номер блока в файле CBp для игрока чёрными
posCBT = [] # Номер турнира в файле CBT
posCBC = [] # Номер комментатора в файле CBC
posCBS = [] # Номер источника в файле CBS
date = [] # Даты проведения партий
result_party = [] # Результаты партий
scoreLineParty = [] # Оценка линии в партии
round = []
podround = []
eloRatingWhite = []
eloRatingBlack = []
posECO = [] ##########################
flagMedal = [] # Флаги медалей
flag1 = [] # Флаги
flag2 = []
flag3 = []
flag4 = []
lesson = [] # Содержит ли партия упражнения
countStepParty = [] # Количество ходов в партии


translate_16_2 = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
                   '8': '1000','9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'}


def Translate_16_2(number):
    result = ''
    number = str(number)
    for i in number:
        result += translate_16_2[i]
        
    return result




def hexConvert(hex_list):
    for i in range(len(hex_list)):
        if(len(hex_list[i]) == 1):
            hex_list[i] = '0' + hex_list[i]
    return hex_list

def bitSlice(number, a, b):
    number = Translate_16_2(number)
    if(a > len(number)):
        return 0
    return int(number[-b:len(number)-a:1], 2)


def offsetsAndBytes(hex_list, offset, bytes, number):
    buff = ''
    for i in range(offset, offset+bytes, 1):
        buff += hex_list[i + number]
    
    return int(buff, 16)


def offsetsAndBytes0(hex_list, offset, bytes, number):
    buff = ''
    for i in range(offset, offset+bytes, 1):
        buff += hex_list[i + number]
    if(int(buff, 16) == 0):
        return 'Значение не задано'
    return int(buff, 16)

def Decode(CBH_Decode, byte, move):
    buff = CBH_Decode[(int(byte, 16) - move) % 256]
    return str(hex(buff))[2:]

# Открываем файл в режиме "rb" (бинарный режим чтения)
with open('CBH/chess/CBH/q.cbh', 'rb') as f:
    # Читаем содержимое файла в виде байтов
    data = f.read()

# Преобразуем байты в список шестнадцатеричных чисел
hex_list = [hex(b)[2:] for b in data]

# Выведем список на экран

# Делаем вместо 1 нуля 2 и ставим 0 в начало:
hex_list = hexConvert(hex_list)

buff = ''


#####################################################
for i in range(46): # расшифровка заголовка cbh файла
    if(i < 6): #  Смещение 0
        buff += hex_list[i]
        if(i == 5):
            print(buff)
            if(buff == '00002c002e01'):
                print('ChessBase 9')
            else:
                print('CBlight')
            buff = ''
    if(i >= 6 and i < 10): # Вычисление количества партий
        buff += hex_list[i]
        if(i == 9):
            count_party = int(buff, 16) - 1
            print("Количество партий:", count_party)
            buff = ''
    if(i >= 40 and i < 44):
        buff += hex_list[i]
        if(i == 43):
            print(buff)
            count_party_two = int(buff, 16)
            print("Количество партий:(2 вариант)", count_party_two)
            buff = ''
#####################################################
for i in range(46, len(hex_list), 46):
    if(bitSlice(hex_list[i], 0, 2) == 1):
        partyOrText.append(1)
    elif(bitSlice(hex_list[i], 0, 2) == 3):
        partyOrText.append(0)
    elif(bitSlice(hex_list[i], 7, 8) == 1):
        partyOrText.append(2)
    posCBG.append(offsetsAndBytes(hex_list, 1, 4, i))
    if(partyOrText[partyNow] == 1): # Описании партии
        posCBA.append(offsetsAndBytes(hex_list, 5, 4, i))
        posCBPWhite.append(offsetsAndBytes(hex_list, 9, 3, i))
        posCBPBlack.append(offsetsAndBytes(hex_list, 12, 3, i))
        posCBT.append(offsetsAndBytes(hex_list, 15, 3, i))
        posCBC.append(offsetsAndBytes(hex_list, 18, 3, i))
        posCBS.append(offsetsAndBytes(hex_list, 21, 3, i))

        buff = ''
        buff += str(bitSlice(hex_list[i+24], 0, 4)) + '.'
        buff += str(bitSlice(hex_list[i+24] + hex_list[i+25], 5, 8)) + '.'
        buff += str(bitSlice(hex_list[i+24] + hex_list[i+25] + hex_list[i+26], 9, 21))
        date.append(buff)
        buff = ''

        buff = int(Translate_16_2(hex_list[i+27]), 2) # Смещение 27
        if(buff == 0):
            result_party.append('0-1')
        elif(buff == 1):
            result_party.append('1/2-1/2')
        elif(buff == 2):
            result_party.append('1-0')
        elif(buff == 3):
            result_party.append('28')
        elif(buff == 4):
            result_party.append('-:+')
        elif(buff == 5):
            result_party.append('=:=')
        elif(buff == 6):
            result_party.append('+:-')
        elif(buff == 7):
            result_party.append('0-0')
        if(result_party[i//46 - 1] == '28'):
            buff = hex_list[i + 28]
            if(buff == '00'):
                scoreLineParty.append("Оценка не задана")
            elif(buff == '0b'):
                scoreLineParty.append("=")
            elif(buff == '0d'):
                scoreLineParty.append("Позиция неясная")
            elif(buff == '0e'):
                scoreLineParty.append("+/=")
            elif(buff == '0f'):
                scoreLineParty.append("-/=")
            elif(buff == '10'):
                scoreLineParty.append("+/-")
            elif(buff == '11'):
                scoreLineParty.append("-/+")
            elif(buff == '12'):
                scoreLineParty.append("+-")
            elif(buff == '13'):
                scoreLineParty.append("-+")
            elif(buff == '20'):
                scoreLineParty.append("Развитие превосходства")
            elif(buff == '24'):
                scoreLineParty.append("С инициативой")
            elif(buff == '28'):
                scoreLineParty.append("С атакаой")
            elif(buff == '2c'):
                scoreLineParty.append("с компенсацией материала")
            elif(buff == '84'):
                scoreLineParty.append("С контригрой")
            elif(buff == '8a'):
                scoreLineParty.append("цейтнот")
            elif(buff == '92'):
                scoreLineParty.append("новинка")
        else:
            scoreLineParty.append('')
        


        round.append(offsetsAndBytes0(hex_list, 29, 1, i))
        podround.append(offsetsAndBytes0(hex_list, 30, 1, i))
        eloRatingWhite.append(offsetsAndBytes0(hex_list, 31, 2, i))
        eloRatingBlack.append(offsetsAndBytes0(hex_list, 33, 2, i))
        posECO.append(offsetsAndBytes0(hex_list, 35, 2, i)) # не доделано
        flagMedal.append(offsetsAndBytes(hex_list, 37, 2, i)) # не доделано
        flag1.append(offsetsAndBytes(hex_list, 39, 1, i)) # не доделано
        flag2.append(offsetsAndBytes(hex_list, 40, 1, i)) # не доделано
        lesson.append(offsetsAndBytes(hex_list, 41, 1, i)) # не доделано
        flag3.append(offsetsAndBytes(hex_list, 42, 1, i)) # не доделано
        flag4.append(offsetsAndBytes(hex_list, 44, 1, i)) # не доделано
        countStepParty.append(offsetsAndBytes(hex_list, 45, 1, i)) # не доделано




    elif(partyOrText[partyNow] == 0): # Сопроводительный текст(не доделано) надо добавить добавление пустных строк ну и по смещениям передвигаться там немного
        pass
    if(partyOrText[partyNow] == 2): # Удаленный блок
        pass
####################################################################
party = []
for i in range(count_party):
    party.append(list())

#CBG файл - информация о партиях
# Открываем файл в режиме "rb" (бинарный режим чтения)
with open('CBH/chess/CBH/q.cbg', 'rb') as f:
    # Читаем содержимое файла в виде байтов
    data = f.read()

# Преобразуем байты в список шестнадцатеричных чисел
hex_listCBG = [hex(b)[2:] for b in data]

# Выведем список на экран


# Делаем вместо 1 нуля 2 и ставим 0 в начало:
hex_listCBG = hexConvert(hex_listCBG)

law = {
        18: "a8", 28: "b8", 38: "c8", 48: "d8", 58: "e8", 68: "f8", 78: "g8", 88: "h8",
        17: "a7", 27: "b7", 37: "c7", 47: "d7", 57: "e7", 67: "f7", 77: "g7", 87: "h7",
        16: "a6", 26: "b6", 36: "c6", 46: "d6", 56: "e6", 66: "f6", 76: "g6", 86: "h6",
        15: "a5", 25: "b5", 35: "c5", 45: "d5", 55: "e5", 65: "f5", 75: "g5", 85: "h5",
        14: "a4", 24: "b4", 34: "c4", 44: "d4", 54: "e4", 64: "f4", 74: "g4", 84: "h4",
        13: "a3", 23: "b3", 33: "c3", 43: "d3", 53: "e3", 63: "f3", 73: "g3", 83: "h3",
        12: "a2", 22: "b2", 32: "c2", 42: "d2", 52: "e2", 62: "f2", 72: "g2", 82: "h2",
        11: "a1", 21: "b1", 31: "c1", 41: "d1", 51: "e1", 61: "f1", 71: "g1", 81: "h1"
}

figureForKill = ['r1', 'r2', 'r3', 'n1', 'n2', 'n3', 'b1', 'b2', 'b3','q1', 'q2', 'q3',
                 'R1', 'R2', 'R3', 'N1', 'N2', 'N3', 'B1', 'B2', 'B3','Q1', 'Q2', 'Q3'
                ]



def killOld():
    for i in posFigure:
        if(i in figureForKill):
            if(posFigure[i] == 0):
                if(i[1] == '2' and posFigure[i[0] + '3'] != 0):
                    posFigure[i[0] + '2'] = posFigure[i[0] + '3']
                    posFigure[i[0] + '3'] = 0
                if(i[1] == '1' and posFigure[i[0] + '2'] != 0):
                    posFigure[i] = posFigure[i[0] + '2']
                    posFigure[i[0] + '2'] = 0
                    if(i == 'q2' or i == 'Q2'):
                        posFigure[i[0] + '2'] = 0
                    if(posFigure[i[0] + '3'] != 0):
                        posFigure[i[0] + '2'] = posFigure[i[0] + '3']
                        posFigure[i[0] + '3'] = 0
    for i in posFigure:
        if(i in figureForKill):
            if(posFigure[i] == 0):
                if(i[1] == '2' and posFigure[i[0] + '3'] != 0):
                    posFigure[i[0] + '2'] = posFigure[i[0] + '3']
                    posFigure[i[0] + '3'] = 0
                if(i[1] == '1' and posFigure[i[0] + '2'] != 0):
                    posFigure[i] = posFigure[i[0] + '2']
                    posFigure[i[0] + '2'] = 0
                    if(i == 'q2' or i == 'Q2'):
                        posFigure[i[0] + '2'] = 0
                    if(posFigure[i[0] + '3'] != 0):
                        posFigure[i[0] + '2'] = posFigure[i[0] + '3']
                        posFigure[i[0] + '3'] = 0
                




def PrintBoard():
    bb = {
            18: "..", 28: "..", 38: "..", 48: "..", 58: "..", 68: "..", 78: "..", 88: "..",
            17: "..", 27: "..", 37: "..", 47: "..", 57: "..", 67: "..", 77: "..", 87: "..",
            16: "..", 26: "..", 36: "..", 46: "..", 56: "..", 66: "..", 76: "..", 86: "..",
            15: "..", 25: "..", 35: "..", 45: "..", 55: "..", 65: "..", 75: "..", 85: "..",
            14: "..", 24: "..", 34: "..", 44: "..", 54: "..", 64: "..", 74: "..", 84: "..",
            13: "..", 23: "..", 33: "..", 43: "..", 53: "..", 63: "..", 73: "..", 83: "..",
            12: "..", 22: "..", 32: "..", 42: "..", 52: "..", 62: "..", 72: "..", 82: "..",
            11: "..", 21: "..", 31: "..", 41: "..", 51: "..", 61: "..", 71: "..", 81: "..",
        }
    for i in posFigure:
        if(posFigure[i] == 0):
            pass
        else:
            bb[posFigure[i]] = i

    for i in range(1, 9, 1):
        for j in range(1, 9, 1):
            if(bb[j*10 + (9 - i)] == 'K'):
                print("K ", end='   ', sep='')
            elif(bb[j*10 + (9 - i)] == 'k'):
                print("k ", end='   ', sep='')
            else:
                print(bb[j*10 + (9 - i)], end='   ', sep='')
        print()
            

def translateCBHtoMe(name, x, y, color): # Перевод из CBH форматов в обычный типа: a2a4 и тд
    #print("color = ", color)
    if(color == 1):
        name = name.upper()
        #print("NAMENAMENAME = ", name)
        buff = posFigure[name]
        moveIn = ((buff // 10 + x - 1) % 8 + 1) * 10 + (buff % 10 + y - 1) % 8 + 1
        for i in posFigure:
            if(posFigure[i] == moveIn):
                posFigure[i] = 0
                killOld()
        posFigure[name] = moveIn
        ''' print("x, y = ", x, y)
        print("moveIn = ", moveIn)'''
        return law[buff] + law[moveIn]
    else:
        name = name.lower()
        buff = posFigure[name]
        #print(posFigure)
        if(name[0] == 'p'):
            moveIn = ((buff // 10 - x - 1) % 8 + 1) * 10 + (buff % 10 - y - 1) % 8 + 1
            for i in posFigure:
                if(posFigure[i] == moveIn):
                    posFigure[i] = 0
                    killOld()
            posFigure[name] = moveIn
            '''print("NAMENAMENAME = ", name)
            print("x, y = ", x, y)
            print("buff = ", buff)
            print("moveIn = ", moveIn)'''
            return law[buff] + law[moveIn]
        else:
            moveIn = ((buff // 10 + x - 1) % 8 + 1) * 10 + (buff % 10 + y - 1) % 8 + 1
            for i in posFigure:
                if(posFigure[i] == moveIn):
                    posFigure[i] = 0
                    killOld()
            posFigure[name] = moveIn
            '''print("NAMENAMENAME = ", name)
            print("x, y = ", x, y)
            print("buff = ", buff)
            print("moveIn = ", moveIn)'''
            return law[buff] + law[moveIn]
        
def translateCBHtoMe2Byte(name, x, y, color):
    pass
    


# В формате заголовка храниятся лишь позиция первой записанной партии, конец CBG файла и скммарное значение изменённых байтов по всем партиями
lenDataParty = [] # Размер блока
unPosParty = [] # начинается ли с нестандартной позиции
for i in range(count_party):
    posFigure = {
        "r1": 18, "n1": 28, "b1": 38, "q1": 48, "k": 58, "b2": 68, "n2": 78, "r2": 88,
        "p1": 17, "p2": 27, "p3": 37, "p4": 47, "p5": 57, "p6": 67, "p7": 77, "p8": 87,
        "P1": 12, "P2": 22, "P3": 32, "P4": 42, "P5": 52, "P6": 62, "P7": 72, "P8": 82,
        "R1": 11, "N1": 21, "B1": 31, "Q1": 41, "K": 51, "B2": 61, "N2": 71, "R2": 81,
        "r3": 0, "n3": 0, "b3": 0, "q2": 0, "q3": 0,
        "R3": 0, "N3": 0, "B3": 0, "Q2": 0, "Q3": 0
}
    if(i == 15):
        break
    move = 0
    print(i)
    start = posCBG[i]
    buff = hex_listCBG[start] + hex_listCBG[start+1] + hex_listCBG[start+2] + hex_listCBG[start+3]
    lenDataParty.append(bitSlice(buff, 0, 30))
    unPosParty.append(bitSlice(buff, 30, 31))
    start += 4
    #unPosParty.append(bitSlice(buff, 30, 31)) 31 смещение CBG фомат даных партии
    counter = 0
    color = True # True - ходят белые
    byte2 = 0 # Количество двухбайтовых ходов * 2
    numBranch = 1 # Указывает на количество ответвлений
    counterBranch = 0 # Указывает на количество байт затраченных на ответвления
    buffMove = 0 # Указывает на количество совершенных ходов до ответвления
    ignor = 0 # Для игнорирования одного из байтов

    while(True):
        tempor = Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor], move)
        
        if(len(tempor) == 1):
            tempor = '0' + tempor
        #print("move = ", move, '; tempor =  ', tempor)
        if(tempor == 'fe'):
            buffMove = move
            party[i].append('(') # ( - означает, что новое ответвление
            numBranch += 1
            counterBranch += 1
            continue
        if(tempor == 'ff'):
            numBranch -= 1
            if(numBranch == 0):
                break
                
            else:
                counterBranch += move - buffMove + 1
                move = buffMove
                party[i].append(')') # ) - означает окончание ответвления
                continue
            
        if(tempor == 'eb'): # Переход в двухбайтовые ходы
            summ2Byte = ''
            if(len(Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 1], move)) == 1):
                summ2Byte += '0' + Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 1], move)
            else:
                summ2Byte += Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 1], move)
            if(len(Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 2], move)) == 1):
                summ2Byte += '0' + Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 2], move)
            else:
                summ2Byte += Decode(CBH_Decode, hex_listCBG[start + move + byte2 + counterBranch + ignor + 2], move)
            strokaFrom = bitSlice(summ2Byte, 0, 3)
            stolbFrom = bitSlice(summ2Byte, 3, 6)
            strokaIn = bitSlice(summ2Byte, 6, 9)
            stolbIn = bitSlice(summ2Byte, 9, 12)
            who = bitSlice(summ2Byte, 12, 14)
            From = (stolbFrom+1)*10 + strokaFrom + 1
            In = (stolbIn+1)*10 + strokaIn + 1
            for j in posFigure:
                if(posFigure[j] == In):
                    posFigure[j] = 0
                    killOld()
            tqt = 0
            if(color == 1):
                for j in posFigure:
                    if(posFigure[j] == From and j[0] == 'P'):

                        if(strokaFrom == 6):
                            tqt = 1
                            #print('who = ', who)
                            if(who == 0):
                                if('Q2' in posFigure):
                                    posFigure['Q3'] = In
                                else:
                                    posFigure['Q2'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'Q'
                                killOld()
                            elif(who == 1):
                                posFigure['R3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'R'
                                killOld()
                            elif(who == 2):
                                posFigure['B3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'B'
                                killOld()
                            elif(who == 3):
                                posFigure['N3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'N'
                                killOld()
                        break
                if(tqt != 1):
                    posFigure[j] = In
                    moveUCI = law[From] + law[In]
                    killOld()
            else:
                for j in posFigure:
                    #print("name=", j)
                    if(posFigure[j] == From and j[0] == 'p'):
                        #print('strokaFrom = ', strokaFrom)
                        #print('who', who)
                        if(strokaFrom == 1):
                            tqt = 1
                            if(who == 0):
                                if(posFigure['q2'] != 0):
                                    posFigure['q3'] = In
                                else:
                                    posFigure['q2'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'q'
                               # print("nenennene", moveUCI)
                                killOld()
                                break
                            elif(who == 1):
                                posFigure['r3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'r'
                                killOld()
                                break
                            elif(who == 2):
                                posFigure['b3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'b'
                                killOld()
                                break
                            elif(who == 3):
                                posFigure['n3'] = In
                                posFigure[j] = '0'
                                moveUCI = law[From] + law[In] + 'n'
                                killOld()
                                break
                        break
                if(tqt != 1):
                    posFigure[j] = In
                    moveUCI = law[From] + law[In]
                    killOld()
                
            #print('move = ', move)
            byte2 += 2
            #print('Двухбайтовый!')
        if(tempor == 'ec'):# Игнорировать этот байт и не добавлять move
            ignor += 1
            continue

        if(tempor == '01'):
            moveUCI = translateCBHtoMe('k', 0, 1, color)
        elif(tempor == '02'):
            moveUCI = translateCBHtoMe('k', 1, 1, color)
        elif(tempor == '03'):
            moveUCI = translateCBHtoMe('k', 1, 0, color)
        elif(tempor == '04'):
            moveUCI = translateCBHtoMe('k', 1, 7, color)
        elif(tempor == '05'):
            moveUCI = translateCBHtoMe('k', 0, 7, color)
        elif(tempor == '06'):
            moveUCI = translateCBHtoMe('k', 7, 7, color)
        elif(tempor == '07'):
            moveUCI = translateCBHtoMe('k', 7, 0, color)
        elif(tempor == '08'):
            moveUCI = translateCBHtoMe('k', 7, 1, color)
        elif(tempor == '09'): # O-O
            moveUCI = 'O-O'
            if(color == 1):
                posFigure['K'] = 71
                posFigure['R2'] = 61
            else:
                posFigure['k'] = 78
                posFigure['r2'] = 68
        elif(tempor == '0a'): # O-O-O
            moveUCI = 'O-O-O'
            if(color == 1):
                posFigure['K'] = 31
                posFigure['R1'] = 41
            else:
                posFigure['k'] = 38
                posFigure['r1'] = 48
            
        elif(tempor == '0b'):
            moveUCI = translateCBHtoMe('q1', 0, 1, color)
        elif(tempor == '0c'):
            moveUCI = translateCBHtoMe('q1', 0, 2, color)
        elif(tempor == '0d'):
            moveUCI = translateCBHtoMe('q1', 0, 3, color)
        elif(tempor == '0e'):
            moveUCI = translateCBHtoMe('q1', 0, 4, color)
        elif(tempor == '0f'):
            moveUCI = translateCBHtoMe('q1', 0, 5, color)
        elif(tempor == '10'):
            moveUCI = translateCBHtoMe('q1', 0, 6, color)
        elif(tempor == '11'):
            moveUCI = translateCBHtoMe('q1', 0, 7, color)
        elif(tempor == '12'):
            moveUCI = translateCBHtoMe('q1', 1, 0, color)
        elif(tempor == '13'):
            moveUCI = translateCBHtoMe('q1', 2, 0, color)
        elif(tempor == '14'):
            moveUCI = translateCBHtoMe('q1', 3, 0, color)
        elif(tempor == '15'):
            moveUCI = translateCBHtoMe('q1', 4, 0, color)
        elif(tempor == '16'):
            moveUCI = translateCBHtoMe('q1', 5, 0, color)
        elif(tempor == '17'):
            moveUCI = translateCBHtoMe('q1', 6, 0, color)
        elif(tempor == '18'):
            moveUCI = translateCBHtoMe('q1', 7, 0, color)
        elif(tempor == '19'):
            moveUCI = translateCBHtoMe('q1', 1, 1, color)
        elif(tempor == '1a'):
            moveUCI = translateCBHtoMe('q1', 2, 2, color)
        elif(tempor == '1b'):
            moveUCI = translateCBHtoMe('q1', 3, 3, color)
        elif(tempor == '1c'):
            moveUCI = translateCBHtoMe('q1', 4, 4, color)
        elif(tempor == '1d'):
            moveUCI = translateCBHtoMe('q1', 5, 5, color)
        elif(tempor == '1e'):
            moveUCI = translateCBHtoMe('q1', 6, 6, color)
        elif(tempor == '1f'):
            moveUCI = translateCBHtoMe('q1', 7, 7, color)
        elif(tempor == '20'):
            moveUCI = translateCBHtoMe('q1', 1, 7, color)
        elif(tempor == '21'):
            moveUCI = translateCBHtoMe('q1', 2, 6, color)
        elif(tempor == '22'):
            moveUCI = translateCBHtoMe('q1', 3, 5, color)
        elif(tempor == '23'):
            moveUCI = translateCBHtoMe('q1', 4, 4, color)
        elif(tempor == '24'):
            moveUCI = translateCBHtoMe('q1', 5, 3, color)
        elif(tempor == '25'):
            moveUCI = translateCBHtoMe('q1', 6, 2, color)
        elif(tempor == '26'):
            moveUCI = translateCBHtoMe('q1', 7, 1, color)
        elif(tempor == '27'):
            moveUCI = translateCBHtoMe('r1', 0, 1, color)
        elif(tempor == '28'):
            moveUCI = translateCBHtoMe('r1', 0, 2, color)
        elif(tempor == '29'):
            moveUCI = translateCBHtoMe('r1', 0, 3, color)
        elif(tempor == '2a'):
            moveUCI = translateCBHtoMe('r1', 0, 4, color)
        elif(tempor == '2b'):
            moveUCI = translateCBHtoMe('r1', 0, 5, color)
        elif(tempor == '2c'):
            moveUCI = translateCBHtoMe('r1', 0, 6, color)
        elif(tempor == '2d'):
            moveUCI = translateCBHtoMe('r1', 0, 7, color)
        elif(tempor == '2e'):
            moveUCI = translateCBHtoMe('r1', 1, 0, color)
        elif(tempor == '2f'):
            moveUCI = translateCBHtoMe('r1', 2, 0, color)
        elif(tempor == '30'):
            moveUCI = translateCBHtoMe('r1', 3, 0, color)
        elif(tempor == '31'):
            moveUCI = translateCBHtoMe('r1', 4, 0, color)
        elif(tempor == '32'):
            moveUCI = translateCBHtoMe('r1', 5, 0, color)
        elif(tempor == '33'):
            moveUCI = translateCBHtoMe('r1', 6, 0, color)
        elif(tempor == '34'):
            moveUCI = translateCBHtoMe('r1', 7, 0, color)
        elif(tempor == '35'):
            moveUCI = translateCBHtoMe('r2', 0, 1, color)
        elif(tempor == '36'):
            moveUCI = translateCBHtoMe('r2', 0, 2, color)
        elif(tempor == '37'):
            moveUCI = translateCBHtoMe('r2', 0, 3, color)
        elif(tempor == '38'):
            moveUCI = translateCBHtoMe('r2', 0, 4, color)
        elif(tempor == '39'):
            moveUCI = translateCBHtoMe('r2', 0, 5, color)
        elif(tempor == '3a'):
            moveUCI = translateCBHtoMe('r2', 0, 6, color)
        elif(tempor == '3b'):
            moveUCI = translateCBHtoMe('r2', 0, 7, color)
        elif(tempor == '3c'):
            moveUCI = translateCBHtoMe('r2', 1, 0, color)
        elif(tempor == '3d'):
            moveUCI = translateCBHtoMe('r2', 2, 0, color)
        elif(tempor == '3e'):
            moveUCI = translateCBHtoMe('r2', 3, 0, color)
        elif(tempor == '3f'):
            moveUCI = translateCBHtoMe('r2', 4, 0, color)
        elif(tempor == '40'):
            moveUCI = translateCBHtoMe('r2', 5, 0, color)
        elif(tempor == '41'):
            moveUCI = translateCBHtoMe('r2', 6, 0, color)
        elif(tempor == '42'):
            moveUCI = translateCBHtoMe('r2', 7, 0, color)
        elif(tempor == '43'):
            moveUCI = translateCBHtoMe('b1', 1, 1, color)
        elif(tempor == '44'):
            moveUCI = translateCBHtoMe('b1', 2, 2, color)
        elif(tempor == '45'):
            moveUCI = translateCBHtoMe('b1', 3, 3, color)
        elif(tempor == '46'):
            moveUCI = translateCBHtoMe('b1', 4, 4, color)
        elif(tempor == '47'):
            moveUCI = translateCBHtoMe('b1', 5, 5, color)
        elif(tempor == '48'):
            moveUCI = translateCBHtoMe('b1', 6, 6, color)
        elif(tempor == '49'):
            moveUCI = translateCBHtoMe('b1', 7, 7, color)
        elif(tempor == '4a'):
            moveUCI = translateCBHtoMe('b1', 1, 7, color)
        elif(tempor == '4b'):
            moveUCI = translateCBHtoMe('b1', 2, 6, color)
        elif(tempor == '4c'):
            moveUCI = translateCBHtoMe('b1', 3, 5, color)
        elif(tempor == '4d'):
            moveUCI = translateCBHtoMe('b1', 4, 4, color)
        elif(tempor == '4e'):
            moveUCI = translateCBHtoMe('b1', 5, 3, color)
        elif(tempor == '4f'):
            moveUCI = translateCBHtoMe('b1', 6, 2, color)
        elif(tempor == '50'):
            moveUCI = translateCBHtoMe('b1', 7, 1, color)
        elif(tempor == '51'):
            moveUCI = translateCBHtoMe('b2', 1, 1, color)
        elif(tempor == '52'):
            moveUCI = translateCBHtoMe('b2', 2, 2, color)
        elif(tempor == '53'):
            moveUCI = translateCBHtoMe('b2', 3, 3, color)
        elif(tempor == '54'):
            moveUCI = translateCBHtoMe('b2', 4, 4, color)
        elif(tempor == '55'):
            moveUCI = translateCBHtoMe('b2', 5, 5, color)
        elif(tempor == '56'):
            moveUCI = translateCBHtoMe('b2', 6, 6, color)
        elif(tempor == '57'):
            moveUCI = translateCBHtoMe('b2', 7, 7, color)
        elif(tempor == '58'):
            moveUCI = translateCBHtoMe('b2', 1, 7, color)
        elif(tempor == '59'):
            moveUCI = translateCBHtoMe('b2', 2, 6, color)
        elif(tempor == '5a'):
            moveUCI = translateCBHtoMe('b2', 3, 5, color)
        elif(tempor == '5b'):
            moveUCI = translateCBHtoMe('b2', 4, 4, color)
        elif(tempor == '5c'):
            moveUCI = translateCBHtoMe('b2', 5, 3, color)
        elif(tempor == '5d'):
            moveUCI = translateCBHtoMe('b2', 6, 2, color)
        elif(tempor == '5e'):
            moveUCI = translateCBHtoMe('b2', 7, 1, color)
        elif(tempor == '5f'):
            moveUCI = translateCBHtoMe('n1', 2, 1, color)
        elif(tempor == '60'):
            moveUCI = translateCBHtoMe('n1', 1, 2, color)
        elif(tempor == '61'):
            moveUCI = translateCBHtoMe('n1', 7, 2, color)
        elif(tempor == '62'):
            moveUCI = translateCBHtoMe('n1', 6, 1, color)
        elif(tempor == '63'):
            moveUCI = translateCBHtoMe('n1', 6, 7, color)
        elif(tempor == '64'):
            moveUCI = translateCBHtoMe('n1', 7, 6, color)
        elif(tempor == '65'):
            moveUCI = translateCBHtoMe('n1', 1, 6, color)
        elif(tempor == '66'):
            moveUCI = translateCBHtoMe('n1', 2, 7, color)
        elif(tempor == '67'):
            moveUCI = translateCBHtoMe('n2', 2, 1, color)
        elif(tempor == '68'):
            moveUCI = translateCBHtoMe('n2', 1, 2, color)
        elif(tempor == '69'):
            moveUCI = translateCBHtoMe('n2', 7, 2, color)
        elif(tempor == '6a'):
            moveUCI = translateCBHtoMe('n2', 6, 1, color)
        elif(tempor == '6b'):
            moveUCI = translateCBHtoMe('n2', 6, 7, color)
        elif(tempor == '6c'):
            moveUCI = translateCBHtoMe('n2', 7, 6, color)
        elif(tempor == '6d'):
            moveUCI = translateCBHtoMe('n2', 1, 6, color)
        elif(tempor == '6e'):
            moveUCI = translateCBHtoMe('n2', 2, 7, color)
        elif(tempor == '6f'):
            moveUCI = translateCBHtoMe('p1', 0, 1, color)
        elif(tempor == '70'):
            moveUCI = translateCBHtoMe('p1', 0, 2, color)
        elif(tempor == '71'):
            moveUCI = translateCBHtoMe('p1', 1, 1, color)
        elif(tempor == '72'):
            moveUCI = translateCBHtoMe('p1', 7, 1, color)
        elif(tempor == '73'):
            moveUCI = translateCBHtoMe('p2', 0, 1, color)
        elif(tempor == '74'):
            moveUCI = translateCBHtoMe('p2', 0, 2, color)
        elif(tempor == '75'):
            moveUCI = translateCBHtoMe('p2', 1, 1, color)
        elif(tempor == '76'):
            moveUCI = translateCBHtoMe('p2', 7, 1, color)
        elif(tempor == '77'):
            moveUCI = translateCBHtoMe('p3', 0, 1, color)
        elif(tempor == '78'):
            moveUCI = translateCBHtoMe('p3', 0, 2, color)
        elif(tempor == '79'):
            moveUCI = translateCBHtoMe('p3', 1, 1, color)
        elif(tempor == '7a'):
            moveUCI = translateCBHtoMe('p3', 7, 1, color)
        elif(tempor == '7b'):
            moveUCI = translateCBHtoMe('p4', 0, 1, color)
        elif(tempor == '7c'):
            moveUCI = translateCBHtoMe('p4', 0, 2, color)
        elif(tempor == '7d'):
            moveUCI = translateCBHtoMe('p4', 1, 1, color)
        elif(tempor == '7e'):
            moveUCI = translateCBHtoMe('p4', 7, 1, color)
        elif(tempor == '7f'):
            moveUCI = translateCBHtoMe('p5', 0, 1, color)
        elif(tempor == '80'):
            moveUCI = translateCBHtoMe('p5', 0, 2, color)
        elif(tempor == '81'):
            moveUCI = translateCBHtoMe('p5', 1, 1, color)
        elif(tempor == '82'):
            moveUCI = translateCBHtoMe('p5', 7, 1, color)
        elif(tempor == '83'):
            moveUCI = translateCBHtoMe('p6', 0, 1, color)
        elif(tempor == '84'):
            moveUCI = translateCBHtoMe('p6', 0, 2, color)
        elif(tempor == '85'):
            moveUCI = translateCBHtoMe('p6', 1, 1, color)
        elif(tempor == '86'):
            moveUCI = translateCBHtoMe('p6', 7, 1, color)
        elif(tempor == '87'):
            moveUCI = translateCBHtoMe('p7', 0, 1, color)
        elif(tempor == '88'):
            moveUCI = translateCBHtoMe('p7', 0, 2, color)
        elif(tempor == '89'):
            moveUCI = translateCBHtoMe('p7', 1, 1, color)
        elif(tempor == '8a'):
            moveUCI = translateCBHtoMe('p7', 7, 1, color)
        elif(tempor == '8b'):
            moveUCI = translateCBHtoMe('p8', 0, 1, color)
        elif(tempor == '8c'):
            moveUCI = translateCBHtoMe('p8', 0, 2, color)
        elif(tempor == '8d'):
            moveUCI = translateCBHtoMe('p8', 1, 1, color)
        elif(tempor == '8e'):
            moveUCI = translateCBHtoMe('p8', 7, 1, color)
        elif(tempor == '8f'):
            moveUCI = translateCBHtoMe('q2', 0, 1, color)
        elif(tempor == '90'):
            moveUCI = translateCBHtoMe('q2', 0, 2, color)
        elif(tempor == '91'):
            moveUCI = translateCBHtoMe('q2', 0, 3, color)
        elif(tempor == '92'):
            moveUCI = translateCBHtoMe('q2', 0, 4, color)
        elif(tempor == '93'):
            moveUCI = translateCBHtoMe('q2', 0, 5, color)
        elif(tempor == '94'):
            moveUCI = translateCBHtoMe('q2', 0, 6, color)
        elif(tempor == '95'):
            moveUCI = translateCBHtoMe('q2', 0, 7, color)
        elif(tempor == '96'):
            moveUCI = translateCBHtoMe('q2', 1, 0, color)
        elif(tempor == '97'):
            moveUCI = translateCBHtoMe('q2', 2, 0, color)
        elif(tempor == '98'):
            moveUCI = translateCBHtoMe('q2', 3, 0, color)
        elif(tempor == '99'):
            moveUCI = translateCBHtoMe('q2', 4, 0, color)
        elif(tempor == '9a'):
            moveUCI = translateCBHtoMe('q2', 5, 0, color)
        elif(tempor == '9b'):
            moveUCI = translateCBHtoMe('q2', 6, 0, color)
        elif(tempor == '9c'):
            moveUCI = translateCBHtoMe('q2', 7, 0, color)
        elif(tempor == '9d'):
            moveUCI = translateCBHtoMe('q2', 1, 1, color)
        elif(tempor == '9e'):
            moveUCI = translateCBHtoMe('q2', 2, 2, color)
        elif(tempor == '9f'):
            moveUCI = translateCBHtoMe('q2', 3, 3, color)
        elif(tempor == 'a0'):
            moveUCI = translateCBHtoMe('q2', 4, 4, color)
        elif(tempor == 'a1'):
            moveUCI = translateCBHtoMe('q2', 5, 5, color)
        elif(tempor == 'a2'):
            moveUCI = translateCBHtoMe('q2', 6, 6, color)
        elif(tempor == 'a3'):
            moveUCI = translateCBHtoMe('q2', 7, 7, color)
        elif(tempor == 'a4'):
            moveUCI = translateCBHtoMe('q2', 1, 7, color)
        elif(tempor == 'a5'):
            moveUCI = translateCBHtoMe('q2', 2, 6, color)
        elif(tempor == 'a6'):
            moveUCI = translateCBHtoMe('q2', 3, 5, color)
        elif(tempor == 'a7'):
            moveUCI = translateCBHtoMe('q2', 4, 4, color)
        elif(tempor == 'a8'):
            moveUCI = translateCBHtoMe('q2', 5, 3, color)
        elif(tempor == 'a9'):
            moveUCI = translateCBHtoMe('q2', 6, 2, color)
        elif(tempor == 'aa'):
            moveUCI = translateCBHtoMe('q2', 7, 1, color)

        elif(tempor == 'ab'):
            moveUCI = translateCBHtoMe('q3', 0, 1, color)
        elif(tempor == 'ac'):
            moveUCI = translateCBHtoMe('q3', 0, 2, color)
        elif(tempor == 'ad'):
            moveUCI = translateCBHtoMe('q3', 0, 3, color)
        elif(tempor == 'ae'):
            moveUCI = translateCBHtoMe('q3', 0, 4, color)
        elif(tempor == 'af'):
            moveUCI = translateCBHtoMe('q3', 0, 5, color)
        elif(tempor == 'b0'):
            moveUCI = translateCBHtoMe('q3', 0, 6, color)
        elif(tempor == 'b1'):
            moveUCI = translateCBHtoMe('q3', 0, 7, color)
        elif(tempor == 'b2'):
            moveUCI = translateCBHtoMe('q3', 1, 0, color)
        elif(tempor == 'b3'):
            moveUCI = translateCBHtoMe('q3', 2, 0, color)
        elif(tempor == 'b4'):
            moveUCI = translateCBHtoMe('q3', 3, 0, color)
        elif(tempor == 'b5'):
            moveUCI = translateCBHtoMe('q3', 4, 0, color)
        elif(tempor == 'b6'):
            moveUCI = translateCBHtoMe('q3', 5, 0, color)
        elif(tempor == 'b7'):
            moveUCI = translateCBHtoMe('q3', 6, 0, color)
        elif(tempor == 'b8'):
            moveUCI = translateCBHtoMe('q3', 7, 0, color)
        elif(tempor == 'b9'):
            moveUCI = translateCBHtoMe('q3', 1, 1, color)
        elif(tempor == 'ba'):
            moveUCI = translateCBHtoMe('q3', 2, 2, color)
        elif(tempor == 'bb'):
            moveUCI = translateCBHtoMe('q3', 3, 3, color)
        elif(tempor == 'bc'):
            moveUCI = translateCBHtoMe('q3', 4, 4, color)
        elif(tempor == 'bd'):
            moveUCI = translateCBHtoMe('q3', 5, 5, color)
        elif(tempor == 'be'):
            moveUCI = translateCBHtoMe('q3', 6, 6, color)
        elif(tempor == 'bf'):
            moveUCI = translateCBHtoMe('q3', 7, 7, color)
        elif(tempor == 'c0'):
            moveUCI = translateCBHtoMe('q3', 1, 7, color)
        elif(tempor == 'c1'):
            moveUCI = translateCBHtoMe('q3', 2, 6, color)
        elif(tempor == 'c2'):
            moveUCI = translateCBHtoMe('q3', 3, 5, color)
        elif(tempor == 'c3'):
            moveUCI = translateCBHtoMe('q3', 4, 4, color)
        elif(tempor == 'c4'):
            moveUCI = translateCBHtoMe('q3', 5, 3, color)
        elif(tempor == 'c5'):
            moveUCI = translateCBHtoMe('q3', 6, 2, color)
        elif(tempor == 'c6'):
            moveUCI = translateCBHtoMe('q3', 7, 1, color)

        elif(tempor == 'c7'):
            moveUCI = translateCBHtoMe('r3', 0, 1, color)
        elif(tempor == 'c8'):
            moveUCI = translateCBHtoMe('r3', 0, 2, color)
        elif(tempor == 'c9'):
            moveUCI = translateCBHtoMe('r3', 0, 3, color)
        elif(tempor == 'ca'):
            moveUCI = translateCBHtoMe('r3', 0, 4, color)
        elif(tempor == 'cb'):
            moveUCI = translateCBHtoMe('r3', 0, 5, color)
        elif(tempor == 'cc'):
            moveUCI = translateCBHtoMe('r3', 0, 6, color)
        elif(tempor == 'cd'):
            moveUCI = translateCBHtoMe('r3', 0, 7, color)
        elif(tempor == 'ce'):
            moveUCI = translateCBHtoMe('r3', 1, 0, color)
        elif(tempor == 'cf'):
            moveUCI = translateCBHtoMe('r3', 2, 0, color)
        elif(tempor == 'd0'):
            moveUCI = translateCBHtoMe('r3', 3, 0, color)
        elif(tempor == 'd1'):
            moveUCI = translateCBHtoMe('r3', 4, 0, color)
        elif(tempor == 'd2'):
            moveUCI = translateCBHtoMe('r3', 5, 0, color)
        elif(tempor == 'd3'):
            moveUCI = translateCBHtoMe('r3', 6, 0, color)
        elif(tempor == 'd4'):
            moveUCI = translateCBHtoMe('r3', 7, 0, color)

        elif(tempor == 'd5'):
            moveUCI = translateCBHtoMe('b3', 1, 1, color)
        elif(tempor == 'd6'):
            moveUCI = translateCBHtoMe('b3', 2, 2, color)
        elif(tempor == 'd7'):
            moveUCI = translateCBHtoMe('b3', 3, 3, color)
        elif(tempor == 'd8'):
            moveUCI = translateCBHtoMe('b3', 4, 4, color)
        elif(tempor == 'd9'):
            moveUCI = translateCBHtoMe('b3', 5, 5, color)
        elif(tempor == 'da'):
            moveUCI = translateCBHtoMe('b3', 6, 6, color)
        elif(tempor == 'db'):
            moveUCI = translateCBHtoMe('b3', 7, 7, color)
        elif(tempor == 'dc'):
            moveUCI = translateCBHtoMe('b3', 1, 7, color)
        elif(tempor == 'dd'):
            moveUCI = translateCBHtoMe('b3', 2, 6, color)
        elif(tempor == 'de'):
            moveUCI = translateCBHtoMe('b3', 3, 5, color)
        elif(tempor == 'df'):
            moveUCI = translateCBHtoMe('b3', 4, 4, color)
        elif(tempor == 'e0'):
            moveUCI = translateCBHtoMe('b3', 5, 3, color)
        elif(tempor == 'e1'):
            moveUCI = translateCBHtoMe('b3', 6, 2, color)
        elif(tempor == 'e2'):
            moveUCI = translateCBHtoMe('b3', 7, 1, color)

        elif(tempor == 'e3'):
            moveUCI = translateCBHtoMe('n3', 2, 1, color)
        elif(tempor == 'e4'):
            moveUCI = translateCBHtoMe('n3', 1, 2, color)
        elif(tempor == 'e5'):
            moveUCI = translateCBHtoMe('n3', 7, 2, color)
        elif(tempor == 'e6'):
            moveUCI = translateCBHtoMe('n3', 6, 1, color)
        elif(tempor == 'e7'):
            moveUCI = translateCBHtoMe('n3', 6, 7, color)
        elif(tempor == 'e8'):
            moveUCI = translateCBHtoMe('n3', 2, 1, color)
        elif(tempor == 'e9'):
            moveUCI = translateCBHtoMe('n3', 1, 6, color)
        elif(tempor == 'ea'):
            moveUCI = translateCBHtoMe('n3', 2, 7, color)
        #print("i = ", i)
        #print("moveUCI", moveUCI)
        party[i].append(moveUCI)
        #print('byte = ', hex_listCBG[start + move + byte2 + counterBranch + ignor])
        #print('tempor = ', tempor)
        
        
        #PrintBoard()
        #Update(screen, textRectObj, textSurfaceObj, clock)
        #clock.tick(MAX_FPS)
        #p.display.flip()
        move += 1
        color = -color
        #input()




        #counter += 1
print(lenDataParty[0])
print(unPosParty[0])
print(date[0])
print(result_party[0])
print(round[0])
print(podround[0])
print("Откуда начинаются партии: ", posCBG[:2])

############
#CBP file
with open('CBH/chess/CBH/q.cbp', 'rb') as f:
    # Читаем содержимое файла в виде байтов
    data = f.read()

# Преобразуем байты в список шестнадцатеричных чисел
hex_listCBP = [hex(b)[2:] for b in data]

# Выведем список на экран


# Делаем вместо 1 нуля 2 и ставим 0 в начало:
hex_listCBP = hexConvert(hex_listCBP)

print(hex_listCBP[:3])
hi = 'СТРОКА'.encode('utf-8')

for i in range(37, 67, 1):
    print(chr(int(hex_listCBP[i], 16)), end='   ')
print(hi)
print(hex(53252))


print(party[0])



lst = []

for i in range(15):
    lst.append((i+1, date[i], 'qwe'))