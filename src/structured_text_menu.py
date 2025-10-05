"""
structured_text_menu.py
----------------------------------------
3.5.5 — Structured Menu Options for Text Mode
A clean, interactive text-based menu that mirrors voice prompts,
allowing users to select infrastructure details through numbered choices.
"""

import time
from datetime import datetime

# Define color styles for better CLI visuals
class Style:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"


class StructuredTextMenu:
    """Handles structured text-mode menus for infrastructure selection."""

    def __init__(self):
        self.provider_choices = {
            1: ("AWS", "Amazon Web Services", "The most widely used cloud platform"),
            2: ("Azure", "Microsoft Azure", "Microsoft’s enterprise-grade cloud platform"),
            3: ("GCP", "Google Cloud Platform", "Google’s reliable and AI-driven cloud service")
        }
        self.selected_provider = None
        self.selection_time = None

    def display_header(self, title):
        print(f"\n{Style.CYAN}{'═'*70}{Style.RESET}")
        print(f"{Style.BOLD}📘 {title}{Style.RESET}")
        print(f"{Style.CYAN}{'═'*70}{Style.RESET}")

    def display_menu(self):
        """Show numbered provider options."""
        self.display_header("CLOUD PROVIDER SELECTION (TEXT MODE)")
        print(f"{Style.YELLOW}Please choose your preferred cloud provider:{Style.RESET}\n")
        for key, (short, full, desc) in self.provider_choices.items():
            print(f"  {Style.CYAN}{key}.{Style.RESET} {Style.BOLD}{short}{Style.RESET} — {desc}")
        print()

    def get_user_choice(self):
        """Capture and validate user’s numeric choice."""
        while True:
            try:
                choice = int(input(f"{Style.BOLD}Enter your choice (1–3): {Style.RESET}"))
                if choice in self.provider_choices:
                    self.selected_provider = self.provider_choices[choice]
                    self.selection_time = datetime.now()
                    print(f"\n{Style.GREEN}✅ You selected {self.selected_provider[1]} ({self.selected_provider[0]}){Style.RESET}")
                    return
                else:
                    print(f"{Style.RED}❌ Invalid choice. Please enter 1, 2, or 3.{Style.RESET}")
            except ValueError:
                print(f"{Style.RED}⚠️ Please enter a valid number.{Style.RESET}")

    def summarize_selection(self):
        """Display summary and next steps."""
        time.sleep(0.5)
        print(f"\n{Style.CYAN}{'═'*70}{Style.RESET}")
        print(f"{Style.BOLD}📋 SELECTION SUMMARY{Style.RESET}")
        print(f"{Style.CYAN}{'═'*70}{Style.RESET}")

        short, full, desc = self.selected_provider
        print(f"🌐 Cloud Provider: {Style.BOLD}{short}{Style.RESET}")
        print(f"🏷️  Full Name: {full}")
        print(f"📝 Description: {desc}")

        print(f"\n🕒 Selected at: {self.selection_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Style.CYAN}{'-'*70}{Style.RESET}")

        print(f"\n{Style.YELLOW}🚀 Next Steps:{Style.RESET}")
        print(f"   1. Configure credentials for {short}")
        print(f"   2. Select region and availability zones")
        print(f"   3. Define compute and storage preferences")
        print(f"   4. Validate security and networking options")

        print(f"\n{Style.GREEN}✅ Configuration saved! Ready to proceed with infrastructure setup.{Style.RESET}")

    def run(self):
        """Run the full text menu workflow."""
        self.display_menu()
        self.get_user_choice()
        self.summarize_selection()


if __name__ == "__main__":
    print(f"\n{Style.BOLD}🧭 Starting Structured Text Mode Prompt System...{Style.RESET}")
    menu = StructuredTextMenu()
    menu.run()
    print(f"\n{Style.GREEN}🎯 Text Mode Selection Process Complete.{Style.RESET}\n")
