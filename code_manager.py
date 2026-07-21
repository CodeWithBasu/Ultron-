import os
from git_manager import GitManager

class CodeManager:
    """Provides file system operations for Ultron with integrated auto-commits."""
    
    def __init__(self):
        self.git = GitManager()

    def read_file(self, filepath):
        """Reads the content of a file."""
        if not os.path.exists(filepath):
            return f"Error: File '{filepath}' does not exist."
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, filepath, content):
        """Writes content to a file and auto-commits the change."""
        try:
            # Ensure directory exists
            directory = os.path.dirname(filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"[+] CodeManager: Wrote to '{filepath}'")
            
            # Immediately commit and push to boost the user's GitHub commits!
            filename = os.path.basename(filepath)
            self.git.commit_and_push(f"auto: Ultron autonomously edited {filename}")
            
            return f"Success: File '{filepath}' was written and pushed to GitHub."
        except Exception as e:
            return f"Error writing file: {e}"

    def list_directory(self, path="."):
        """Lists files in a directory."""
        try:
            items = os.listdir(path)
            return f"Contents of '{path}':\n" + "\n".join(items)
        except Exception as e:
            return f"Error listing directory: {e}"
