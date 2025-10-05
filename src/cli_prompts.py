def main_menu():
    """Display the main menu and get user choice."""
    print("\n" + "="*40)
    print("   Speak to Infrastructure")
    print("="*40)
    print("\nWhat would you like to do?\n")
    print("  1. Create new infrastructure")
    print("  2. Modify existing infrastructure")
    print("  3. Destroy infrastructure")
    print("  4. View infrastructure status")
    print("  5. Exit")
    print("\n" + "-"*40)
    
    while True:
        choice = input("Please enter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


def handle_choice(choice):
    """Process the user's menu choice."""
    actions = {
        '1': create_infrastructure,
        '2': modify_infrastructure,
        '3': destroy_infrastructure,
        '4': view_status,
        '5': exit_program
    }
    
    action = actions.get(choice)
    if action:
        action()


def create_infrastructure():
    """Handle infrastructure creation."""
    print("\n--- Create New Infrastructure ---")
    print("Creating infrastructure...")
    # Add your infrastructure creation logic here


def modify_infrastructure():
    """Handle infrastructure modification."""
    print("\n--- Modify Existing Infrastructure ---")
    print("Modifying infrastructure...")
    # Add your infrastructure modification logic here


def destroy_infrastructure():
    """Handle infrastructure destruction."""
    print("\n--- Destroy Infrastructure ---")
    confirm = input("Are you sure you want to destroy infrastructure? (yes/no): ")
    if confirm.lower() == 'yes':
        print("Destroying infrastructure...")
        # Add your infrastructure destruction logic here
    else:
        print("Operation cancelled.")


def view_status():
    """Display infrastructure status."""
    print("\n--- Infrastructure Status ---")
    print("Viewing current infrastructure status...")
    # Add your status viewing logic here


def exit_program():
    """Exit the program."""
    print("\nThank you for using Speak to Infrastructure!")
    print("Goodbye!")
    exit(0)


def main():
    """Main program loop."""
    while True:
        user_choice = main_menu()
        handle_choice(user_choice)
        
        if user_choice != '5':
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()