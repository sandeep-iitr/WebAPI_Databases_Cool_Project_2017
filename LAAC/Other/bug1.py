# prints the prime factorization of the user's number


#gets number from user
print ("Insert a number:")

num = int(input())
ori = num

#breaks down the number into its prime factorization in order
a = []
while(num > 1):
    for count in range(2, num+1):
        
        print(num, count)
        if(num % count == 0):
            a.append(count)
            num = int(num / count)
            
            if(count == ori):
                a.insert(0, 1)
    
a.sort()
print(a)

