import random
print("I will Guess a Number")
sum = random.randint(1,10)
a=int(input("Enter a number between 1 and 10: "))
if a == sum:
    print("You guessed it right!")
else:
    print("Oops! Try again.")

print(sum)