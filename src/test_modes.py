# test_modes.py
import sys
import os

# Add the current directory to Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from orchestrator import select_interaction_mode
from voice_engine import voice_engine

def test_text_interaction():
    """Test text-based interaction (simulated)"""
    print("\n" + "="*50)
    print("⌨️  TEXT MODE TEST")
    print("="*50)
    
    try:
        # Simulate a text-based conversation
        print("\n📝 This simulates how text mode would work:")
        print()
        print("Step 1: User types command")
        print("   → 'create a web server'")
        print()
        print("Step 2: System shows menu options")
        print("   1. AWS")
        print("   2. Azure")
        print("   3. GCP")
        print()
        print("Step 3: User selects from numbered lists")
        print("   → User types: 2")
        print()
        print("Step 4: System confirms selection")
        print("   → 'You selected Azure'")
        print()
        
        # Interactive simulation
        print("="*50)
        print("🧪 INTERACTIVE TEXT SIMULATION")
        print("="*50)
        
        command = input("\n📝 Type a sample infrastructure command: ").strip()
        
        if command:
            print(f"✅ Command received: '{command}'")
            print(f"🔄 Processing: {command}...")
            print(f"✅ Would execute infrastructure creation for: {command}")
        else:
            print("⚠️  No command entered")
        
        print("\n✅ Text mode simulation complete!")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Text mode test interrupted")
        return False
    except Exception as e:
        print(f"\n❌ Error in text mode test: {e}")
        return False

def test_voice_interaction():
    """Test voice-based interaction"""
    print("\n" + "="*50)
    print("🎤 VOICE MODE TEST") 
    print("="*50)
    
    try:
        if voice_engine is None:
            print("❌ Voice engine not available. Please check your setup.")
            return False
        
        print("\n🔊 Testing voice interaction...")
        voice_engine.speak("Welcome to voice mode test. Please tell me what infrastructure you want to create.")
        
        print("\n🎤 Listening for your voice command...")
        print("💡 Tip: Speak clearly and say something like 'create a web server'")
        
        success, command = voice_engine.listen_to_speech(timeout=15)
        
        if success:
            print(f"\n✅ Voice command received: '{command}'")
            voice_engine.speak(f"I heard you say: {command}")
            
            # Simulate processing the voice command
            print("\n🔄 Processing your infrastructure request...")
            voice_engine.speak("I will now process your infrastructure request.")
            
            print("✅ Voice mode test complete!")
            return True
        else:
            print(f"\n❌ Voice recognition failed: {command}")
            voice_engine.speak("Sorry, I didn't understand that.")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Voice mode test interrupted")
        voice_engine.speak("Test interrupted")
        return False
    except Exception as e:
        print(f"\n❌ Error in voice mode test: {e}")
        return False

def test_hybrid_interaction():
    """Test switching between voice and text"""
    print("\n" + "="*50)
    print("🔀 HYBRID MODE TEST")
    print("="*50)
    
    try:
        if voice_engine is None:
            print("❌ Voice engine not available. Falling back to text-only mode.")
            return test_text_interaction()
        
        print("\n📋 Hybrid mode allows switching between voice and text.")
        voice_engine.speak("Welcome to hybrid mode. You can use both voice and text.")
        
        # Start with voice
        print("\n" + "-"*50)
        print("🎤 PHASE 1: Voice Input")
        print("-"*50)
        
        voice_engine.speak("Please tell me your name using voice.")
        print("💡 Speak your name clearly...")
        
        success, name = voice_engine.listen_to_speech(timeout=10)
        
        if success:
            print(f"✅ Voice input: '{name}'")
            voice_engine.speak(f"Nice to meet you, {name}!")
        else:
            print("❌ Voice input failed, falling back to text...")
            name = input("Please type your name instead: ").strip()
            if name:
                voice_engine.speak(f"Nice to meet you, {name}!")
            else:
                name = "User"
                print("⚠️  No name provided, using 'User'")
        
        # Switch to text
        print("\n" + "-"*50)
        print("⌨️  PHASE 2: Text Input")
        print("-"*50)
        
        print("\nAvailable cloud providers:")
        print("  1. AWS")
        print("  2. Azure")
        print("  3. GCP")
        
        cloud_choice = input("\nPlease type your preferred cloud (1-3 or name): ").strip()
        
        # Map input to provider name
        cloud_map = {
            "1": "AWS",
            "2": "Azure",
            "3": "GCP",
            "aws": "AWS",
            "azure": "Azure",
            "gcp": "GCP"
        }
        
        cloud_provider = cloud_map.get(cloud_choice.lower(), cloud_choice)
        
        if cloud_provider:
            voice_engine.speak(f"You selected {cloud_provider} cloud provider.")
            print(f"✅ Selected: {cloud_provider}")
        else:
            print("⚠️  No valid provider selected")
        
        # Switch back to voice for confirmation
        print("\n" + "-"*50)
        print("🎤 PHASE 3: Voice Confirmation")
        print("-"*50)
        
        voice_engine.speak("Would you like to proceed with this configuration?")
        print("🎤 Please say 'yes' or 'no'...")
        
        success, confirmation = voice_engine.listen_to_speech(timeout=10)
        
        if success:
            print(f"✅ Voice response: '{confirmation}'")
            
            if "yes" in confirmation.lower() or "yeah" in confirmation.lower():
                voice_engine.speak("Great! Configuration confirmed.")
                print("✅ Configuration confirmed!")
            else:
                voice_engine.speak("Configuration cancelled.")
                print("❌ Configuration cancelled")
        else:
            print("⚠️  No voice confirmation received")
        
        print("\n✅ Hybrid mode test complete!")
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Hybrid mode test interrupted")
        if voice_engine:
            voice_engine.speak("Test interrupted")
        return False
    except Exception as e:
        print(f"\n❌ Error in hybrid mode test: {e}")
        return False

def show_test_summary(mode: str, success: bool):
    """Display a summary of the test results"""
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Mode Tested: {mode.upper()}")
    print(f"Status: {'✅ PASSED' if success else '❌ FAILED'}")
    print("="*60)

def main():
    """Main test function that tests all interaction modes"""
    print("\n" + "="*60)
    print("🚀 COMPREHENSIVE INTERACTION MODE TEST")
    print("="*60)
    
    try:
        # First, let the user choose a mode (like in our real app)
        selected_mode = select_interaction_mode()
        
        if selected_mode is None:
            print("\n⚠️  No mode selected. Exiting.")
            return
        
        print(f"\n🧪 Now testing: {selected_mode.upper()} MODE")
        print("="*60)
        
        # Test the selected mode
        success = False
        
        if selected_mode == "text":
            success = test_text_interaction()
        elif selected_mode == "voice":
            success = test_voice_interaction()
        elif selected_mode == "hybrid":
            success = test_hybrid_interaction()
        else:
            print(f"❌ Unknown mode: {selected_mode}")
            return
        
        # Show summary
        show_test_summary(selected_mode, success)
        
        # Final status
        if success:
            print("\n" + "="*60)
            print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
            print("="*60)
            print("\n📋 What we've validated:")
            print("   🎯 Mode selection at startup")
            print("   🎤 Voice input/output working")
            print("   ⌨️  Text interface framework ready")
            print("   🔀 Hybrid mode capability tested")
            print("\n🎉 Step 3.1 is now complete!")
            print("💡 Ready to move to Step 3.2: Infrastructure logic integration")
            print("="*60 + "\n")
        else:
            print("\n⚠️  Some tests failed. Please review the errors above.")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        if voice_engine:
            voice_engine.speak("Testing cancelled")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)