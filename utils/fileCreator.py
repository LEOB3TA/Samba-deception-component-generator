from datetime import datetime
import random


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


def create_files(dim_min, dim_max, num_file):
    for _ in range(num_file):
        file_dim = random.uniform(dim_min, dim_max)
        file_dim_str = str(file_dim)
        file_round_dim_str = file_dim_str
        if file_dim_str.find('.') != -1:
            file_round_dim_str = file_dim_str[:file_dim_str.find('.')]
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d")
        nome_file = f"{formatted_datetime}_{file_round_dim_str}MB.txt"
        print(nome_file)

        with open(nome_file, "w") as file:
            num_words = random.randint(5, 15)  # Random number of words per sentence
            num_sentences = int((file_dim * 1000000) / (num_words * 5))  # Assuming average word length of 5 characters

            for _ in range(num_sentences):
                sentence = generate_random_sentence(num_words) + '\n'
                file.write(sentence)
    return


if __name__ == '__main__':
    dim_min = 100
    dim_max = 200
    num_file = 1
    create_files(dim_min, dim_max, num_file)
