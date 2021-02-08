from tkinter import *;
from random import *;
from math import *;

BLOCK_WIDTH = 50;    # 方块宽度
ROW = 10;            # 行数
COLUMN = 10;         # 列数
LANDMINE_COUNT = 10; # 地雷个数
DEBUG=0;             # 是否开启DEBUG

# 地雷数据标记
F_UNSWEPT = -1;      # 未扫过的
F_FLAG = -2;         # 旗子
F_LANDMINE = -3;     # 地雷

# 运行时数据
landmineData = [];
data = [];
gameover = 0;

window = Tk()   # 创建Tk绘图对象
width = BLOCK_WIDTH*(COLUMN+2);
height = BLOCK_WIDTH*(ROW+2);
window.geometry("{width}x{height}".format(width=width, height=height))  # 几何绘制管理器
canvas = Canvas(window, width=width, height=height,bg="white")  # 创建画布

def initData():
    # 创建10*10的二维数组
    for y in range(0,ROW):
        landmineData.append([]);
        data.append([]);
        for x in range(0,COLUMN):
            landmineData[y].append(0);
            data[y].append(F_UNSWEPT);

    # 随机生成LANDMINE个地雷
    for n in range(0,LANDMINE_COUNT):
        while 1:
            x = randint(0,COLUMN-1);
            y = randint(0,ROW-1);
            if landmineData[y][x] == 1:
                continue;
            else:
                landmineData[y][x] =1;
                break;

def paint():
    if gameover:
        canvas.create_text(BLOCK_WIDTH*COLUMN/2,BLOCK_WIDTH/2,text='Game Over');
    for y in range(0,ROW):
        for x in range(0,COLUMN):
            fill = '';
            ifgameover:
                fill = 'green';
                if landmineData[y][x] == 1:
                    fill = 'red';
            else:
                fill = 'grey';
                if data[y][x] <= 8 and data[y][x] >=0:
                    fill = 'lightgrey';
            x1 = x*BLOCK_WIDTH + 50;
            y1 = y*BLOCK_WIDTH + 50;
            x2 = (x+1)*BLOCK_WIDTH + 50;
            y2 = (y+1)*BLOCK_WIDTH + 50;
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill);
            if data[y][x] == F_LANDMINE:
                canvas.create_text(x1+BLOCK_WIDTH/2,y1+BLOCK_WIDTH/2,text='雷');
            if data[y][x] == F_FLAG:
                canvas.create_text(x1+BLOCK_WIDTH/2,y1+BLOCK_WIDTH/2,text='旗');
            elif data[y][x] >=0:
                canvas.create_text(x1+BLOCK_WIDTH/2,y1+BLOCK_WIDTH/2,text=str(data[y][x]));

def isLandmine(column, row):
    if column<0 or row<0 or column>=COLUMN or row>=ROW:
        return 0;
    else:
        return landmineData[row][column];

def clearLandmine(column, row):
    if column<0 or row<0 or column>=COLUMN or row>=ROW:
        return;
    if data[row][column] != F_UNSWEPT:
        return;
    around = (
        (column-1,row-1),
        (column-1,row),
        (column-1,row+1),
        (column,row-1),
        (column,row+1),
        (column+1,row-1),
        (column+1,row),
        (column+1,row+1),
    );
    s = 0;
    for (c, r) in around:
        s = s+isLandmine(c,r);
    data[row][column] = s;
    if s == 0:
        for (c, r) in around:
            s = clearLandmine(c,r);

def mouse_left_click(event):
    column = floor((event.x - 50) / BLOCK_WIDTH);
    row = floor((event.y - 50) / BLOCK_WIDTH);
    if column<0 or row<0 or column>=COLUMN or row>=ROW:
        return;
    if landmineData[row][column] == 1:
        gameover = 1;
        data[row][column] = F_LANDMINE;
    else:
        clearLandmine(column, row);
    paint();

def mouse_right_click(event):
    column = floor((event.x - 50) / BLOCK_WIDTH);
    row = floor((event.y - 50) / BLOCK_WIDTH);
    if column<0 or row<0 or column>=COLUMN or row>=ROW:
        return;
    data[row][column] = F_FLAG;
    paint();

initData();
paint();

canvas.bind("<Button-1>", mouse_left_click);
canvas.bind("<Button-2>", mouse_right_click);
canvas.pack();
window.mainloop();

