# orchestrator.py
import os
import sys

def clear_screen():
    """Clear the terminal screen for a cleaner interface."""
    os.system('cls' if os.name == 'nt' else 'clear')

def select_interaction_mode():
    """
    Presents a menu to the user to select their preferred interaction mode.
    This is the FIRST thing that happens when the tool starts.
    
    Returns:
        str: Selected mode ('text', 'voice', 'hybrid') or None if user quits
    """
    try:
        clear_screen()
        print("\n" + "="*50)
        print("🚀 SPEAK-TO-INFRASTRUCTURE")
        print("="*50)
        print("Welcome! How would you like to interact?")
        print()
        print("1. Text Mode (Type your commands)")
        print("2. Voice Mode (Speak your commands)")
        print("3. Hybrid Mode (Switch between voice and text)")
        print("4. Exit")
        print()
        
        while True:
            choice = input("Please enter your choice (1-4): ").strip().lower()
            
            # Handle both number and first letter
            if choice in ["1", "t", "text"]:
                print("\n✅ Text Mode selected. Ready for your commands.")
                return "text"
            elif choice in ["2", "v", "voice"]:
                print("\n🎤 Voice Mode selected. Please ensure your microphone is on.")
                return "voice"
            elif choice in ["3", "h", "hybrid"]:
                print("\n🔀 Hybrid Mode selected. You can switch between voice and text.")
                return "hybrid"
            elif choice in ["4", "e", "exit", "quit"]:
                print("\n👋 Goodbye!")
                return None
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        return None
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        return None

def main():
    """Main entry point for the orchestrator."""
    selected_mode = select_interaction_mode()
    
    if selected_mode is None:
        sys.exit(0)
    
    print(f"\n[DEBUG] You selected: {selected_mode}")
    print("[DEBUG] The next step would be to launch the main logic in this mode.")
    
    # TODO: Import and call the appropriate mode handler
    # if selected_mode == "text":
    #     from text_mode import start_text_mode
    #     start_text_mode()
    # elif selected_mode == "voice":
    #     from voice_mode import start_voice_mode
    #     start_voice_mode()
    # elif selected_mode == "hybrid":
    #     from hybrid_mode import start_hybrid_mode
    #     start_hybrid_mode()

if __name__ == "__main__":
    main()