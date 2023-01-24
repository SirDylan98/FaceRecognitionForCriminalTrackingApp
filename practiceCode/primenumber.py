  
adder_lambda = lambda a, b: a + b
print(adder_lambda(5,9))
n="5fgdf"

print(str(n))
# print(primenumber)                
listnumber = [11,5,9,4,66,3,85,57,7,3]
primes=[]
# If given number is greater than 1
for num in listnumber:
	# Iterate from 2 to n / 2
	for i in range(2, int(num/2)+1):
		# If num is divisible by any number between
		# 2 and n / 2, it is not prime
		if (num % i) == 0:
			print(num, "is not a prime number")
			break
	else:
        
      
	    primes.append(num)
       
print(primes)