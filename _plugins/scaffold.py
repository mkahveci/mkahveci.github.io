#!/usr/bin/env python3

"""
Jekyll Content Scaffolding Script (V4.1)

This script interactively scaffolds new content for a Jekyll website
by an external template-driven system.

(Updated main function: If no post_type argument is given,
the script now displays an interactive menu of all
available post types.)

Requirements:
- PyYAML (pip install PyYAML)
- sys (standard library)
"""

import os
import random
import datetime
import re
import argparse
import string
import sys  # <-- Import sys to check for arguments
import yaml  # Requires: pip install PyYAML
from pathlib import Path
from typing import Set, Dict, Any, List, Optional

# --- Constants ---

#: Directory where post templates are stored
TEMPLATE_DIR = "_scaffold_templates"
#: Characters to use for random permalink generation
PERMALINK_CHARS = string.ascii_lowercase
#: Length of the random permalink
PERMALINK_LENGTH = 3
#: Location of the team collection posts
TEAM_DATA_DIR = "team/_posts"

#: Directories to exclude from the permalink scan
EXCLUDED_DIRS = {
    "_site",
    "_scaffold_templates",
    "_plugins",
    "node_modules",
    ".git",
    ".idea"
}

# --- Core Functions ---

def load_team_data(team_dir: str) -> List[Dict[str, Any]]:
    """
    Loads team members by scanning and parsing the YAML front matter
    from all .md files in the team_dir.
    """
    team_path = Path(team_dir)
    team_members: List[Dict[str, Any]] = []

    if not team_path.exists():
        print(f"Info: Team directory not found at '{team_dir}'. Falling back to manual author entry.")
        return []

    print(f"Scanning '{team_dir}' for team members...")

    # Regex to match the 'YYYY-MM-DD-' prefix
    date_prefix_re = re.compile(r'^\d{4}-\d{2}-\d{2}-')

    for file_path in team_path.rglob('*.md'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Robust front matter parsing
            if not content.startswith('---'):
                continue
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue # No closing '---'
            yaml_content = parts[1]

            if not yaml_content:
                continue

            front_matter = yaml.safe_load(yaml_content)

            if isinstance(front_matter, dict) and 'name' in front_matter:

                # --- Get slug from filename ---
                slug = file_path.stem
                if date_prefix_re.match(slug):
                    slug = slug[11:] # 'annemarie-kegler'
                front_matter['file_slug'] = slug
                # --- End ---

                team_members.append(front_matter)

        except yaml.YAMLError as e:
            print(f"  Warning: Could not parse YAML in {file_path}. Error: {e}")
        except Exception as e:
            print(f"  Warning: Could not read or process file {file_path}. Error: {e}")

    print(f"Found {len(team_members)} team members.")
    team_members.sort(key=lambda x: x.get('name', ''))
    return team_members


def load_existing_permalinks(root_dir: str) -> Set[str]:
    """
    Recursively scans all .md and .html files from the root directory,
    parses their YAML front matter, and extracts 'permalink' values.
    Skips directories defined in EXCLUDED_DIRS.
    """
    print(f"Scanning '{root_dir}' for existing permalinks...")
    permalinks: Set[str] = set()
    root_path = Path(root_dir)

    # Regex to match the 'YYYY-MM-DD-' prefix
    date_prefix_re = re.compile(r'^\d{4}-\d{2}-\d{2}-')

    for file_path in root_path.rglob('*.*'):
        if not (file_path.suffix in ['.md', '.html']):
            continue

        # Check if any part of the path is in the exclude list
        if any(part in EXCLUDED_DIRS for part in file_path.parts):
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            found_slug = None

            # --- STRATEGY 1: Check for explicit 'permalink: /foo' ---
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    if yaml_content:
                        front_matter = yaml.safe_load(yaml_content)
                        if isinstance(front_matter, dict):
                            permalink_val = front_matter.get('permalink')
                            if isinstance(permalink_val, str) and permalink_val:
                                slug = permalink_val.lstrip('/')
                                if slug:
                                    found_slug = slug

            # --- STRATEGY 2: If no explicit permalink, parse filename ---
            if not found_slug:
                filename = file_path.stem # 'YYYY-MM-DD-slug' or 'slug'

                # Check if it's a post with a date prefix
                if date_prefix_re.match(filename):
                    # Extract 'slug' from 'YYYY-MM-DD-slug'
                    found_slug = filename[11:]
                else:
                    # Assume the whole filename is the slug (e.g., 'scaffold.md')
                    found_slug = filename

            if found_slug:
                permalinks.add(found_slug)

        except yaml.YAMLError as e:
            print(f"  Warning: Could not parse YAML in {file_path}. Error: {e}")
        except Exception as e:
            print(f"  Warning: Could not read or process file {file_path}. Error: {e}")

    print(f"Found {len(permalinks)} existing permalinks.")
    return permalinks


def generate_unique_permalink(existing_links: Set[str]) -> str:
    """
    Generates a new, unique 3-letter permalink.
    """
    while True:
        new_link = ''.join(random.choice(PERMALINK_CHARS) for _ in range(PERMALINK_LENGTH))
        if new_link not in existing_links:
            return new_link


def get_target_dir(post_type: str) -> Path:
    """
    Determines the correct output directory for the new post.
    """
    if post_type in ["course", "project", "talk"]:
        dir_name = post_type + "s"
    else:
        dir_name = post_type

    target_path = Path(dir_name) / "_posts"
    target_path.mkdir(parents=True, exist_ok=True)
    return target_path


def select_team_indices(team: List[Dict[str, Any]], post_type: str) -> Optional[List[int]]:
    """
    Displays a numbered list of team members and asks the user
    to select them in order.
    """
    if not team:
        return None

    print(f"\n--- Select Contributors ({post_type}) ---")
    for i, member in enumerate(team):
        print(f"  {i+1}. {member.get('name', 'Unnamed')}")

    try:
        input_str = input("Enter numbers in order (e.g., 1,3,2), or leave blank for manual entry: ").strip()
        if not input_str:
            return None

        selected_indices = []
        indices_str = input_str.split(',')

        for s in indices_str:
            idx = int(s.strip()) - 1  # Convert 1-based to 0-based
            if 0 <= idx < len(team):
                selected_indices.append(idx)
            else:
                print(f"  Warning: '{s}' is not a valid number. Skipping.")

        return selected_indices

    except ValueError:
        print("  Invalid input. Falling back to manual entry.")
        return None


def get_user_input(post_type: str, team_members: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Interactively prompts the user for data based on the post type.
    """
    print("-" * 30)
    print(f"Enter details for new '{post_type}':")

    data: Dict[str, Any] = {}

    while not (title := input("Title: ").strip()):
        print("Title is required.")

    # 'year' prompt is now only for post types that need it
    if post_type not in ['blog', 'album']:
        data["year"] = input(f"Year (e.g., {datetime.date.today().year}): ").strip() or str(datetime.date.today().year)

    # --- Type-Specific Prompts ---

    if post_type == 'project':
        data["projectid"] = input("Project ID (e.g., pec-leap): ").strip()

        selected_indices = select_team_indices(team_members, "project")
        if selected_indices:
            selected_authors = [team_members[i] for i in selected_indices]

            author_links = []
            for auth in selected_authors:
                name = auth.get('name', auth.get('citation_name', ''))
                file_slug = auth.get('file_slug')

                if file_slug:
                    author_links.append(f"[{name}](/{file_slug}/)")
                else:
                    author_links.append(name)

            data["contributors"] = ", ".join(author_links)

        else:
            data["contributors"] = input("Contributors (manual, e.g., [Name](/url)): ").strip()

        data["duration"] = input("Duration (e.g., 2023 - 2024): ").strip()

        pi_info_str = "PI: [Kahveci M](/murat)" # Default fallback
        for member in team_members:
            if "murat" in member.get("file_slug", ""):
                pi_name = member.get('citation_name', member.get('name'))
                pi_slug = member.get('file_slug')
                pi_info_str = f"PI: [{pi_name}](/{pi_slug}/)"
                break

        position_prompt = f"Position (default: {pi_info_str}): "
        user_position = input(position_prompt).strip()

        if not user_position: # If user hits Enter
            data["position"] = pi_info_str
        else:
            data["position"] = user_position

        data["hostedby"] = input("Hosted By: ").strip()
        data["fundedby"] = input("Funded By: ").strip()
        data["excerpt"] = input("Excerpt (short description): ").strip()

    elif post_type == 'course':
        data["code"] = input("Course Code (e.g., FSCI): ").strip()
        data["institution"] = input("Institution (e.g., Chicago Public Schools): ").strip()
        inst_url = input("Institution/Classroom URL (e.g., https://classroom.google.com/): ").strip()
        data["insturl"] = inst_url
        data["web"] = inst_url # Set both fields
        data["clevel"] = input("Course Level (e.g., High School): ").strip()
        data["level"] = input("Level (e.g., HS): ").strip()
        data["semester"] = input("Semester(s) (e.g., Fall 2025, Spring 2026): ").strip()
        data["excerpt"] = input("Excerpt (short description): ").strip()

    elif post_type == 'talk':
        data["subtitle_desc"] = input("Subtitle Description: ").strip()
        data["event"] = input("Event: ").strip()
        data["location"] = input("Location (e.g., Chicago): ").strip()
        data["type"] = input("Type (invited/conference): ").strip() or "invited"

        selected_indices = select_team_indices(team_members, "talk")
        if selected_indices:
            author_objects = []
            for i in selected_indices:
                team_member_data = team_members[i]

                explicit_url = team_member_data.get('url')
                file_slug_url = f"/{team_member_data.get('file_slug')}/"

                author = {
                    "name": team_member_data.get('name', ''),
                    "affiliation": team_member_data.get('position', ''),
                    "photo": team_member_data.get('image', ''),
                    "url": explicit_url or file_slug_url # Use explicit, or fall back
                }
                author_objects.append(author)
            data["authors"] = author_objects

        else:
            print("\n--- Authors (Manual Entry) ---")
            data["authors"] = []
            while True:
                name = input("Add Author Name (or blank to finish): ").strip()
                if not name:
                    break
                author = {
                    "name": name,
                    "affiliation": input(f"  Affiliation for {name}: ").strip(),
                    "photo": input(f"  Photo URL for {name}: ").strip(),
                    "url": input(f"  URL for {name}: ").strip()
                }
                data["authors"].append(author)
            if not data["authors"]:
                print("  Warning: No authors added.")

        data["funding"] = []
        print("\n--- Funding ---")
        while True:
            funder = input("Add Funding Source (or blank to finish): ").strip()
            if not funder:
                break
            data["funding"].append(funder)

    elif post_type == 'album':
        data["place"] = input("Place (e.g., Loyola University Chicago): ").strip()
        data["image"] = input("Image Path (e.g., /images/album/foo.jpg): ").strip()

    elif post_type == 'blog':
        tags_str = input("Tags (comma-separated, e.g., quant, trading): ").strip()
        if tags_str:
            data["tags"] = [tag.strip() for tag in tags_str.split(',')]
        else:
            data["tags"] = ["Misc"]

        data["excerpt"] = input("Excerpt (short description): ").strip()

        print("\n--- Related Project ---")
        project_name = input("Project Name (or blank to skip): ").strip()
        if project_name:
            project_url = input(f"  Project URL for '{project_name}' (e.g., /qma/): ").strip()
            data["related_project"] = {
                "name": project_name,
                "url": project_url
            }
        else:
            data["related_project"] = {"name": "", "url": ""}

    print("-" * 30)
    return data


def create_post_from_templates(post_type: str, context: Dict[str, Any]) -> None:
    """
    Loads YAML and Markdown templates, merges them with the context data,
    and writes the new post file.
    """
    # --- 1. Load YAML Front Matter Template ---
    yaml_template_path = Path(TEMPLATE_DIR) / f"{post_type}.yml"
    try:
        with open(yaml_template_path, 'r', encoding='utf-8') as f:
            final_data = yaml.safe_load(f)
            if not isinstance(final_data, dict):
                final_data = {}
    except FileNotFoundError:
        print(f"Error: YAML template not found: {yaml_template_path}")
        return
    except yaml.YAMLError as e:
        print(f"Error: Could not parse YAML template {yaml_template_path}. Error: {e}")
        return

    # --- 2. Merge Base Template with User Context ---
    final_data.update(context)

    if post_type == 'talk':
        final_data['authors'] = context.get('authors', [])
        final_data['funding'] = context.get('funding', [])
    elif post_type == 'blog':
        final_data['tags'] = context.get('tags', [])
        final_data['related_project'] = context.get('related_project', {"name": "", "url": ""})
        if not final_data['related_project']['name']:
            del final_data['related_project']


    try:
        yaml_string = yaml.dump(
            final_data,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
            width=80
        )
    except Exception as e:
        print(f"Error dumping final YAML: {e}")
        return

    # --- 3. Load Markdown Body Template (if it exists) ---
    md_template_path = Path(TEMPLATE_DIR) / f"{post_type}.md"
    md_content = ""
    if md_template_path.exists():
        try:
            with open(md_template_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            print(f"Warning: Could not read MD template {md_template_path}. Error: {e}")

    # --- 4. Assemble and Write the Final File ---
    final_content = f"---\n{yaml_string}---\n\n{md_content}"

    target_dir = get_target_dir(post_type)
    file_slug = context["permalink"][1:]  # Get 'qrx' from '/qrx'

    if post_type == 'talk':
        extension = '.html'
    else:
        extension = '.md'

    filename = f"{context['date']}-{file_slug}{extension}"
    filepath = target_dir / filename

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"\nSuccess! New post created at: {filepath}")
    except Exception as e:
        print(f"\nError: Could not write final file to {filepath}. Error: {e}")


# --- Main Execution ---

def main():
    """
    Main function to run the scaffolding script.
    """
    # *** UPDATED LOGIC: Handle interactive menu ***

    try:
        available_types = sorted([
            f.stem for f in Path(TEMPLATE_DIR).glob('*.yml')
        ])
    except FileNotFoundError:
        print(f"Error: Template directory '{TEMPLATE_DIR}' not found.")
        return

    if not available_types:
        print(f"Error: No .yml templates found in '{TEMPLATE_DIR}'.")
        return

    parser = argparse.ArgumentParser(
        description="Create a new Jekyll post from templates.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # Make the 'post_type' argument optional
    parser.add_argument(
        "post_type",
        nargs='?', # <-- Makes it optional
        choices=available_types,
        help="Type of the post to create (optional)."
    )
    args = parser.parse_args()

    post_type = args.post_type

    # If no argument was given, show the interactive menu
    if not post_type:
        print("Select a post type to create:")
        for i, pt in enumerate(available_types):
            print(f"  {i+1}. {pt.capitalize()}")

        while True:
            try:
                choice_str = input(f"Enter a number (1-{len(available_types)}): ")
                choice_idx = int(choice_str) - 1
                if 0 <= choice_idx < len(available_types):
                    post_type = available_types[choice_idx]
                    break
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(available_types)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return

    # *** END UPDATED LOGIC ***

    print(f"\nStarting to scaffold new '{post_type}'...")

    # --- Step 1: Find all existing permalinks for collision check ---
    existing_links = load_existing_permalinks('.')
    new_permalink = generate_unique_permalink(existing_links)

    # --- Step 2: Load Team Data ---
    team_members = load_team_data(TEAM_DATA_DIR)

    # --- Step 3: Get interactive user input ---
    user_data = get_user_input(post_type, team_members)

    # --- Step 4: Prepare the final data context ---
    today = datetime.date.today()

    context = user_data.copy()
    context["date"] = today.isoformat()
    context["permalink"] = f"/{new_permalink}" # e.g., /qrx

    if post_type not in ['blog', 'album']:
        if "year" not in user_data:
            context["year"] = today.year
        else:
            context["year"] = user_data["year"]
    elif post_type == 'blog':
        context["year"] = today.year

    # --- Step 5: Create the post ---
    create_post_from_templates(post_type, context)


if __name__ == "__main__":
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML library not found.")
        print("Please install it by running: pip install PyYAML")
        exit(1)

    main()