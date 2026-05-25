import sys
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def visualize_structure(path, indent=""):
    try:
        p = Path(path)
        
        if not p.exists():
            print(Fore.RED + f"Error: Path '{path}' does not exist.")
            return
        if not p.is_dir():
            print(Fore.RED + f"Error: '{path}' is not a directory.")
            return

        # Get list of files and folders
        items = sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

        for item in items:
            # Add ignoring system folders
            if item.name in ['venv', '__pycache__', '.git', '.ipynb_checkpoints']:
                continue

            if item.is_dir():
                # Print folder in blue color
                print(f"{indent}{Fore.BLUE}📁 {item.name}")
                # Recursively go inside
                visualize_structure(item, indent + "    ")
            else:
                # Print file in green color
                print(f"{indent}{Fore.GREEN}📜 {item.name}")

    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Fore.YELLOW + "Usage: python main.py [path_to_directory]")
    else:
        root_path = sys.argv[1]
        print(Fore.CYAN + f"\nDirectory structure: {root_path}\n" + "-"*30)
        visualize_structure(root_path)