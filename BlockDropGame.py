import tkinter
import random
import copy

kTargetFps = 60

index = 0 # 0 : intro, 1: playing, 2: gameover
timer = 0
score = 0
tsugi = 0

cursor_x = 0
cursor_y = 0
mouse_c = False

neko = []
check = []
img_neko = None
cvs = None
bPendSetNeko = False

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
    global tsugi, index, cvs, img_neko, bPendSetNeko
    if mouse_c == False:
        toggle_pressed_trigger()
        if index == 0:
            for y in range(10):
                for x in range(8):
                    neko[y][x] = 0
            cvs.delete("TITLE")
            score = 0
            tsugi = random.randint(1,6)
            bPendSetNeko = True
            root.after(0, game_main1)
        if index == 1:
            # 커서 위치에 고양이 배치
            if neko[cursor_y][cursor_x] == 0:
                neko[cursor_y][cursor_x] = tsugi
                tsugi = random.randint(1,6)
                cvs.create_image(cursor_x* 72 + 60, cursor_y * 72 + 60\
                                    , image = img_neko[neko[cursor_y][cursor_x]], tag="NEKO")
                bPendSetNeko = True
        root.after(int(1/kTargetFps), toggle_pressed_trigger)
        
def draw_neko():
    global cvs, img_neko, neko
    cvs.delete("NEKO")
    for y in range(10):
        for x in range(8):
            if neko[y][x] > 0:
                cvs.create_image(x* 72 + 60, y * 72 + 60, image = img_neko[neko[y][x]], tag="NEKO")

def check_neko():
    bChecked = False
    check = copy.deepcopy(neko)
    # 가로 3개 연속
    for y in range(10):
        for x in range(1,7):
            if check[y][x] > 0:
                if check[y][x-1] == check[y][x]\
                        and check[y][x+1] == check[y][x]:
                    neko[y][x-1] = 7
                    neko[y][x] = 7
                    neko[y][x+1] = 7
                    bChecked = True
    # 세로 3개 연속
    for y in range(1,9):
        for x in range(0,8):
            if check[y][x] > 0:
                if check[y-1][x] == check[y][x]\
                        and check[y+1][x] == check[y][x]:
                    neko[y-1][x] = 7
                    neko[y][x] = 7
                    neko[y+1][x] = 7
                    bChecked = True
    # 대각 3개 연속
    for y in range(1,9):
        for x in range(1,7):
            if check[y][x] > 0:
                # 우하향
                if check[y-1][x-1] == check[y][x]\
                        and check[y+1][x+1] == check[y][x]:
                    neko[y-1][x-1] = 7
                    neko[y][x] = 7
                    neko[y+1][x+1] = 7
                    bChecked = True
                # 우상향
                if check[y+1][x-1] == check[y][x]\
                        and check[y-1][x+1] == check[y][x]:
                    neko[y+1][x-1] = 7
                    neko[y][x] = 7
                    neko[y-1][x+1] = 7
                    bChecked = True
    return bChecked

def sweep_neko():
    global neko
    num = 0
    for y in range(10):
        for x in range(8):
            if neko[y][x] == 7:
                neko[y][x] = 0
                num += 1    
    return num

def drop_neko():
    global root
    bDropped = False
    for y in range(8, -1, -1):
        for x in range(8):
            if neko[y][x] != 0 and neko[y+1][x] == 0 :
                neko[y+1][x] = neko[y][x]
                neko[y][x] = 0
                bDropped = True
    return bDropped
    
# 가장 윗줄에 고양이가 있는 지 확인
def over_neko():
    for x in range(8):
        if neko[0][x] != 0:
            return True
    return False
    
# 가장 윗줄에 랜덤 고양이 1줄 배치
def set_neko():
    for x in range(8):
        if neko[0][x] == 0:
            neko[0][x] = random.randint(0,6)

def draw_txt(txt, x, y, siz, col, tg):
    fnt = ("Times New Roman", siz, "bold")
    cvs.create_text(x+2,y+2,text=txt, fill="black", font=fnt, tag=tg) # 그림자
    cvs.create_text(x,y,text=txt, fill=col, font=fnt, tag=tg)

def draw_UI():
    global cvs, tsugi, img_neko, score
    cvs.delete("INFO")
    draw_txt("SCORE " + str(score), 160, 60, 32, "blue", "INFO")
    if tsugi > 0:
        cvs.create_image(752, 128, image=img_neko[tsugi], tag="INFO")
    
def game_init():
    global root, cvs, bg, cursor, img_neko
    for i in range(10):
        neko.append([0, 0, 0, 0, 0, 0, 0, 0])
        check.append([0, 0, 0, 0, 0, 0, 0, 0])
    root = tkinter.Tk()
    root.title("낙하 퍼즐 '야옹야옹' ")
    root.resizable(False, False)
    root.bind("<Motion>", mouse_move)
    root.bind("<ButtonPress>", mouse_press)
    cvs = tkinter.Canvas(root, width=912, height=768)
    cvs.pack()
    
    bg = tkinter.PhotoImage(file="neko_bg.png")
    cursor = tkinter.PhotoImage(file="neko_cursor.png")
    img_neko = [
        None,
        tkinter.PhotoImage(file="neko1.png"),
        tkinter.PhotoImage(file="neko2.png"),
        tkinter.PhotoImage(file="neko3.png"),
        tkinter.PhotoImage(file="neko4.png"),
        tkinter.PhotoImage(file="neko5.png"),
        tkinter.PhotoImage(file="neko6.png"),
        tkinter.PhotoImage(file="neko_niku.png"),
    ]
    cvs.create_image(456, 384, image=bg) # 배경
    tsugi = random.randint(1,6)
        
def game_start():
    global index, mouse_c, score, tsugi, cursor_x, cursor_y, cvs
    cvs.delete("NEKO")
    cvs.delete("OVER")
    draw_txt("야옹야옹", 312, 240, 100, "violet", "TITLE")
    draw_txt("Click to Start.", 312, 560, 50, "orange", "TITLE")
    index = 0
    
def game_over():
    global root, index, cvs
    index = 2
    cvs.delete("NEKO")
    draw_txt("GAME OVER", 312, 348, 60, "red", "OVER")
    draw_UI()
    root.after(5000, game_start)
# 블록 떨구기, 매칭 체크
def game_main1():
    global root, score, timer, index, bPendSetNeko
    index = 1
    if not drop_neko():    
        if check_neko():
            root.after(500, game_main2)
        elif over_neko():
            root.after(0, game_over)
        else:
            root.after(500, game_main1)
    else:
        root.after(500, game_main1)
    if bPendSetNeko:
        set_neko()
        bPendSetNeko = False
    draw_neko()
    draw_UI()
    
# 매칭 치우기, 스위핑, 게임오버 결정
def game_main2():
    global root, score, timer, index
    sc = sweep_neko()
    if sc > 0 :
        score += sc * 10
    draw_neko()
    draw_UI()
    root.after(0, game_main1)
    
game_init()
game_start()
root.mainloop()