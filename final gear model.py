import simpy as s
import random


delayArray = []
delayMillingArray = []
delayDrillingArray = []
delayPaintArray = []
delayPolishArray = []


g1sIn = []
g1sOut = []
g2sIn = []
g2sOut = []
g3sIn = []
g3sOut = []


#G1 operations 
milling1=35
drilling1=20
painting1=55
polishing1=15
#G2 operations
milling2=25
painting2=35
polishing2=15 
#G3 operations 
drilling3=18
painting3=35
polishing3=15

#Locations
ad_to_mill=100 
ad_to_drill=100
mill_to_drill=300
mill_to_paint=400
mill_to_polish=150
paint_to_polish=300
drill_to_paint=150
drill_to_polish=400
paint_to_ad=250
polish_to_ad=250
polish_to_exit=200
exit_to_ad=550
exit_to_drill=500
exit_to_mill=300
exit_to_paint=400
exit_to_polish=200


systemTime=8*60
truckSpeed=100
minarrival=400
mxarrival=600

def getDisatance(gearLocation,gearDestination):
    distance=0
    if (gearLocation=="arrival" and gearDestination=="milling" )or(gearDestination=="arrival" and gearLocation=="milling"):
        distance=ad_to_mill
    elif(gearLocation=="arrival" and gearDestination=="drilling" )or(gearDestination=="arrival" and gearLocation=="drilling"):
        distance=ad_to_drill
    elif(gearLocation=="arrival" and gearDestination=="paint" )or(gearDestination=="arrival" and gearLocation=="paint"):
        distance=paint_to_ad
    elif(gearLocation=="arrival" and gearDestination=="polishing" )or(gearDestination=="arrival" and gearLocation=="polishing"):
        distance=polish_to_ad
    elif(gearLocation=="arrival" and gearDestination=="Exit" )or(gearDestination=="arrival" and gearLocation=="Exit"):
        distance=exit_to_ad 
    elif(gearLocation=="milling" and gearDestination=="drilling" )or(gearDestination=="milling" and gearLocation=="drilling"):
        distance=mill_to_drill
    elif(gearLocation=="milling" and gearDestination=="paint" )or(gearDestination=="milling" and gearLocation=="paint"):
        distance=mill_to_paint
    elif(gearLocation=="milling" and gearDestination=="polishing" )or(gearDestination=="milling" and gearLocation=="polishing"):
        distance=mill_to_polish
    elif(gearLocation=="milling" and gearDestination=="Exit" )or(gearDestination=="milling" and gearLocation=="Exit"):
        distance=exit_to_mill
    elif(gearLocation=="drilling" and gearDestination=="paint" )or(gearDestination=="drilling" and gearLocation=="paint"):
        distance=drill_to_paint
    elif(gearLocation=="drilling" and gearDestination=="Exit" )or(gearDestination=="drilling" and gearLocation=="Exit"):
        distance=exit_to_drill
    elif(gearLocation=="paint" and gearDestination=="polishing" )or(gearDestination=="paint" and gearLocation=="polishing"):
        distance=paint_to_polish
    elif(gearLocation=="paint" and gearDestination=="Exit" )or(gearDestination=="paint" and gearLocation=="Exit"):
        distance=exit_to_paint
    elif(gearLocation=="polishing" and gearDestination=="Exit" )or(gearDestination=="polishing" and gearLocation=="Exit"):
        distance=exit_to_polish 
    return distance


timeMill = 0
lastTimeMill = 0
interruptMill = False

timeDrill = 0
lastTimeDrill = 0
interruptDrill = False

timePaint = 0
lastTimePaint = 0
interruptPaint = False

timePolish = 0
lastTimePolish = 0
interruptPolish = False


def millCheckAfter(env,millstation):
    global timeMill
    global lastTimeMill
    global interruptMill

    if millstation.count == 0 and not interruptMill:
            interruptMill = True
            lastTimeMill = env.now
            print(env.now)


def millCheckBefore(env,millstation):
    global timeMill
    global lastTimeMill
    global interruptMill

    if millstation.count != 0 and interruptMill:
        interruptMill = False
        timeMill = timeMill + env.now - lastTimeMill
        lastTimeMill = env.now
    print(timeMill, env.now)
#----------------------------------------------------------------------------
def drillCheckAfter(env,drillstation):
    global timeDrill
    global lastTimeDrill
    global interruptDrill

    if drillstation.count == 0 and not interruptDrill:
            interruptDrill = True
            lastTimeDrill = env.now
            print(env.now)


def drillCheckBefore(env,drillstation):
    global timeDrill
    global lastTimeDrill
    global interruptDrill

    if drillstation.count != 0 and interruptDrill:
        interruptDrill = False
        timeDrill = timeDrill + env.now - lastTimeDrill
        lastTimeDrill = env.now
    print(timeDrill, env.now)
#----------------------------------------------------------------------------
def paintCheckAfter(env,paintstation):
    global timePaint
    global lastTimePaint
    global interruptPaint

    if paintstation.count == 0 and not interruptPaint:
            interruptPaint = True
            lastTimePaint = env.now
            print(env.now)


def paintCheckBefore(env,paintstation):
    global timePaint
    global lastTimePaint
    global interruptPaint

    if paintstation.count != 0 and interruptPaint:
        interruptPaint = False
        timePaint = timePaint + env.now - lastTimePaint
        lastTimePaint = env.now
    print(timePaint, env.now)
#----------------------------------------------------------------------------
def polishCheckAfter(env,polishstation):
    global timePolish
    global lastTimePolish
    global interruptPolish

    if polishstation.count == 0 and not interruptPolish:
            interruptPolish = True
            lastTimePolish = env.now
            print(env.now)


def polishCheckBefore(env,polishstation):
    global timePolish
    global lastTimePolish
    global interruptPolish

    if polishstation.count != 0 and interruptPolish:
        interruptPolish = False
        timePolish = timePolish + env.now - lastTimePolish
        lastTimePolish = env.now
    print(timeMill, env.now)



def getNextDestination(gearName,gearDestination,millstation,drillstation,paintstation,polishstation,arriving):
    if gearName.find("G1")!= -1:
        if gearDestination=="arrival":
            return "milling"
        elif gearDestination=="milling": 
            with millstation.request() as req:
                yield req
                millCheckBefore(env,millstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayMillingArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(milling1) 
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            millCheckAfter(env,millstation)
            return "drilling"
        elif gearDestination=="drilling":
            with drillstation.request() as req:
                yield req
                drillCheckBefore(env,drillstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayDrillingArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(drilling1)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            drillCheckAfter(env,drillstation)
            return "paint"  
        elif gearDestination=="paint":
            with paintstation.request() as req:
                yield req
                paintCheckBefore(env,paintstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPaintArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(painting1)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            paintCheckAfter(env,paintstation)
            return "polishing"
        elif gearDestination=="polishing":
            with polishstation.request() as req:
                yield req
                polishCheckBefore(env,polishstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPolishArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(polishing1)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            polishCheckAfter(env,polishstation)
            return "Exit"
    elif gearName.find("G2")!= -1:
        if gearDestination=="arrival":
            return "milling"
        elif gearDestination=="milling":
            with millstation.request() as req:
                yield req 
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayMillingArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(milling2)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            millCheckAfter(env,millstation)
            return "paint"
        elif gearDestination=="paint":
            with paintstation.request() as req:
                yield req
                paintCheckBefore(env,paintstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPaintArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(painting2)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            paintCheckAfter(env,paintstation)
            return "polishing"  
        elif gearDestination=="polishing":
            with polishstation.request() as req:
                yield req
                polishCheckBefore(env,polishstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPolishArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(polishing2)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            polishCheckAfter(env,polishstation)
            return "Exit"  
    elif gearName.find("G3")!= -1:
        if gearDestination=="arrival":
            return "drilling"
        elif gearDestination=="drilling":
            with drillstation.request() as req:
                yield req
                drillCheckBefore(env,drillstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayDrillingArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(drilling3)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            drillCheckAfter(env,drillstation)
            return "paint"
        elif gearDestination=="paint":
            with paintstation.request() as req:
                yield req
                paintCheckBefore(env,paintstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPaintArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(painting3)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            paintCheckAfter(env,paintstation)
            return "polishing"  
        elif gearDestination=="polishing":
            with polishstation.request() as req:
                yield req
                polishCheckBefore(env,polishstation)
                print(f"gear starts {gearDestination}  at {env.now} gear type {gearName}")
                delayPolishArray.append(env.now-arriving)
                delayArray.append("gear " + gearName + " waits in " + str(gearDestination) + " to enter for" + str(env.now-arriving))
                print(f"gear waits in {gearDestination} to enter for",env.now-arriving)
                yield env.timeout(polishing3)
                print(f"gear finishes {gearDestination}  at {env.now} gear type {gearName}")
            polishCheckAfter(env,polishstation)
            return "Exit"               

truck1LastPlace = "arrival"
truck2LastPlace = "arrival"

def temp(req2):
    yield req2

def fillTruck(env,gearName,gearLocation,gearDestination,truck1,truck2,millstation,drillstation,paintstation,polishstation):
    if gearLocation=="Exit":
        if gearName.find("G1")!= -1:
            g1sOut.append(env.now)
        elif gearName.find("G2")!= -1:
            g2sOut.append(env.now)
        elif gearName.find("G3")!= -1:
            g3sOut.append(env.now)
        return
    distance=getDisatance(gearLocation,gearDestination)
    #calculate time
    time=distance/truckSpeed
    print(f"gear waits truck to move from {gearLocation} to {gearDestination} at {env.now} gear type {gearName}")
    arriving = -1
    with truck1.request() as req1, truck2.request() as req2:
        result = yield req1 | req2
        if req1 in result:
            truck2.release(req2)
            global truck1LastPlace
            truckDistance=getDisatance(truck1LastPlace,gearLocation)
            truckTime=truckDistance/truckSpeed
            print(f"Truck1 moving from {truck1LastPlace} to {gearLocation}")
            yield env.timeout(truckTime)
            truck1LastPlace = gearDestination
            print(f"Truck1 starts move from {gearLocation} to {gearDestination} at {env.now} gear type {gearName}")
            yield env.timeout(time)
            print(f"gear arriving {gearDestination} by Truck1 at {env.now} gear type {gearName}")
            truck1.release(req1)
        else:
            truck1.release(req1)
            global truck2LastPlace
            truckDistance=getDisatance(truck2LastPlace,gearLocation)
            truckTime=truckDistance/truckSpeed
            print(f"Truck2 moving from {truck1LastPlace} to {gearLocation}")
            yield env.timeout(truckTime)
            truck2LastPlace = gearDestination
            print(f"Truck2 starts move from {gearLocation} to {gearDestination} at {env.now} gear type {gearName}")
            yield env.timeout(time)
            print(f"gear arriving {gearDestination} by Truck2 at {env.now} gear type {gearName}")
            truck2.release(req2)
        arriving = env.now


    nextDestination= yield env.process (getNextDestination(gearName,gearDestination,millstation,drillstation,paintstation,polishstation,arriving))             
    
        
    yield env.process(fillTruck(env,gearName,gearDestination,nextDestination,truck1,truck2,millstation,drillstation,paintstation,polishstation))


def arrivingBatches(env,truck1,truck2,millstation,drillstation,paintstation,polishstation):
    counter=0
    pdf = [0.5, 0.3, 0.2]
    cdf = []
    cumulative = 0
    for i in range(len(pdf)):
        cumulative = cumulative + pdf[i]
        cdf.append(cumulative)
    while True:
        counter=counter+1                            
        batch=10
        print(f"Batch arriving at {env.now}")
        for i in range (batch):
            randomeGearNumber = random.uniform(0,1)
            gearType = "none"
            for j in range(len(cdf)):
                if randomeGearNumber <= cdf[j]:
                    gearType = "G"+str(j+1)
                    break
            if gearType == "G1":
                g1sIn.append(env.now)
                env.process(fillTruck(env, "Batch %d  Gear type G1 %d" %(counter,i),"arrival" , "milling",truck1,truck2,millstation,drillstation,paintstation,polishstation))
            elif gearType == "G2":
                g2sIn.append(env.now)
                env.process(fillTruck(env, "Batch %d  Gear type G2 %d" %(counter,i),"arrival" , "milling",truck1,truck2,millstation,drillstation,paintstation,polishstation))
            elif gearType == "G3":
                g3sIn.append(env.now)
                env.process(fillTruck(env, "Batch %d  Gear type G3 %d" %(counter,i),"arrival" , "drilling",truck1,truck2,millstation,drillstation,paintstation,polishstation))
        interarrival=random.uniform(minarrival,mxarrival)
        yield env.timeout(interarrival)

        
        
env=s.Environment()
millstation =s.Resource(env, capacity=4)
drillstation =s.Resource(env, capacity=3)
paintstation =s.Resource(env, capacity=2)
polishstation =s.Resource(env, capacity=1)
truck1 =s.Resource(env, capacity=1)
truck2 =s.Resource(env, capacity=1)
env.process(arrivingBatches(env,truck1,truck2,millstation,drillstation,paintstation,polishstation))


env.run(until=systemTime)

millCheckAfter(env,millstation)
drillCheckAfter(env,drillstation)
paintCheckAfter(env,paintstation)
polishCheckAfter(env,polishstation)


systemTimeG1 = 0
systemTimeG2 = 0
systemTimeG3 = 0
for i in range(len(g1sOut)):
    systemTimeG1 = systemTimeG1 + (g1sOut[i] - g1sIn[i])
for i in range(len(g2sOut)):
    systemTimeG2 = systemTimeG2 + (g2sOut[i] - g2sIn[i])
for i in range(len(g3sOut)):
    systemTimeG3 = systemTimeG3 + (g3sOut[i] - g3sIn[i])

print("average system time for G1 is:", systemTimeG1/len(g1sOut))
print("average system time for G2 is:", systemTimeG2/len(g2sOut))
print("average system time for G3 is:", systemTimeG3/len(g3sOut))


print("utilizations for milling is", (systemTime - timeMill)/systemTime)
print("utilizations for drilling is", (systemTime - timeDrill)/systemTime)
print("utilizations for paint is", (systemTime - timePaint)/systemTime)
print("utilizations for polish is", (systemTime - timePolish)/systemTime)


print()
print()
print()

for i in range(len(delayArray)):
    print(delayArray[i])

print()
print()

print("The avarge time for Milling is ", (sum(delayMillingArray)/len(delayMillingArray)))
print("The avarge time for Drilling is ", (sum(delayDrillingArray)/len(delayDrillingArray)))
print("The avarge time for delayPaintArray is ", (sum(delayPaintArray)/len(delayPaintArray)))
print("The avarge time for Polish is ", (sum(delayPolishArray)/len(delayPolishArray)))
