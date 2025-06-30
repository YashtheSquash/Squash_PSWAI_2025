import string

user_input = input("Enter a sentence: ")
cleaned = user_input.translate(str.maketrans('', '', string.punctuation))
words = cleaned.split()
unique_words = set(words)
print(unique_words)
