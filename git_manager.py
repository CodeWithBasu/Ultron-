import subprocess
import os

class GitManager:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path
    
    def commit_and_push(self, commit_message):
        """Adds all changes, commits, and pushes to remote to boost commits."""
        try:
            print(f"[*] Auto-committing to GitHub: {commit_message}")
            # Add all changes
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            
            # Commit changes
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            
            # Push changes
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            print("[+] Successfully pushed to GitHub!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[-] Git auto-commit failed (or no changes to commit): {e}")
            return False

if __name__ == "__main__":
    # Test the git manager
    manager = GitManager()
    manager.commit_and_push("chore: auto-commit via GitManager")
