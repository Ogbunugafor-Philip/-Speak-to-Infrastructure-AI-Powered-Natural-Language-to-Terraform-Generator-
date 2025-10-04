# test_hearing.py
import speech_recognition as sr
import time

def test_microphone():
    """
    Tests microphone functionality and speech recognition.
    Returns True if successful, False otherwise.
    """
    print("\n" + "="*50)
    print("🔊 MICROPHONE TEST")
    print("="*50)
    
    # Create a recognizer instance (our "ears")
    recognizer = sr.Recognizer()
    
    # Adjust sensitivity settings for better recognition
    recognizer.energy_threshold = 4000  # Minimum audio energy to consider for recording
    recognizer.dynamic_energy_threshold = True  # Automatically adjust to ambient noise
    recognizer.pause_threshold = 0.8  # Seconds of non-speaking audio before phrase is complete
    
    try:
        # First, check if microphone is available
        print("\n🔍 Checking for available microphones...")
        mic_list = sr.Microphone.list_microphone_names()
        
        if not mic_list:
            print("❌ No microphones detected. Please check your hardware.")
            return False
        
        print(f"✅ Found {len(mic_list)} microphone(s):")
        for i, mic_name in enumerate(mic_list):
            print(f"   {i}: {mic_name}")
        
        # Use the default microphone
        print(f"\n🎤 Using default microphone: {mic_list[0] if mic_list else 'Unknown'}")
        
        # Test microphone
        with sr.Microphone() as source:
            print("\n📊 Calibrating for ambient noise... (please remain quiet)")
            print("   This will take ~2 seconds...")
            
            # Adjust for ambient noise with a longer duration for better accuracy
            recognizer.adjust_for_ambient_noise(source, duration=2)
            
            print(f"✅ Calibration complete. Energy threshold: {recognizer.energy_threshold}")
            print("\n🎤 Ready! Please speak clearly into your microphone...")
            print("   (Speak a short phrase, then pause)")
            
            # Add a small delay so user can prepare
            time.sleep(0.5)
            
            # Capture the audio with timeout
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
                print("✅ Audio captured successfully!")
            except sr.WaitTimeoutError:
                print("❌ Timeout: No speech detected within 10 seconds.")
                return False
        
        # Process the captured audio
        print("\n🔄 Processing audio... (this may take a few seconds)")
        
        try:
            # Use Google's speech recognition to convert audio to text
            text = recognizer.recognize_google(audio)
            print(f"\n{'='*50}")
            print(f"🤖 SUCCESS! I heard: \"{text}\"")
            print(f"{'='*50}")
            return True
            
        except sr.UnknownValueError:
            # This happens if the speech is unintelligible
            print("\n❌ Could not understand the audio. Possible reasons:")
            print("   • Speech was too quiet or unclear")
            print("   • Too much background noise")
            print("   • Microphone is too far away")
            print("\n💡 Try speaking louder and more clearly.")
            return False
            
        except sr.RequestError as e:
            # This happens if there's a problem with the service
            print(f"\n❌ Service error: {e}")
            print("\n💡 Possible reasons:")
            print("   • No internet connection")
            print("   • Google Speech Recognition service is down")
            print("   • Network firewall blocking the request")
            return False
    
    except OSError as e:
        print(f"\n❌ Microphone access error: {e}")
        print("\n💡 Possible solutions:")
        print("   • Check if another application is using the microphone")
        print("   • Check microphone permissions in system settings")
        print("   • Try reconnecting your microphone")
        return False
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def main():
    """Main entry point for the microphone test."""
    try:
        success = test_microphone()
        
        print("\n" + "="*50)
        if success:
            print("✅ MICROPHONE TEST PASSED")
            print("Your microphone is working correctly!")
        else:
            print("❌ MICROPHONE TEST FAILED")
            print("Please resolve the issues above and try again.")
        print("="*50 + "\n")
        
        return success
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user. Goodbye!")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)