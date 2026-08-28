def calculate_total(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

numbers = [10, 20, 30]
print("Total:", calculate_total(numbers))
