#!/usr/bin/env python3
import os
import shutil
import argparse

DEMO_DIR = "demo"

def find_files(root_path, extension):
    """Finds all files ending with extension in root_path (recursive)."""
    matches = []
    for dirpath, _, filenames in os.walk(root_path):
        for f in filenames:
            if f.endswith(extension):
                matches.append(os.path.join(dirpath, f))
    return matches

def init_demo():
    """Renames .gitignore.example -> .gitignore"""
    examples = find_files(DEMO_DIR, ".gitignore.example")
    count = 0
    for ex in examples:
        target = ex.replace(".gitignore.example", ".gitignore")
        if not os.path.exists(target):
            shutil.move(ex, target)
            print(f"[SETUP] Created: {target}")
            count += 1
        else:
            print(f"[SKIP] Exists: {target}")
    print(f"\nInitialized {count} demo files. You can now run 'python3 toggle_ignore.py --status'")

def clean_demo():
    """Renames .gitignore -> .gitignore.example"""
    active = find_files(DEMO_DIR, ".gitignore")
    count = 0
    for ac in active:
        target = ac + ".example"
        shutil.move(ac, target)
        print(f"[CLEAN] Restored: {target}")
        count += 1
    print(f"\nCleaned up {count} demo files.")

def main():
    parser = argparse.ArgumentParser(description="Setup demo environment for testing.")
    parser.add_argument('--init', action='store_true', help="Rename examples to active .gitignore")
    parser.add_argument('--clean', action='store_true', help="Rename active .gitignore back to examples")
    
    args = parser.parse_args()
    
    if not os.path.exists(DEMO_DIR):
        print(f"Error: '{DEMO_DIR}' directory not found.")
        return

    if args.init:
        init_demo()
    elif args.clean:
        clean_demo()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
