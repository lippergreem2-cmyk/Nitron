def generate_python(topic):

    topic = topic.lower().strip()

    programs = {

        "hello": '''
print("Hello from Nitron!")
''',

        "calculator": '''
print("Nitron Calculator")

a = float(input("First number: "))
b = float(input("Second number: "))

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)

if b != 0:
    print("Division:", a / b)
else:
    print("Cannot divide by zero")
''',

        "for loop": '''
for i in range(1,11):
    print(i)
''',

        "while loop": '''
count = 1

while count <= 10:
    print(count)
    count += 1
''',

        "if statement": '''
age = int(input("Age: "))

if age >= 18:
    print("Adult")
else:
    print("Minor")
''',

        "function": '''
def greet(name):
    print("Hello", name)

greet("Nitron")
''',

        "class": '''
class Student:

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def show(self):
        print(self.name)
        print(self.age)


student = Student("Nitron",20)

student.show()
''',

        "list": '''
numbers = [1,2,3,4,5]

for n in numbers:
    print(n)
''',

        "dictionary": '''
student = {
    "name":"Nitron",
    "age":20,
    "country":"Kenya"
}

print(student)
''',

        "guess game": '''
import random

number = random.randint(1,10)

while True:

    guess = int(input("Guess: "))

    if guess == number:
        print("Correct!")
        break

    elif guess < number:
        print("Too low")

    else:
        print("Too high")
''',

        "password generator": '''
import random
import string

chars = string.ascii_letters + string.digits + "!@#$%^&*"

password = ""

for i in range(16):
    password += random.choice(chars)

print(password)
''',

        "bank system": '''
balance = 1000

while True:

    print("""
1. Deposit
2. Withdraw
3. Balance
4. Exit
""")

    choice = input("> ")

    if choice == "1":

        amount = float(input("Amount: "))
        balance += amount

    elif choice == "2":

        amount = float(input("Amount: "))

        if amount <= balance:
            balance -= amount
        else:
            print("Insufficient funds")

    elif choice == "3":

        print("Balance:",balance)

    elif choice == "4":

        break
''',

        "student manager": '''
students=[]

while True:

    print("""
1. Add Student
2. Show Students
3. Exit
""")

    choice=input("> ")

    if choice=="1":

        name=input("Name: ")
        age=input("Age: ")

        students.append({
            "name":name,
            "age":age
        })


    elif choice=="2":

        for student in students:
            print(student)

    else:
        break
'''

    }


    if topic in programs:
        return programs[topic]


    return f"No code generator found for '{topic}'."
