#!/usr/bin/env python3
import os
import sys
import re
import datetime
import subprocess

def get_value(html, key):
    pattern = rf'<div class="k">{key}</div>\s*<div class="v">(.*?)</div>'
    match = re.search(pattern, html, re.DOTALL)
    return match.group(1).strip() if match else ""

def set_value(html, key, new_val):
    pattern = rf'(<div class="k">{key}</div>\s*<div class="v">)(.*?)(</div>)'
    return re.sub(pattern, rf'\g<1>{new_val}\g<3>', html)

def prompt_user(key, default_val):
    # AppleScript dialog that pops up in the front user session
    applescript = f'''
    tell application "SystemUIServer"
        activate
        set response to display dialog "What are you currently {key.lower()}?" default answer "{default_val}" with title "Activity Update" buttons {{"Cancel", "Save"}} default button "Save" with icon note
        return text returned of response
    end tell
    '''
    try:
        proc = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True, check=True)
        return proc.stdout.strip()
    except subprocess.CalledProcessError:
        # User clicked Cancel
        return None

def main():
    force = "--force" in sys.argv or "--dry-run" in sys.argv
    
    if not force:
        today = datetime.date.today()
        # Saturday is 5 (0=Monday, 6=Sunday).
        # We only run on the first Saturday of the month (day <= 7).
        if today.weekday() != 5 or today.day > 7:
            print("Today is not the first Saturday of the month. Exiting silently.")
            sys.exit(0)

    html_path = "/Users/aaron/Sites/aaronsofaly/index.html"
    if not os.path.exists(html_path):
        print(f"Error: index.html not found at {html_path}", file=sys.stderr)
        sys.exit(1)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Retrieve current values
    current_reading = get_value(html, "Reading")
    current_listening = get_value(html, "Listening")
    current_playing = get_value(html, "Playing")
    current_watching = get_value(html, "Watching")

    # Prompt user for new values
    new_reading = prompt_user("Reading", current_reading)
    if new_reading is None:
        print("Update cancelled by user.")
        sys.exit(0)

    new_listening = prompt_user("Listening", current_listening)
    if new_listening is None:
        print("Update cancelled by user.")
        sys.exit(0)

    new_playing = prompt_user("Playing", current_playing)
    if new_playing is None:
        print("Update cancelled by user.")
        sys.exit(0)

    new_watching = prompt_user("Watching", current_watching)
    if new_watching is None:
        print("Update cancelled by user.")
        sys.exit(0)

    changed = (new_reading != current_reading or
               new_listening != current_listening or
               new_playing != current_playing or
               new_watching != current_watching)

    if changed:
        html = set_value(html, "Reading", new_reading)
        html = set_value(html, "Listening", new_listening)
        html = set_value(html, "Playing", new_playing)
        html = set_value(html, "Watching", new_watching)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print("index.html updated successfully with new activities.")

        # Git operations
        cwd = "/Users/aaron/Sites/aaronsofaly"
        git_path = "/usr/bin/git"
        try:
            subprocess.run([git_path, "add", "index.html"], cwd=cwd, check=True)
            subprocess.run([git_path, "commit", "-m", "feat: updated activity"], cwd=cwd, check=True)
            print("Git commit completed.")
            
            # Push to origin
            subprocess.run([git_path, "push", "origin", "main"], cwd=cwd, check=True)
            print("Pushed to origin main successfully.")
            
            # Push to gitlab
            subprocess.run([git_path, "push", "gitlab", "main"], cwd=cwd, check=True)
            print("Pushed to gitlab main successfully.")
        except Exception as e:
            print(f"Git push failed: {e}", file=sys.stderr)
    else:
        print("No changes were made to the current activities.")

if __name__ == "__main__":
    main()
