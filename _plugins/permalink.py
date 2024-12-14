import os
import random
import datetime  # Import the datetime module

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
#     print(new_permalink)

def create_new_post(filename):
    # Create the new .md file with the pre-formatted content
    with open(filename, "w") as f:
        permalink = filename.split('-')[-1].split('.')[0]  # Extract permalink from filename
        f.write(f"---\n")
        f.write(f"layout: post\n")
        f.write(f"title:  \"Title of your post\"\n")
        f.write(f"permalink: /{permalink}\n")
        f.write(f"---\n\n")
        f.write("Your content here.\n")

    print(f"New post created: {filename}")

if __name__ == "__main__":
    existing_permalinks = find_existing_permalinks('.')

    os.makedirs("_plugins", exist_ok=True)
    with open('_plugins/existing_permalinks.txt', 'w') as f:
        for permalink in existing_permalinks:
            f.write(permalink + '\n')

    new_permalink = generate_permalink()

    # Generate the filename with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{current_date}-{new_permalink}.md"

    create_new_post(filename)  # Create the new post file