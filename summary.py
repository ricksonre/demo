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
        self.size  = 0
        self.numMonths = 0

    def printPurchase(self, aux):
        print("{}, {}, {}".format(time.strftime("%m/%d/%Y", aux[0]),
                              aux[1], str(aux[2])))

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
                    #appends it in the temp list
                    auxList.append((date, row[1], value))
                
                #sorts the list based on the daate
                auxList.sort(key = lambda element: element[0])
                #sets the size of the total number of purchases
                self.size = len(auxList)

                #gets the number of the first month
                month = auxList[0][0].tm_mon
                index = 0
                #add all purchases into the months list 
                # with each months having its own index
                for e in auxList:
                    if(e[0].tm_mon != month): 
                        index +=1
                    self.months[index].append(e)
                #set the total number of months
                self.numMonths = len(self.months)
        except:
            print("File not found")

    
    #searches for the index of a date
    # or if not found the next index
    def binarySearch(self, element):
        
        mIndex = 0
        pIndex = 0

        low = 0
        high = self.numMonths - 1
        #binary search to find the index of the month
        while(low < high):
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
        while(low < high):
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
            pIndex = middle

        return (mIndex,pIndex)

    def printRange(self, begin, end):
        aux = self.months
        #out of range
        if(aux[0][0] > end or aux[self.size-1][0] < begin):
            return

        index = self.binarySearch(begin)
        while(aux[index][0] <= end):
            self.printPurchase(aux[index])
            index += 1
"""
    def printLastMonth(self):
        aux = self.months
        index  = self.binarySearch(time.struct_time(tm_mon = aux[self.size-1][0][1]))

        for i in range(index, self.size-1):
            self.printPurchase(aux[i])
   """     


def main():
    fileName = "2019.csv"

    cont = Controller()
    cont.readFile(fileName)

    print(cont.months)

    #cont.printRange(time.strptime("03/03/2019", "%m/%d/%Y"),
    #               time.strptime("05/03/2019", "%m/%d/%Y"))

    #cont.printLastMonth()    

    


if __name__ == "__main__":
    main()
