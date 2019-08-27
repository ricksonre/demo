
#type dict separates the items into different types
#general list one with all info for total wtc...
#queries that divide the info into smaller lists
#   like getmay(list) 

#overall info
# year info
#month info


import time
from re import sub
from decimal import Decimal
import os


type = {
    "U OF BC - OKANA ": "restaurant",
        "BIGWHITE-F&B": "restaurant",
        "FATBURGER": "restaurant",
        "MI-NE SUSHI HOU": "restaurant",
        """PETER'S YIG STO""": "market",
        "FORTISBC1": "bill",
        "GRAND 10 CINEMA": "other",
        "U OF BC - OKANA": "restaurant",
        "TIM HORTONS #30": "restaurant",
        "REAL CDN SUPERS": "market",
        "MONEY MART": "other",
        "SAFEWAY": "market"
}

def get_type(aux):

    return aux

def clear():
    
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    return
    

def new_file():
    file = open("2019.csv","r") 
    #file = open(str(input("Open file: ")),"r") 

    list = []
    _ = file.read(3)
    
    for line in file:
        aux = line.split(",")
       
        t = time.strptime(aux[0],"%m/%d/%Y")
        v =  Decimal(sub(r'[^\d\-.]', '', aux[2]))

        list.append([t,aux[1],v,get_type(aux[1])])

    file.close()   

    return list

def menu():
    print(
"""
-------------------------------------
| Commands:                         |
|                                   |
|                                   |
|                                   |
|                                   |
|                                   |
|    0 - exit                       |
-------------------------------------
""")

    command = input("Enter a command: ")

    clear()

    return int(command)

def main():

    

    #list = new_file()


    #while(True):
        
        #command = menu()


        #if(command == 0):return


    return
    

if __name__ == "__main__":
    main()
