from datetime import datetime
import socket
import threading
import random
import requests
import pickle
import time
import os
import io
import configparser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pypresence import Presence
import pypresence

pygame.init()

config = configparser.ConfigParser()
config.read("settings.ini")
asettings = config["AttackSettings"]
msettings = config["MovementSettings"]

def load_img_url(url):
	return pygame.image.load(io.BytesIO(requests.get(url).content))

def center_rotate(image, angle, pos):
	rot_image = pygame.transform.rotate(image, angle)
	pos = rot_image.get_rect(center = image.get_rect(topleft = pos).center).topleft
	return rot_image, pos

'''
OFFLINE MODE
start_img = pygame.image.load("PURPLE-DC.png")
icon = pygame.image.load("purple32.png")
character1_p = pygame.image.load("character1.png")
character2_p = pygame.image.load("character2.png")
character3_p = pygame.image.load("character3.png")
shuriken_p = pygame.image.load("shuriken.png")
knife_p = pygame.image.load("knife.png")

DEV-STYLE
character1_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE-dev-style/main/character1.png")
character2_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE-dev-style/main/character2.png")
character3_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE-dev-style/main/character3.png")
knife_p = pygame.transform.scale(load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE-dev-style/main/knife.png"), (200,200))
shuriken_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/shuriken.png")
'''

start_img = load_img_url("https://cdn.discordapp.com/attachments/767022409563504672/820584228915904512/purplogo4.3.png")
icon = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/PURPLE32.png")
character1_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character1.png")
character2_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character2.png")
character3_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character3.png")
knife_p = pygame.transform.scale(load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/sword.png"), (200,200))
toothgear_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/toothwheel.png")
shuriken_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/shuriken.png")

pleace = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
pygame.display.set_caption("PURPLE")
pygame.display.set_icon(icon)
playing= True

#players_x = input["players"]["x"]
#players_y = input["players"]["y"]

r = False
fullscreen = False
i2 = 0
i = 0
x = 0
slot = []
y = 0
key = "-"
got = False
debug = True
start = 2
musica = 0
render = False
volume = 0.3
connected = False
typing = False
host = ""
name = ""
win = -1
stime=0
wdata = {"visible":False, "x":25,"y":25, "state":0, "reloaded":True}
has_discord = True
start_x = 0
#           piros         kék           zöld          sárga           fehér        fekete
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 255, 255), (0, 0, 0)]

rgb_scale = 255
cmyk_scale = 100

#Discord RPC: Has Discord ran?
try:
	RPC = Presence(794267714797043793)
	RPC.connect()
	RPC.update(large_image="logo", large_text="PURPLE")
except pypresence.exceptions.InvalidPipe:
	has_discord = False

def check():
	global host
	global connected
	global stime
	global s
	stime = datetime.now().timestamp()
	if host != "":
		s = socket.socket()
		while not connected:
			try:s.connect((host, 1074))
			except:
				print("Not valid hostname! Please try again!")
			else:
				connected = True
		if has_discord:
			RPC.update(large_image="logo", large_text="PURPLE",
					state="Multiplayer",
					start = stime)
	else:
		if has_discord:
			RPC.update(large_image="logo", large_text="PURPLE",
					state="Singleplayer",
					start = stime)
		connected = False

'''
if has_discord:
	client = pypresence.Client(794267714797043793)
	client.start()
	client.register_event("ACTIVITY_JOIN", join, args={})
'''
def rgb_to_cmyk(r : float,g : float,b : float):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    # rgb [0,255] -> cmy [0,1]
    c = 1 - r / float(rgb_scale)
    m = 1 - g / float(rgb_scale)
    y = 1 - b / float(rgb_scale)

    # extract out k [0,1]
    min_cmy = min(c, m, y)
    c = (c - min_cmy)
    m = (m - min_cmy)
    y = (y - min_cmy)
    k = min_cmy

    # rescale to the range [0,cmyk_scale]
    return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale

def cmyk_to_rgb(c,m,y,k):
    """
    """
    r = rgb_scale*(1.0-(c+k)/float(cmyk_scale))
    g = rgb_scale*(1.0-(m+k)/float(cmyk_scale))
    b = rgb_scale*(1.0-(y+k)/float(cmyk_scale))
    return (r,g,b)

def ink_add_for_rgb(list_of_colours : list):
    """input: list of rgb, opacity (r,g,b,o) colours to be added, o acts as weights.
    output (r,g,b)
    """
    C = 0
    M = 0
    Y = 0
    K = 0

    for (r,g,b,o) in list_of_colours:
        c,m,y,k = rgb_to_cmyk(r, g, b)
        C+= o*c
        M+=o*m
        Y+=o*y
        K+=o*k

    return cmyk_to_rgb(C, M, Y, K)

class Player(pygame.sprite.Sprite):
	def __init__(self, color, scale, type, pos = [25,25]):
		pygame.sprite.Sprite.__init__(self)
		
		
		self.type = type
		self.pos = pos
		self.level = 0
		self.count = 0
		self.color = color
		self.aimd = 0
		self.win = -1
		self.wdata = {"visible":False, "x":pos[0],"y":pos[1], "state":0, "reloaded":True}
		self.scale = scale
		self.image = pygame.Surface([50*scale, 50*scale])
		self.image.fill(color)
	
	def weapon(self):
		self.wdata["visible"] = True
		self.wdata["reloaded"] = False
		if self.type == 1:
			while (self.aimd == 1 and self.wdata["y"] > 75) or (self.aimd == 3 and self.wdata["y"] < 625) or (self.aimd == 2 and self.wdata["x"] > 75) or (self.aimd == 0 and self.wdata["x"] < 625):
				if self.aimd == 0: self.wdata["x"] += 100
				elif self.aimd == 1: self.wdata["y"] -= 100
				elif self.aimd == 2: self.wdata["x"] -= 100
				elif self.aimd == 3: self.wdata["y"] += 100
				if self.wdata["state"] == 1: self.wdata["state"] = 0
				else: self.wdata["state"] += 1
				time.sleep(0.25)
				if debug: print(f"Oh yes I am going! My location: X: {self.wdata['x']} ; Y: {self.wdata['y']} ; AIMD: {self.aimd}")
			self.wdata.update({"visible":False, "reloaded":True, "x":self.pos[0], "y":self.pos[1]})
		elif self.type == 2:	
			if self.aimd == 0 and self.pos[0] < 525: 
				self.wdata["state"] = 0
				self.wdata["y"] -= 100
				time.sleep(0.2)
				self.pos[0] += 200
				self.count += 2
			elif self.aimd == 1 and self.pos[1] > 175: 
				self.wdata["state"] = 1
				self.wdata["y"] -= 200
				self.wdata["x"] -= 100
				time.sleep(0.2)
				self.pos[1] -= 200
				self.count -= 14
			elif self.aimd == 2 and self.pos[0] > 175: 
				self.wdata["state"] = 2
				self.wdata["x"] -= 200
				self.wdata["y"] -= 100
				time.sleep(0.2)
				self.pos[0] -= 200
				self.count -= 2
			elif self.aimd == 3 and self.pos[1] < 525:
				self.wdata["state"] = 3
				self.wdata["x"] -= 100
				time.sleep(0.2)
				self.pos[1] += 200
				self.count += 14
			self.wdata.update({"visible":False, "reloaded": False})
			print(f"X:{self.wdata['x']}; Y: {self.wdata['y']}")
			time.sleep(0.5)
			self.wdata.update({"visible":False, "reloaded":True, "x":self.pos[0]+25, "y":self.pos[1]+25})

	def coloring(self):
		color = slot[self.count]
		colorline = (self.color[0], self.color[1], self.color[2],0.5)
		if self.color[0] <= 60 or self.color[1] <= 60 or self.color[2] <= 60: colorline = (min(self.color[0]*2, 255),min(self.color[1]*2, 255),min(self.color[2]*2, 255),0.5)
		#(min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5),
		if debug:print(color)
		self.color = ink_add_for_rgb([
						colorline,
						(color[0],color[1],color[2],0.5)
						])
	
	def key_check(self):
		k = "-"
		e = pygame.event.get(eventtype=pygame.KEYUP)
		if self.type == 1 and self.wdata["reloaded"]: self.wdata.update({"visible":False, "reloaded":True, "x":self.pos[0], "y":self.pos[1]})
		elif self.type == 2 and self.wdata["reloaded"]: self.wdata.update({"visible":False, "reloaded":True, "x":self.pos[0]+25, "y":self.pos[1]+25})
		if len(e) > 0: 
			key = str(e[0].key)
		else: return
		oldc = self.count
		if key == str(pygame.K_w) or key == pygame.K_UP:
			if self.pos[1] > 75 and not connected:
				self.pos[1] -= 100
				self.count -= 7
			else: k = "w"
		elif key == str(pygame.K_s) or key == pygame.K_DOWN:
			if self.pos[1] < 625 and not connected:
				self.pos[1] += 100	
				self.count += 7
			else: k = "s"
		elif key == str(pygame.K_a) or key == pygame.K_LEFT:
			if self.pos[0] > 75 and not connected:
				self.pos[0] -= 100
				self.count -= 1
			else: k="a"
		elif key == str(pygame.K_d) or key == pygame.K_RIGHT:
			if self.pos[0] < 625 and not connected:
				self.pos[0] += 100
				self.count += 1
			else: k = "d"
		elif key == asettings["attack"] and self.wdata["reloaded"]:
			if self.type > 0 and not connected: threading.Thread(target=self.weapon).start()
			key = "attack"
		elif key == pygame.K_c:
			self.color = (0, 0, 0)
			self.level = 0
		elif key == asettings["aimNorth"]:
			self.aimd = 1
		elif key == asettings["aimSouth"]:
			self.aimd = 3
		elif key == asettings["aimWest"]:
			self.aimd = 2
		elif key == asettings["aimEast"]:
			self.aimd = 0
		if oldc != self.count:	
			if not key == asettings["attack"] and self.wdata["reloaded"]:
				color = colors[random.randint(0, 5)]
				slot[oldc] = color
			if self.win == 1:
				self.coloring()
			if self.win >= 0:
				self.win -= 1
			else:
				if not key == pygame.K_KP0: self.coloring()
		
		return k
	
class Button:
	def __init__(self, x : int, y : int, dx : int, dy : int, color, font : str, fs : int, fc):
		
		global pleace
		self.s = pleace
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.c = color
		self.f = font
		self.fs = fs
		self.visible = True
		self.fc = fc
		self.click = pygame.mouse.get_pressed()
	def show(self, visible = True):
		self.visible = visible
		if self.visible:
			pygame.draw.rect(self.s, self.c, pygame.Rect(self.x, self.y, self.dx, self.dy))
			self.s.blit(pygame.font.SysFont("Courier New", self.fs).render(self.f, True, self.fc), (self.x, self.y))
	def is_pressed(self):
		pos = pygame.mouse.get_pos()
		if pos[0] > self.x and pos[1] > self.y and pos[0] < self.x+self.dx and pos[1] < self.y+self.dy and pygame.mouse.get_pressed(3) == (True,False,False):
			return True
		else:
			return False

class Window:
	def __init__(self, x:int, y:int , dx:int , dy:int,color ,title:str, description=""):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.c = color
		self.t = title
		self.d = description
		self.s = pleace
		self.fpx = x
		self.fpy = y+24
		self.buttons = []
	def add_button(self, button, tabb=True):
		if tabb:self.fpx += button.x
		old_x = button.x
		button.x = self.fpx
		button.y = self.fpy+button.y
		self.buttons.append(button)
		#if tabb: self.fpx += old_x
	def show(self,visible=True):
		pygame.draw.rect(self.s, self.c, pygame.Rect(self.x, self.y, self.dx, self.dy))
		self.s.blit(pygame.font.SysFont("Courier New", 26).render(self.t, True, (255,255,255)), (self.x, self.y))
		for button in self.buttons:
			pygame.draw.rect(self.s, button.c, pygame.Rect(button.x, button.y, button.dx, button.dy))
			self.s.blit(pygame.font.SysFont("Courier New", button.fs).render(button.f, True, button.fc), (button.x, button.y))
#százalékszámítás: 50 : 100 * 50
#           valamennyinek   százaléka
def set_music():
	global musica
	music_list = ["The Best Clouds.wav", "PURPLE.wav"]
	musica +=1
	if musica >= len(music_list):
		print("reset!")
		musica = 0
	#pygame.mixer.music.load(music_list[musica])
	#pygame.mixer.music.set_volume(volume)
	#pygame.mixer.music.play(10000)

def multiplayer():
	global win
	if key != "-" and win != 1:
		d = {"name":name, "key":key, "aimd":aimd}
	else:
		d = {"name":name, "character":character, "aimd":aimd}
	msg = pickle.dumps(d)
	s.send(msg)
	try:
		input = pickle.loads(s.recv(1024))
	except EOFError:
		return
	#except:
	#	input = s.recv(1024)
	#	print("The server said:"+str(input))
	if debug:print(input)
	got = True
	slot = input["slot"]
	if input["players"] > 0 and has_discord:
		RPC.update(large_image="logo", state="Multiplayer",start = stime,party_id=str(host),join=str(input["code"]), party_size=[input["players"], input["max_players"]])
	count = 0
	i2 = 0
	i = 0
	x = start_x
	y = 0
	got = False
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100+start_x
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 50, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, (100,0,100), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x+2, y+2, 98, 98))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = start_x
	i = 0
	for index in input:
		if type(input[index]) == type(dict()) and index != "wdata":
			if input[index]["win"] == 1:
				pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(input[index]["x"]+start_x, input[index]["y"], 50, 50))
				pleace.blit(pygame.font.SysFont("Courier New", 50).render(f"{str(index).capitalize()} won this round!", True, (255, 0, 255)), (start_x+0, 0))
				win = 1
			else: pygame.draw.rect(pleace, input[index]["color"], pygame.Rect(input[index]["x"]+start_x, input[index]["y"], 50, 50))
			if input[index]["character"] == 0:pleace.blit(character1_p,[input[index]["x"]+start_x,input[index]["y"]])
			elif input[index]["character"] == 1:pleace.blit(character2_p,[input[index]["x"]+start_x,input[index]["y"]])
			elif input[index]["character"] == 2:pleace.blit(character3_p,[input[index]["x"]+start_x,input[index]["y"]])
			if input[index].get("wdata") != None: 
				wdata = input[index]["wdata"]
				if input[index]["character"] == 1:
					if wdata["visible"]:
						if wdata["state"] == 0:
							blit_data = center_rotate(shuriken_p, 45, (wdata["x"]+start_x,wdata["y"]))
							pleace.blit(blit_data[0], blit_data[1])
						else: pleace.blit(shuriken_p, [wdata["x"]+start_x,wdata["y"]])
				elif input[index]["character"] == 2:
					if wdata["visible"]:
						if wdata["state"] == 0: 
							img, pos = center_rotate(knife_p, 270, (wdata["x"]+start_x,wdata["y"]))
							pleace.blit(img, pos)
						if wdata["state"] == 1:
							pleace.blit(knife_p,(wdata["x"]+start_x,wdata["y"]))
						if wdata["state"] == 2:
							img, pos = center_rotate(knife_p, 90, (wdata["x"]+start_x,wdata["y"]))
							pleace.blit(img, pos)
						if wdata["state"] == 3:
							img, pos = center_rotate(knife_p, 180, (wdata["x"]+start_x,wdata["y"]))
							pleace.blit(img, pos)
			pleace.blit(pygame.font.SysFont("Courier New", 35).render(str(index), True, (127, 0, 127)), (710+start_x, i*50))
			pleace.blit(pygame.font.SysFont("Courier New", 35).render(str(input[index]["p-c"]), True, (127, 0, 127)), (800+start_x, 0+i*50))
			pleace.blit(pygame.font.SysFont("Courier New", 35).render(str(input[index]["level"]), True, (127, 0, 127)), (900+start_x, 0+i*50))
			pleace.blit(pygame.font.SysFont("Courier New", 25, bold=True).render(str(index), True, (127.5, 127.5, 127.5)), (input[index]["x"]+start_x, input[index]["y"] - 25))
			#pleace.blit(pygame.font.SysFont("Courier New", 35).render(str(input[index]["p-c"]), True, (100, 100, 100)), (input[index]["x"]+ 5+start_x, input[index]["y"]+5))
			i += 1
	i = 0
	# single player : pygame.draw.rect(pleace, pcolor, pygame.Rect(px, py, 50, 50))
def singleplayer():
	i2 = 0
	i = 0
	x = start_x
	y = 0
	count = 0
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100+start_x
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, (100,0,100), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x+2, y+2, 98, 98))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = start_x
	#if debug:print(pcolor)
	#pleace.blit(pygame.font.SysFont("Courier New", 35).render(str(ppleace), True, (100, 100, 100)), (px+ 5, py+5))
	red = p1.color[0]
	green = p1.color[1]
	blue = p1.color[2]
	if p1.color[0] <= 255:
		pygame.draw.rect(pleace,p1.color, pygame.Rect(p1.pos[0]+start_x, p1.pos[1], 50, 50))
		if red == blue and red > green and green < 127.5 and red > 50 and blue > 50 and red < 255 and blue < 255:
			if p1.win < 1:
				p1.win = 15
		if p1.win > 0:
			pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(p1.pos[0]+start_x, p1.pos[1], 50, 50))
		if p1.type == 0:pleace.blit(character1_p,(p1.pos[0]+start_x,p1.pos[1]))
		elif p1.type == 1:
			if p1.wdata["visible"]:
				if p1.wdata["state"] == 0:
					blit_data = center_rotate(shuriken_p, 45, (p1.wdata["x"]+start_x,p1.wdata["y"]))
					pleace.blit(blit_data[0], blit_data[1])
				else: pleace.blit(shuriken_p, (p1.wdata["x"]+start_x,p1.wdata["y"]))
			pleace.blit(character2_p,[p1.pos[0]+start_x,p1.pos[1]])
		elif p1.type == 2:
			pleace.blit(character3_p,[p1.pos[0]+start_x,p1.pos[1]])
			if p1.wdata["visible"]:
				if p1.wdata["state"] == 0: 
					img, pos = center_rotate(knife_p, 270, (p1.wdata["x"]+start_x,p1.wdata["y"]))
					pleace.blit(img, pos)
				if wdata["state"] == 1:
					pleace.blit(knife_p,(p1.wdata["x"]+start_x,p1.wdata["y"]))
				if wdata["state"] == 2:
					img, pos = center_rotate(knife_p, 90, (p1.wdata["x"]+start_x,p1.wdata["y"]))
					pleace.blit(img, pos)
				if wdata["state"] == 3:
					img, pos = center_rotate(knife_p, 180, (p1.wdata["x"]+start_x,p1.wdata["y"]))
					pleace.blit(img, pos)
	pleace.blit(pygame.font.SysFont("Courier New", 25, bold=True).render(name, True, (100, 0, 100)), (p1.pos[0]+start_x, p1.pos[1] - 25))

character1 = Button(0, 200, 233, 400, (127.5,0,127.5), "Smile", 40, (255,255,255))
character2 = Button(233, 200, 233, 400, (127.5,0,0), "Shur Iken", 40, (255,255,255))
character3 = Button(466, 200, 233, 400, (0,0,127.5), "Ninja", 40, (255,255,255))

settings = Window(13,116,667,436,(100, 0, 100),"Attack controls:")
settings.add_button(Button(50,20,500,50,(255,255,0),"Attack",50, (0,0,0)))
settings.add_button(Button(50,90,500,50,(255,255,0),"Aim North",50, (0,0,0)), False)
settings.add_button(Button(50,160,500,50,(255,255,0),"Aim East",50, (0,0,0)), False)
settings.add_button(Button(50,230,500,50,(255,255,0),"Aim South",50, (0,0,0)), False)
settings.add_button(Button(50,300,500,50,(255,255,0),"Aim West",50, (0,0,0)), False)

toothgear = Button(600, 0, 100, 100, (100,100,100),"", 1, (0,0,0))

record = Window(160,200,365,220,(100, 0, 0),"Record", "Press a key to continue...")

#plus = Window(90,267,515,237,(57, 198, 57),"Saját ablak")
#plus.add_button(Button(50,20,50,50,(255,0,0),"R",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,255,0),"G",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,0,255),"B",50, (255,255,255)))

while playing:
	pleace.fill((0,0,0))
	#try:
	#	if str(s.recv(1024)).startswith("÷"):
	#		print(str(s.recv(1024)))
	#		d = {"name":name, "y":py, "x":px, "color":pcolor, "level":ppleace}
	#		msg = pickle.dumps(d)
	#		s.send(msg)
	#except:
	#	pass	
	if start == 1:
		if render: key = p1.key_check()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
			if event.type == pygame.VIDEORESIZE:
				size = pygame.display.get_surface().get_size()
				start_x = int(size[0]/2-350)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:
					volume -= 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F2:
					volume += 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F4:
					if arrows:
						arrows = False
					else:
						arrows = True
				elif event.key == pygame.K_F6:
					pygame.mixer.music.stop()
				elif event.key == pygame.K_F11:
					if not fullscreen:
						pleace = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
						fullscreen = True
					else:
						pleace = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
						fullscreen = False
				if event.key == pygame.K_ESCAPE:
					start = 2
					if connected: s.close()
		if connected:
			pygame.draw.rect(pleace, (127, 0, 127), pygame.Rect(start_x-5, 0, 710, 705))
			multiplayer()
		#GENERATOR
		else:
			pygame.draw.rect(pleace, (127, 0, 127), pygame.Rect(start_x-5, 0, 710, 705))
			if not render:
				render = True
				i2 = 0
				i = 0
				while i2 < 7:
					while i < 7:
						slotr = random.randint(0, 30)
						#if slotr == 1:
						#	slot.append((-1, -1, -1))
						#elif slotr == 2:
						#	slot.append((1000, 1000, 1000))
						#else:
						color = colors[random.randint(0, 5)]
						slot.append(color)
						i += 1
					i = 0
					i2 += 1
			singleplayer()
	elif start == 2:
		reset = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
			if event.type == pygame.VIDEORESIZE:
				size = pygame.display.get_surface().get_size()
				start_x = int(size[0]/2-350)
				toothgear.x = start_x+toothgear.x
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:
					volume -= 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F2:
					volume += 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_RETURN:
					if typing:
						check()
						start = 3
						reset = True
					else:
						typing = True
				elif event.key == pygame.K_F9: start = 4
				elif event.key == pygame.K_DOWN:
					typing = True
				elif event.key == pygame.K_UP:
					typing = False
				elif event.key == pygame.K_BACKSPACE:
					if not typing:
						name = name[:-1]
					else:
						host = host[:-1]
				else:
					if not typing:
						name += event.unicode
					else:
						host += event.unicode
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 400, 2000, 110))
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 540, 2000, 110))
		pleace.blit(pygame.transform.scale(start_img, (693,329)),[start_x,0])
		if toothgear.is_pressed():
			start = 4
		toothgear.show()
		pleace.blit(pygame.transform.scale(toothgear_p, (100,100)),[start_x+600,0])
		pleace.blit(pygame.font.SysFont("Courier New", 50).render("Name:", True, (255, 255, 255)), (0, 400))
		pleace.blit(pygame.font.SysFont("Courier New", 50).render(name , True, (255, 255, 255)), (0, 450))
		pleace.blit(pygame.font.SysFont("Courier New", 50).render("Hostname:", True, (255, 255, 255)), (0, 540))
		pleace.blit(pygame.font.SysFont("Courier New", 50).render(host , True, (255, 255, 255)), (0, 590))
	elif start == 3:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
			if event.type == pygame.VIDEORESIZE:
				size = pygame.display.get_surface().get_size()
				start_x = int(size[0]/2-350)
		character1.show()
		if character1.is_pressed():
			p1 = Player((0,0,0), 1, 0)
			start = 1
		character2.show()
		if character2.is_pressed():
			p1 = Player((0,0,0), 1, 1)
			start = 1
		character3.show()
		if character3.is_pressed():
			p1 = Player((0,0,0), 1, 2)
			start = 1
	elif start == 4:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE: start = 2
		settings.show()
		i = 0
		for button in settings.buttons:
			if button.is_pressed():
				r = True
				i2 = i
				break
			i += 1
		if r:
			record.show()
			e = pygame.event.get(eventtype=pygame.KEYUP)
			if len(e) > 0: 
				if i2 == 0: config["AttackSettings"]["attack"] = str(e[0].key)
				if i2 == 1: config["AttackSettings"]["aimNorth"] = str(e[0].key)
				if i2 == 2: config["AttackSettings"]["aimEast"] = str(e[0].key)
				if i2 == 3: config["AttackSettings"]["aimSouth"] = str(e[0].key)
				if i2 == 4: config["AttackSettings"]["aimWest"] = str(e[0].key)
				config.write(open("settings.ini", "w"))
				config.read("settings.ini")
				asettings = config["AttackSettings"]
				msettings = config["MovementSettings"]
				r = False
	pygame.display.update()
	pygame.time.Clock().tick(60)
