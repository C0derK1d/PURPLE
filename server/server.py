import socket
import random
import pickle
import time
import os
import threading
import configparser

config = configparser.ConfigParser()
config.read("mod.ini")
soptions = config["ServerOptions"]
koptions = config["KillOptions"]
debug = bool(int(soptions["debugMode"]))
max_players = int(soptions["maxPlayers"])
if max_players > 4: max_players = 4
s = socket.socket()
try:
	s.bind((soptions["hostname"], int(soptions["port"])))
	s.listen(5)
except:
	print("This hostname already in use or the hostname is invalid! This will not works!\n\nPress Crtl+C to close!")
	try: 
		while True: pass
	except: quit()

print("I ready")

i = 0
i2 = 0
x = 0
y = 0
slot = []
players = 0
rgb_scale = 255
cmyk_scale = 100
player_datas = {}
a = []
addr = []
slotr = 3
#           piros         kék           zöld          sárga           fehér        fekete
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (255, 255, 255), (0, 0, 0)]

abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

while i2 < 7:
	y = i2*100
	while i < 7:
		x = i*100
		#slotr = random.randint(0, 30)
		if slotr == 1:
			slot.append((-1, -1, -1))
		elif slotr == 2:
			slot.append((1000, 1000, 1000))
		else:
			color = colors[random.randint(0, 5)]
			slot.append(color)
		i += 1
	i = 0
	x = 0
	i2 += 1
code = ""
for x in random.choices(abc, k=10):
	code += x
player_datas.update({"slot":slot,"code":code,"max_players":max_players})

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

def coloring(data):
	pcount = data["pcount"]
	pcolor = data["color"]
	color = slot[pcount]
	colorline = (pcolor[0], pcolor[1], pcolor[2],0.5)
	if pcolor[0] <= 60 or pcolor[1] <= 60 or pcolor[2] <= 60: colorline = (min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5)
	#(min(pcolor[0]*2, 255),min(pcolor[1]*2, 255),min(pcolor[2]*2, 255),0.5),
	pcolor = ink_add_for_rgb([
					colorline,
					(color[0],color[1],color[2],0.5)
					])
	return pcolor

def weapon(data,all, name):
	wdata= data["wdata"]
	aimd = data["aimd"]
	wdata["visible"] = True
	wdata["reloaded"] = False
	if data["character"] == 1:
		while (aimd == 1 and wdata["y"] > 75) or (aimd == 3 and wdata["y"] < 625) or (aimd == 2 and wdata["x"] > 75) or (aimd == 0 and wdata["x"] < 625):
			if aimd == 0: wdata["x"] += 100
			elif aimd == 1: wdata["y"] -= 100
			elif aimd == 2: wdata["x"] -= 100
			elif aimd == 3: wdata["y"] += 100
			if wdata["state"] == 1: wdata["state"] = 0
			else: wdata["state"] += 1
			kill(name, all)
			data["wdata"].update(wdata)
			time.sleep(0.25)
		wdata.update({"visible":False, "reloaded":True, "x":data["x"], "y":data["y"]})
	elif data["character"] == 2:	
		if aimd == 0 and data["x"] < 525: 
			wdata["state"] = 0
			wdata["y"] -= 100
			time.sleep(0.2)
			data["x"] += 200
			data["pcount"] += 2
		elif aimd == 1 and data["y"] > 175: 
			wdata["state"] = 1
			wdata["y"] -= 200
			wdata["x"] -= 100
			time.sleep(0.2)
			data["y"] -= 200
			data["pcount"] -= 14
		elif aimd == 2 and data["x"] > 175: 
			wdata["state"] = 2
			wdata["x"] -= 200
			wdata["y"] -= 100
			time.sleep(0.2)
			data["x"] -= 200
			data["pcount"] -= 2
		elif aimd == 3 and data["y"] < 525:
			wdata["state"] = 3
			wdata["x"] -= 100
			time.sleep(0.2)
			data["y"] += 200
			data["pcount"] += 14
		data["wdata"].update({"visible":False, "reloaded": False})
		time.sleep(0.5)
		wdata.update({"visible":False, "reloaded":True, "x":data["x"]+25, "y":data["y"]+25})
	data["wdata"].update(wdata)

def spawn(player):
	i = random.randint(0,3)
	player.update({"level":0, "color": (0,0,0)})
	if i == 0:player.update({"x":25, "y":25, "pcount":0})
	elif i == 1:player.update({"x":625, "y":625, "pcount":48})
	elif i == 2:player.update({"x":625, "y":25, "pcount":6})
	elif i == 3:player.update({"x":25, "y":625, "pcount":42})
	return player

def kill(name, list):
	if bool(int(koptions["enableKill"])):
		for target in list:
			if type(list[target]) == type(dict()) and target != "wdata":
				if list[name] != list[target]:
					if list[name]["x"] == list[target]["x"] and list[name]["y"] == list[target]["y"]:
						if (list[name]["level"] >= list[target]["level"]) or list[name]["character"] == 0: 
							list[name].update({"level":max(list[name]["level"]-list[target]["level"], 0)})
							list[target].update(spawn(list[target]))
							if list[name]["character"] == 0: print(f"{target} scared by {name}")
							else: print(f"{target} killed by {name}")
						elif (list[name]["level"] < list[target]["level"]) or list[target]["character"] == 0:
							list[target].update({"level":max(list[target]["level"]-list[name]["level"], 0)})
							list[name].update(spawn(list[name]))
							print(f"{name} UNO REVERSE CARDED by {target}")
					elif list[name]["wdata"]["x"] == list[target]["x"] and list[name]["wdata"]["y"] == list[target]["y"] and list[name]["wdata"]["visible"] and list[name]["character"] == 1:
						if list[name]["level"] >= list[target]["level"]:
							list[name].update({"level":max(list[name]["level"]-list[target]["level"], 0)})
							list[target].update(spawn(list[target]))
							print(f"{target} shooted by {name}")
						else:
							tl = list[target]["level"]
							list[target].update({"level": list[target]["level"]- list[name]["level"]})
							list[name].update({"level":list[name]["level"]-list[target]["level"]})
					'''elif list[name]["wdata"]["visible"] and list[name]["character"] == 2:
						if list[name]["aimd"] = 0:
							if list[name]["wdata"]["x"] - 25  == list[target]["x"] and list[name]["wdata"]["x"] == list[target]["x"]
						if list[name]["aimd"] = 1:
						if list[name]["aimd"] = 2:
						if list[name]["aimd"] = 3:
					'''	

def step_timer(t,name):
	global player_datas
	player_datas[name].update({"canStep":False})
	time.sleep(t)
	player_datas[name].update({"canStep":True})

def add_color(new, data):
	aimd = new["aimd"]
	key = new["key"]
	name = new["name"]
	d = data[name]
	ppleace = d["level"]
	pcount = d["pcount"]
	x = d["x"]
	y = d["y"]
	pc = d["p-c"]
	win = d["win"]
	#slotr = random.randint(0, 40)
	#if slotr == 1:
	#	slot[pcount] = (-1, -1, -1)
	#elif slotr == 2:
	#	slot[pcount] = (1000, 1000, 1000)
	#	print("ne má")
	#else:
	if key != "attack" and d["wdata"]["reloaded"]:	
		color = colors[random.randint(0, 5)]
		slot[pcount] = color
	if key == "w" and y > 75:
		pcount -= 7
		y -= 100
	elif key == "s" and y < 625:
		y += 100
		pcount += 7
	elif key == "a" and x > 75:
		x -= 100
		pcount -= 1
	elif key == "d" and x < 625:
		x += 100
		pcount += 1
	elif key == "attack":
		if d["character"] > 0 and d["wdata"]["reloaded"]: 
			d.update({"aimd":aimd})	
			threading.Thread(target=weapon, args=[d, data, name]).start()
	if d["wdata"]["reloaded"]:
		if d["character"] == 1: d["wdata"].update({"x":x, "y":y})
		elif d["character"] == 2: d["wdata"].update({"x":x+25, "y":y+25})
	color = slot[pcount]
	if key != "attack" and d["wdata"]["reloaded"] and (data[name]["x"] != x or data[name]["y"] != y): 
		pcolor = coloring(d)
		ppleace += 1
	else: pcolor = d["color"]
	d.update({"pcount":pcount,"x":x,"y":y})
	data[name].update(d)
	kill(name, data)
	red = pcolor[0]
	green = pcolor[1]
	blue = pcolor[2]
	if red == blue and red > green and green < 127.5 and red > 50 and blue > 50 and red < 255 and blue < 255:
		pc += 1
	if pc >= int(soptions["maxPCoin"]):
		d.update({"win":1,"p-c":pc,"level":ppleace, "color": pcolor})
		print(f"----------------------------\n\n\n\n\n{name.upper()} WON THIS ROUND!!!\n\n\n\n\n--------------------------------")
	d.update({"p-c":pc,"level":ppleace, "color": pcolor})
	return d

def main(h, client):
	global player_datas
	global addr
	global players
	global s
	while players >= 1:
		try:
			data = pickle.loads(client.recv(1024))
			found = 0
			#print(len(addr))
			if player_datas.get(h) != None:
				player_datas.pop(h)
				player_datas.update({data["name"]:{"win":0, "canStep":True,"character":data["character"],"p-c":0,"pcount":0,"color":(0,0,0), "level":0, "x":25, "y":25, "aimd":0,"wdata":{"visible":False, "x":25, "y":25, "state":0, "reloaded":True}}})
				if debug:print("I modifed!")
			if data.get("key") != None:
				if player_datas[data["name"]]["canStep"]: player_datas.update({data["name"]:add_color(data, player_datas)})
				threading.Thread(target=step_timer, args=[0.1, data["name"]]).start()
				if debug:print("Now the data is:"+str(player_datas))
		except ConnectionAbortedError:
			if debug:
				print("ERROR: CAE")
		except ConnectionResetError:
			if debug:
				print("ERROR: CRE")
		except EOFError:
			if debug:
				print("ERROR: No input!")
		except KeyboardInterrupt:
			s.close()
			print("bye!")
			players = 0

		try:
			client.send(pickle.dumps(player_datas))
		except ConnectionError:
			if players == 0:
				pass
			else:
				players -= 1
				player_datas.update({"players":players})
				player_datas[data["name"]].clear()
				player_datas.pop(data["name"])
				print("{} left the game.".format(data["name"]))
				return True
		except KeyboardInterrupt:
			s.close()
			print("bye!")
			players = 0

def accepting():
	global players
	global max_players
	global a
	global addr
	global s
	global close
	global player_datas
	while players < max_players:
		try:
			clientsocket, address = s.accept()
			print(f"A new player: {address} joined to the party")
			players += 1
			h = random.randint(0,30)+random.randint(0,30)
			player_datas.update({"players": players,h: {"win":0,"character":0,"canStep":True ,"p-c":0,"pcount":0, "color":(0,0,0), "level":0, "x":25, "y":25, "aimd":0,"wdata":{"visible":False, "x":25, "y":25, "state":0, "reloaded":True}}})
			threading.Thread(target = main, kwargs={"h":h, "client":clientsocket}).start()
			if players == max_players:
				print("The game is started!")
				i = 0
				try:
					for player in player_datas:
						if type(player_datas[player]) == type(dict()):
							player_datas.update(spawn(player_datas[player]))
							player_datas.update({"p-c": 0})
				except:
					pass
		except KeyboardInterrupt:
			s.close()
			print("bye!")

the_main = threading.Thread(target = accepting)
the_main.start()
#accepting()
#for client in a:
	#client.send(bytes(motd, "utf-8"))
	#client.send(bytes("Waiting to the players...", "utf-8"))
