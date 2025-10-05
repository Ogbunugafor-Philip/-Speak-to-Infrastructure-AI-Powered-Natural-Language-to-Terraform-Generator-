# test_speaking.py
import pyttsx3
import sys

def test_text_to_speech():
    """
    Tests text-to-speech functionality.
    Returns True if successful, False otherwise.
    """
    print("\n" + "="*50)
    print("🗣️ TEXT-TO-SPEECH TEST")
    print("="*50)
    
    try:
        # Create a TTS engine instance (our "voice box")
        print("\n🔧 Initializing text-to-speech engine...")
        engine = pyttsx3.init()
        print("✅ Engine initialized successfully!")
        
        # Get current settings
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        
        print(f"\n📊 Current Settings:")
        print(f"   Speech Rate: {rate} words per minute")
        print(f"   Volume: {volume * 100:.0f}%")
        
        # Let's see what voices are available on your system
        voices = engine.getProperty('voices')
        
        if not voices:
            print("\n❌ No voices detected on your system.")
            print("💡 Please install text-to-speech voices for your OS.")
            return False
        
        print(f"\n🗣️ Available voices on your system ({len(voices)} found):")
        for i, voice in enumerate(voices):
            # Extract gender and language info if available
            gender = getattr(voice, 'gender', 'Unknown')
            languages = getattr(voice, 'languages', ['Unknown'])
            
            print(f"  {i}: {voice.name}")
            print(f"     ID: {voice.id}")
            if gender != 'Unknown':
                print(f"     Gender: {gender}")
            if languages and languages[0] != 'Unknown':
                print(f"     Languages: {', '.join(languages)}")
            print()
        
        # Select voice based on user preference
        selected_voice_index = 0
        if len(voices) > 1:
            print("💡 Multiple voices detected. Using default (first voice).")
            print("   You can modify the code to select a different voice.")
        
        # Set the selected voice
        engine.setProperty('voice', voices[selected_voice_index].id)
        print(f"✅ Using voice: {voices[selected_voice_index].name}")
        
        # Optional: Adjust speech rate and volume for better clarity
        # Uncomment these lines to customize:
        # engine.setProperty('rate', 150)  # Slower = easier to understand
        # engine.setProperty('volume', 0.9)  # 90% volume
        
        # Prepare test message
        test_message = "Hello! I am the Speak to Infrastructure tool. I am now able to speak."
        
        print("\n" + "="*50)
        print("🔊 SPEAKING TEST")
        print("="*50)
        print(f"📝 Message: \"{test_message}\"")
        print("\n🔊 Please listen for the audio...")
        print("   (If you don't hear anything, check your speakers/volume)")
        
        # Make the engine say the message
        engine.say(test_message)
        
        # This command makes the program wait until the speech is finished
        engine.runAndWait()
        
        print("\n✅ Speaking test complete!")
        
        # Test a second phrase to confirm it works consistently
        print("\n🔄 Testing second phrase...")
        second_message = "Speech synthesis is working correctly."
        print(f"📝 Message: \"{second_message}\"")
        
        engine.say(second_message)
        engine.runAndWait()
        
        print("✅ Second test complete!")
        
        # Cleanup
        engine.stop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during text-to-speech test: {e}")
        print("\n💡 Possible solutions:")
        print("   • Ensure pyttsx3 is properly installed: pip install pyttsx3")
        print("   • Check if your system has TTS voices installed")
        print("   • On Linux: Install espeak (sudo apt-get install espeak)")
        print("   • On macOS: TTS should work out of the box")
        print("   • On Windows: SAPI5 voices should be available")
        return False

def customize_voice_settings(engine):
    """
    Optional function to customize voice settings interactively.
    Can be called before speaking if user wants to adjust settings.
    """
    print("\n🎛️ Voice Customization (Optional)")
    print("Current settings can be adjusted:")
    
    # Get current settings
    current_rate = engine.getProperty('rate')
    current_volume = engine.getProperty('volume')
    
    print(f"   Rate: {current_rate} WPM")
    print(f"   Volume: {current_volume * 100:.0f}%")
    
    # Example customizations (uncomment to use):
    # engine.setProperty('rate', 150)    # Slower, clearer speech
    # engine.setProperty('volume', 0.9)  # 90% volume
    
    return engine

def main():
    """Main entry point for the TTS test."""
    try:
        success = test_text_to_speech()
        
        print("\n" + "="*50)
        if success:
            print("✅ TEXT-TO-SPEECH TEST PASSED")
            print("Your TTS engine is working correctly!")
        else:
            print("❌ TEXT-TO-SPEECH TEST FAILED")
            print("Please resolve the issues above and try again.")
        print("="*50 + "\n")
        
        return success
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user. Goodbye!")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)