import tkinter
import random
import copy

kTargetFps = 60
kKindness = 2 # after num of kindness animal put, random line drops

index = 0 # 0 : intro, 1: playing, 2: gameover
timer = 0
score = 0
tsugi = 0
kindnessRemains = 0

cursor_x = 0
cursor_y = 0
mouse_c = False

block = []
check = []
img_block = None
cvs = None
bPendSetblock = False

def update_cursor(x, y):
    global cursor_x, cursor_y, index
    if 24 <= x and x < 24 + 72*8 and 24 <= y and y < 24 + 72*10:
        # 커서 위치 업데이트
        cursor_x = int((x - 24) / 72)
        cursor_y = int((y - 24) / 72)
        
        # 커서 렌더 업데이트
        cvs.delete("CURSOR")
        if index == 1:
            cvs.create_image(cursor_x*72 + 60, cursor_y * 72 + 60, image=cursor, tag="CURSOR")

def mouse_move(e):
    # cursor ui update
    update_cursor(e.x, e.y)
    
def toggle_pressed_trigger():
    global mouse_c
    mouse_c = not mouse_c

def mouse_press(e):
    global mouse_c, cursor_x, cursor_y
    global tsugi, index, cvs, img_block, bPendSetblock, kindnessRemains
    if mouse_c == False:
        toggle_pressed_trigger()
        if index == 0:
            for y in range(10):
                for x in range(8):
                    block[y][x] = 0
            cvs.delete("TITLE")
            score = 0
            tsugi = random.randint(1,6)
            bPendSetblock = True
            root.after(0, game_main1)
        if index == 1:
            # 커서 위치에 고양이 배치
            if block[cursor_y][cursor_x] == 0:
                block[cursor_y][cursor_x] = tsugi
                tsugi = random.randint(1,6)
                cvs.create_image(cursor_x* 72 + 60, cursor_y * 72 + 60\
                                    , image = img_block[block[cursor_y][cursor_x]], tag="block")
                if kindnessRemains == 0:
                    bPendSetblock = True
                    kindnessRemains = kKindness
                else:
                    kindnessRemains -= 1
        root.after(int(1/kTargetFps), toggle_pressed_trigger)
        
def draw_block():
    global cvs, img_block, block
    cvs.delete("block")
    for y in range(10):
        for x in range(8):
            if block[y][x] > 0:
                cvs.create_image(x* 72 + 60, y * 72 + 60, image = img_block[block[y][x]], tag="block")

def check_block():
    bChecked = False
    check = copy.deepcopy(block)
    # 가로 3개 연속
    for y in range(10):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x]\
                        and check[y][x+1] == check[y][x]:
                    block[y][x-1] = 7
                    block[y][x] = 7
                    block[y][x+1] = 7
                    bChecked = True
    # 세로 3개 연속
    for y in range(1,9):
        for x in range(0,8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x]\
                        and check[y+1][x] == check[y][x]:
                    block[y-1][x] = 7
                    block[y][x] = 7
                    block[y+1][x] = 7
                    bChecked = True
    # 대각 3개 연속
    for y in range(1,9):
        for x in range(1,7):
            if check[y][x] > 0:
                # 우하향
                if check[y-1][x-1] == check[y][x]\
                        and check[y+1][x+1] == check[y][x]:
                    block[y-1][x-1] = 7
                    block[y][x] = 7
                    block[y+1][x+1] = 7
                    bChecked = True
                # 우상향
                if check[y+1][x-1] == check[y][x]\
                        and check[y-1][x+1] == check[y][x]:
                    block[y+1][x-1] = 7
                    block[y][x] = 7
                    block[y-1][x+1] = 7
                    bChecked = True
    return bChecked

def sweep_block():
    global block
    num = 0
    for y in range(10):
        for x in range(8):
            if block[y][x] == 7:
                block[y][x] = 0
                num += 1    
    return num

def drop_block():
    global root
    bDropped = False
    for y in range(8, -1, -1):
        for x in range(8):
            if block[y][x] != 0 and block[y+1][x] == 0 :
                block[y+1][x] = block[y][x]
                block[y][x] = 0
                bDropped = True
    return bDropped
    
# 가장 윗줄에 고양이가 있는 지 확인
def over_block():
    for x in range(3,5): # 상단 중앙 2칸만 확인
        if block[0][x] != 0:
            return True
    return False
    
# 가장 윗줄에 랜덤 고양이 1줄 배치
def set_block():
    for x in range(8):
        if block[0][x] == 0:
            block[0][x] = random.randint(1,6)

def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Times New Roman", siz, "bold")
    cvs.create_text(x+2,y+2,text=txt, fill="black", font=fnt, tag=tg) # 그림자
    cvs.create_text(x,y,text=txt, fill=col, font=fnt, tag=tg)

def draw_UI():
    global cvs, tsugi, img_block, score
    cvs.delete("INFO")
    draw_txt("SCORE " + str(score), 160, 60, 32, "blue", "INFO")
    if tsugi > 0:
        cvs.create_image(752, 128, image=img_block[tsugi], tag="INFO")
    
def game_init():
    global root, cvs, bg, cursor, img_block
    for i in range(10):
        block.append([0, 0, 0, 0, 0, 0, 0, 0])
        check.append([0, 0, 0, 0, 0, 0, 0, 0])
    root = tkinter.Tk()
    root.title("퍼즐게임 '애니블럭' ")
    root.resizable(False, False)
    root.bind("<Motion>", mouse_move)
    root.bind("<ButtonPress>", mouse_press)
    cvs = tkinter.Canvas(root, width=912, height=768)
    cvs.pack()
    
    bg = tkinter.PhotoImage(file="resources/bg2.png")
    cursor = tkinter.PhotoImage(file="resources/cursor.png")
    img_block = [
        None,
        tkinter.PhotoImage(file="resources/block1.png"),
        tkinter.PhotoImage(file="resources/block2.png"),
        tkinter.PhotoImage(file="resources/block3.png"),
        tkinter.PhotoImage(file="resources/block4.png"),
        tkinter.PhotoImage(file="resources/block5.png"),
        tkinter.PhotoImage(file="resources/block6.png"),
        tkinter.PhotoImage(file="resources/block_fade.png"),
    ]
    cvs.create_image(456, 384, image=bg) # 배경
    tsugi = random.randint(1,6)
        
def game_start():
    global index, mouse_c, score, tsugi, cursor_x, cursor_y, cvs, kindnessRemains
    cvs.delete("block")
    cvs.delete("OVER")
    draw_txt("애니블럭", 312, 240, 100, "violet", "TITLE")
    draw_txt("Click to Start", 312, 560, 50, "orange", "TITLE")
    index = 0
    score = 0
    kindnessRemains = kKindness
    
def game_over():
    global root, index, cvs
    index = 2
    cvs.delete("block")
    draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
    draw_UI()
    root.after(5000, game_start)
# 블록 떨구기, 매칭 체크
def game_main1():
    global root, score, timer, index, bPendSetblock
    index = 1
    if not drop_block():    
        if check_block():
            root.after(500, game_main2)
        elif over_block():
            root.after(0, game_over)
        else:
            root.after(500, game_main1)
    else:
        root.after(500, game_main1)
    if bPendSetblock:
        set_block()
        bPendSetblock = False
    draw_block()
    draw_UI()
    
# 매칭 치우기, 스위핑, 게임오버 결정
def game_main2():
    global root, score, timer, index
    sc = sweep_block()
    if sc > 0 :
        score += sc * 10
    draw_block()
    draw_UI()
    root.after(0, game_main1)
    
game_init()
game_start()
root.mainloop()