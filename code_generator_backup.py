def generate_python(topic):

    topic = topic.lower().strip()

    programs = {

        "hello": '''
print("Hello from Nitron!")
''',

        "calculator": '''
print("Simple Calculator")

a = float(input("First Number: "))
b = float(input("Second Number: "))

print("Addition =", a + b)
print("Subtraction =", a - b)
print("Multiplication =", a * b)

if b != 0:
    print("Division =", a / b)
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

    def __init__(self, name, age):
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

for number in numbers:
    print(number)
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

secret = random.randint(1,10)

while True:

    guess = int(input("Guess: "))

    if guess == secret:
        print("Correct")
        break

    elif guess < secret:
        print("Too Low")

    else:
        print("Too High")
''',

        "password generator": '''
import random
import string

characters = string.ascii_letters + string.digits + "!@#$%^&*"

password = ""

for i in range(16):
    password += random.choice(characters)

print(password)
''',

        "prime numbers": '''
for num in range(2,101):

    prime = True

    for i in range(2,num):

        if num % i == 0:
            prime = False
            break

    if prime:
        print(num)
''',

        "fibonacci": '''
a = 0
b = 1

for i in range(20):

    print(a)

    a,b = b,a+b
''',

        "factorial": '''
number = int(input("Number: "))

result = 1

for i in range(1,number+1):
    result *= i

print(result)
''',

        "file": '''
with open("notes.txt","w") as file:

    file.write("Hello Nitron")

with open("notes.txt") as file:

    print(file.read())
'''
    }

    if topic in programs:
        return programs[topic]

    return f"No code generator found for '{topic}'."        "bank system": '''
balance = 1000

while True:

    print("1. Deposit")
    print("2. Withdraw")
    print("3. Balance")
    print("4. Exit")

    choice = input("Choice: ")

    if choice == "1":
        amount = float(input("Deposit: "))
        balance += amount

    elif choice == "2":
        amount = float(input("Withdraw: "))

        if amount <= balance:
            balance -= amount
        else:
            print("Insufficient funds")

    elif choice == "3":
        print("Balance =", balance)

    elif choice == "4":
        break
''',

        "student manager": '''
students = []

while True:

    print("1.Add")
    print("2.Show")
    print("3.Exit")

    choice = input("> ")

    if choice == "1":

        name = input("Name: ")

        age = input("Age: ")

        students.append({"name":name,"age":age})

    elif choice == "2":

        for s in students:

            print(s)

    else:

        break
''',

        "todo": '''
tasks=[]

while True:

    print("1.Add")
    print("2.Show")
    print("3.Exit")

    c=input("> ")

    if c=="1":

        tasks.append(input("Task: "))

    elif c=="2":

        for i,t in enumerate(tasks):

            print(i+1,t)

    else:

        break
''',

        "temperature converter": '''
temp=float(input("Temperature: "))

print("1.Celsius to Fahrenheit")
print("2.Fahrenheit to Celsius")

choice=input("> ")

if choice=="1":

    print((temp*9/5)+32)

else:

    print((temp-32)*5/9)
''',

        "bmi": '''
weight=float(input("Weight kg: "))

height=float(input("Height m: "))

bmi=weight/(height*height)

print("BMI =",bmi)
''',

        "multiplication table": '''
number=int(input("Number: "))

for i in range(1,13):

    print(number,"x",i,"=",number*i)
''',

        "countdown": '''
import time

seconds=10

while seconds>0:

    print(seconds)

    time.sleep(1)

    seconds-=1

print("Finished")
''',

        "dice": '''
import random

print(random.randint(1,6))
''',

        "coin flip": '''
import random

print(random.choice(["Heads","Tails"]))
''',

        "random password": '''
import random
import string

chars=string.ascii_letters+string.digits+"!@#$%^&*"

password=""

for i in range(20):

    password+=random.choice(chars)

print(password)
''',        "contact book": '''
contacts = {}

while True:

    print("1. Add Contact")
    print("2. Show Contacts")
    print("3. Search")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":

        name = input("Name: ")
        phone = input("Phone: ")

        contacts[name] = phone

    elif choice == "2":

        for name, phone in contacts.items():

            print(name, "-", phone)

    elif choice == "3":

        name = input("Search: ")

        print(contacts.get(name, "Not Found"))

    else:

        break
''',

        "quiz": '''
score = 0

answer = input("Capital of Kenya? ")

if answer.lower() == "nairobi":
    score += 1

answer = input("5 + 5 = ")

if answer == "10":
    score += 1

print("Score:", score)
''',

        "rock paper scissors": '''
import random

choices = ["rock", "paper", "scissors"]

computer = random.choice(choices)

player = input("Choose rock, paper or scissors: ").lower()

print("Computer:", computer)

if player == computer:

    print("Draw")

elif (player == "rock" and computer == "scissors") or \\
     (player == "paper" and computer == "rock") or \\
     (player == "scissors" and computer == "paper"):

    print("You Win!")

else:

    print("You Lose!")
''',

        "number statistics": '''
numbers = []

while True:

    value = input("Enter number (or q): ")

    if value == "q":
        break

    numbers.append(float(value))

print("Count:", len(numbers))
print("Maximum:", max(numbers))
print("Minimum:", min(numbers))
print("Average:", sum(numbers)/len(numbers))
''',

        "alarm": '''
import time

seconds = int(input("Seconds: "))

print("Waiting...")

time.sleep(seconds)

print("Time is up!")
''',

        "stopwatch": '''
import time

input("Press Enter to start")

start = time.time()

input("Press Enter to stop")

end = time.time()

print("Elapsed:", end - start, "seconds")
''',        "expense tracker": '''
expenses = []

while True:

    print("1. Add Expense")
    print("2. Show Expenses")
    print("3. Total")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":

        name = input("Expense: ")
        amount = float(input("Amount: "))

        expenses.append((name, amount))

    elif choice == "2":

        for item in expenses:

            print(item[0], "-", item[1])

    elif choice == "3":

        total = sum(amount for name, amount in expenses)

        print("Total =", total)

    else:

        break
''',

        "library": '''
books = []

while True:

    print("1. Add Book")
    print("2. Show Books")
    print("3. Exit")

    choice = input("> ")

    if choice == "1":

        books.append(input("Book Name: "))

    elif choice == "2":

        for book in books:

            print(book)

    else:

        break
''',

        "inventory": '''
inventory = {}

while True:

    print("1. Add Item")
    print("2. Show Inventory")
    print("3. Exit")

    choice = input("> ")

    if choice == "1":

        item = input("Item: ")
        quantity = int(input("Quantity: "))

        inventory[item] = quantity

    elif choice == "2":

        for item, quantity in inventory.items():

            print(item, quantity)

    else:

        break
''',

        "login": '''
username = "admin"

password = "1234"

user = input("Username: ")

pwd = input("Password: ")

if user == username and pwd == password:

    print("Login Successful")

else:

    print("Access Denied")
''',

        "file organizer": '''
import os

folder = input("Folder Path: ")

for filename in os.listdir(folder):

    print(filename)
''',

        "text editor": '''
filename = input("File Name: ")

text = input("Write Text: ")

with open(filename, "w") as file:

    file.write(text)

print("Saved Successfully")
''',        "tic tac toe": '''
board = [" "]*9

def show():

    print(board[0],"|",board[1],"|",board[2])
    print("--+---+--")
    print(board[3],"|",board[4],"|",board[5])
    print("--+---+--")
    print(board[6],"|",board[7],"|",board[8])

player = "X"

while " " in board:

    show()

    move = int(input("Position (0-8): "))

    if board[move] == " ":

        board[move] = player

        if player == "X":
            player = "O"
        else:
            player = "X"

show()
''',

        "hangman": '''
word = "python"

hidden = ["_"] * len(word)

attempts = 6

while attempts > 0 and "_" in hidden:

    print("".join(hidden))

    letter = input("Letter: ")

    if letter in word:

        for i,c in enumerate(word):

            if c == letter:

                hidden[i] = letter

    else:

        attempts -= 1

print("Word:", word)
''',

        "calendar": '''
import calendar

year = int(input("Year: "))

month = int(input("Month: "))

print(calendar.month(year, month))
''',

        "clock": '''
from datetime import datetime

while True:

    print(datetime.now().strftime("%H:%M:%S"))
''',

        "email validator": '''
email = input("Email: ")

if "@" in email and "." in email:

    print("Valid Email")

else:

    print("Invalid Email")
''',

        "url opener": '''
import webbrowser

url = input("Website: ")

webbrowser.open(url)
''',

        "json reader": '''
import json

with open("data.json") as file:

    data = json.load(file)

print(data)
''',

        "json writer": '''
import json

data = {

    "name":"Nitron",

    "version":"1.0"

}

with open("data.json","w") as file:

    json.dump(data,file,indent=4)

print("Saved")
''',        "sqlite database": '''
import sqlite3

conn = sqlite3.connect("nitron.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
""")

cursor.execute(
    "INSERT INTO users(name, age) VALUES(?, ?)",
    ("Nitron", 20)
)

conn.commit()

for row in cursor.execute("SELECT * FROM users"):
    print(row)

conn.close()
''',

        "web scraper": '''
import requests
from bs4 import BeautifulSoup

url = input("URL: ")

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)
''',

        "weather api": '''
import requests

city = input("City: ")

print("Replace YOUR_API_KEY with your weather API key.")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"

response = requests.get(url)

print(response.json())
''',

        "system information": '''
import platform

print("System:", platform.system())
print("Release:", platform.release())
print("Machine:", platform.machine())
print("Processor:", platform.processor())
''',

        "file copier": '''
source = input("Source file: ")
destination = input("Destination file: ")

with open(source, "rb") as src:

    data = src.read()

with open(destination, "wb") as dst:

    dst.write(data)

print("File copied.")
''',

        "directory viewer": '''
import os

path = input("Folder: ")

for item in os.listdir(path):

    print(item)
''',

        "word counter": '''
text = input("Enter text: ")

words = text.split()

print("Words:", len(words))
''',

        "number guess ai": '''
import random

secret = random.randint(1,100)

attempts = 0

while True:

    guess = int(input("Guess: "))

    attempts += 1

    if guess == secret:

        print("Correct!")

        print("Attempts:", attempts)

        break

    elif guess < secret:

        print("Too low")

    else:

        print("Too high")
''',        "chatbot": '''
print("Nitron Chatbot")

while True:

    message = input("You: ").lower()

    if message == "hello":
        print("Nitron: Hello!")

    elif message == "how are you":
        print("Nitron: I am running perfectly.")

    elif message == "bye":
        print("Nitron: Goodbye!")
        break

    else:
        print("Nitron: I don't understand yet.")
''',

        "markdown viewer": '''
filename = input("Markdown file: ")

with open(filename,"r") as file:

    print(file.read())
''',

        "simple logger": '''
from datetime import datetime

message = input("Log message: ")

with open("log.txt","a") as file:

    file.write(
        f"[{datetime.now()}] {message}\\n"
    )

print("Saved")
''',

        "text encryptor": '''
text = input("Text: ")

shift = 3

encrypted = ""

for ch in text:

    encrypted += chr(ord(ch)+shift)

print(encrypted)
''',

        "text decryptor": '''
text = input("Encrypted Text: ")

shift = 3

decrypted = ""

for ch in text:

    decrypted += chr(ord(ch)-shift)

print(decrypted)
''',

        "unit converter": '''
value = float(input("Meters: "))

print("Centimeters =", value*100)

print("Kilometers =", value/1000)

print("Millimeters =", value*1000)
''',

        "age calculator": '''
from datetime import date

birth = int(input("Birth Year: "))

current = date.today().year

print("Age =", current-birth)
''',

        "palindrome": '''
text = input("Text: ")

if text == text[::-1]:

    print("Palindrome")

else:

    print("Not Palindrome")
''',

        "vowel counter": '''
text = input("Text: ").lower()

count = 0

for letter in text:

    if letter in "aeiou":

        count += 1

print("Vowels =", count)
''',

        "simple calculator gui": '''
import tkinter as tk

window = tk.Tk()

window.title("Calculator")

label = tk.Label(window,text="Nitron Calculator")

label.pack()

window.mainloop()
''',        "attendance system": '''
students = {}

while True:

    print("1. Mark Present")
    print("2. View Attendance")
    print("3. Exit")

    choice = input("> ")

    if choice == "1":

        name = input("Student Name: ")

        students[name] = "Present"

    elif choice == "2":

        for name, status in students.items():

            print(name, "-", status)

    else:

        break
''',

        "shopping list": '''
shopping = []

while True:

    item = input("Item (or exit): ")

    if item.lower() == "exit":

        break

    shopping.append(item)

print()

print("Shopping List")

for item in shopping:

    print("-", item)
''',

        "notes app": '''
while True:

    note = input("Write Note (exit to stop): ")

    if note.lower() == "exit":

        break

    with open("notes.txt","a") as file:

        file.write(note + "\\n")

print("Notes Saved")
''',

        "timer": '''
import time

seconds = int(input("Seconds: "))

while seconds > 0:

    print(seconds)

    time.sleep(1)

    seconds -= 1

print("Done")
''',

        "multiplication quiz": '''
import random

score = 0

for i in range(5):

    a = random.randint(1,10)

    b = random.randint(1,10)

    answer = int(input(f"{a} x {b} = "))

    if answer == a*b:

        print("Correct")

        score += 1

    else:

        print("Wrong")

print("Score =", score)
''',

        "random quote": '''
import random

quotes = [

    "Keep learning.",

    "Practice every day.",

    "Small progress is still progress.",

    "Never stop building."

]

print(random.choice(quotes))
''',

        "simple menu": '''
while True:

    print("1. Hello")

    print("2. Time")

    print("3. Exit")

    choice = input("> ")

    if choice == "1":

        print("Hello!")

    elif choice == "2":

        from datetime import datetime

        print(datetime.now())

    else:

        break
''',        "phone book": '''
contacts = {}

while True:

    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Show Contacts")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":

        name = input("Name: ")
        phone = input("Phone: ")

        contacts[name] = phone

    elif choice == "2":

        name = input("Search: ")

        print(contacts.get(name, "Not Found"))

    elif choice == "3":

        for name, phone in contacts.items():

            print(name, "-", phone)

    else:

        break
''',

        "grade calculator": '''
marks = []

for i in range(5):

    marks.append(float(input("Mark: ")))

average = sum(marks)/len(marks)

print("Average =", average)

if average >= 80:

    print("Grade A")

elif average >= 70:

    print("Grade B")

elif average >= 60:

    print("Grade C")

elif average >= 50:

    print("Grade D")

else:

    print("Grade F")
''',

        "currency converter": '''
rate = 129.50

usd = float(input("USD: "))

print("KES =", usd * rate)
''',

        "count words": '''
sentence = input("Sentence: ")

words = sentence.split()

print("Total Words =", len(words))
''',

        "reverse text": '''
text = input("Text: ")

print(text[::-1])
''',

        "even odd": '''
number = int(input("Number: "))

if number % 2 == 0:

    print("Even")

else:

    print("Odd")
''',

        "simple ai": '''
while True:

    message = input("You: ").lower()

    if message == "hello":

        print("Nitron: Hello Boss.")

    elif message == "time":

        from datetime import datetime

        print(datetime.now().strftime("%H:%M:%S"))

    elif message == "bye":

        print("Nitron: Goodbye.")

        break

    else:

        print("Nitron: I'm still learning.")
''',

        "mini database": '''
database = []

while True:

    print("1. Add")
    print("2. Show")
    print("3. Exit")

    choice = input("> ")

    if choice == "1":

        database.append(input("Record: "))

    elif choice == "2":

        for record in database:

            print(record)

    else:

        break
''',        "matrix addition": '''
rows = 2
cols = 2

A = [[1,2],[3,4]]
B = [[5,6],[7,8]]

C = [[0,0],[0,0]]

for i in range(rows):

    for j in range(cols):

        C[i][j] = A[i][j] + B[i][j]

for row in C:

    print(row)
''',

        "binary search": '''
numbers = [2,4,6,8,10,12,14,16]

target = int(input("Number: "))

low = 0
high = len(numbers)-1

while low <= high:

    mid = (low+high)//2

    if numbers[mid] == target:

        print("Found")

        break

    elif numbers[mid] < target:

        low = mid+1

    else:

        high = mid-1
''',

        "bubble sort": '''
numbers = [8,5,2,7,1,4]

for i in range(len(numbers)):

    for j in range(len(numbers)-1-i):

        if numbers[j] > numbers[j+1]:

            numbers[j],numbers[j+1] = numbers[j+1],numbers[j]

print(numbers)
''',

        "linear search": '''
numbers = [10,20,30,40,50]

target = int(input("Number: "))

for i in numbers:

    if i == target:

        print("Found")

        break
''',

        "password checker": '''
password = input("Password: ")

if len(password) < 8:

    print("Weak Password")

elif password.isalpha():

    print("Add numbers")

else:

    print("Strong Password")
''',

        "file size": '''
import os

filename = input("File: ")

print(os.path.getsize(filename),"bytes")
''',

        "rename file": '''
import os

old = input("Old Name: ")

new = input("New Name: ")

os.rename(old,new)

print("Renamed")
''',

        "random student": '''
import random

students = [

"Alice",

"Brian",

"Charles",

"Nitron",

"David"

]

print(random.choice(students))
''',        "stack": '''
stack = []

while True:

    print("1. Push")
    print("2. Pop")
    print("3. Show")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":

        stack.append(input("Value: "))

    elif choice == "2":

        if stack:

            print("Removed:", stack.pop())

        else:

            print("Stack Empty")

    elif choice == "3":

        print(stack)

    else:

        break
''',

        "queue": '''
from collections import deque

queue = deque()

while True:

    print("1. Enqueue")
    print("2. Dequeue")
    print("3. Show")
    print("4. Exit")

    choice = input("> ")

    if choice == "1":

        queue.append(input("Value: "))

    elif choice == "2":

        if queue:

            print(queue.popleft())

        else:

            print("Queue Empty")

    elif choice == "3":

        print(list(queue))

    else:

        break
''',

        "merge sort": '''
def merge_sort(arr):

    if len(arr) > 1:

        mid = len(arr)//2

        left = arr[:mid]

        right = arr[mid:]

        merge_sort(left)

        merge_sort(right)

        i=j=k=0

        while i<len(left) and j<len(right):

            if left[i] < right[j]:

                arr[k]=left[i]

                i+=1

            else:

                arr[k]=right[j]

                j+=1

            k+=1

        while i<len(left):

            arr[k]=left[i]

            i+=1

            k+=1

        while j<len(right):

            arr[k]=right[j]

            j+=1

            k+=1

numbers=[9,4,7,1,3]

merge_sort(numbers)

print(numbers)
''',

        "json api": '''
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response.json())
''',

        "uuid": '''
import uuid

print(uuid.uuid4())
''',

        "sha256": '''
import hashlib

text = input("Text: ")

result = hashlib.sha256(text.encode()).hexdigest()

print(result)
''',

        "csv reader": '''
import csv

with open("data.csv") as file:

    reader = csv.reader(file)

    for row in reader:

        print(row)
''',

        "csv writer": '''
import csv

with open("data.csv","w",newline="") as file:

    writer = csv.writer(file)

    writer.writerow(["Name","Age"])

    writer.writerow(["Nitron",20])

print("Done")
''',        "calendar app": '''
import calendar

year = int(input("Year: "))
month = int(input("Month: "))

print(calendar.month(year, month))
''',

        "digital clock": '''
from datetime import datetime
import time

while True:

    print(datetime.now().strftime("%H:%M:%S"))

    time.sleep(1)
''',

        "countdown timer": '''
import time

seconds = int(input("Seconds: "))

while seconds > 0:

    print(seconds)

    time.sleep(1)

    seconds -= 1

print("Time Finished")
''',

        "stopwatch": '''
import time

input("Press Enter to Start")

start = time.time()

input("Press Enter to Stop")

end = time.time()

print("Elapsed:", round(end-start,2),"seconds")
''',

        "random password": '''
import random
import string

characters = string.ascii_letters
characters += string.digits
characters += "!@#$%^&*"

password = ""

for i in range(20):

    password += random.choice(characters)

print(password)
''',

        "qr generator": '''
import qrcode

text = input("Text: ")

image = qrcode.make(text)

image.save("qrcode.png")

print("Saved as qrcode.png")
''',

        "barcode generator": '''
from barcode import Code128
from barcode.writer import ImageWriter

text = input("Barcode: ")

code = Code128(text, writer=ImageWriter())

code.save("barcode")

print("Saved")
''',

        "pdf creator": '''
from reportlab.pdfgen import canvas

pdf = canvas.Canvas("nitron.pdf")

pdf.drawString(100,750,"Hello from Nitron")

pdf.save()

print("PDF Created")
''',        "http server": '''
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(("0.0.0.0",8000), SimpleHTTPRequestHandler)

print("Server running at http://localhost:8000")

server.serve_forever()
''',

        "tcp client": '''
import socket

host = input("Server IP: ")
port = int(input("Port: "))

client = socket.socket()

client.connect((host, port))

while True:

    message = input("Message: ")

    client.send(message.encode())

    if message.lower() == "exit":

        break

client.close()
''',

        "tcp server": '''
import socket

server = socket.socket()

server.bind(("0.0.0.0",5000))

server.listen(1)

print("Waiting...")

client,address = server.accept()

print("Connected:",address)

while True:

    data = client.recv(1024).decode()

    if not data:

        break

    print(data)

client.close()

server.close()
''',

        "port scanner": '''
import socket

host = input("Host: ")

for port in range(1,101):

    sock = socket.socket()

    sock.settimeout(0.2)

    result = sock.connect_ex((host,port))

    if result == 0:

        print("Open:",port)

    sock.close()
''',

        "ping checker": '''
import subprocess

host = input("Host: ")

subprocess.run(["ping","-c","4",host])
''',

        "system monitor": '''
import psutil

print("CPU:", psutil.cpu_percent(), "%")

print("RAM:", psutil.virtual_memory().percent, "%")

print("Disk:", psutil.disk_usage("/").percent, "%")
''',

        "battery": '''
import psutil

battery = psutil.sensors_battery()

if battery:

    print("Battery:", battery.percent, "%")
''',

        "wifi info": '''
import psutil

print(psutil.net_if_addrs())
''',        "image viewer": '''
from PIL import Image

filename = input("Image File: ")

image = Image.open(filename)

image.show()
''',

        "image information": '''
from PIL import Image

filename = input("Image File: ")

image = Image.open(filename)

print("Width:", image.width)
print("Height:", image.height)
print("Format:", image.format)
print("Mode:", image.mode)
''',

        "image resize": '''
from PIL import Image

filename = input("Image File: ")

image = Image.open(filename)

width = int(input("New Width: "))
height = int(input("New Height: "))

new_image = image.resize((width,height))

new_image.save("resized.png")

print("Saved as resized.png")
''',

        "text file search": '''
filename = input("File: ")

keyword = input("Keyword: ")

with open(filename,"r") as file:

    for number,line in enumerate(file,1):

        if keyword.lower() in line.lower():

            print(number, line.strip())
''',

        "folder statistics": '''
import os

path = input("Folder: ")

files = 0

folders = 0

for item in os.listdir(path):

    full = os.path.join(path,item)

    if os.path.isfile(full):

        files += 1

    elif os.path.isdir(full):

        folders += 1

print("Files:", files)

print("Folders:", folders)
''',

        "text backup": '''
source = input("Source File: ")

backup = source + ".bak"

with open(source,"r") as s:

    data = s.read()

with open(backup,"w") as b:

    b.write(data)

print("Backup Created")
''',

        "json formatter": '''
import json

filename = input("JSON File: ")

with open(filename) as file:

    data = json.load(file)

print(json.dumps(data, indent=4))
''',

        "uuid list": '''
import uuid

for i in range(10):

    print(uuid.uuid4())
''',
