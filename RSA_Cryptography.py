from Help import *
import random
'''
Tyler Watson
Final Project
June 1st, 2018

Program to set up, encode, and decrypt messages using RSA cryptography
'''

def GetInteger():
    '''Function to call every time the user must enter an integer'''
    while True:
        num = input("Type in an integer: ")
        try:
            num = int(num) #Check if the number can be turned into an integer (int or float)
            return num #this will only run if the statement above does not result in an error
        except ValueError: #this will run if the user enters a letter or other symbol
            print("That is not an integer. Please try again.")


def PickPrimes():
    print("To help you choose two primes, give me a minimum of at least 2627 and maximum and I will display all primes in that range.")
    m = 0 #Initialize a minimum
    M = 0 #Initialize a maximum
    while True: #Run until a proper minimum has been chosen
        print("Let's start with the minimum (at least 2627).")
        m = GetInteger()
        if m >= 2627:
            while True: #Run until a proper maximum has been chosen
                print("Please give me a maximum.")
                M = GetInteger()
                if M > m and M > 2646 and len(ListPrime(m, M)) > 1: #Make sure that two primes are available in that range
                    break #if maximum works, move on
                else:
                    print("That maximum is too small. A proper list of primes of length greater than 2 cannot be generated Please try again.")
                    print()
        if M: #If the maximum has been approved, move on
                break
        print("That minimum is too small. Please try again.")
        print()
    P = ListPrime(m, M)
    print("Here's the list of primes in that range: ", P)
    print("Now we need two primes from that list.")
    while True: #loop until two primes in the list have been chosen
        print("Please pick a first prime from the list.")
        p = GetInteger()
        if p in P: #Verifies that p is a prime because it is in the list P
            print("Please pick a second prime from the list (cannot be the same as the first).")
            q = GetInteger()
            if p != q: #make sure primes are different
                if q in P: #make sure the prime is in the list
                    print("Those primes work!")
                    print()
                    break
                else: #If the second prime is not in the list
                    print("That is not in the list above. Let's try again.")
                    print()
            else: #if the primes are the same
                print("Those are the same primes! Let's try again. ")
                print()
        else: #if the first prime is not in the list
            print("That's not a prime in the list! Please pick again.")
            print()
    return (p, q)
    


def RandomPickPrimes():
    print("To help you choose two primes, give me a minimum of at least 2627 and maximum and I will randomly pick two primes from that range.")
    m = 0 #Initialize a minimum
    M = 0 #Initialize a maximum
    while True: #Run until a proper minimum has been chosen
        print("Let's start with the minimum (at least 2627).")
        m = GetInteger()
        if m >= 2627:
            while True: #Run until a proper maximum has been chosen
                print("Please give me a maximum.")
                M = GetInteger()
                if M > m and M > 2646 and len(ListPrime(m, M)) > 1: #Make sure that two primes are available in that range
                    break #if maximum works, move on
                else:
                    print("That maximum is too small. A proper list of primes of length greater than 2 cannot be generated Please try again.")
                    print()
        if M: #If the maximum has been approved, move on
                break
        print("That minimum is too small. Please try again.")
        print()
    primes = ListPrime(m, M)
    while True:
        p = primes[random.randint(0, len(primes)-1)]
        q = primes[random.randint(0, len(primes)-1)]
        if p != q: #make sure primes are different
            print("Two primes have been picked! They are:", p, "and", q)
            print()
            break
        
    return (p,q)
        
def SetUp():
    '''Function to initialize setting up RSA'''
    while True: #Loop until a proper option is inputed
        a = input('''Let's set up RSA. To do so, we need two prime numbers.
    Would you like to pick your own primes from a list or have me randomly pick from a list?
    1 - Pick your own primes from a range
    2 - Have me choose random primes from a range
    ''')
        print()
        if a == "1": #User wants to pick prims
            primes = PickPrimes()
            break
        elif a == "2": #User wants the computer to pick random primes
            primes = RandomPickPrimes()
            break
        print("That is not a valid entry. Please try again.")
        print()
    p = primes[0]
    q = primes[1]
    n = p*q #Compute n
    phi_n = (p-1)*(q-1) #Compute phi(n)
    
    while True: #Loop until proper power is selected
        print("Please pick a power.")
        e = GetInteger()
        if RelativelyPrime(e, phi_n): #make sure the inputed exponent is relatively prime to phi(n) for RSA to work properly
            break
        print("That is not relatively prime to phi of n", phi_n, ". Please try again.")
        print()
    d = Inverse(e, phi_n) #Compute inverse of e mod phi(n)
    return (n,e,d)

def GetLetter():
    '''Function to get one letter at a time from the user.'''
    while True:
        letter = input("Type in the letter or space you want to send or type 1 to end your message : ")
        if letter.isalpha() and len(letter) == 1: #Make sure the entered value is a single letter only
            return letter.upper()
        elif letter == ' ': #Check for entered space value
            return letter
        elif letter == '1': #Check for entered 1 to indicate end of message
            return letter
        print("The value you entered is not a single letter or space. Please try again.")
        print()
            

def GetMessage():
    '''Function to obtain message to encrypt.'''
    Message = [] #Initialize empty list
    a = GetLetter() #Start with the first letter
    while a != '1': #Loop until user enters '1' to end message
        Message.append(a)
        a = GetLetter()
    if len(Message)%2 == 1: #Once the user is done entering the message, ensure that the length of the message is an even number
        Message.append(' ')
    return Message

def LetterToNumber(Message):
    '''Function to transform list of letters into their numbers.'''
    MessageInNumber = []
    for letter in Message:
        MessageInNumber.append(Number[letter]) #Change each letter into its number based on the Number dictionary
    return MessageInNumber

def Encode(Message,n,e):
    '''Function to encrypt a message.'''
    InNumber = LetterToNumber(Message) #Use letter to number function
    Coded = []
    while len(InNumber) > 0: #loop until InNumber is empty
        x = InNumber.pop(0)
        y = InNumber.pop(0)
        NumberToEncrypt = 100*x + y #Compute the number to encrypt (two letters put together)
        Coded.append(pow(NumberToEncrypt, e, n)) #Add on the number^e mod n
    return Coded

def GetMessageNumber():
    '''Function to get the message the user wants to derypt.'''
    NumbersToDecrypt = []
    print("Please give me a message to decrypt. What is the first number of the encrypted message?")
    number = GetInteger() #start with the first number
    NumbersToDecrypt.append(number)
    while True:
        print("What is the next number? (Type '-1' to end the message) ")
        number = GetInteger() #Ensures that the entered value is an integer
        if number == -1: #Indicates that the user wants to end the message to decrypt
            return NumbersToDecrypt
        NumbersToDecrypt.append(number)
    return NumbersToDecrypt
    


def NumberToLetter(Message):
    '''Transforms a list of numbers into their respective letters'''
    letters = []
    for num in Message:
        letters.append(Letter[num]) #Changes each number into its letter based on the Letter dictionary
    return letters


def Decode(Message,n,d):
    '''Function to decrypt an encrypted message.'''
    decrypted = [] #Initialize a list to add each individual number onto 
    for number in Message:
        num = pow(number, d, n) #Use the private key to decrypt each number in the encrypted message
        y = num%100 #Reverse operation of going from a four digits number to two two-digit numbers
        x = (num - y)//100 #Obtain the first number
        decrypted.append(x)
        decrypted.append(y)
        if x > 27 or y > 27: #Make sure that the numbers actually correspond to letters
            return "Error! One or more of the numbers you entered is not a valid encrypted message."
    final_message = NumberToLetter(decrypted) #Run the function to turn each number into its respective letter to show the decrypted message
    return final_message
    

print('Welcome to the program! I am here to help you set up RSA cryptography, encrypt messages, and decrypt messages.')
    
n,e,d = SetUp() #Start the program

choice = "Not Chosen" #initialize a variable 
while choice != '6': #As long as the user does not press the key to leave
    choice = input('''
What would you like to do?
1 - Set up RSA again
2 - Encrypt a message
3 - Decrypt a message
4 - Print the public key (n,e)
5 - Print the private key
6 - Leave
''')
    if choice == '1':
        n,e,d = SetUp()
    elif choice == '2':
        print('The encrypted message is: ', Encode(GetMessage(),n,e))
    elif choice == '3':
        print('The decrypted message is: ', Decode(GetMessageNumber(),n,d))
    elif choice == '4':
        print("The public key is (n,e) = (", n,',', e, ')')
    elif choice == '5':
        print("The private key is d = ", d)
        
            
            
        
    
        
        
        
        

