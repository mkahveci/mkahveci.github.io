import os
import random
import datetime

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

def create_new_post(filename, post_type):
    # Define YAML front matter based on post type
    yaml_data = {
        "paper": {
            "layout": "paper",
            "title": "Title here",
            "image": "/images/ai/001.jpg",
            "authors": "Kahveci M, Wan X, Colacchio B",
            "year": "in-press",
            "publisher": "Journal Here",
            "projectid": "",
            "ref": '"[Kahveci M](/murat), [Wan X](/xiang). & [Colacchio B](/bridget), (in-press). [Title here](/' + filename.split('-')[-1].split('.')[0] + ') _Journal Name Here_."',  # Added double quotes
            "pdf": "",
            "rgpdf": "",
            "doi": "",
            "slides": "",
            "journal": True,
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
        },
        "project": {
            "layout": "project",
            "title": "Project Title",
            "image": "/images/ai/project-11.jpg",
            "projectid": "Project ID",
            "contributors": "Kahveci M",
            "duration": "2025 - 2028",
            "year": 2025,
            "publisher": "",  # Empty string for publisher
            "position": '"PI: [Kahveci M](/murat)"',
            "hostedby": "University Name",
            "fundedby": "Funding Inst Name",
            "budget": "N/A",
            "pdf": "",  # Empty string for pdf
            "web": "https://kahveci.pw/" + filename.split('-')[-1].split('.')[0],
            "project": True,
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
        },
        "course": {
            "layout": "course",
            "image": "/images/courses/wheeling-uni.png",
            "code": "Code here",
            "title": "Course name here",
            "instructor": "Murat Kahveci",
            "instructorurl": "/murat",
            "institution": "Name University",
            "insturl": "University URL here",
            "clevel": "Undergraduate",
            "year": 2025,
            "semester": "Fall 2025",
            "pdf": "",  # Empty string for pdf
            "web": "LMS link here",
            "published": True,
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
        },
        "album": {
            "layout": "album",
            "title": "Title here",  # Set default title
            "image": "/images/album/",  # Set default image path
            "author": "Murat Kahveci",
            "place": "City, Country",  # Added place
            "published": True,  # Added published field
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
        },
        "blog": {
            "layout": "post",
            "author": "Murat Kahveci",
            "title": "",
            "tags": ["Misc"],
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
        },
        "talk": {
            "layout": "talk",
            "title": "",
            "author": "Kahveci M",
            "slides_id": "2PACX-1vQe_l-4D1fSnJl18tt0nO5czuVWtpAzrS0cTOHdTFxt31JHv2OZQzeRXEQd29BWCWzvwLqvCfDh4BqQ",
            "event": "",
            "venue": "",
            "author": "Kahveci M",
            "year": "",
            "paper_link": "",
            "project_link": "",
            "permalink": "/" + filename.split('-')[-1].split('.')[0],
            "talk": True,
            "published": True,
        }
    }

    front_matter = yaml_data.get(post_type, yaml_data["blog"])

    # Create the new .md file in the appropriate folder
    if post_type in ["course", "project", "paper", "paper", "talk"]:  # Add "s" only for these post types
        post_dir = os.path.join(post_type + "s", "_posts")
    else:
        post_dir = os.path.join(post_type, "_posts")

    os.makedirs(post_dir, exist_ok=True)
    filepath = os.path.join(post_dir, filename)

    with open(filepath, "w") as f:
        f.write("---\n")
        for key, value in front_matter.items():
            if isinstance(value, list):
                f.write(f"{key}:\n")
                for item in value:
                    f.write(f"  - {item}\n")
            else:
                f.write(f"{key}: {value}\n")
        f.write("---\n\n")

        if post_type == "paper":  # Add placeholders only for papers
            f.write("Abstract here\n\n")
            f.write("**Keywords**\n\n")
            f.write("*Artificial Intelligence, Generative Artificial Intelligence, MORE*\n\n")
            f.write("{%- include citation.html -%}\n")

        elif post_type == "project":  # Add placeholders for projects
                    f.write("## Synopsis\n\n")
                    f.write("## Project Acronym\n\n")
                    f.write("**EChEmpower**\n\n")
                    f.write("**ECh**: Enhancing Chemistry\n")
                    f.write("**Empower**: Signifies the empowerment of both educators and students through innovative pedagogical approaches. By addressing misconceptions and enhancing the learning experience, the project aims to empower all stakeholders involved in chemistry education.\n\n")
                    f.write("## Project Description\n\n")
                    f.write("1. **Background and Motivation**: \n\n")
                    f.write("2. **Collaborative Approach**: \n\n")
                    f.write("3. **Research Phases**: \n\n")
                    f.write("4. **Pedagogical Frameworks**: \n\n")
                    f.write("5. **Outcomes and Contribution**: \n\n")
                    f.write("6. **Research Dissemination**: \n\n")
                    f.write("### Conclusion\n\n")
                    f.write("Conclusion here\n\n")
                    f.write("{%- include project-contributions.html -%}\n")

        elif post_type == "course":  # Add placeholders for courses
                    f.write("# Course Description\n\n")
                    f.write("## Materials\n\n")
                    f.write("Students are required to have the following materials:\n")
                    f.write("- **Notebook**\n")
                    f.write("- **Writing utensils**\n")
                    f.write("- **Scientific Calculator**  \n")
                    f.write("  Recommended options:\n")
                    f.write("    - TI-30X (~$10–$15)\n")
                    f.write("    - TI-84 (graphing calculator with advanced functionality)\n\n")
                    f.write("All class resources, announcements, and assignments will be managed through **Google Classroom**.\n\n")
                    f.write("## Grade Distribution\n\n")
                    f.write("| Assessment Type       | Included Assessments                             | Percentage of Grade |\n")
                    f.write("|-----------------------|-------------------------------------------------|---------------------|\n")
                    f.write("| Classwork            | Homework, participation, discussions, bellringers | 20%                |\n")
                    f.write("| Formative Assessments| Frequent small assessments (retakes allowed)     | 40%                |\n")
                    f.write("| Summative Assessments| Labs, projects, unit exams                       | 40%                |\n\n")
                    f.write("### Grading Scale:\n")
                    f.write("- 90% – 100%: A\n")
                    f.write("- 80% – 89%: B\n")
                    f.write("- 70% – 79%: C\n")
                    f.write("- 60% – 69%: D\n")
                    f.write("- Below 50%: F\n\n")
                    f.write("## Scope and Sequence\n\n")
                    f.write("| Unit | Driving Question                                                                                           |\n")
                    f.write("|------|-----------------------------------------------------------------------------------------------------------|\n")
                    f.write("| 1    | Why did Tom get melanoma, and how can we treat it?                                                        |\n")
                    f.write("| 2    | Why does sickle cell disease cause so many symptoms, and how did Alexandria get it?                        |\n\n")
                    f.write("## Classroom Policies\n\n")
                    f.write("- **Conduct**: Students must maintain a respectful and productive learning environment, upholding principles of integrity and engagement.\n")
                    f.write("- **Attendance**: Students are responsible for catching up on missed work outside of class. Absences will not be addressed during class time.\n")
                    f.write("- **Homework and Late Work**: Late work is penalized at 50% and will not be accepted after the unit ends.\n")
                    f.write("- **Extra Credit**: Opportunities are provided sparingly.\n\n")
                    f.write("## Science Safety Agreement\n")

    print(f"New post created: {filepath}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a new post with YAML front matter.")
    parser.add_argument("post_type", choices=["paper", "project", "course", "album", "blog", "talk"], help="Type of the post")
    args = parser.parse_args()

    existing_permalinks = find_existing_permalinks('.')

    os.makedirs("_plugins", exist_ok=True)
    with open('_plugins/existing_permalinks.txt', 'w') as f:
        for permalink in existing_permalinks:
            f.write(permalink + '\n')

    new_permalink = generate_permalink()

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{current_date}-{new_permalink}.md"

    create_new_post(filename, args.post_type)