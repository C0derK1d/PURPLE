<<<<<<< HEAD
from datetime import datetime
import sys
import socket
import threading
import random
import requests
import pickle
import time
import os
import io
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import subprocess
import pygame
import tkinter
from tkinter import filedialog
from pypresence import Presence
import pypresence

pygame.init()

#host = str(input("Hostname(default:singleplayer):"))
#name = str(input("Your name:"))

def load_img_url(url):
	return pygame.image.load(io.BytesIO(requests.get(url).content))


start_img = load_img_url("https://cdn.discordapp.com/attachments/767022409563504672/820584228915904512/purplogo4.3.png")
icon = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/PURPLE32.png")
character1_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character1.png")
character2_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character2.png")
character3_p = load_img_url("https://raw.githubusercontent.com/BotiPro2007/PURPLE/main/character3.png")

pleace = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
pygame.display.set_caption("PURPLE")
pygame.display.set_icon(icon)
playing= True

#players_x = input["players"]["x"]
#players_y = input["players"]["y"]

i2 = 0
i = 0
x = 0
slot = []
y = 0
py = 25
px = 25
pcount = 0
ppleace = 0
key = "-"
got = False
debug = False
start = 2
musica = 0
render = False
volume = 0.3
connected = False
typing = False
host = ""
name = ""
redc = 1
bluec = 1
greenc = 1
pcolor = (0,0,0)
arrows = False
win = -1
i = 0
stime=0
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

def join(asd):
	print("nice")

def check():
	global host
	global connected
	global stime
	global s
	stime = datetime.now().timestamp()
	if host != "":
		s = socket.socket()
		while not connected:
			try:s.connect((host, 1094))
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
			self.s.blit(pygame.font.SysFont("Arial", self.fs).render(self.f, True, self.fc), (self.x, self.y))
	def is_pressed(self, num : int):
		pos = pygame.mouse.get_pos()
		if pos[0] > self.x and pos[1] > self.y and pos[0] < self.dx:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
					return True
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
	def add_button(self, button):
		self.fpx += button.x
		old_x = button.x
		button.x = self.fpx
		button.y = self.fpy+button.y
		self.buttons.append(button)
		self.fpx += old_x
	def show(self,visible=True):
		pygame.draw.rect(self.s, self.c, pygame.Rect(self.x, self.y, self.dx, self.dy))
		self.s.blit(pygame.font.SysFont("Arial", 22).render(self.t, True, (255,255,255)), (self.x, self.y))
		for button in self.buttons:
			pygame.draw.rect(self.s, button.c, pygame.Rect(button.x, button.y, button.dx, button.dy))
			self.s.blit(pygame.font.SysFont("Arial", button.fs).render(button.f, True, button.fc), (button.x, button.y))
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
def coloring():
	global pcolor
	color = slot[pcount]
	colorline = (pcolor[0], pcolor[1], pcolor[2],0.5)
	if pcolor[0] <= 60 or pcolor[1] <= 60 or pcolor[2] <= 60: colorline = (min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5)
	#(min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5),
	if debug:print(color)
	pcolor = ink_add_for_rgb([
					colorline,
					(color[0],color[1],color[2],0.5)
					])
def add_color(key):
	global slot
	global pcount
	global ppleace
	global pcolor
	global bluec
	global greenc
	global redc
	global win
	slotr = random.randint(0, 40)
	#if slotr == 1:
	#	slot[pcount] = (-1, -1, -1)
	#elif slotr == 2:
	#	slot[pcount] = (1000, 1000, 1000)
	#	print("ne má")
	#else:
	color = colors[random.randint(0, 5)]
	slot[pcount] = color
	ppleace += 1
	if key == "w":
		pcount -= 7
	elif key == "s":
		pcount += 7
	elif key == "a":
		pcount -= 1
	elif key == "d":
		pcount += 1
	color = slot[pcount]
	#print(str(pcolor))
	#print(win)
	if win == 1:
		coloring()
	if win >= 0:
		win -= 1
	else:
		coloring()

def multiplayer():
	global win
	if key != "-" and win != 1:
		d = {"name":name, "key":key, "character":character}
	else:
		d = {"name":name, "character":character}
	msg = pickle.dumps(d)
	s.send(msg)
	try:
		input = pickle.loads(s.recv(1024))
	except EOFError:
		d = {"name":name, "key":key, "character":character}
		msg = pickle.dumps(d)
		s.send(msg)
		print("Waiting for input...")
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
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = start_x
	i = 0
	for index in input:
		if type(input[index]) == type(dict()):
			if input[index]["win"] == 1:
				pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(input[index]["x"]+start_x, input[index]["y"], 50, 50))
				pleace.blit(pygame.font.SysFont("Arial", 75).render(f"{str(index).capitalize()} won this round!", True, (255, 0, 255)), (0, 0))
				win = 1
			else: pygame.draw.rect(pleace, input[index]["color"], pygame.Rect(input[index]["x"]+start_x, input[index]["y"], 50, 50))
			if input[index]["character"] == 0:pleace.blit(character1_p,[input[index]["x"]+start_x,input[index]["y"]])
			elif input[index]["character"] == 1:pleace.blit(character2_p,[input[index]["x"]+start_x,input[index]["y"]])
			elif input[index]["character"] == 2:pleace.blit(character3_p,[input[index]["x"]+start_x,input[index]["y"]])
			pleace.blit(pygame.font.SysFont("Arial", 25).render(str(index), True, (127.5, 127.5, 127.5)), (input[index]["x"]+start_x, input[index]["y"] - 25))
			pleace.blit(pygame.font.SysFont("Arial", 35).render(str(input[index]["p-c"]), True, (100, 100, 100)), (input[index]["x"]+ 5+start_x, input[index]["y"]+5))
		i += 1
	i = 0
	# single player : pygame.draw.rect(pleace, pcolor, pygame.Rect(px, py, 50, 50))
def singleplayer():
	global name
	global px
	global py
	global colors
	global win
	global slot
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
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = start_x
	if debug:print(pcolor)
	#pleace.blit(pygame.font.SysFont("Arial", 35).render(str(ppleace), True, (100, 100, 100)), (px+ 5, py+5))
	red = pcolor[0]
	green = pcolor[1]
	blue = pcolor[2]
	if pcolor[0] <= 255:
		pygame.draw.rect(pleace,pcolor, pygame.Rect(px+start_x, py, 50, 50))
		if red == blue and red > green and green < 127.5 and red > 50 and blue > 50 and red < 255 and blue < 255:
			if win < 1:
				win = 15
		if win > 0:
			pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(px + 5+start_x, py + 5, 40, 40))
		if character == 0:pleace.blit(character1_p,[px+start_x,py])
		elif character == 1:pleace.blit(character2_p,[px+start_x,py])
		elif character == 2:pleace.blit(character3_p,[px+start_x,py])
	#elif pcolor[0] > 1000:
	#	pygame
	pleace.blit(pygame.font.SysFont("Arial", 25).render(name, True, (127.5, 127.5, 127.5)), (px+start_x, py - 25))
	#print(pcolor)

character1 = Button(0, 200, 233, 400, (127.5,0,127.5), "Smile", 50, (255,255,255))
character2 = Button(233, 200, 466, 400, (127.5,0,0), "Shur Iken", 50, (255,255,255))
character3 = Button(466, 200, 700, 400, (0,0,127.5), "Ninja", 50, (255,255,255))

#plus = Window(90,267,515,237,(57, 198, 57),"Saját ablak")
#plus.add_button(Button(50,20,50,50,(255,0,0),"R",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,255,0),"G",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,0,255),"B",50, (255,255,255)))

while playing:
	#try:
	#	if str(s.recv(1024)).startswith("÷"):
	#		print(str(s.recv(1024)))
	#		d = {"name":name, "y":py, "x":px, "color":pcolor, "level":ppleace}
	#		msg = pickle.dumps(d)
	#		s.send(msg)
	#except:
	#	pass
	if start == 1:
		key = "-"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					if not arrows:
						if py > 75:
							py -= 100
							if not connected: add_color("w")
							else: key = "w"
				elif event.key == pygame.K_s:
					if not arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_d:
					if not arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_a:
					if not arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_UP:
					if arrows:
						if py > 75:
							py -= 100
							if not connected:add_color("w")
							else: key = "w"
				elif event.key == pygame.K_DOWN:
					if arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_RIGHT:
					if arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_LEFT:
					if arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_c:
					pcolor = (0, 0, 0)
					ppleace = 0
				elif event.key == pygame.K_ESCAPE:
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
				elif event.key == pygame.K_F3:
					pygame.mixer.music.stop()
					root = tkinter.Tk()
					root.withdraw()
					pygame.mixer.music.load(str(filedialog.askopenfilename()))
					pygame.mixer.music.play(1000000)
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F4:
					if arrows:
						arrows = False
					else:
						arrows = True
				elif event.key == pygame.K_F6:
					pygame.mixer.music.stop()
		if connected:
			multiplayer()
		#GENERATOR
		else:
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
		lol = False
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
				elif event.key == pygame.K_RETURN:
					if typing:
						check()
						start = 3
						lol = True
					else:
						typing = True
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
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 400, 700, 110))
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 540, 700, 110))
		pleace.blit(pygame.transform.scale(start_img, (693,329)),[0,0])
		pleace.blit(pygame.font.SysFont("Arial", 50).render("Name:", True, (255, 255, 255)), (0, 400))
		pleace.blit(pygame.font.SysFont("Arial", 50).render(name , True, (255, 255, 255)), (0, 450))
		pleace.blit(pygame.font.SysFont("Arial", 50).render("Hostname:", True, (255, 255, 255)), (0, 540))
		pleace.blit(pygame.font.SysFont("Arial", 50).render(host , True, (255, 255, 255)), (0, 590))
		if lol: pleace.fill((0,0,0))
	elif start == 3:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
			if event.type == pygame.VIDEORESIZE:
				size = pygame.display.get_surface().get_size()
				start_x = int(size[0]/2-350)
		character1.show()
		if character1.is_pressed(0):
			character = 0
			start = 1
		character2.show()
		if character2.is_pressed(0):
			start = 1
			character = 1
		character3.show()
		if character3.is_pressed(0):
			start = 1
			character = 2
	pygame.display.update()
	pygame.time.Clock().tick(60)
=======
from datetime import datetime
import sys
import socket
import threading
import random
import requests
import pickle
import time
import os
import io
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import subprocess
import pygame
import tkinter
from tkinter import filedialog
from pypresence import Presence
import pypresence

pygame.init()

#host = str(input("Hostname(default:singleplayer):"))
#name = str(input("Your name:"))


pleace = pygame.display.set_mode((700, 700))
pygame.display.set_caption("PURPLE")
pygame.display.set_icon(pygame.image.load("PURPLE32.png"))
playing= True

#players_x = input["players"]["x"]
#players_y = input["players"]["y"]

i2 = 0
i = 0
x = 0
slot = []
y = 0
py = 25
px = 25
pcount = 0
ppleace = 0
key = "-"
got = False
start = 2
musica = 0
render = False
volume = 0.3
typing = False
host = ""
name = ""
redc = 1
bluec = 1
greenc = 1
pcolor = (0,0,0)
arrows = False
win = -1
i = 0
stime=0
has_discord = True
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

def join(asd):
        print("nice")

def load_img_url(url):
        return pygame.image.load(io.BytesIO(requests.get(url).content))

def check():
	global host
	global connected
	global stime
	global s
	stime = datetime.now().timestamp()
	if host != "":
		s = socket.socket()
		s.connect((host, 1094))
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

if has_discord:
	client = pypresence.Client(794267714797043793)
	client.start()
	client.register_event("ACTIVITY_JOIN", join, args={})

def rgb_to_cmyk(r : float,g : float,b : float):
    if (r == 0) and (g == 0) and (b == 0):
        # black
        return 0, 0, 0, cmyk_scale

    print(type(r))

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
			self.s.blit(pygame.font.Font("arial.ttf", self.fs).render(self.f, True, self.fc), (self.x, self.y))
	def is_pressed(self, num : int):
		pos = pygame.mouse.get_pos()
		if pos[0] > self.x and pos[1] > self.y and pos[0] < self.dx:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
					return True
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
	def add_button(self, button):
		self.fpx += button.x
		old_x = button.x
		button.x = self.fpx
		button.y = self.fpy+button.y
		self.buttons.append(button)
		self.fpx += old_x
	def show(self,visible=True):
		pygame.draw.rect(self.s, self.c, pygame.Rect(self.x, self.y, self.dx, self.dy))
		self.s.blit(pygame.font.Font("arial.ttf", 22).render(self.t, True, (255,255,255)), (self.x, self.y))
		for button in self.buttons:
			pygame.draw.rect(self.s, button.c, pygame.Rect(button.x, button.y, button.dx, button.dy))
			self.s.blit(pygame.font.Font("arial.ttf", button.fs).render(button.f, True, button.fc), (button.x, button.y))
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
def coloring():
	global pcolor
	color = slot[pcount]
	colorline = (pcolor[0], pcolor[1], pcolor[2],0.5)
	if pcolor[0] <= 60 or pcolor[1] <= 60 or pcolor[2] <= 60: colorline = (min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5)
	#(min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5),
	print(color)
	pcolor = ink_add_for_rgb([
					colorline,
					(color[0],color[1],color[2],0.5)
					])
def add_color(key):
	global slot
	global pcount
	global ppleace
	global pcolor
	global bluec
	global greenc
	global redc
	global win
	slotr = random.randint(0, 40)
	#if slotr == 1:
	#	slot[pcount] = (-1, -1, -1)
	#elif slotr == 2:
	#	slot[pcount] = (1000, 1000, 1000)
	#	print("ne má")
	#else:
	color = colors[random.randint(0, 5)]
	slot[pcount] = color
	ppleace += 1
	if key == "w":
		pcount -= 7
	elif key == "s":
		pcount += 7
	elif key == "a":
		pcount -= 1
	elif key == "d":
		pcount += 1
	color = slot[pcount]
	#print(str(pcolor))
	#print(win)
	if win == 1:
		coloring()
	if win >= 0:
		win -= 1
	else:
		coloring()
def multiplayer():
	global name
	global px
	global py
	global color
	global win
	global RPC

	if key != "-":
		d = {"name":name, "key":key, "character":character}
	else:
		d = {"name":name, "character":character}
	msg = pickle.dumps(d)
	s.send(msg)
	try:
		input = pickle.loads(s.recv(1024))
	except EOFError:
		d = {"name":name, "key":key, "character":character}
		msg = pickle.dumps(d)
		s.send(msg)
		print("Waiting for input...")
	#except:
	#	input = s.recv(1024)
	#	print("The server said:"+str(input))
	print(input)
	got = True
	slot = input["slot"]
	if input["players"] > 0 and has_discord:
		RPC.update(large_image="logo", state="Multiplayer",start = stime,party_id=str(host),join=str(input["code"]), party_size=[input["players"], input["max_players"]])
	count = 0
	i2 = 0
	i = 0
	x = 0
	y = 0
	got = False
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 50, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = 0
	i = 0
	for index in input:
		if input[index] != input["slot"]:
			try:
				pygame.draw.rect(pleace, input[index]["color"], pygame.Rect(input[index]["x"], input[index]["y"], 50, 50))
				if input[index]["character"] == 0:pleace.blit(pygame.image.load("character1.png"),[input[index]["x"],input[index]["y"]])
				elif input[index]["character"] == 1:pleace.blit(pygame.image.load("character2.png"),[input[index]["x"],input[index]["y"]])
				elif input[index]["character"] == 2:pleace.blit(pygame.image.load("character3.png"),[input[index]["x"],input[index]["y"]])
				if win == 1:
					pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(input[index]["x"] + 5, input[index]["y"] + 5, 55, 55))
					pleace.blit(pygame.font.Font("arial.ttf", 150).render(str(index), True, (255, 0, 255)), (0, 400))
				pleace.blit(pygame.font.Font("arial.ttf", 25).render(str(index), True, (127.5, 127.5, 127.5)), (input[index]["x"], input[index]["y"] - 25))
				pleace.blit(pygame.font.Font("arial.ttf", 35).render(str(input[index]["p-c"]), True, (100, 100, 100)), (input[index]["x"]+ 5, input[index]["y"]+5))
			except:
				pass
		i += 1
	i = 0
	# single player : pygame.draw.rect(pleace, pcolor, pygame.Rect(px, py, 50, 50))
def singleplayer():
	global name
	global pcolor
	global px
	global py
	global colors
	global pleace
	global win
	global name
	global slot
	i2 = 0
	i = 0
	x = 0
	y = 0
	count = 0
	while i2 < 7:
		y = i2*100
		while i < 7:
			x = i*100
			if slot[count] == (1000, 1000, 1000):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
			elif slot[count] == (-1, -1, -1):
				pygame.draw.rect(pleace, (255, 255, 255), pygame.Rect(x, y, 100, 100))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 25, y + 37, 50, 25))
				pygame.draw.rect(pleace, (0, 0, 0), pygame.Rect(x + 37, y + 23, 25, 50))
			else:
				pygame.draw.rect(pleace, slot[count], pygame.Rect(x, y, 100, 100))
			i += 1
			count += 1
		i2 += 1
		i = 0
		x = 0
	print(pcolor)
	#pleace.blit(pygame.font.Font("arial.ttf", 35).render(str(ppleace), True, (100, 100, 100)), (px+ 5, py+5))
	red = pcolor[0]
	green = pcolor[1]
	blue = pcolor[2]
	if pcolor[0] <= 255:
		pygame.draw.rect(pleace,pcolor, pygame.Rect(px, py, 50, 50))
		if red == blue and red > green and green < 127.5 and red > 50 and blue > 50 and red < 255 and blue < 255:
			if win < 1:
				win = 15
		if win > 0:
			pygame.draw.rect(pleace, (255, 153, 0), pygame.Rect(px + 5, py + 5, 40, 40))
		if character == 0:pleace.blit(pygame.image.load("character1.png"),[px,py])
		elif character == 1:pleace.blit(pygame.image.load("character2.png"),[px,py])
		elif character == 2:pleace.blit(pygame.image.load("character3.png"),[px,py])
	#elif pcolor[0] > 1000:
	#	pygame
	pleace.blit(pygame.font.Font("arial.ttf", 25).render(name, True, (127.5, 127.5, 127.5)), (px, py - 25))
	#print(pcolor)

character1 = Button(0, 200, 233, 400, (127.5,0,127.5), "Smile", 50, (255,255,255))
character2 = Button(233, 200, 466, 400, (127.5,0,0), "Shur Iken", 50, (255,255,255))
character3 = Button(466, 200, 700, 400, (0,0,127.5), "Ninja", 50, (255,255,255))

#plus = Window(90,267,515,237,(57, 198, 57),"Saját ablak")
#plus.add_button(Button(50,20,50,50,(255,0,0),"R",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,255,0),"G",50, (255,255,255)))
#plus.add_button(Button(50,20,50,50,(0,0,255),"B",50, (255,255,255)))

while playing:
	#try:
	#	if str(s.recv(1024)).startswith("÷"):
	#		print(str(s.recv(1024)))
	#		d = {"name":name, "y":py, "x":px, "color":pcolor, "level":ppleace}
	#		msg = pickle.dumps(d)
	#		s.send(msg)
	#except:
	#	pass
	if start == 1:
		key = "-"
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					if not arrows:
						if py > 75:
							py -= 100
							if not connected: add_color("w")
							else: key = "w"
				elif event.key == pygame.K_s:
					if not arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_d:
					if not arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_a:
					if not arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_UP:
					if arrows:
						if py > 75:
							py -= 100
							if not connected:add_color("w")
							else: key = "w"
				elif event.key == pygame.K_DOWN:
					if arrows:
						if py < 625:
							py += 100
							if not connected:add_color("s")
							else: key = "s"
				elif event.key == pygame.K_RIGHT:
					if arrows:
						if px < 625:
							px += 100
							if not connected:add_color("d")
							else: key = "d"
				elif event.key == pygame.K_LEFT:
					if arrows:
						if px > 75:
							px -= 100
							if not connected:add_color("a")
							else: key = "a"
				elif event.key == pygame.K_c:
					pcolor = (0, 0, 0)
					ppleace = 0
				elif event.key == pygame.K_ESCAPE:
					playing = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F1:
					volume -= 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F2:
					volume += 0.02
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F3:
					pygame.mixer.music.stop()
					root = tkinter.Tk()
					root.withdraw()
					pygame.mixer.music.load(str(filedialog.askopenfilename()))
					pygame.mixer.music.play(1000000)
					pygame.mixer.music.set_volume(volume)
				elif event.key == pygame.K_F4:
					if arrows:
						arrows = False
					else:
						arrows = True
				elif event.key == pygame.K_F6:
					pygame.mixer.music.stop()
		if connected:
			multiplayer()
		#GENERATOR
		else:
			if not render:
				render = True
				i2 = 0
				i = 0
				while i2 < 7:
					y = i2*100
					while i < 7:
						x = i*100
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
					x = 0
					i2 += 1
				i = 0
				x = 0
				y = 0
				i2 = 0
			singleplayer()
	elif start == 2:
		lol = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if connected:
					s.close()
				playing = False
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
						lol = True
					else:
						typing = True
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
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 400, 700, 110))
		pygame.draw.rect(pleace, (127.5, 0, 127.5), pygame.Rect(0, 540, 700, 110))
		pleace.blit(pygame.transform.scale(load_img_url("https://cdn.discordapp.com/attachments/767022409563504672/820584228915904512/purplogo4.3.png"), (693,329)),[0,0])
		pleace.blit(pygame.font.Font("arial.ttf", 50).render("Name:", True, (255, 255, 255)), (0, 400))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render(name , True, (255, 255, 255)), (0, 450))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render("Hostname:", True, (255, 255, 255)), (0, 540))
		pleace.blit(pygame.font.Font("arial.ttf", 50).render(host , True, (255, 255, 255)), (0, 590))
		if lol: pleace.fill((0,0,0))
	elif start == 3:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
		character1.show()
		if character1.is_pressed(0):
			character = 0
			start = 1
			print("nice")
		character2.show()
		if character2.is_pressed(0):
			start = 1
			character = 1
			print("nice")
		character3.show()
		if character3.is_pressed(0):
			start = 1
			character = 2
			print("nice")
	pygame.display.update()
	pygame.time.Clock().tick(60)
>>>>>>> ffa90bc621fcd7d3d2e0b32a59fa6631b2ddeeb3
