# Gitignore Toggler

I believe `.gitignore` should be used specifically to exclude files from version control. However, some AI agents, like Google Antigravity, appears to also exclude files in `.gitignore` from being seen/edited by the AI Agent.

This makes it inconvenient to disable rows in .gitignore when working with AG agent, and then enabling it again before committing. As such, here's a simple "Quality of Life" Python script designed to temporarily expose specific internal files (like agent documentation, scratchpads, or secret notes) to your working environment without risking them being permanently committed or exposed to the public.

It works by selectively toggling comments in your `.gitignore` files, allowing you to "reveal" files to tools (like AI agents or your IDE) while working, and "hide" them again before committing.

You can even ask your AI agent to run this script to check if it's in "Work Mode" or "Commit Mode" before running a commit. I suggest including this in your AGENTS.md

```
**For AI Agents**: This repo has a script in the root directory called `toggle_ignore.py` that can be used to toggle the visibility of files in the `.gitignore` file. Use it with `--work` flag to expose files to your tools while working, and with `--commit` flag to hide them again before committing.
```

## Why?
You might have `agents.md` or `internal_docs/` that you want your AI assistant to read, but you **never** want to commit them to your remote repository.

## Dependencies

*   Python 3.x
*   No external libraries required (uses standard `os`, `sys`, `argparse`).

## Setup

1.  Place `toggle_ignore.py` in your project root.
2.  Open your `.gitignore` file.
3.  Wrap the rules you want to toggle inside the `<ag-toggle>` tags:

```gitignore
node_modules/
.DS_Store

# <ag-toggle>
agents.md
internal_docs/
my_scratchpad.txt
# </ag-toggle>

build/
```

## Usage

### 1. Start Working (Expose Files)
Make the files visible to Git and your tools:
```bash
python3 toggle_ignore.py --work
```
*   *What happens:* The lines inside the block are commented out (e.g., `# agents.md`).
*   *Result:* Git sees these files. You can now use them with your AI tools.

### 2. Finish Working (Hide Files)
Make the files ignored again before you push:
```bash
python3 toggle_ignore.py --commit
```
*   *What happens:* The lines are uncommented (e.g., `agents.md`).
*   *Result:* Git ignores these files. They will not appear in `git status`.

### 3. Check Status
See if you are in "Work Mode" or "Commit Mode":
```bash
python3 toggle_ignore.py --status
```
*   **Work Mode**: ⚠️ Warning. Internal files are visible.
*   **Commit Mode**: ✅ Safe. Internal files are ignored.

## Notes
*   **Project-Wide**: The script recursively searches the entire directory tree (starting from where you run it) for `.gitignore` files.
*   **Performance**: Safely skips `node_modules`, `.git`, and other heavy folders during search.

## 🧪 Try the Demo
This repo includes a `demo/` folder so you can test the script safely.

1.  **Setup**: Use the helper script to activate the demo files:
    ```bash
    python3 setup_demo.py --init
    ```
    *(This renames `gitignore.example` files in `demo/` to `.gitignore`)*

2.  **Test**:
    *   Run `python3 toggle_ignore.py --work`
    *   Check the files in `demo/` (they should be updated!).
    *   Run `python3 toggle_ignore.py --status` (should see "WORK MODE").
    *   Run `python3 toggle_ignore.py --commit` (should revert).

3.  **Cleanup**:
    ```bash
    python3 setup_demo.py --clean
    ```
    *(Restores them to `gitignore.example`)*

```bash
python3 toggle_ignore.py --help
```
