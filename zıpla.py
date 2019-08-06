from tkinter import *
import time
import random
import sys
import os

WIDTH = 600
HEIGHT = 600

tk = Tk()
tk.resizable(0,0)
tk.title("Haydi Zıpla")
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="pink")
canvas.pack()

uygulama = Frame(tk)
uygulama.pack()

restartBtn=None


def restart_program():
    python = sys.executable
    os.execl(python, python,*sys.argv)


class Oyuncu:
    def __init__(self):
        self.sol_gifler = [PhotoImage(file="sol1.gif"),
                         PhotoImage(file="sol2.gif"),
                         PhotoImage(file="sol3.gif")]

        self.sağ_gifler = [PhotoImage(file="sağ1.gif"),
                         PhotoImage(file="sağ2.gif"),
                         PhotoImage(file="sağ3.gif")]


        self.image = canvas.create_image(WIDTH / 2, HEIGHT - 100, anchor=NW,
                                         image=self.sağ_gifler[0])
        self.x_hız = 0
        self.y_hız = 0

        canvas.bind_all("<KeyPress-Left>", self.hareket)
        canvas.bind_all("<KeyPress-Right>", self.hareket)
        canvas.bind_all("<KeyPress-space>", self.zıpla)
        canvas.bind_all("<KeyRelease-Left>", self.dur)
        canvas.bind_all("<KeyRelease-Right>", self.dur)
        self.zıplıyor = False
        self.güncel_gif = 0
        self.güncel_gif_ekle = 1
        self.last_time = time.time()
# event callback fonksiyondur. başka bir fonksiyon içinde parametre olarak kullanılır.
    def zıpla(self, event):
        if not self.zıplıyor:
            self.zıplıyor = True
            self.y_hız = -22

    def dur(self, event):
        self.x_hız = 0
# keysym stringler için
    def hareket(self, event):
        if event.keysym == 'Right':
            self.x_hız = 5
        if event.keysym == 'Left':
            self.x_hız = -5

    def animasyon(self):
        now = time.time()
        if now - self.last_time > 0.05:
            self.last_time = now
            self.güncel_gif += self.güncel_gif_ekle
            if self.güncel_gif >= 1:
                self.güncel_gif_ekle = -1
            if self.güncel_gif <= -0:
                self.güncel_gif_ekle = 1


        if self.x_hız < 0:
            if self.y_hız != 0:
                canvas.itemconfig(self.image,image=self.sol_gifler[2])
            else:
                canvas.itemconfig(self.image,image=self.sol_gifler[self.güncel_gif])

        elif self.x_hız > 0:
            if self.y_hız != 0:
                canvas.itemconfig(self.image,image=self.sağ_gifler[2])
            else:
                canvas.itemconfig(self.image,image=self.sağ_gifler[self.güncel_gif])


    def güncelle(self):
        self.animasyon()
        self.y_hız += 1
        canvas.move(self.image, self.x_hız, self.y_hız)
        ko = canvas.coords(self.image) #canvas.coord(item,*coords)  Koordinat belirtilmedi.self.image in ilk koordinatları return edilir.
        self.ko = ko
        sol, sağ = ko[0], ko[0] + 27
        üst, alt = ko[1], ko[1] + 30

        # oyuncu platforma çarparsa
        for plat in platforms:
            if self.y_hız > 0:
                çarpıyor = canvas.find_overlapping(sol, üst, sağ, alt)
                if plat.image in çarpıyor:
                    self.zıplıyor = False
                    self.y_hız = 0
                    canvas.coords(self.image, sol, plat.üst - 30)


        # wrap around edges of screen
        if sağ > WIDTH:
            canvas.coords(self.image, 0, üst)
        if sol < 0:
            canvas.coords(self.image, WIDTH-27, üst)



class Platform:
    def __init__(self, x, y, width, height):
        self.image = canvas.create_rectangle(x, y, x + width, y + height, fill="aqua")
        self.üst = y


oyuncu = Oyuncu()
platforms = []
plat1 = Platform(0, HEIGHT - 20, WIDTH, 20)
platforms.append(plat1)
platforms.append(Platform(150, 205, 100, 20))
platforms.append(Platform(450, 120, 100, 20))
platforms.append(Platform(375, 420, 200, 20))
platforms.append(Platform(45, 20, 100, 20))
skor = 0
canvas.create_text(510,30,text="Score:",font=('Segoe Script',15))
skor_label = canvas.create_text(570, 30, text="0", font=('Segoe Script',15))
while True:
    canvas.itemconfig(skor_label, text=str(skor))
    oyuncu.güncelle()
    # bitiş
    if oyuncu.ko[1] > HEIGHT:
       canvas.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER!", font=('Segoe Script', 40))
       if restartBtn is None:
           restartBtn = Button(uygulama, text='restart', width=5, height=2,bg="orange", command=restart_program)
           restartBtn.pack(padx=0,pady=0)


    # oyuncu ekranın 1/4 üne geldiğinde ekranı kaydır
    if oyuncu.ko[1 ] < HEIGHT / 10 and oyuncu.y_hız < 0:
        canvas.move(oyuncu.image, 0, -oyuncu.y_hız)
        for plat in platforms:
            canvas.move(plat.image, 0, -oyuncu.y_hız)
            plat.üst -= oyuncu.y_hız
            if plat.üst > HEIGHT:
                skor += 10
                canvas.delete(plat.image)
                platforms.remove(plat)
    while len(platforms) < 5:
        yeni_platform = Platform(random.randrange(0, WIDTH - 100),
                           random.randrange(-50, -30),
                           random.randrange(50, 150),
                           20)
        platforms.append(yeni_platform)





    tk.update()
    time.sleep(0.01)



