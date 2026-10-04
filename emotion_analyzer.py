"""
emotion_analyzer.py
Analyzes the sentiment/emotion behind a piece of text using TextBlob
(simple, lightweight NLP -- no heavy transformer models needed).
"""

from textblob import TextBlob


def analyze(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity        # -1 (negative) to +1 (positive)
    subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)

    if polarity > 0.5:
        mood = "Very Positive"
    elif polarity > 0.1:
        mood = "Positive"
    elif polarity < -0.5:
        mood = "Very Negative"
    elif polarity < -0.1:
        mood = "Negative"
    else:
        mood = "Neutral"

    word_freq = {}
    for word in blob.words.lower():
        if len(word) > 3:  # skip short filler words
            word_freq[word] = word_freq.get(word, 0) + 1
    top_words = sorted(word_freq.items(), key=lambda x: -x[1])[:5]

    return {
        "text": text,
        "mood": mood,
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "top_words": top_words,
    }


def print_report(result: dict):
    print(f"\nYour message: {result['text']}")
    print(f"\nDetected mood: {result['mood']}")
    print(f"Polarity: {result['polarity']} (Subjectivity: {result['subjectivity']})")
    print("\nMost influential words:")
    for word, count in result["top_words"]:
        print(f"  {word}: {count} time(s)")


if __name__ == "__main__":
    text = input("Enter a message to analyze: ")
    result = analyze(text)
    print_report(result)
