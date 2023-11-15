import os
import random
import sys

def generate_random_sentence(num_words):
    words = [
        'apple', 'banana', 'orange', 'grape', 'kiwi', 'python', 'programming',
        'random', 'file', 'dimension', 'dog', 'cat', 'house', 'car', 'beach',
        'computer', 'cloud', 'flower', 'mountain', 'ocean', 'sun', 'moon',
        'rainbow', 'coffee', 'book', 'music', 'dance', 'happy', 'friend',
        'journey', 'adventure', 'love', 'peace', 'smile', 'laughter', 'family',
        'holiday', 'vacation', 'explore', 'discover', 'treasure', 'magic',
        'wonder', 'secret', 'fantasy', 'imagination', 'create', 'inspire',
        'dream', 'believe', 'achieve', 'success', 'victory', 'celebrate',
        'challenge', 'effort', 'energy', 'focus', 'persevere', 'progress',
        'mindful', 'grateful', 'kindness', 'forgive', 'compassion', 'courage',
        'strength', 'patience', 'wisdom', 'knowledge', 'learn', 'teach', 'grow',
        'expansion', 'innovation', 'evolve', 'change', 'transform', 'balance',
        'harmony', 'connect', 'communicate', 'collaborate', 'community', 'together',
        'support', 'embrace', 'kindred', 'soul', 'heart', 'spirit', 'nature',
        'semicolon', 'colon'
    ]
    sentence = ' '.join(random.choice(words) + random.choice(['', ',', ';', ':']) for _ in range(num_words))
    return sentence.capitalize() + '.'

def main():
    if len(sys.argv) != 4:
        print("Usage: python file_creator.py <dimMin> <dimMax> <numFile>")
        sys.exit(-1)

    dimMin = float(sys.argv[1])
    dimMax = float(sys.argv[2])
    numFile = int(sys.argv[3])

    for _ in range(numFile):
        dimA = str(random.uniform(dimMin,dimMax))
        nomeFile = f"file{dimA}.txt" #TODO acpire come arrotorndare il nome

        with open(nomeFile, "w") as file:
            dim = random.uniform(dimMin, dimMax)
            numWords = random.randint(5, 15)  # Random number of words per sentence
            numSentences = int((dim * 1000000) / (numWords * 5))  # Assuming average word length of 5 characters

            for _ in range(numSentences):
                sentence = generate_random_sentence(numWords) + '\n'
                file.write(sentence)

if __name__ == "__main__":
    main()
