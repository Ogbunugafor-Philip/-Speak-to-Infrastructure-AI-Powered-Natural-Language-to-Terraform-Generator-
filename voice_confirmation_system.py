"""
Voice Confirmation System
=========================
Simple, working voice confirmation: "Did I hear you correctly?"

Dependencies: speech_recognition, pyttsx3
Install: pip install SpeechRecognition pyttsx3 pyaudio
"""

import speech_recognition as sr
import pyttsx3
import sys
import time


class VoiceConfirmation:
    """
    Simple voice confirmation system that:
    1. Listens to a command
    2. Repeats it back
    3. Asks "Did I hear you correctly?"
    4. Listens for yes/no response
    """
    
    def __init__(self):
        """Initialize speech recognition and text-to-speech."""
        print("\nInitializing voice confirmation system...")
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
        # Check microphone
        try:
            self.microphone = sr.Microphone()
            print("Microphone: OK")
        except OSError as e:
            print(f"ERROR: Microphone not available - {e}")
            sys.exit(1)
        
        # Initialize text-to-speech
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 170)
            self.tts.setProperty('volume', 0.9)
            print("Text-to-speech: OK")
        except Exception as e:
            print(f"ERROR: Text-to-speech failed - {e}")
            sys.exit(1)
        
        print("Voice confirmation system ready\n")
    
    def speak(self, text):
        """Speak text aloud."""
        print(f"[SPEAKING] {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"ERROR speaking: {e}")
    
    def listen(self, timeout=10):
        """
        Listen for speech and return transcribed text.
        
        Returns:
            tuple: (success: bool, text: str)
        """
        try:
            print("\n[LISTENING] Adjusting for noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("[LISTENING] Speak now...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            print("[PROCESSING] Analyzing speech...")
            text = self.recognizer.recognize_google(audio)
            
            if not text.strip():
                return False, "No speech detected"
            
            print(f"[HEARD] {text}")
            return True, text.strip()
            
        except sr.WaitTimeoutError:
            return False, "Timeout - no speech detected"
        except sr.UnknownValueError:
            return False, "Could not understand speech"
        except sr.RequestError as e:
            return False, f"Service error: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def confirm_yes_no(self, question):
        """
        Ask a yes/no question and get voice response.
        
        Returns:
            bool: True if yes, False if no/unclear
        """
        self.speak(question)
        
        success, response = self.listen(timeout=8)
        
        if not success:
            print(f"[ERROR] {response}")
            return False
        
        response_lower = response.lower()
        
        # Check for yes
        yes_words = ['yes', 'yeah', 'yep', 'correct', 'right', 'ok', 'okay', 'sure', 'confirm']
        for word in yes_words:
            if word in response_lower:
                print(f"[CONFIRMED] Detected: {word}")
                return True
        
        # Check for no
        no_words = ['no', 'nope', 'wrong', 'incorrect', 'cancel', 'stop']
        for word in no_words:
            if word in response_lower:
                print(f"[DENIED] Detected: {word}")
                return False
        
        # Unclear - default to no for safety
        print("[UNCLEAR] Response ambiguous, treating as NO")
        return False
    
    def get_confirmed_command(self, max_attempts=3):
        """
        Complete workflow: Listen → Confirm → Return verified command.
        
        Returns:
            tuple: (success: bool, command: str)
        """
        print("="*60)
        print("VOICE COMMAND CONFIRMATION")
        print("="*60)
        
        for attempt in range(1, max_attempts + 1):
            print(f"\nAttempt {attempt} of {max_attempts}")
            print("-"*60)
            
            # Step 1: Get command
            self.speak("What infrastructure would you like to create?")
            success, command = self.listen()
            
            if not success:
                print(f"Failed to capture command: {command}")
                if attempt < max_attempts:
                    self.speak("Let me try again.")
                    time.sleep(1)
                continue
            
            # Step 2: Confirm command
            print(f"\n[COMMAND] {command}")
            confirmation_question = f"Did I hear you correctly? You said: {command}. Please say yes or no."
            
            confirmed = self.confirm_yes_no(confirmation_question)
            
            if confirmed:
                self.speak("Confirmed. Proceeding with your command.")
                print("\n" + "="*60)
                print(f"SUCCESS: Command confirmed")
                print(f"Command: {command}")
                print("="*60)
                return True, command
            else:
                self.speak("Okay, let's try again.")
                print("[RETRY] Command not confirmed")
        
        # Failed after all attempts
        self.speak("I'm having trouble understanding. Please try text input instead.")
        print("\n" + "="*60)
        print("FAILED: Could not confirm command")
        print("="*60)
        return False, ""


def test_voice_confirmation():
    """Test the voice confirmation system."""
    print("\n" + "="*60)
    print("VOICE CONFIRMATION TEST")
    print("="*60)
    print("\nThis will test:")
    print("1. Speaking a command")
    print("2. System repeats it back")
    print("3. You confirm with yes/no")
    print("\nTest commands to try:")
    print("- Deploy a web server")
    print("- Create a database")
    print("- Set up Kubernetes cluster")
    print("\n" + "="*60)
    
    try:
        # Initialize system
        vc = VoiceConfirmation()
        
        # Run confirmation workflow
        success, command = vc.get_confirmed_command(max_attempts=3)
        
        # Show results
        print("\n" + "="*60)
        print("TEST RESULTS")
        print("="*60)
        
        if success:
            print(f"Status: PASSED")
            print(f"Confirmed Command: {command}")
            print("\nNext step: This command would be sent to infrastructure creation")
        else:
            print(f"Status: FAILED")
            print("Recommendation: Use text input mode")
        
        print("="*60)
        
        return success
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return False
    except Exception as e:
        print(f"\nTest failed: {e}")
        return False


if __name__ == "__main__":
    try:
        success = test_voice_confirmation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)