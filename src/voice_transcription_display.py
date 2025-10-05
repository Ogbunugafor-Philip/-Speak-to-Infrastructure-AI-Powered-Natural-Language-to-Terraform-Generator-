"""
Voice Transcription Display System
===================================
Provides visual confirmation of transcribed speech.
Displays what the system heard on screen for dual verification (audio + visual).

Dependencies: speech_recognition, pyttsx3
Install: pip install SpeechRecognition pyttsx3 pyaudio
"""

import speech_recognition as sr
import pyttsx3
import sys
import time


class VoiceTranscriptionDisplay:
    """
    Displays voice transcriptions in real-time with visual formatting.
    Combines audio feedback with visual text display for better verification.
    """
    
    def __init__(self):
        """Initialize voice recognition and text-to-speech engines."""
        print("\nInitializing transcription display system...")
        
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
        
        print("Transcription display ready\n")
    
    def display_box(self, text, box_type="info"):
        """
        Display text in a formatted box.
        
        Args:
            text: Text to display
            box_type: Type of box (info, command, success, error, warning)
        """
        width = 70
        
        if box_type == "command":
            border = "="
            prefix = "[COMMAND]"
        elif box_type == "success":
            border = "="
            prefix = "[SUCCESS]"
        elif box_type == "error":
            border = "-"
            prefix = "[ERROR]"
        elif box_type == "warning":
            border = "-"
            prefix = "[WARNING]"
        else:
            border = "-"
            prefix = "[INFO]"
        
        print(f"\n{border * width}")
        print(f"{prefix} {text}")
        print(f"{border * width}")
    
    def speak(self, text):
        """Speak text aloud."""
        print(f"\n[SPEAKING] {text}")
        try:
            self.tts.say(text)
            self.tts.runAndWait()
        except Exception as e:
            print(f"ERROR speaking: {e}")
    
    def listen_with_display(self, prompt="Please speak your command"):
        """
        Listen for speech and display the transcription.
        
        Args:
            prompt: What to ask the user
            
        Returns:
            tuple: (success: bool, transcribed_text: str)
        """
        # Display and speak the prompt
        self.display_box(prompt, "info")
        self.speak(prompt)
        
        # Visual indicator that system is listening
        print("\n" + "="*70)
        print("LISTENING - Speak now")
        print("="*70)
        
        try:
            # Adjust for ambient noise
            print("\nCalibrating microphone...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print("Ready - Speak clearly...")
            
            # Listen for speech
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=10, 
                    phrase_time_limit=15
                )
            
            # Processing indicator
            print("\n" + "="*70)
            print("PROCESSING - Transcribing speech")
            print("="*70)
            time.sleep(0.5)  # Brief pause for visual effect
            
            # Transcribe
            text = self.recognizer.recognize_google(audio)
            
            if not text.strip():
                self.display_box("No speech detected", "error")
                return False, "No speech detected"
            
            # Display transcription prominently
            self.display_box(f"Transcribed: {text}", "command")
            
            return True, text.strip()
            
        except sr.WaitTimeoutError:
            error_msg = "Timeout - no speech detected within 10 seconds"
            self.display_box(error_msg, "error")
            return False, error_msg
            
        except sr.UnknownValueError:
            error_msg = "Could not understand the speech"
            self.display_box(error_msg, "error")
            self.speak("I couldn't understand that. Please speak more clearly.")
            return False, error_msg
            
        except sr.RequestError as e:
            error_msg = f"Service error: {e}"
            self.display_box(error_msg, "error")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.display_box(error_msg, "error")
            return False, error_msg
    
    def confirm_transcription(self, transcribed_text):
        """
        Ask user to confirm the transcription (yes/no).
        
        Args:
            transcribed_text: The text that was transcribed
            
        Returns:
            bool: True if confirmed, False otherwise
        """
        # Show what we're confirming
        self.display_box(f"Confirm: '{transcribed_text}'", "warning")
        
        # Ask for confirmation
        question = f"I heard: {transcribed_text}. Is this correct? Say yes or no."
        self.speak(question)
        
        # Visual indicator
        print("\n" + "="*70)
        print("AWAITING CONFIRMATION - Say 'yes' or 'no'")
        print("="*70)
        
        # Listen for yes/no
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("\nListening for confirmation...")
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=5)
            
            response = self.recognizer.recognize_google(audio)
            response_lower = response.lower().strip()
            
            self.display_box(f"Response: {response}", "info")
            
            # Check for affirmative
            yes_words = ['yes', 'yeah', 'yep', 'correct', 'right', 'ok', 'okay']
            for word in yes_words:
                if word in response_lower:
                    self.display_box("Confirmed - Proceeding", "success")
                    self.speak("Confirmed. Proceeding with your command.")
                    return True
            
            # Check for negative
            no_words = ['no', 'nope', 'wrong', 'incorrect', 'cancel']
            for word in no_words:
                if word in response_lower:
                    self.display_box("Not confirmed - Will retry", "warning")
                    self.speak("Understood. Let's try again.")
                    return False
            
            # Ambiguous
            self.display_box("Response unclear - Treating as NO", "warning")
            return False
            
        except Exception as e:
            self.display_box(f"Confirmation failed: {e}", "error")
            return False
    
    def get_verified_command(self, max_attempts=3):
        """
        Complete workflow: Listen, Display, Confirm, Verify.
        
        Args:
            max_attempts: Maximum number of attempts
            
        Returns:
            tuple: (success: bool, verified_command: str, attempts: int)
        """
        print("\n" + "="*70)
        print("VOICE COMMAND VERIFICATION WITH VISUAL DISPLAY")
        print("="*70)
        
        for attempt in range(1, max_attempts + 1):
            print(f"\n\nAttempt {attempt} of {max_attempts}")
            print("-"*70)
            
            # Step 1: Listen and display transcription
            success, command = self.listen_with_display(
                "What infrastructure would you like to create?"
            )
            
            if not success:
                if attempt < max_attempts:
                    self.speak("Let me try again.")
                    time.sleep(1)
                continue
            
            # Step 2: Confirm the transcription
            confirmed = self.confirm_transcription(command)
            
            if confirmed:
                # Success!
                print("\n" + "="*70)
                print("VERIFICATION COMPLETE")
                print("="*70)
                print(f"Verified Command: {command}")
                print(f"Attempts Used: {attempt}")
                print("="*70)
                return True, command, attempt
            
            # Not confirmed, retry if attempts remain
            if attempt < max_attempts:
                time.sleep(1)
        
        # All attempts failed
        self.display_box(
            "Verification failed after maximum attempts", 
            "error"
        )
        self.speak("Unable to verify command. Please use text input mode.")
        
        print("\n" + "="*70)
        print("VERIFICATION FAILED")
        print("="*70)
        print(f"Attempts Used: {max_attempts}")
        print("Recommendation: Switch to text input mode")
        print("="*70)
        
        return False, "", max_attempts


def test_transcription_display():
    """Test the transcription display system."""
    print("\n" + "="*70)
    print("VOICE TRANSCRIPTION DISPLAY TEST")
    print("="*70)
    
    print("\nThis test demonstrates:")
    print("1. Voice input with real-time transcription display")
    print("2. Visual confirmation of what was heard")
    print("3. Dual verification (audio + visual)")
    
    print("\nSuggested test commands:")
    print("- Deploy a web server with database")
    print("- Create a Kubernetes cluster on AWS")
    print("- Set up a VPC with three subnets")
    
    print("\n" + "="*70)
    
    try:
        # Initialize system
        display = VoiceTranscriptionDisplay()
        
        # Run verification workflow
        success, command, attempts = display.get_verified_command(max_attempts=3)
        
        # Show final results
        print("\n\n" + "="*70)
        print("TEST RESULTS")
        print("="*70)
        
        if success:
            print(f"Status: SUCCESS")
            print(f"Verified Command: {command}")
            print(f"Attempts: {attempts}")
            print("\nThe transcription display system is working correctly!")
        else:
            print(f"Status: FAILED")
            print(f"Attempts: {attempts}")
            print("\nRecommendation: Check microphone and try again")
        
        print("="*70)
        
        return success
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        return False
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        return False


if __name__ == "__main__":
    try:
        success = test_transcription_display()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)