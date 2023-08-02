import random
import string
import os
import nltk

def download_nltk_word_list():
    nltk.download("words", quiet=True)

def load_common_word_list():
    return nltk.corpus.words.words("en")

def is_common_english_word(word, common_word_list):
    return word.lower() in common_word_list

def generate_gmail(common_word_list):
    while True:
        username = random.choice(common_word_list)
        if len(username) >= 6 and is_common_english_word(username, common_word_list):
            return username.lower() + "@gmail.com"

def main():
    try:
        num_emails = int(input("Enter the number of Gmail addresses to generate: "))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return

    if num_emails <= 0:
        print("The number of emails should be greater than 0.")
        return

    download_nltk_word_list()
    common_word_list = load_common_word_list()

    print(f"Maximum number of common words available in the nltk word list: {len(common_word_list)}")

    gmails = [generate_gmail(common_word_list) for _ in range(num_emails)]
    folder_name = "Wonderland"
    file_name = "check_gmail.txt"
    file_path = os.path.join(folder_name, file_name)

    try:
        os.makedirs(folder_name, exist_ok=True)
        with open(file_path, "w") as file:
            for gmail in gmails:
                file.write(gmail + "\n")
        print(f"{num_emails} Gmail addresses have been generated and saved to {file_path}.")
    except IOError:
        print(f"Error: Unable to write to the file {file_path}.")

if __name__ == "__main__":
    main()
