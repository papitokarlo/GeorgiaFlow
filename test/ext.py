while True:
    k = input("Enter operation: ")
    if k=='fesvi':
        x = int(input("Enter x: "))
        if x>0:
            import math
            print(math.sqrt(x))
        else:
            print("error during opperation, input ")
    else:
        x = int(input("Enter x: "))
        y = int(input("Enter y: "))
        if k == "**" :        
            print(x ** y)
        elif k == "%":
            print(x / 100 * y)
        elif k == "+":
            print(x + y)
        elif k == "-":
            print(x - y)
        elif k == "*":
            print(x * y)
        elif k == "/":
            if y!=0:
                print(x / y)
            else:
                print("Zerro Devision Error")

    # elif k == "fesvi":
    #     if x>0:
    #         import math
    #         print(math.sqrt(x))
    #     else:
    #         print("error during opperation, input ")