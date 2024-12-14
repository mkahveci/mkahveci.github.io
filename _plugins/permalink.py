import os
import random

def find_existing_permalinks(root_dir):
    permalinks = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".md") and filename != "README.md":
                try:
                    permalink = filename.split('-')[-1].split('.')[0]
                    if len(permalink) == 3 and permalink.islower() and permalink.isalpha():
                        permalinks.append(permalink)
                except IndexError:
                    pass
    return permalinks

def permalink_exists(permalink):
    for filename in os.listdir('.'):
        if filename.endswith(".md") and permalink in filename:
            return True
    return False

def read_existing_permalinks(filename="existing_permalinks.txt"):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        return []

def generate_permalink():
    letters = 'abcdefghijklmnopqrstuvwxyz'
    existing_permalinks = read_existing_permalinks("_plugins/existing_permalinks.txt")
    while True:
        new_permalink = ''.join(random.choice(letters) for i in range(3))
        if not permalink_exists(new_permalink) and new_permalink not in existing_permalinks:
            return new_permalink
        # No need for 'else' here, the loop continues automatically

if __name__ == "__main__":
    existing_permalinks = find_existing_permalinks('.')

    os.makedirs("_plugins", exist_ok=True)
    with open('_plugins/existing_permalinks.txt', 'w') as f:
        for permalink in existing_permalinks:
            f.write(permalink + '\n')

    new_permalink = generate_permalink()
    print(new_permalink)