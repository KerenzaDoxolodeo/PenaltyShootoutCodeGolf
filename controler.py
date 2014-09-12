import subprocess
from threading import Timer
from sys import executable,argv,stdin
from random import randint

myFile=open("log.log","w")

def run(file,cmd): #This is the guy who gives YOUR program the STDIN. All kneel to him!
  proc = subprocess.Popen(file, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
  kill_proc = lambda p: p.kill()
  timer = Timer(1, kill_proc, [proc])
  timer.start()
  respond= proc.communicate(cmd)[0]
  timer.cancel()
  return respond.strip("\n")

def calculateDistance(shooter,keeper): #The distance?
    distance=((shooter[0]-keeper[0])**2+(shooter[1]-keeper[1])**2)**0.5
    return distance>=50 # Returns 1 if it's out of goal keeper's 50 cm reach.

def validAnswer(input):
    failedReturn=['350','100','350','100']
    if len(input)!=4:
        print input
        return failedReturn
    try:
        input =[int(i) for i in input]
    except valueError:
        print input
        return failedReturn
    return input

c=stdin.readline().strip("\n").split(" ")
path=[]
#Parsing File
for k in range (len(c)):
    if c[k].endswith(".py"):
        path.append([executable,c[k]])
    elif c[k].endswith(".exe"):
        path.append(c[k])
    else:
        print "Error: Illegal file : "+c[k]
        quit()

#Scoreboard

leaderboard=[int(0) for i in path]

# Now , please welcome the mechanism who runs the program!

# Note, the folowing program below maybe not readable at all =p

# Here's a bit of description what is happening
#
# It pairs two file, then it structing the command (by the variable)</code>cmd</cmd> then sent it through
# the function run. (Unfortunately 'compile error' is silenced by this function). Then pass the output the
# function valid answer. Had the program had give me bad input, it will be set to [350 100 350 100] and you'll be alerted.
# Then it calculates if it's a goal or not. Rinse and repeat 10 times.
# End game prematurely if it's impossible to at least tie.

for a in range(0,len(path)):
    for b in range(a+1,len(path)):
        myFile.write(c[a]+" "+c[b])
        digits=[a,b]
        score=[0,0]
        move=[[],[],[],[],[],[],[],[]]#Keeps list. X attack from P1, Y P1, X defend P1, soon]
        for round in range(1,11):
            answer=[[],[]]
            for x in range(2):
                word1=",".join(move[((x+1)%2)*4])
                word2=",".join(move[((x+1)%2*4)+1])
                word3=",".join(move[((x+1)%2*4)+2])
                word4=",".join(move[((x+1)%2*4)+3])
                cmd=str(round)+" "+word1+" "+word2+" "+word3+" "+word4
                if round==1:
                    responce=run(path[digits[x]],"1").split(" ")
                else:
                    responce=run(path[digits[x]],cmd).split(" ")
                answer[x]=validAnswer(responce)
            for x in range(2):
                xWind=randint(-50,50)# The wind
                yWind=randint(-50,50)
                xFinal=answer[x][0]+xWind #Ball final coordinate after the wind
                yFinal=answer[x][1]+yWind
                xKeeper=answer[(x+1)%2][2]
                yKeeper=answer[(x+1)%2][3]
                score[x]+=calculateDistance([xFinal,yFinal],[xKeeper,yKeeper])and 0<=xFinal<=700 and 0<=yFinal<=200
                move[(x*4)].append(answer[x][0])
                move[(x*4)+1].append(answer[x][1])
                move[((x+1)%2*4)+2].append(answer[(x+1)%2][2])
                move[((x+1)%2*4)+3].append(answer[(x+1)%2][3])
                myFile.write(c[digits[x]]+" "+" ".join([str(xFinal),str(yFinal),str(xKeeper),str(yKeeper)])+"\n")
            if abs(score[0]-score[1])>10-round:
                break
        if score[0]>score[1]:
            leaderboard[a]+=3
        elif score[1]>score[0]:
            leaderboard[b]+=3
        else:
            leaderboard[a]+=1
            leaderboard[b]+=1
        print score
"""
What hurts the most, that it's so close.....
"""
myLeaderBoardFile=open("standing.txt","w")
for k in range(len(c)):
    print c[k]+" "+str(leaderboard[k])
    myLeaderBoardFile.write(c[k]+" "+str(leaderboard[k])+"\n")
myFile.close()
