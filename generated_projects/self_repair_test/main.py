def calculate_score(name):
    score = 100
    print(f"Player: {name}")
    if score > 50:
        print("High score")
    return score

if __name__ == "__main__":
    calculate_score("Nitron")
