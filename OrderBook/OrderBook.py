import numpy as np
from matplotlib import pyplot as plt
import pandas
import csv

print "Loading data..."
orderBook = {} #This is a dictionary that will hold the orderbook
reader=csv.reader(open("GOOG.csv","rb"),delimiter=',') #Read in the messages. Notice that each field is loaded as a string
x=list(reader)
messages = np.array(x)
print "Complete."

#We will hold the spread high and low here in these variables
#We will update them as we process each line
spreadHigh = np.inf
spreadLow = -np.inf

u_means_remove = True #This variable keeps track of if the next "U" message is a removal or addition

def process(r):
    r[4] = r[4].strip()
    #Addition
    if r[1] == "A": #Add
        addition(r[6], r[5], r[4])

    elif r[1] == "C": #Execute with price
        #TODO: Implement?
        #The "C" message is only 35 messages of the >300,000 messages
        #It is complicated since it means an order was executed at not the original price
        #Since this is hard to implement and is insignificant, I think we should skip it.
        return

    #Deletion
    elif r[1] == "D": #Delete
        code = remove(r[6], r[5], r[4])
        if code == -1:
            print "D"

    elif r[1] == "E": #Execute
        code = remove(r[6], r[5], r[4])
        if code == -1:
            print "E"
    
    elif r[1] == "F": #Add with MPID
        addition(r[6], r[5], r[4])

    elif r[1] == "P": #Execute non-displayable trade
        remove(r[6], r[5], r[4])
        return
    
    elif r[1] == "U":
        global u_means_remove
        if u_means_remove == True:
            code = remove(r[6], r[5], r[4])
            if code == -1:
               print "U"
            u_means_remove = False
        else:
            addition(r[6], r[5], r[4])
            u_means_remove = True

    #Execute
    elif r[1] == "X": #Cancel
        code = remove(r[6], r[5], r[4])
        if code == -1:
            print "X"

#Process an addition
def addition(price, numShares, b_s):
    numShares = int(numShares) #numShares is a string, so we change it to an int
    '''
    if float(price) > 5000: #there are a few orders at $200,000 which are not relevant and mess up the graph, so we simply do not add these.
        return -1
    '''
    if price in orderBook:
        if b_s == "B" or b_s == " B":
            orderBook[price] = (orderBook[price][0] + numShares, "B")
        else:
            orderBook[price] = (orderBook[price][0] + numShares, "S")
    else:
        if b_s == "B" or b_s == " B":
            orderBook[price] = (numShares, "B")
        else:
            orderBook[price] = (numShares, "S")
    return 0
    #TODO
    #Code to update the spreadHigh and spreadLow
    '''
    if r[4] == "B":
        if r[6] > spreadLow:
            spreadLow == r[6]
    else:
        if r[6] < spreadHigh:
            spreadHigh == r[6]
    '''

def remove(price, numShares, b_s):
    #TODO: update spread variables
    numShares = int(numShares) #numShares is a string, so we change it to an int
    if price in orderBook:
        if orderBook[price][0] >= numShares:
            orderBook[price] = (orderBook[price][0] - numShares, b_s)
        else:
            #print str(numShares) + " shares are trying to be removed at price " + str(price) + " but only " + str(orderBook[price]) + " are on the book."
            return 3
        if orderBook[price][0] == 0: #If there are no shares under that price, delete the entry
            orderBook.pop(price, None)
            return 1
        return 0
    else: 
        #Sometimes the price is not in orderBook despite a request to remove
        #This is probably due to the fact that I'm not processing updates and other things
        #This code captures when that happens and displays a message so it's clear what happened
        #print "Tried to remove " + str(price) + " from orderBook, but the key does not exist"
        return -1

def plotOrderBook(oBook):
    BAR_SIZE = .01
    #print "Converting dictionary to array..."
    dictlist = []
    #Just iterate through all the keys in the dictionary and put them into a list
    for key, value in oBook.iteritems():
        temp = [float(key), float(value[0]), value[1]]
        dictlist.append(temp)
    dictlist = np.array(dictlist)
    print "Plotting..."

    buys = np.array([dictlist[i] for i in xrange(len(dictlist)) if (dictlist[i, 2] == "B") or (dictlist[i, 2] == " B")])
    sells = np.array([dictlist[i] for i in xrange(len(dictlist)) if dictlist[i, 2] == "S"])

    #What we might want to do here is use np.histogram() to clean this up
    #Right now the bars overlap and there is some ugliness
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.bar(buys[:, 0].astype(float), buys[:, 1].astype(float), width=BAR_SIZE, color="blue") #On the x axis we have the prices, y axis is number of shares
    ax.bar(sells[:, 0].astype(float), sells[:, 1].astype(float), width=BAR_SIZE, color="red") #On the x axis we have the prices, y axis is number of shares
    plt.xlim((557, 559))
    plt.ylim((0,500))
    plt.show()

def getSpread(oBook):
    buys = []
    sells = []

    #Just iterate through all the keys in the dictionary and put them into a list
    for key, value in oBook.iteritems():
        if value[1] == "B":
            buys.append(float(key))
        else:
            sells.append(float(key))

    maxBuy = np.max(buys)
    minSell = np.min(sells)
    return minSell-maxBuy

def volumeProcess(r):
    if r[1] == "C": #Execute with price
        return int(r[5])

    elif r[1] == "E": #Execute
        return int(r[5])

    elif r[1] == "P": #Execute non-displayable trade
        return int(r[5])
    else:
        return 0

#Plot the order book...
print "Building the order book..."
for row in messages[1:]:
    if float(row[2]) >= 37800: #37800 is 10:30
        print "It's 10:30!!!"
        break
    else:
        process(row)

print "Order book built."
plotOrderBook(orderBook)
print "Finished plotting the order book."


#Code to calculate the average spread
orderBook = {}
stop = 34200 #First stop is at 9:30AM, opening time
CLOSING_TIME = 57600 #4PM
AVERAGE_SPREAD_CALCULATION_INTERVAL = 1
print "Calculating average spread using steps of " + str(AVERAGE_SPREAD_CALCULATION_INTERVAL) + " seconds..."
spreads = []
extraSpreads = []
for row in messages[1:]:
    process(row)
    if float(row[2]) >= stop:
        spread = getSpread(orderBook)
        spreads.append([spread, float(row[2])])
        stop += AVERAGE_SPREAD_CALCULATION_INTERVAL
    if float(row[2]) >= CLOSING_TIME:
        spread = getSpread(orderBook)
        extraSpreads.append([spread, float(row[2])])
        stop += AVERAGE_SPREAD_CALCULATION_INTERVAL

spreads = np.array(spreads)
extraSpreads = np.array(extraSpreads)
average_spread = np.average(spreads[:, 0])
print "AVERAGE SPREAD =" + str(average_spread*100) + " cents"

spreads = np.vstack((spreads, extraSpreads))

#Code to calculate total volume traded
print "Calculating the volume of executed trades..."
orderBook = {}
totVolume = 0
for row in messages[1:]:
    totVolume += volumeProcess(row) #WHAT DOES THIS DO?????

print "TOTAL VOLUME OF EXECUTED TRADES: " + str(totVolume)

print "Calculating total profits by market makers..."
profits = 0

def getSpreadAtTime(t, spreads):
    i = 0
    while spreads[i, 1] < t:
        i += 1
    return spreads[i, 0]

for row in messages[1:]:
    if row[1] == "E" or row[1] == "C" or row[1] == "P":
        profits += (float(row[5])/2.) * getSpreadAtTime(float(row[2]), spreads)

print "TOTAL PROFITS BY MARKET MAKERS: " + str(profits)

'''
Calculating up and downticks to get V1 and V0
'''
date=[]
Open=[]
high=[]
low=[]
close=[]
volume = []

 
with open('google_historical_stock_data.csv','r') as csv_file:
    csv_reader=csv.reader(csv_file)
    for DATE, OPEN, HIGH, LOW, CLOSE, VOLUME in csv_reader:
        for line in csv_reader:
            date.append(line[0])
            Open.append(line[1])
            high.append(line[2])
            low.append(line[3])
            close.append(line[4])
            volume.append(line[5])
 
def destring(arrayin):
    a=len(arrayin)
    for i in xrange(a):
        arrayin[i]=float(arrayin[i])
 
    return arrayin
 
#destring(date)
destring(Open)
destring(high)
destring(low)
destring(close)
#destring(volume)
 
Open = np.asarray(Open)
high = np.asarray(high)
low = np.asarray(low)
close = np.asarray(close)
#volume = np.asarray(volume)
 
google_ret = (close[1:]-close[:-1])/close[:-1]
 
google_std_dev = np.std(google_ret)
annual_volatility = np.sqrt(252.)*google_std_dev
print "Annual google volatility", annual_volatility
 
up = np.exp(annual_volatility*np.sqrt(1/252.))
down = np.exp(-annual_volatility*np.sqrt(1/252.))
print "up", up 
print "down", down
V = Open[0]
V0 = Open[0]*down
V1 = Open[0]*up
 
 
print "V", V
print "V0",V0
print "V1", V1
 
prob_informed_trade = average_spread/(V1-V0)
print "Probability of informed trade", prob_informed_trade


