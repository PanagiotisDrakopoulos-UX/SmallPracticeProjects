#Prime Factorization - 
#Have the user enter a number and find all Prime Factors (if there are any) and display them.

def prime_factorization():  
    x= int(input("Please enter a number: "))
    d=2
    mylimit =  x ** 0.5
    my_list = []
    while x<= 1:
        print("Error, the number must be bigger than 1 - TRY AGAIN!")
        x= int(input("Please enter a number: "))
    else:
        while d<= mylimit:
            while x % d == 0:
                x = x / d
                my_list.append(d)
            else:
                d += 1
                
    for i in my_list:
        print(i)

prime_factorization()