from flask import Flask, render_template, request
app = Flask(__name__)
from random import randint
import time

#Obtaining and interpreting ir sensor data
def get_position():
    data = []
    liftposition = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

    with open ("Sensordatas.txt", 'r') as f:
        for r in f.readlines():
            #data = r.strip("\x00\n").split(",")
            data = r.strip("\x00\n").split(",")

    with open ("Sensordatas.txt", 'w') as f:
        f.write("")
    print(data)
    for i in range(len(data)):
        liftposition[i//3 + 1][i%3] = int(data[i][1])
    

    if liftposition[3] == [1,1,0]: #presence of trolley in first row
        liftposition[3] = ["T", "O"]
    elif liftposition[3] == [0,1,1]: #presence of trolley in first row
        liftposition[3] = ["O","T"]
    
    for row in range(len(liftposition)):
        for i in range(len(liftposition[row])):
            if liftposition[row][i] == 1:
                if i == 2:
                    liftposition[row][i] = "PL"
                elif i == 1:
                    liftposition[row][i] = "PF"
                else:
                    liftposition[row][i] = "PR"
            elif liftposition[row][i] == 0:
                liftposition[row][i] = "O"
                
    return liftposition

#Initialize simulated level
currentlevel = 1

#Initialize lift1 level and direction
lift1capacity = 0
lift1position = [[1,1,1],[0,0,0],[0,0,0],[0,0,0]]
lift1current = 1
movingtimer = 0
waitingtimer = 0
lift1prev = "up" #up or down
lift1direction = "up" #up, down, 0

lift1image = ""
direction1image = ""

#Initialize lift2 level and direction
lift2capacity = 6
lift2position = [["O","PF","O"],["PR","PF","O"],["O","PF","PL"],["O","PF","O"]]
lift2current = 1
lift2direction = 0 #up, down, 0s
lift2prev = lift2current

lift2image = ""
direction2image = ""

from random import randint
@app.route("/")
def home():

	global currentlevel

	global lift1direction
	global lift1position
	global lift1prev
	global lift1current
	global lift1capacity
	global lift1image
	global direction1image
	global movingtimer
	global waitingtimer

	global lift2direction
	global lift2position
	global lift2current
	global lift2capacity
	global lift2image
	global direction2image
	global lift2prev



	
	
	#Manual lift 1
	lift1current = 3
	lift1direction = "down"

	lift1position = get_position() #Obtaining and interpreting ir sensor data from arduino
	#lift1position = [["O","O","O"],["T","PL"],["O","O","O"], ["O","O","O"]] #just for testing without ir sensor data
	lift1capacity = 12
	for row in lift1position:
		for entry in row:
			if entry == "O":
				lift1capacity -= 1
    
	#Manual lift 2
	
	#lift2current = 2
	#lift2direction = "down"
	#Auto lift 2 (people position and capacity)

	#Auto lift 2 (direction and level)
	if lift2direction == 0:
		waitingtimer += 1
		if waitingtimer == 1:
			possible = ["PL","PR","PF","O"]
			lift2capacity = 0
			for row in range(len(lift2position)):
				for spot in range(len(lift2position[row])):
					lift2position[row][spot] = possible[randint(0,3)]
					if lift2position[row][spot] in ["PL", "PR", "PF"]:
						lift2capacity += 1
		if waitingtimer > 20:#waits for 20 seconds then goes to next
			waitingtimer = 0
			if lift2current == 1:
				lift2direction = "up"
				lift2prev = lift2direction
			elif lift2current == 5:
				lift2direction = "down"
				lift2prev = lift2direction
			else:
				lift2direction = lift2prev

	else:
		movingtimer += 1
		if movingtimer > 5:
			movingtimer = 0
			if lift2direction == "up":
				lift2current += 1
			else:
				lift2current -= 1
			lift2direction = 0
	
	if currentlevel == lift1current and lift1direction == 0:
		lift1image = "./static/"+ str(lift1current) + "red.png"

	else:
		lift1image = "./static/"+ str(lift1current) + ".png"
	
	if currentlevel == lift2current and lift2direction == 0:
		lift2image = "./static/"+ str(lift2current) + "red.png"
	else:
		lift2image = "./static/"+ str(lift2current) + ".png"

	if lift1direction == "up":
		if lift1current == currentlevel-1:
			direction1image = "./static/upred.png"
		else:
			direction1image = "./static/up.png"

	elif lift1direction == "down":
		if lift1current == currentlevel+1:
			direction1image = "./static/downred.png"
		else:
			direction1image = "./static/down.png"
	
	else:
		if lift1current == currentlevel:
			direction1image = "./static/arrivered.png"
		else:
			direction1image = "./static/arrive.png"

	if lift2direction == "up":
		if lift2current == currentlevel-1:
			direction2image = "./static/upred.png"
		else:
			direction2image = "./static/up.png"

	elif lift2direction == "down":
		if lift2current == currentlevel+1:
			direction2image = "./static/downred.png"
		else:
			direction2image = "./static/down.png"
	
	else:
		if lift2current == currentlevel:
			direction2image = "./static/arrivered.png"
		else:
			direction2image = "./static/arrive.png"
	


	return render_template("display.html", currentlevel = currentlevel, direction1image = direction1image, lift1capacity = lift1capacity, lift1direction = lift1direction, lift1position = lift1position, lift1current = lift1current, lift1image = lift1image, lift2direction = lift2direction, lift2position = lift2position, lift2capacity = lift2capacity, lift2current = lift1current, lift2image = lift2image, direction2image = direction2image)



if __name__ == "__main__":
 	app.run()









