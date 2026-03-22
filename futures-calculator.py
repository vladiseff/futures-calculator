from tkinter import *
import math
import numpy as np
from TkToolTip import ToolTip

# --- Инициализация главного окна ---
root = Tk()
root.title('Калькулятор')
root.geometry('380x240')
root.resizable(False, False)

app_font = ('Times New Roman', 12)

var_T = DoubleVar(value=10)
var_k = DoubleVar(value=9)
var_t = DoubleVar(value=7)
var_proc = DoubleVar(value=5)
var_E = DoubleVar(value=70)


def calc(T, t, k, Pr, E):
    k_int = int(k)
    t_int = int(t)
    n = 10
    Pr_val = Pr / 100
    tn = T / n
    sigma = 0.1
    u = math.exp(sigma * math.sqrt(T / n))
    d = 1 / u
    p = (math.exp((Pr_val * tn)) - d) / (u - d)
    q = 1 - p

    prStavka = np.zeros((n + 1, n + 1))
    prStavka[n][0] = Pr
    j = 1
    for i in range(n - 1, -1, -1):
        prStavka[i][j] = prStavka[i + 1][j - 1] * u
        j = j + 1
    for i in range(n, -1, -1):
        for j in range(1, n + 1):
            if prStavka[i][j] == 0:
                prStavka[i][j] = prStavka[i][j - 1] * d

    ZCB10 = np.zeros((n + 1, n + 1))
    for i in range(0, n + 1):
        ZCB10[i][n] = 100
    g = 1
    for j in range(n - 1, -1, -1):
        for i in range(g, n + 1):
            ZCB10[i][j] = (p * (ZCB10[i - 1][j + 1]) / 100 + q * (ZCB10[i][j + 1]) / 100) / (1 + (prStavka[i][j]) / 100)
            ZCB10[i][j] = ZCB10[i][j] * 100
        if j > 0:
            g = g + 1
    val_price = f"{max(0, ZCB10[10][0]):.2f}%"

    ZCBt = np.zeros((t_int + 1, t_int + 1))
    for i in range(0, t_int + 1):
        ZCBt[i][t_int] = 100
    rows = prStavka.shape[0]
    prStavkaС = prStavka[rows - (t_int + 1):rows, 0:(t_int + 1)].copy()
    g = 1
    for j in range(t_int - 1, -1, -1):
        for i in range(g, t_int + 1):
            ZCBt[i][j] = (p * (ZCBt[i - 1][j + 1]) / 100 + q * (ZCBt[i][j + 1]) / 100) / (1 + (prStavkaС[i][j]) / 100)
            ZCBt[i][j] = ZCBt[i][j] * 100
        if j > 0:
            g = g + 1
    val_forward = f"{(ZCB10[10][0] / ZCBt[t_int][0]) * 100:.2f}%"

    rows_z = ZCB10.shape[0]
    ZCB10C = ZCB10[rows_z - (k_int + 1):rows_z, 0:(k_int + 1)].copy()
    futV = ZCB10C
    g = 1
    for j in range(k_int - 1, -1, -1):
        for i in range(g, k_int + 1):
            futV[i][j] = p * (futV[i - 1][j + 1]) / 100 + q * (futV[i][j + 1]) / 100
            futV[i][j] = futV[i][j] * 100
        if j > 0:
            g = g + 1
    val_futures = f"{futV[k_int][0]:.2f}%"

    opCall = np.zeros((k_int + 1, k_int + 1))
    for i in range(0, k_int + 1):
        opCall[i][k_int] = max(0, futV[i][k_int] - E)
    g = 1
    for j in range(k_int - 1, -1, -1):
        for i in range(g, k_int + 1):
            a = p * (opCall[i - 1][j + 1] / 100)
            b = q * (opCall[i][j + 1] / 100)
            c = math.exp((Pr_val * T) / k_int)
            d_val = futV[i][j] / 100 - E / 100
            opCall[i][j] = max((a + b) / c, max(0, d_val))
            opCall[i][j] = opCall[i][j] * 100
        if j > 0:
            g = g + 1
    val_call = f"{opCall[k_int][0]:.2f}%"

    res_win = Toplevel(root)
    res_win.title('Результаты')
    res_win.geometry('340x240')
    res_win.resizable(False, False)

    labels = [
        ('Цена ZCB₁₀:', val_price),
        ('Форвард:', val_forward),
        ('Фьючерс:', val_futures),
        ('Опцион Call:', val_call)
    ]

    curr_y = 25
    for text, val in labels:
        l1 = Label(res_win, text=text, font=app_font)
        l1.place(x=30, y=curr_y)
        l2 = Label(res_win, text=val, font=app_font, fg='blue')
        l2.place(x=170, y=curr_y)
        curr_y += 50

    ToolTip(res_win, text="Результаты расчета по биномиальной модели", delay=0.5)


lblT = Label(root, text='T = ', font=app_font)
lblk = Label(root, text='k = ', font=app_font)
lblPr = Label(root, text='% = ', font=app_font)
lblE = Label(root, text='E = ', font=app_font)
lblt = Label(root, text='t = ', font=app_font)

edtT = Spinbox(root, from_=0, to=100, increment=1, width=5, textvariable=var_T, state='readonly', font=app_font)
edtk = Spinbox(root, from_=0, to=10, increment=1, width=5, textvariable=var_k, state='readonly', font=app_font)
edtPr = Spinbox(root, from_=0, to=100, increment=0.5, width=5, textvariable=var_proc, state='readonly', font=app_font)
edtE = Spinbox(root, from_=0, to=100, increment=1, width=5, textvariable=var_E, state='readonly', font=app_font)
edtt = Spinbox(root, from_=0, to=10, increment=1, width=5, textvariable=var_t, state='readonly', font=app_font)

lblT.place(x=30, y=20)
edtT.place(x=80, y=20)
lblPr.place(x=200, y=20)
edtPr.place(x=260, y=20)

lblk.place(x=30, y=75)
edtk.place(x=80, y=75)
lblE.place(x=200, y=75)
edtE.place(x=260, y=75)

lblt.place(x=130, y=130)
edtt.place(x=185, y=130)

btn1 = Button(root, text='Результат', font=app_font, bg='#f0f0f0',
              command=lambda: calc(var_T.get(), var_t.get(), var_k.get(), var_proc.get(), var_E.get()))
btn1.place(x=135, y=185, width=110, height=35)

ToolTip(lblT, text="T — срок модели (лет).", delay=0.5)
ToolTip(lblt, text="t — момент исполнения форварда.", delay=0.5)
ToolTip(lblk, text="k — момент исполнения фьючерса.", delay=0.5)
ToolTip(lblPr, text="r₀ — начальная процентная ставка (%).", delay=0.5)
ToolTip(lblE, text="E — страйк опциона.", delay=0.5)

root.mainloop()