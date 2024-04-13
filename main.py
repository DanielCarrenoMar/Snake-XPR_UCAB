import pygame as pg
import pygame_menu as pgm
from random import randrange, choice
pg.init()
H = pg.display.Info().current_h
W = pg.display.Info().current_w
CLOCK = pg.time.Clock()

pg.display.set_mode((W//2,H//2), pg.RESIZABLE) 
pg.display.set_caption("Snake")

listColorName = ["Azul", "Azul Oscuro", "Amarillo", "Blanco", "Celeste", "Colmena 1", "Colmena 2", "Colmena 3", "Gris", "Rosado", "Rojo", "Morado", "Negro", "Naranja", "Verde Oscuro", "Verde"]
listColor = ["#0079B0", "#003AB0", "#EBF41C","#FFFFFF", "#00BEBF", "#F4BE2E", "#35AEDC", "#047732", "#808080", "#FF63A8", "#952121", "#7E228A", "#000000", "#FF8614","#10BD3E","#01DF3C"]
configColors = {
    "marco": "#FFFFFF",
    "background": "#000000",
    "head": "#10BD3E",
    "body": "#01DF3C",
    "head2": "#F4BE2E",
    "body2": "#EBF41C",
    "food": "#952121",
    "ui": "#FFFFFF",
}
configNumbers = {
    "dimention": 25,
    "numManzanas": 1,
    "longManzana": 1,
    "speed": 250,
    "multiSnake": False,
}

class Intro():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.alpha = -5
        self.imgLogo = pg.image.load("./images/logo.png")
        
    def bucle(self, events:list):
        global page
        for event in events:
            if event.type == pg.KEYDOWN: page = 1

        self.screen.fill("#000000")
        width, height = self.screen.get_size()

        imgLogo_copy = self.imgLogo.copy()
        imgLogo_copy = pg.transform.scale(imgLogo_copy, (height,height))
        imgSize = imgLogo_copy.get_size()
        imgLogo_copy.set_alpha(self.alpha)
        self.screen.blit(imgLogo_copy, ((width-imgSize[0])/2,0))
        self.alpha += 1

        if self.alpha > 155:
            page = 1

class Start():
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.multi = False
        sound = pgm.sound.Sound()
        sound.load_example_sounds()
        self.imgWin = pg.image.load("./images/win.png")

        mytheme = pgm.Theme()
        mytheme.title_bar_style = pgm.widgets.MENUBAR_STYLE_SIMPLE
        mytheme.widget_font_color = "#70888C"
        mytheme.selection_color = "#6E2A48"
        mytheme.background_color = "#DAEBEE"
        mytheme.title_font_color = "#DAEBEE"
        mytheme.title_background_color = "#6E2A48"

        screenW, screenH = self.screen.get_size()
        self.menuColors = pgm.pygame_menu.Menu('Colores', screenW, screenH,theme=mytheme, center_content=True)
        self.menuColors.set_sound(sound, False)
        def changeColor(*args, **kwargs):
            configColors.update({kwargs["kwargs"]: listColor[args[0][1]]})
        self.menuColors.add.dropselect('Marco = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["marco"]) ,onchange=changeColor, kwargs="marco", font_color="#375D64")
        self.menuColors.add.dropselect('Texto = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["ui"]) ,onchange=changeColor, kwargs="ui", font_color="#56929D")
        self.menuColors.add.dropselect('Fondo = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["background"]) ,onchange=changeColor, kwargs="background", font_color="#375D64")
        self.menuColors.add.dropselect('Comida = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["food"]) ,onchange=changeColor, kwargs="food", font_color="#56929D")
        self.menuColors.add.vertical_margin(10)
        self.menuColors.add.label("Jugador")
        self.menuColors.add.dropselect('Cabeza = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["head"]) ,onchange=changeColor, kwargs="head", font_color="#375D64")
        self.menuColors.add.dropselect('Cuerpo = ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["body"]) ,onchange=changeColor, kwargs="body", font_color="#56929D")

        self.menuNumber = pgm.pygame_menu.Menu('Parametros de juego', screenW, screenH,theme=mytheme, center_content=True)
        self.menuNumber.set_sound(sound, False)
        def changeNumber(*args, **kwargs):
            if (num := args[0]) < 2: num = 2
            configNumbers.update({kwargs["kwargs"]: num})
        def changeSpeed(*args, **kwargs):
            if (num := args[0]) < 1: num = 1
            num = 1000-num*10
            if (args[0]) == 99: num = 1
            configNumbers.update({"speed": num})

        self.menuNumber.add.text_input('Tamaño del tablero = ', default=str(configNumbers["dimention"]), input_type=pgm.locals.INPUT_INT, maxchar=3, onchange=changeNumber, kwargs="dimention", font_color="#375D64")
        self.menuNumber.add.text_input('Cantidad de comida en pantalla = ', default=str(configNumbers["numManzanas"]), input_type=pgm.locals.INPUT_INT, maxchar=3, onchange=changeNumber, kwargs="numManzanas", font_color="#56929D")
        self.menuNumber.add.text_input('Aumento por comida = ', default=str(configNumbers["longManzana"]), input_type=pgm.locals.INPUT_INT, maxchar=3, onchange=changeNumber, kwargs="longManzana", font_color="#375D64")
        self.menuNumber.add.text_input('Velocidad = ', default=str(100-configNumbers["speed"]//10), input_type=pgm.locals.INPUT_INT, maxchar=2, onchange=changeSpeed, font_color="#56929D")

        self.menu = pgm.pygame_menu.Menu('Configuracion', screenW, screenH,theme=mytheme, columns=1, rows=4, center_content=True)
        self.menu.set_sound(sound, False)
        def next(): global page; page = 2
        self.menu.add.button('Iniciar', next, font_color='#467780')
        self.menu.add.button('Parametros de juego', self.menuNumber)
        self.menu.add.button('Colores', self.menuColors)
        self.menu.add.button('Salir', pgm.events.EXIT)
        
    def bucle(self, events:list):
        if self.menu.is_enabled():
            for event in events:
                if event.type == pg.VIDEORESIZE:
                    screenW, screenH = self.screen.get_size()
                    self.menu.resize(screenW, screenH)
                    self.menuColors.resize(screenW, screenH)
                    self.menuNumber.resize(screenW, screenH)
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.menu.reset(1)

            if configNumbers["multiSnake"] and not self.multi:
                self.multi = True
                self.menuNumber.add.selector('Multiplayer', items=["N", "S"], default=1 if configNumbers["multiSnake"] else 0 ,onchange=lambda *args, **kwargs: configNumbers.update({"multiSnake": args[0][1] == 1}), font_color="#375D64")
                self.menuColors.add.vertical_margin(10)
                self.menuColors.add.label("Jugador 2")
                self.menuColors.add.dropselect('Cabeza: ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["head2"]) ,onchange=lambda *args, **kwargs: configColors.update({"head2": listColor[args[0][1]]}), kwargs="head2", font_color="#375D64")
                self.menuColors.add.dropselect('Cuerpo: ', items=[(i, "") for i in listColorName], default=listColor.index(configColors["body2"]) ,onchange=lambda *args, **kwargs: configColors.update({"body2": listColor[args[0][1]]}), kwargs="body2", font_color="#56929D")

            self.menu.update(events)
            self.menu.draw(self.screen)

            if win:self.screen.blit(self.imgWin, ((self.screen.get_width()-64,0)))

class Game():
    def __init__(self):
        self.screen = pg.display.get_surface()

        self.foods = []

        self.snakes = Snake(1,2,self.foods), Snake(3,4,self.foods)
        self.time = 0

        self.conami = False
    def reset(self):
        self.foods = []
        self.snakes = Snake(1,2,self.foods), Snake(3,4,self.foods)
        for s in self.snakes:
            s.reset = True

    def bucle(self, events:list):
        global page
        dimention = configNumbers["dimention"]
        self.screen.fill(configColors["marco"])
        self.matriz = [[0 for _ in range(dimention)] for _ in range(dimention)]

        for x,y in self.foods:
            self.matriz[y][x] = 5

        if not configNumbers["multiSnake"]: 
            self.snakes[0].bucle(self.matriz, [[pg.K_UP,pg.K_w],[pg.K_DOWN, pg.K_s],[pg.K_LEFT, pg.K_a],[pg.K_RIGHT, pg.K_d]])
        else:
            self.snakes[0].bucle(self.matriz, [[pg.K_UP],[pg.K_DOWN],[pg.K_LEFT],[pg.K_RIGHT]])
            self.snakes[1].bucle(self.matriz,  [[pg.K_w],[pg.K_s],[pg.K_a],[pg.K_d]])

        if len(self.foods) < configNumbers["numManzanas"] and len(zeros := [[j, i] for i, row in enumerate(self.matriz) for j, val in enumerate(row) if val == 0]) >= 1:
                ram = choice(zeros)
                self.foods.append(ram)

        if len([[j, i] for i, row in enumerate(self.matriz) for j, val in enumerate(row) if val in [0,1]]) == 1:
            if sound: soundMultiSnake.play()
            global win
            if not win: win = True

        realTime = pg.time.get_ticks()
        if realTime - self.time > configNumbers["speed"]: 
            self.time = realTime
            self.snakes[0].tick()
            if configNumbers["multiSnake"]: self.snakes[1].tick()

        self.box = self.screen.get_size()[1] // dimention
        for y in range(dimention):
            for x in range(dimention):
                draw = lambda color: pg.draw.rect(self.screen, color, ((x*self.box + (self.screen.get_size()[0] - dimention*self.box)//2), y*self.box, self.box, self.box))
                if self.matriz[y][x] == 0:
                    draw(configColors["background"])
                elif self.matriz[y][x] == 1:
                    draw(configColors["head"])
                elif self.matriz[y][x] == 2:
                    draw(configColors["body"])
                elif self.matriz[y][x] == 3:
                    draw(configColors["head2"])
                elif self.matriz[y][x] == 4:
                    draw(configColors["body2"])
                elif self.matriz[y][x] == 5:
                    draw(configColors["food"])
            
        textTam =self.screen.get_size()[1]//20
        bordeStartX = (self.screen.get_size()[0] - dimention*self.box)//2
        bordeEndX = bordeStartX + dimention*self.box

        font = pg.font.SysFont("Arial", textTam)

        text_surface = pg.font.SysFont("Arial", textTam//2).render("Presiona Esc para regresar", True, configColors["ui"])
        bordeMidleX = bordeStartX +( dimention*self.box - text_surface.get_width())//2 
        self.screen.blit(text_surface, (bordeMidleX,textTam//4))
        if not configNumbers["multiSnake"]:
            self.screen.blit(font.render(f"Puntuacion: {self.snakes[0].point}", True, configColors["ui"]), (bordeStartX,0))
            self.screen.blit(font.render(f"Récord: {self.snakes[0].record}", True, configColors["ui"]), (bordeEndX- textTam*6,0))
        else:
            self.screen.blit(font.render(f"Puntuacion: {self.snakes[0].point}", True, configColors["head"]), (bordeStartX,0))
            self.screen.blit(font.render(f"Puntuacion: {self.snakes[1].point}", True, configColors["head2"]), (bordeStartX,textTam))
            self.screen.blit(font.render(f"Récord: {self.snakes[0].record}", True, configColors["head"]), (bordeEndX- textTam*6,0))
            self.screen.blit(font.render(f"Récord: {self.snakes[1].record}", True, configColors["head2"]), (bordeEndX- textTam*6,textTam))

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.reset()
                page = 1
                pg.event.post(pg.event.Event(pg.VIDEORESIZE))

class Snake():
    def __init__(self, mathead:int, matbody:int, foods:list[int]):
        self.ramd2 = lambda: [randrange(0, configNumbers["dimention"]), randrange(0, configNumbers["dimention"])]

        self.mathead = mathead
        self.matbody = matbody
        self.foods = foods

        self.reset = True
        self.point = 0 
        self.record = 0
        self.time = 0 
        self.head = self.ramd2()
        self.body = [self.head.copy()]
        self.long = 1
        self.move = [0,0]
        self.moved = False

    def gameover(self):
        if sound: 
            soundGameOver.play()
        self.move = [0,0]
        self.point = 0
        self.long = 1

        self.head = self.ramd2()
        self.body = [self.head.copy()]

    def bucle(self, matriz:list, controls:list):
        if self.reset:
            self.reset = False
            self.record = self.point
            self.head = self.ramd2()
            self.body = [self.head.copy()]
            self.long = 1
            self.move = [0,0]
            self.point = 0

        if self.point > self.record:
                self.record = self.point
                if sound: soundRecord.play()

        self.ramd2 = lambda: [randrange(0, configNumbers["dimention"]), randrange(0, configNumbers["dimention"])]
        self.matriz = matriz
        self.numBox = len(matriz[0])

        for x,y in self.body[:-1]:
            matriz[y][x] = self.matbody
        matriz[self.body[-1][1]][self.body[-1][0]] = self.mathead
        
        key = pg.key.get_pressed()
        if self.moved == False:
            if any(key[k] for k in controls[0]) and self.move[1] != 1:
                self.move = [0,-1]
                self.moved = True
            elif any(key[k] for k in controls[1]) and self.move[1] != -1:
                self.move = [0,1]
                self.moved = True
            elif any(key[k] for k in controls[2]) and self.move[0] != 1:
                self.move = [-1,0]
                self.moved = True
            elif any(key[k] for k in controls[3]) and self.move[0] != -1:
                self.move = [1,0]
                self.moved = True      
    def tick(self):
        self.moved = False
        self.head[0] += self.move[0]; self.head[1] += self.move[1]

        for food in self.foods:
            if self.head == food:
                self.long += configNumbers["longManzana"]
                self.foods.remove(food)
                self.point += 10
                if sound: soundPoint.play()

        if len(self.body) >= self.long:
            self.body.pop(0)
            self.body.append(self.head.copy())
        else:
            self.body.append(self.head.copy())

        if self.head[0] < 0 or self.head[0] >= self.numBox or self.head[1] < 0 or self.head[1] >= self.numBox:
            self.gameover()

        if self.matriz[self.head[1]][self.head[0]] not in [0, 5, self.mathead]:
            self.gameover()

page = 0
win = False

sound = True
if pg.mixer.get_init() is None:
    sound = False
else:
    soundMultiSnake = pg.mixer.Sound('./sounds/snakeMulti.mp3')
    soundRecord = pg.mixer.Sound('./sounds/record.mp3')
    soundPoint = pg.mixer.Sound('./sounds/point.mp3')
    soundGameOver = pg.mixer.Sound('./sounds/gameOver.mp3')

intro, start, game = Intro(), Start(), Game()
pages = [intro, start, game]


CODE = [pg.K_UP, pg.K_UP, pg.K_DOWN, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT, pg.K_LEFT, pg.K_RIGHT, pg.K_b, pg.K_a]
code = []
index = 0

while True:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            quit()      
        if event.type == pg.KEYDOWN:
            if event.key == CODE[index]:
                code.append(event.key)
                if index < 9: index += 1
                
                if code == CODE:
                    index = 0
                    configNumbers["multiSnake"] = True
                    if sound: soundMultiSnake.play()
            else:
                code = []
                index = 0

    pages[page].bucle(events)

    pg.display.flip()
    CLOCK.tick(60)