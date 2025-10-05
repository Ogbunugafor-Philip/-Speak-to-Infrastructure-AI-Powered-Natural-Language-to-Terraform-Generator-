# enhanced_voice_engine.py
"""
Enhanced Voice Engine with robust speech recognition and error handling.
This builds upon the basic voice_engine.py with automatic retries and better user feedback.
"""

import speech_recognition as sr
import pyttsx3
from typing import Tuple, Optional
import sys
import time

class EnhancedVoiceEngine:
    """
    Advanced voice engine with automatic retries, detailed error handling,
    and user-friendly feedback.
    """
    
    def __init__(self, rate: int = 170, volume: float = 0.9):
        """
        Initialize the enhanced voice engine.
        
        Args:
            rate: Speech rate in words per minute (default: 170)
            volume: Speech volume from 0.0 to 1.0 (default: 0.9)
        """
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            
            # Configure recognizer for better accuracy
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Initialize microphone
            try:
                self.microphone = sr.Microphone()
                print("✅ Microphone detected")
            except OSError as e:
                print(f"⚠️  Warning: Microphone issue: {e}")
                self.microphone = None
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings for clearer speech
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                print(f"✅ TTS engine ready with voice: {voices[0].name}")
            
            print("🎤 Enhanced voice engine initialized!")
            print("   Features: Auto-retry, Better error messages, User guidance")
            
        except Exception as e:
            print(f"❌ Error initializing enhanced voice engine: {e}")
            raise
    
    def listen_with_retry(
        self, 
        timeout: int = 10, 
        phrase_time_limit: int = 15, 
        max_retries: int = 2,
        ambient_duration: float = 1.0
    ) -> Tuple[bool, str]:
        """
        Robust speech recognition with automatic retries and detailed error handling.
        
        Args:
            timeout: How long to wait for speech to start (seconds)
            phrase_time_limit: Maximum length of speech (seconds) 
            max_retries: How many times to retry on failure
            ambient_duration: How long to adjust for ambient noise (seconds)
            
        Returns:
            Tuple of (success: bool, recognized_text: str)
        """
        if self.microphone is None:
            error_msg = "Microphone not available. Please check your hardware."
            print(f"❌ {error_msg}")
            self.speak(error_msg)
            return False, error_msg
        
        retry_count = 0
        last_error = ""
        
        while retry_count <= max_retries:
            try:
                # Give user appropriate feedback based on retry count
                if retry_count == 0:
                    self.speak("I'm listening now. Please speak clearly.")
                    print("\n🎤 Listening for your command...")
                else:
                    self.speak(f"Let me try again. Attempt {retry_count + 1}.")
                    print(f"\n🔄 Retry {retry_count + 1} of {max_retries + 1}...")
                
                # Calibrate microphone for current environment
                print(f"   Adjusting for background noise... (ambient duration: {ambient_duration}s)")
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=ambient_duration)
                    print(f"   Energy threshold: {self.recognizer.energy_threshold}")
                
                print("   Ready! Speak now...")
                
                # Small delay to let user prepare
                time.sleep(0.3)
                
                # Capture audio with timeout protection
                with self.microphone as source:
                    audio = self.recognizer.listen(
                        source, 
                        timeout=timeout,
                        phrase_time_limit=phrase_time_limit
                    )
                
                print("   Processing your speech...")
                
                # Convert speech to text using Google's service
                text = self.recognizer.recognize_google(audio)
                cleaned_text = text.strip()
                
                # Validate we got actual content
                if not cleaned_text:
                    raise sr.UnknownValueError("No recognizable words detected.")
                
                # Success! Return the recognized text
                print(f"✅ Success! Recognized: '{cleaned_text}'")
                return True, cleaned_text
                
            except sr.WaitTimeoutError:
                # No speech detected within timeout period
                last_error = "I didn't hear anything. Please speak when you see the listening prompt."
                print(f"❌ Timeout: {last_error}")
                
                if retry_count < max_retries:
                    self.speak("I didn't hear anything. Please try speaking again.")
                
            except sr.UnknownValueError as e:
                # Speech was detected but couldn't be understood
                last_error = "I heard sound but couldn't understand the words. Please speak more clearly."
                print(f"❌ Understanding: {last_error}")
                
                if retry_count < max_retries:
                    self.speak("I couldn't understand that. Please try again with clearer speech.")
                
            except sr.RequestError as e:
                # Problem with the speech recognition service
                last_error = f"Speech service error: {e}. Please check your internet connection."
                print(f"❌ Service: {last_error}")
                self.speak("There's a problem with the speech service. Please check your internet connection.")
                return False, last_error  # Don't retry on service errors
                
            except OSError as e:
                # Microphone access issues
                last_error = f"Microphone access error: {e}"
                print(f"❌ Hardware: {last_error}")
                self.speak("I'm having trouble accessing the microphone.")
                return False, last_error  # Don't retry on hardware errors
                
            except Exception as e:
                # Any other unexpected errors
                last_error = f"Unexpected error: {e}"
                print(f"❌ Technical: {last_error}")
                
                if retry_count < max_retries:
                    self.speak("A technical issue occurred. Let's try again.")
            
            retry_count += 1
        
        # If we've exhausted all retries
        final_error = "I'm having trouble with voice input after multiple attempts. Let's switch to text mode."
        print(f"\n❌ {final_error}")
        self.speak(final_error)
        return False, last_error if last_error else "Voice recognition failed after maximum retries"
    
    def speak(self, text: str, wait: bool = True) -> bool:
        """
        Convert text to speech with enhanced reliability.
        
        Args:
            text: The text to speak aloud
            wait: If True, wait for speech to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  Warning: No text to speak")
            return False
        
        try:
            print(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            
            if wait:
                self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Text-to-speech error: {e}")
            return False
    
    def stop_speaking(self):
        """Stop any ongoing speech."""
        try:
            self.tts_engine.stop()
            print("⏹️  Speech stopped")
        except Exception as e:
            print(f"❌ Error stopping speech: {e}")
    
    def adjust_settings(self, rate: Optional[int] = None, volume: Optional[float] = None):
        """
        Adjust TTS settings dynamically.
        
        Args:
            rate: New speech rate (words per minute)
            volume: New volume level (0.0 to 1.0)
        """
        try:
            if rate is not None:
                self.tts_engine.setProperty('rate', rate)
                print(f"✅ Speech rate set to {rate} WPM")
            
            if volume is not None:
                if 0.0 <= volume <= 1.0:
                    self.tts_engine.setProperty('volume', volume)
                    print(f"✅ Volume set to {volume * 100:.0f}%")
                else:
                    print("❌ Volume must be between 0.0 and 1.0")
                    
        except Exception as e:
            print(f"❌ Error adjusting settings: {e}")


def test_enhanced_speech_recognition():
    """
    Comprehensive test of the enhanced speech recognition system.
    """
    print("\n" + "="*60)
    print("🔊 ENHANCED SPEECH RECOGNITION TEST")
    print("="*60)
    
    try:
        engine = EnhancedVoiceEngine()
        
        print("\nThis test demonstrates:")
        print("• Automatic retry on failure")
        print("• Specific error messages") 
        print("• User guidance throughout")
        print("• Graceful fallback options")
        
        engine.speak("Welcome to the enhanced speech recognition test. Please say a simple command like deploy a server or create a database.")
        
        print("\n" + "="*60)
        print("🎤 TESTING SPEECH RECOGNITION")
        print("="*60)
        
        success, result = engine.listen_with_retry(max_retries=2)
        
        print("\n" + "="*60)
        print("📊 TEST RESULTS")
        print("="*60)
        
        if success:
            engine.speak(f"Perfect! I understood your command: {result}")
            print(f"✅ FINAL RESULT: '{result}'")
            print("✅ Enhanced speech recognition working correctly!")
        else:
            engine.speak("I'll switch to text input mode now.")
            print(f"❌ RECOGNITION FAILED: {result}")
            print("⚠️  System will fall back to text input")
        
        print("="*60 + "\n")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    try:
        success = test_enhanced_speech_recognition()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)