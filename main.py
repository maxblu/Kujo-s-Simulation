from src import Kujo
from colorama import Fore, Back, Style
import sys



if __name__ == "__main__":
    # simula_kujos()
    print("Welcome to Kujo's Kitchen simulator" )
    print("Please introduce the values of the times between clientes arrival for intervals, separated by white space:")
    print("If you press enter the defaults will be loaded")
    lamdas=input()
    print("How many days do you want to simulate:")
    print("If you press enter the defaults will be loaded")
    days=30
    try:
        days =int(input())
    except Exception as identifier:
        days=30
        
    
    params=[]
    default=False
    try:
        for x in lamdas.split(' '):
            params.append(int(x))
    
    except Exception as identifier:
        default=True
    
    lenth=len(params)
    if not default:
        try:
            lamdas1=params[0]
            lamdas2=params[1]
            lamdas3=params[2]
            lamdas4=params[3]
            lamdas5=params[4]
        
        except Exception  as identifier:
            print('Introduce the the five params')

        
        
        Kujo.simula_kujos(dias=days ,cooks=2,lambd1=lamdas1,lambd2=lamdas2,lambd3=lamdas3,lambd4=lamdas4,lambd5=lamdas5)
        Kujo.simula_kujos(dias=days, lambd1=lamdas1,lambd2=lamdas2,lambd3=lamdas3,lambd4=lamdas4,lambd5=lamdas5)
    else:
        Kujo.simula_kujos(dias=days,cooks=2)
        Kujo.simula_kujos(dias=days,cooks=3)
    # plt.plot(range(efi[0][0]),efi[0][1])
    Kujo.plt.show()