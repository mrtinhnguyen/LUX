import os
import shutil
import re

def rebrand_project(root_dir, old_name, new_name):
    """
    Rebrands the project from old_name to new_name.
    Handles file content replacement and file/directory renaming.
    """
    old_name_lower = old_name.lower()
    new_name_lower = new_name.lower()
    
    # Replacement mapping
    replacements = {
        old_name: new_name,
        old_name_lower: new_name_lower,
        "lux-format": f"{new_name_lower}-format",
        "Lightweight Ultra-compressed Xchange": "Lightweight Ultra-compressed Xchange",
        ".luxf": f".{new_name_lower}f",
        "LUB": f"{new_name[0:2]}B".upper() # For binary format magic header
    }

    print(f"🚀 Starting rebranding from {old_name} to {new_name}...")

    # 1. First pass: Replace content in files
    for root, dirs, files in os.walk(root_dir):
        # Skip some directories
        if any(skip in root for skip in ['.git', '__pycache__', '.venv', '.egg-info', 'build', 'dist']):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            # Only process text files
            if file.endswith(('.py', '.md', '.toml', '.txt', '.yaml', '.yml', '.in', 'LICENSE')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content
                    for old, new in replacements.items():
                        content = content.replace(old, new)

                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"  📝 Updated content: {file_path}")
                except Exception as e:
                    print(f"  ❌ Error processing {file_path}: {e}")

    # 2. Second pass: Rename files and directories
    # We use os.walk with topdown=False to rename children before parents
    for root, dirs, files in os.walk(root_dir, topdown=False):
        if any(skip in root for skip in ['.git', '__pycache__', '.venv']):
            continue

        # Rename files
        for file in files:
            if old_name_lower in file:
                old_file_path = os.path.join(root, file)
                new_file_name = file.replace(old_name_lower, new_name_lower)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"  📂 Renamed file: {old_file_path} -> {new_file_name}")

        # Rename directories
        for name in dirs:
            if old_name_lower in name:
                old_dir_path = os.path.join(root, name)
                new_dir_name = name.replace(old_name_lower, new_name_lower)
                new_dir_path = os.path.join(root, new_dir_name)
                # Use shutils for moving if rename fails (across devices) or simple os.rename
                os.rename(old_dir_path, new_dir_path)
                print(f"  📁 Renamed dir: {old_dir_path} -> {new_dir_name}")

    print(f"✅ Rebranding completed successfully! Project is now {new_name}.")

if __name__ == "__main__":
    # Get the project root directory (parent of scripts)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rebrand_project(project_root, "LUX", "LUX")
