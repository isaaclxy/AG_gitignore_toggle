#!/usr/bin/env python3
import os
import argparse
import sys

# Configuration
START_TAG = "# <ag-toggle>"
END_TAG = "# </ag-toggle>"

def find_all_gitignores(root_path="."):
    """Recursively finds all .gitignore files in the directory tree."""
    gitignore_files = []
    # reliable walk, skipping common huge ignored dirs to speed up
    skip_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build'}
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Modify dirnames in-place to skip specific directories
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        
        if ".gitignore" in filenames:
            gitignore_files.append(os.path.join(dirpath, ".gitignore"))
            
    return gitignore_files

def get_file_status(gitignore_path):
    """
    Returns 'exposed' (Work Mode), 'hidden' (Commit Mode), or 'clean' (No tags).
    """
    try:
        with open(gitignore_path, 'r') as f:
            lines = f.readlines()
    except Exception:
        return 'error'

    in_block = False
    has_block = False
    exposed_count = 0
    hidden_count = 0

    for line in lines:
        stripped = line.strip()
        if stripped == START_TAG:
            in_block = True
            has_block = True
            continue
        if stripped == END_TAG:
            in_block = False
            continue

        if in_block:
            if line.startswith("# "):
                # It's commented out -> EXPOSED to git (Work Mode)
                exposed_count += 1
            else:
                # It's active -> HIDDEN from git (Commit Mode)
                hidden_count += 1
    
    if not has_block:
        return 'clean'
    
    # If we have any exposed lines, we are effectively in "Work Mode" (Unsafe to commit)
    if exposed_count > 0:
        return 'exposed'
    
    # If we have lines but none are exposed, we are in "Commit Mode" (Safe)
    if hidden_count > 0:
        return 'hidden'
        
    return 'clean' # Block exists but is empty

def toggle_ignore(gitignore_path, mode):
    """
    Toggles lines between the tags.
    mode: 'expose' (comment out lines) or 'hide' (uncomment lines)
    """
    with open(gitignore_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_block = False
    modified = False

    for line in lines:
        stripped = line.strip()
        
        if stripped == START_TAG:
            in_block = True
            new_lines.append(line)
            continue
        
        if stripped == END_TAG:
            in_block = False
            new_lines.append(line)
            continue

        if in_block:
            if mode == 'expose':
                # We want to EXPOSE these files, so we COMMENT them out from gitignore
                if not line.startswith("# "):
                    new_lines.append(f"# {line}")
                    modified = True
                else:
                    new_lines.append(line) # Already commented
            elif mode == 'hide':
                # We want to HIDE these files, so we UNCOMMENT them in gitignore
                if line.startswith("# "):
                    # Only uncomment if it follows our pattern (simple space safe check)
                    new_lines.append(line[2:])
                    modified = True
                else:
                    new_lines.append(line) # Already active
        else:
            new_lines.append(line)

    if modified:
        with open(gitignore_path, 'w') as f:
            f.writelines(new_lines)
        print(f"[UPDATED] {gitignore_path}")
        return True
    return False

def check_status(files):
    print(f"Scanning {len(files)} .gitignore files...\n")
    exposed_files = []
    hidden_files = []
    clean_files = []

    for path in files:
        status = get_file_status(path)
        if status == 'exposed':
            exposed_files.append(path)
        elif status == 'hidden':
            hidden_files.append(path)
        else:
            clean_files.append(path)

    if exposed_files:
        print("\033[91m⚠️  WORK MODE (Unsafe to commit)\033[0m")
        print("The following files permit internal docs to be seen by Git:")
        for f in exposed_files:
            print(f"  - {f}")
        print("\nRun '--commit' to hide them before pushing.")
    elif hidden_files:
        print("\033[92m✅ COMMIT MODE (Safe to commit)\033[0m")
        print("Internal docs are safely ignored in:")
        for f in hidden_files:
            print(f"  - {f}")
    else:
        print("No <ag-toggle> blocks found. Project is standard.")

def main():
    parser = argparse.ArgumentParser(description="Toggle visibility of specific internal files in .gitignore")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--work', action='store_const', dest='mode', const='expose', help="Expose internal files (comment out in gitignore)")
    group.add_argument('--commit', action='store_const', dest='mode', const='hide', help="Hide internal files (uncomment in gitignore)")
    group.add_argument('--status', action='store_const', dest='mode', const='status', help="Check current status")
    
    args = parser.parse_args()
    
    # Now searches recursively from CWD
    gitignore_files = find_all_gitignores(".")
    
    if not gitignore_files:
        print("No .gitignore files found in this directory tree.")
        sys.exit(0)
        
    if args.mode == 'status':
        check_status(gitignore_files)
    else:
        changes = 0
        for path in gitignore_files:
            if toggle_ignore(path, args.mode):
                changes += 1
        
        if changes == 0:
            print(f"Checked {len(gitignore_files)} files. No changes needed.")
        else:
            print(f"Updated {changes} .gitignore files.")

if __name__ == "__main__":
    main()
