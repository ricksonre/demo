import csv
import time
from re import sub
from decimal import Decimal
import os

class Controller:

    """
    initializes:
       months: the a list of lists of all months with its purchases
       priceePerMonth: total amount spent on each month [month, year, amount]
       size: the total number of purchases
       numMonths: number of months
       totalPrice: total amount spent
    """ 
    def __init__(self):
        self.months = []
        self.pricePerMonth = []
        self.size  = 0
        self.numMonths = 0
        self.totalPrice = Decimal(0)

    #prints a purchase in the style: mm/dd/yyy, location, value
    def printPurchase(self, aux):
        print("{}, {}, {}".format(time.strftime("%m/%d/%Y", aux[0]),
                              aux[1], str(aux[2])))

    #calculates the amount spent on each month 
    # and adds then to the list pricePerMonth
    def calculatePricePerMonth(self):
        #loops through all months
        for month in self.months:
            #initializes the amount of the month as 0 
            aux = Decimal(0)
            for p in month:
                #increases the amount by each purchase
                aux +=p[2]
            #appends the into a list a list of [month, year, amount]
            self.pricePerMonth.append([p[0].tm_mon, p[0].tm_year, aux])
                
    #reads the the file of the given fileName
    def readFile(self, fileName):
        #list to read all purchases into
        auxList = []
       
        try:
            
            with open(fileName) as file:
                reader = csv.reader(file)
                for row in reader:
                    #saves the date as a struct_time
                    date = time.strptime(row[0], "%m/%d/%Y")
                    #saves the price as a decimal
                    value = Decimal(sub(r'[^\d\-.]', '', row[2]))
                    #increase the total price spent
                    self.totalPrice += value
                    #appends it in the temp list
                    auxList.append((date, row[1], value))
               
                #sorts the list based on the daate
                auxList.sort(key = lambda element: element[0])
                #sets the size of the total number of purchases
                self.size = len(auxList)
                
                #gets the number of the first month
                month = auxList[0][0].tm_mon
                begin = 0
                #add all purchases into the months list 
                # with each months having its own index
                for i in range(0,len(auxList)):
                    if (i == len(auxList)-1):
                        self.months.append(auxList[begin: i + 1])
                    elif(auxList[i + 1][0].tm_mon != month):
                        month = auxList[i+1][0].tm_mon
                        self.months.append(auxList[begin: i + 1])
                        begin = i + 1
                        #print("Month: {}  begin: {} i {} len {}\n e: {}\n\n\n\n".format(
                        #    auxList[i][0].tm_mon, begin, i, len(auxList), auxList[begin: i]))

                #set the total number of months
                self.numMonths = len(self.months)
                self.calculatePricePerMonth()

            return True
        except FileNotFoundError:
            print("File not found")
            return False
    
    """
    calculates the amount per location on the time period
    returns a hash map of it
    """
    def getLocationAmount(self, begin, end):
        map = dict()
        aux = self.months

        #returns if the range is outside the scope of the first and last purchase
        if(aux[0][0][0] > end or aux[self.numMonths-1][len(aux[self.numMonths-1])-1][0] < begin):
            return

        temp = self.binarySearch(begin)
        m = temp[0]
        d = temp[1]
        #loops up to the end of the range
        while(aux[m][d][0] <= end):
            purchase = aux[m][d]
            #increases the total if it has the purchase location as key
            # if not assines the value to the location
            if(purchase[1] in map):
                map[purchase[1]] +=purchase[2]
            else:
                map[purchase[1]] = purchase[2]

            if(d + 1 >= len(aux[m])):
                m += 1
                d = 0
            else:
                d += 1  

            if(m >= self.numMonths or d >= len(aux[m])):
                break
            
        return map

    #searches for the index of a date
    # or if not found the next index
    def binarySearch(self, element):
        mIndex = 0
        pIndex = 0

        low = 0
        high = self.numMonths - 1
        #binary search to find the index of the month
        while(low <= high):
            middle = int((high + low)/2)
            current = self.months[middle][0][0]
            #if the month or year is smaller
            if(current.tm_mon < element.tm_mon or current.tm_year < element.tm_year):
                low = middle + 1
            #if the month or year is bigger
            elif(current.tm_mon > element.tm_mon or current.tm_year > element.tm_year):
                high = middle - 1
            #they are the same
            else:
                mIndex = middle
                break
            mIndex = middle
            
        low = 0
        high = len(self.months[mIndex]) -1
        #binary search to find the first purchase of the day
        while(low <= high):
            middle = int((high + low)/2)
            #reference to the date th verify
            current = self.months[mIndex][middle][0]
            #if the current day is smaller
            if(current < element):
                low = middle + 1
            #if the current day is bigger
            elif(current > element):
                high = middle - 1
            #if the current day and the element day are the say
            else:
                #iterates up to the first purchase of the day
                while(self.months[mIndex][middle - 1][0] 
                    == self.months[mIndex][middle][0]):
                    middle -= 1
                pIndex = middle
                break
            pIndex = middle + 1
        #retuns the index of the month and day    
        return [mIndex,pIndex]

    #prints the purchases inside the range
    def printRange(self, begin, end):
        aux = self.months
        #out of range
        if(aux[0][0][0] > end or aux[self.numMonths-1][len(aux[self.numMonths-1])-1][0] < begin):
            return
        
        temp = self.binarySearch(begin)
        m = temp[0]
        d = temp[1]
        #print(" {} {}".format(m,d))
        while(aux[m][d][0] <= end):
            self.printPurchase(aux[m][d])
            if(d + 1 >= len(aux[m])):
                m += 1
                d = 0
            else:
                d += 1

            if(m >= self.numMonths or d >= len(aux[m])):
                break

