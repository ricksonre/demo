import csv;
import time
from re import sub
from decimal import Decimal
import os

class Controller:

    """
    initializes:
       months: the a list of lists of all months with its purchases
       size: the total number of purchases
       numMonths: number of months
    """ 
    def __init__(self):
        self.months = []
        self.pricePerMonth = []
        self.size  = 0
        self.numMonths = 0
        self.totalPrice = Decimal(0)

    def printPurchase(self, aux):
        print("{}, {}, {}".format(time.strftime("%m/%d/%Y", aux[0]),
                              aux[1], str(aux[2])))

    def calculatePricePerMonth(self):
        for month in self.months:
            aux = Decimal(0)
            for p in month:
                aux +=p[2]
            self.pricePerMonth.append(aux)
                

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
                    if(auxList[i][0].tm_mon != month):
                        self.months.append(auxList[begin: i])
                        month = auxList[i][0].tm_mon
                        begin = i+1
                        #print("Month: {}  begin: {}".format(
                        #    auxList[i][0].tm_mon, begin))

                #set the total number of months
                self.numMonths = len(self.months)
                self.calculatePricePerMonth()

            return True
        except FileNotFoundError:
            print("File not found")
            return False

    
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
            if(current.tm_mon < element.tm_mon or current.tm_year < element.tm_year):
                low = middle + 1
            elif(current.tm_mon > element.tm_mon or current.tm_year > element.tm_year):
                high = middle - 1
            else:
                mIndex = middle
                break
            mIndex = middle
            
        low = 0
        high = len(self.months[mIndex]) -1
        #binary search to find the first purchase of the day
        while(low <= high):
            middle = int((high + low)/2)
            current = self.months[mIndex][middle][0]
            if(current < element):
                low = middle + 1
            elif(current > element):
                high = middle - 1
            else:
                #iterates up to the first element of the day
                while(self.months[mIndex][middle - 1][0] 
                    == self.months[mIndex][middle][0]):
                    middle -= 1
                pIndex = middle
                break
            pIndex = middle + 1
            
        
        return [mIndex,pIndex]

    def printRange(self, begin, end):
        aux = self.months
        #out of range
        if(aux[0][0][0] > end or aux[self.numMonths-1][len(aux[self.numMonths-1])-1][0] < begin):
            return
        
        temp = self.binarySearch(begin)
        m = temp[0]
        d = temp[1]
        print(" {} {}".format(m,d))
        while(aux[m][d][0] <= end):
            self.printPurchase(aux[m][d])
            if(d + 1 >= len(aux[m])):
                m += 1
                d = 0
            else:
                d += 1

"""
    def printLastMonth(self):
        aux = self.months
        index  = self.binarySearch(time.struct_time(tm_mon = aux[self.size-1][0][1]))

        for i in range(index, self.size):
            self.printPurchase(aux[i])
   """     


def main():
    fileName = "C:/Users/ricksonre/Documents/GitHub/accounting/2019.csv"

    cont = Controller()
    while(not cont.readFile(fileName)):
        break
    
    print(cont.totalPrice)

    p = Decimal(0)
    for pp in cont.pricePerMonth:
        p+=pp
    print(p)
    #for i,month in enumerate(cont.months):
    #    print(i)
    #    for p in month:
    #        cont.printPurchase(p)

    #cont.printRange(time.strptime("03/01/2019", "%m/%d/%Y"),
    #           time.strptime("05/03/2019", "%m/%d/%Y"))

    #cont.printLastMonth()    

    


if __name__ == "__main__":
    main()
