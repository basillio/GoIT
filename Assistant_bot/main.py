"""
Personal Assistant Bot - Main entry point
Supports both CLI and GUI modes
"""
import sys


def main():
    print("\n" + "="*50)
    print("PERSONAL ASSISTANT BOT")
    print("="*50)
    print("\nSelect mode:")
    print("  1. CLI (Command Line Interface)")
    print("  2. GUI (Graphical User Interface)")
    print("  0. Exit")
    print("="*50)

    choice = input("\nEnter your choice (0-2): ").strip()

    if choice == "1":
        from assistant import AssistantBot
        bot = AssistantBot()
        bot.run()
    elif choice == "2":
        from gui import main as gui_main
        gui_main()
    elif choice == "0":
        print("\nGoodbye!")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice. Please try again.")
        main()


if __name__ == "__main__":
    main()
