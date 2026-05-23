from collections import Counter

def freq_counter(str):
    cleand = ''

    for char in str:
        if char.isalnum() or char == " ":
            cleand += char.lower()

    words = cleand.split()
    return dict(Counter(words))

s = "Hello Yash how are you !YASH"
print(freq_counter(s))