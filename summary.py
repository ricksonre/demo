import csv;
import time
from re import sub
from decimal import Decimal
from controller import Controller
import matplotlib.pyplot as plt
import os

# receives a input and transforms it into a struc_time
# extra: used to fill the date if necessary
# returns the struct_time
def getTime(str, extra=""):
    t = ""
    #while the format is invalid and a exception is raised loop
    while True:
        t = input(str)
        try:
            t = extra + t
            t = time.strptime(t, "%d/%m/%Y")
            return t
        except:
            print("format not accepted try again.")

#gets the input of a range of time
#returns a list with the begin and the end
def getRange():
    begin = getTime(
        "Enter the start of the range in the format (dd/mm/yyyy): ")
    end = getTime(
        "Enter the end of the range in the format (dd/mm/yyyy): ")

    return [begin, end]

#list's the amount spent on each location
#with options to print all, a month, a range of time
def listLocations(cont):
    #prints the options
    print("""

        1 - list all
        2 - list range
        3 - list month
        4 - return

    """)
    command = input("Enter a command: ")
    #map to keep the locations as keys and the amount as the values
    map = dict()
    if(command == "1"):
        #uses the range from the first date in the list of purchases to the last one
        map = cont.getLocationAmount(cont.months[0][0][0],
                                     cont.months[cont.numMonths-1][len(cont.months[cont.numMonths-1])-1][0])
    elif(command == "2"):
        #asks fro input of a range of dates
        range = getRange()
        #asks for a map using the range gotten previously
        map = cont.getLocationAmount(range[0], range[1])
    elif(command == "3"):
        #asks for input of a month and year
        start = getTime("input the month in the format: mm/yyyy: ", "1/")
        #generates a new date on the end of the month of the start date
        end = time.strptime("{}/{}/{}"
                            .format(31, ("%02d" % start.tm_mon), start.tm_year), "%d/%m/%Y")
        map = cont.getLocationAmount(start, end)
    else:
        #if it received any other command return to the main menu
        return

    #sorts the maps based on the values
    map = sorted(map.items(), key=lambda e: e[1])
    print()
    for e in map:
        #prints all elements from the map
        print("{}: {}".format(e[0], e[1]))
    print()

#lists all purchases
# from the period of: all, a range of dates, a month, or the last month
def listPurchases(cont):
    #prints all options
    print("""

        1 - list all
        2 - list range
        3 - list month
        4 - list last month
        5 - return

    """)
    #asks for a input
    command = input("Enter a command: ")

    if(command == "1"):
        print()
        #loops through all purchases and prints them
        for month in cont.months:
            for p in month:
                cont.printPurchase(p)
        print()
    elif(command == "2"):
        range = getRange()
        print()
        #prints all purchases between the range included
        cont.printRange(range[0], range[1])
        print()
    elif(command == "3"):
        #asks for input of a month
        start = getTime("input the month in the format: mm/yyyy: ", "1/")
        #generates a new date on the end of the month of the start date
        end = time.strptime("{}/{}/{}"
                            .format(31, ("%02d" % start.tm_mon), start.tm_year), "%d/%m/%Y")
        print()
        #prints the range
        cont.printRange(start, end)
        print()
    elif(command == "4"):
        #gets a reference for the last month and prints it
        month = cont.months[cont.numMonths - 1]
        print()
        for p in month:
            cont.printPurchase(p)
        print()
    else:
        return

#clears the console
def clearConsole():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    #initializes the class that deal with the data
    cont = Controller()
    #asks for the input of a file to open
    fileName = input("Enter the file name: ")
    #loops until the file is found
    while(not cont.readFile(fileName)):
        fileName = input("try again: ")

    #main loop
    while True:
        #display options
        print("""

            1 - list purchases
            2 - list amount spent per location
            3 - total amount spent
            4 - list total amount spent per month
            5 - graph total amount spent per month
            6 - close

        """)
        #asks for a inut
        command = input("Enter a command: ")
        
        clearConsole()
        #quits
        if(command == "6"):
            break
        elif(command == "1"):
            #goes to a secondary menu
            listPurchases(cont)
        elif(command == "2"):
            #goes to a secondary menu
            listLocations(cont)
        elif(command == "3"):
            #prints the total amount
            print("Total amount: " + str(cont.totalPrice))
        elif(command == "4"):
            #loops through
            for e in cont.pricePerMonth:
                t = time.strptime("{}/{}".format(e[0], e[1]), "%m/%Y")
                print("{}: {}".format(time.strftime("%b, %Y", t), e[2]))
        elif(command == "5"):
            #initializes 2 empty lists
            dates = []
            values = []
            # loops throu the lists of prices spent on each month
            for e in cont.pricePerMonth:
                #transforms ints int struc_time string
                t = time.strptime("{}/{}".format(e[0], e[1]), "%m/%Y")
                #appends the the month into the list
                dates.append(time.strftime("%b, %Y", t))
                #appends the amount of the month into 
                values.append(e[2])
            #creates a plot with the 2 lists
            plt.plot(dates,values)
            plt.grid(color="#9c9996", linestyle="-", linewidth=1)
            plt.title("Time x Amount Spent")
            plt.xlabel("time")
            plt.ylabel("Amount Spent (cad)")
        
            plt.show()
        else:
            next

        #asks for input before returning to the main options
        input("press any key to return...")
        clearConsole()

#runs the main method if the file is run
if __name__ == "__main__":
    main()
