from ursina import *
from ursina.shaders import basic_lighting_shader, lit_with_shadows_shader
from ursina import curve
from random import randint
# from car8 import *
from car8_odev import *
from ursina_neat import *

Entity.default_shader = lit_with_shadows_shader 

items = False

money = 1000
parkingAreaList = [] # otopark listesi

def input(key):
    global money
    try:
        if key == "left mouse down" and distance(building1, mouse.world_point)<2:
            building1.clicked = not building1.clicked

        if key == "left mouse down" and distance(building2, mouse.world_point)<3:
            building2.clicked = not building2.clicked

        if key == "left mouse down" and distance(parkingArea, mouse.world_point)<2:
            parkingArea.clicked = not parkingArea.clicked

        if key == "left mouse down" and distance(duz_yol, mouse.world_point)<2:
            duz_yol.clicked = not duz_yol.clicked

        if key == "left mouse down" and distance(rampa, mouse.world_point)<2:
            rampa.clicked = not rampa.clicked
        
        if key == "left mouse down" and distance(kopru, mouse.world_point)<2:
            kopru.clicked = not kopru.clicked
    except: pass

    if key == "middle mouse down":
        if int(btn_m.text[:-2]) <= 0:
            return
        if building1.clicked:
            duplicate(building1, clicked=False, unlit=True)
            text_popup("-100 $", building1)
            money -= 100
            btn_m.text = str(money) + " $"
            
        
        if building2.clicked:
            duplicate(building2, clicked=False, unlit=True)
            text_popup("-100 $", building2)
            money -= 100
            btn_m.text = str(money) + " $"

        if parkingArea.clicked: # parkingArea tıkladıysak
            p = duplicate(parkingArea, clicked=False, unlit=True, visible=True, sayac=0)
            parkingAreaList.append(p)
            text_popup("+10 $", p)
            money += 10
            btn_m.text = str(money) + " $"

        if duz_yol.clicked: # duz_yol tıkladıysak
            d = duplicate(duz_yol, clicked=False, unlit=True, visible=True,shader=basic_lighting_shader)
            text_popup("-5 $", d)
            money -= 5
            btn_m.text = str(money) + " $"

        if egri_yol.clicked: # duz_yol tıkladıysak
            d = duplicate(egri_yol, clicked=False, unlit=True, visible=True, shader=basic_lighting_shader)
            text_popup("-5 $", d)
            money -= 5
            btn_m.text = str(money) + " $"

        if rampa.clicked: # rampa tıkladıysak
            d = duplicate(rampa, clicked=False, unlit=True, visible=True, shader=basic_lighting_shader)
            text_popup("-5 $", d)
            money -= 5
            btn_m.text = str(money) + " $"
            rampalar.append(d)

        if kopru.clicked: # kopru tıkladıysak
            d = duplicate(kopru, clicked=False, unlit=True, visible=True, shader=basic_lighting_shader)
            text_popup("-5 $", d)
            money -= 5
            btn_m.text = str(money) + " $"
            kopruler.append(d)

        if house.clicked: # kopru tıkladıysak
            d = duplicate(house, clicked=False, unlit=True, visible=True, shader=basic_lighting_shader)
            text_popup("-5 $", d)
            money -= 5
            btn_m.text = str(money) + " $"

    # butonlar bölümü
    if key == "tab":
        global items, btn_build1, btn_build2, btn_park, b_yol, btn_egriyol, btn_rampa, btn_kopru
        global btn_house
        items = not items
       
        if items:
            btn_house = Entity(model="quad", parent=camera.ui, scale=(0.30, 0.15), x=0.40, y=-.4, texture="house", collider="box")
            btn_house.on_click = lambda: select_obj(house)  

            btn_build1 = Entity(model="quad", parent=camera.ui, scale=(0.30, 0.20), x=-.05, y=-.4, texture="building1", collider="box")
            btn_build1.on_click = lambda: select_obj(building1) 

            btn_build2 = Entity(model="quad", parent=camera.ui, scale=(0.30, 0.20), x=0.1, y=-.4, texture="building2", collider="box")
            btn_build2.on_click = lambda: select_obj(building2) 

            btn_park = Entity(model="quad", parent=camera.ui, scale=0.30, x=0.30, y=-.4, texture="parkingArea", collider="box")
            btn_park.color = color.white # orjinal renk
            btn_park.on_click = lambda: select_obj(parkingArea) # üzerine tıkla

            b_yol = Entity(model="quad", parent=camera.ui, scale=0.30, x= -0.20, y=-.4, texture="duz_yol", collider="box")
            b_yol.color = color.white # orjinal renk
            b_yol.on_click = lambda: select_obj(duz_yol) # üzerine tıkla

            btn_egriyol = Entity(model="quad", parent=camera.ui, scale=0.30, x= -0.40, y=-.4, texture="egri_yol", collider="box")
            btn_egriyol.on_click = lambda: select_obj(egri_yol) # üzerine tıkla

            btn_rampa = Entity(model="quad", parent=camera.ui, scale=0.30, x= -0.60, y=-.4, texture="rampa", collider="box")
            btn_rampa.color = color.white # orjinal renk
            btn_rampa.on_click = lambda: select_obj(rampa) # üzerine tıkla

            btn_kopru = Entity(model="quad", parent=camera.ui, scale=0.30, x= -0.80, y=-.4, texture="bridge", collider="box")
            btn_kopru.color = color.white # orjinal renk
            btn_kopru.on_click = lambda: select_obj(kopru) # üzerine tıkla

            
        else:
           select_obj(Entity()) # aktif nesnesini seçimini iptal et 
           destroy(btn_house)
           destroy(btn_build1)
           destroy(btn_build2)
           destroy(btn_park)
           destroy(b_yol)
           destroy(btn_egriyol)
           destroy(btn_rampa)
           destroy(btn_kopru)

    # ders8 nesneleri döndürmek
    if key == "r":
        for e in scene.entities:
            if hasattr(e, "clicked"):
                if e.clicked : e.rotation_y += 45
    # ders8 odak moduna geçmek
    if key == "o": 
        for e in scene.entities: 
            if hasattr(e, "clicked"):
                if e.clicked : origin.position = e.position
        
    # araba ekleme
    if key == "left shift":
        car = Car(model="car1.glb", position=mouse.world_point, unlit=False)
    elif key == "right shift":
        car = Car(model="car2.glb", position=mouse.world_point, unlit=False)
    
    elif key == "n":
        Cars.ignoreList[0] = ground
        car = Cars(model="car", position=mouse.world_point+Vec3(0,.5,0), unlit=False)
    
    elif key == "t":
        Cars.toggle_collisions = not Cars.toggle_collisions

        for e in scene.entities: 
            if hasattr(e, "clicked"):
                if Cars.toggle_collisions:
                    e.collider = "box"
                else: e.collider = None

def update():
    if not mouse.world_point:
        return
    if building1.clicked:
        building1.position = mouse.world_point
        building1.y -= .6
    elif building2.clicked:
        building2.position = mouse.world_point
        building2.y -= .6
    elif parkingArea.clicked: # mouse takp et
        parkingArea.position = mouse.world_point
        parkingArea.y += .1
    elif duz_yol.clicked: # mouse takp et
        duz_yol.position = mouse.world_point
        duz_yol.y -= .7
    elif egri_yol.clicked: # mouse takp et
        egri_yol.position = mouse.world_point
        egri_yol.y -= .4
    elif rampa.clicked: # mouse takip et
        rampa.position = mouse.world_point
        rampa.y -= .3
    elif kopru.clicked: # mouse takip et
        kopru.position = mouse.world_point
        kopru.y -= .3
    elif house.clicked: # mouse takip et
        house.position = mouse.world_point
        house.y -= .3

    if parkingAreaList : # eğer liste dolu ise çalıştır
        for pA in parkingAreaList:
            pA.sayac += 1
            invoke(text_popup, "+10 $", pA, delay=pA.sayac) 
            # invoke -> tetiklemek, başlatmak
            # delay 

    # 8.ders eklendi
    # odak modunda kamera hareketi
    origin.rotation_y += ( mouse.velocity[0] * mouse.right * 100)
    origin.rotation_x -= ( mouse.velocity[1] * mouse.right * 100)

                
def select_obj(obj): 
    # ders7 de bu kısım eklendi
    for e in scene.entities:
        if hasattr(e, "lines"): # yani bu nesne bir araba mıdır?
            e.clicked = False # arabanın seçimini iptal et
            e.color = color.white # orjinal rengine çevir

        # ders8 de bu kısım eklendi
        if hasattr(e, "clicked"): 
            if e.clicked:
                e.clicked = False
                e.visible = False # butonları kapatınca sahnede seçili nesne varsa iptal et
    
    obj.clicked = True # nesneyi seç
    obj.visible = True # nesneyi görünür yap


def text_popup(txt="", obj=None) -> None:
        text = Text(text=txt, position = obj.screen_position)
        text.animate_position((text.x, (text.y + randint(5, 10)/100)), duration=1.5, curve=curve.linear)
        text.animate_color(color.rgb(255, 255, 255, 0), duration=1.5, curve=curve.linear)

        # We destroy it after a second
        destroy(text, delay=1)
    
app = Ursina(borderless = False) # pencere ekle

Sky()


building1 = Entity(model="Building_1", unlit=True, clicked=False, visible=False)
building2 = Entity(model="Building_2", unlit=True, clicked=False, visible=False)

parkingArea = Entity(model="ParkingArea2", clicked=False, scale=10, visible=False)

# tree = Entity(model="tree", unlit=True, clicked=False, scale=5, y=1, z=10)
tree1 = Entity(model="tree1.obj", texture="tree1", unlit=True, clicked=False, scale=5, y=0, z=-10)


coin_icon = Entity(model="Coin1", scale= 0.025, color=color.white,parent=camera.ui, z=0, x=.74, y=.45, rotation_y=45, shader=basic_lighting_shader, unlit=True)
btn_m = Button(text="1000", scale=(0.1, 0.05), x=.82, y=.45, color=color.black90) # scale= 0.08

duz_yol = Entity(model="duzYol.obj", texture="duz_yol_baked",unlit=True, clicked=False, scale=2, visible=False, shader=basic_lighting_shader)

egri_yol = Entity(model="egri_yol.obj", texture="egri_yol_baked",unlit=True, clicked=False, scale=8, visible=False)

rampa = Entity(model="rampa.obj", texture="rampa_baked",unlit=True, clicked=False, scale=2, visible=False, shader=basic_lighting_shader)

kopru = Entity(model="bridge.obj", texture="bridge_baked",unlit=True, clicked=False, scale=2, visible=False, shader=basic_lighting_shader)

house = Entity(model="house.obj", texture="house_baked",unlit=True, clicked=False, scale=0.1, visible=False, shader=basic_lighting_shader)

ground = Entity(model="plane", scale=400, texture="grass", collider="box")

# 8.ders odak modu eklendi
EditorCamera(z=-20, y=20, rotation_x = 45) 

origin = Entity()
camera.parent = origin

sun = DirectionalLight() # yönlendirilmiş ışık 
sun.look_at((-1, -1, 1))

app.run()
