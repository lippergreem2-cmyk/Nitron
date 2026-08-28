
while True:

    print("\nCalculator")

    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Exit")

    choice = input("> ")

    if choice == "5":
        break

    a = float(input("First Number: "))
    b = float(input("Second Number: "))

    if choice == "1":
        print("Answer:", a + b)

    elif choice == "2":
        print("Answer:", a - b)

    elif choice == "3":
        print("Answer:", a * b)

    elif choice == "4":
        print("Answer:", a / b)
