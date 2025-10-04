# voice_engine.py
import speech_recognition as sr
import pyttsx3
from typing import Optional, Tuple
import sys

class VoiceEngine:
    """
    Handles all voice-related functionality: listening and speaking.
    This is our reusable voice engine.
    """
    
    def __init__(self, rate: int = 180, volume: float = 0.9):
        """
        Initialize the voice engine with speech recognition and text-to-speech.
        
        Args:
            rate: Speech speed (words per minute), default 180
            volume: Volume level (0.0 to 1.0), default 0.9
        """
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            
            # Configure recognizer settings for better accuracy
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Check if microphone is available
            try:
                self.microphone = sr.Microphone()
                print("✅ Microphone detected and ready")
            except OSError as e:
                print(f"⚠️  Warning: Microphone initialization issue: {e}")
                self.microphone = None
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self.tts_engine.setProperty('rate', rate)
            self.tts_engine.setProperty('volume', volume)
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                print(f"✅ TTS engine initialized with voice: {voices[0].name}")
            
            print("🎤 Voice engine initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing voice engine: {e}")
            raise
    
    def listen_to_speech(
        self, 
        timeout: int = 10, 
        phrase_time_limit: int = 15,
        ambient_duration: float = 1.0
    ) -> Tuple[bool, str]:
        """
        Listen to microphone input and convert speech to text.
        
        Args:
            timeout: How long to wait for speech to start (seconds)
            phrase_time_limit: Maximum length of speech (seconds)
            ambient_duration: How long to adjust for ambient noise (seconds)
            
        Returns:
            Tuple of (success: bool, text: str)
            - success: True if speech was recognized, False otherwise
            - text: Recognized text if successful, error message if not
        """
        if self.microphone is None:
            return False, "Microphone not available. Please check your hardware."
        
        try:
            # Adjust for ambient noise each time we listen
            print("\n🎤 Adjusting for ambient noise... Please wait.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=ambient_duration)
                print(f"   Energy threshold set to: {self.recognizer.energy_threshold}")
            
            print("🎤 Listening... Please speak now.")
            print("   (Speak clearly, then pause)")
            
            # Listen for audio input
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("✅ Audio captured. Processing...")
            
            # Convert speech to text using Google's service
            text = self.recognizer.recognize_google(audio)
            
            if not text.strip():
                return False, "No speech content detected."
            
            return True, text.strip()
            
        except sr.WaitTimeoutError:
            return False, "No speech detected within the timeout period."
        except sr.UnknownValueError:
            return False, "Sorry, I could not understand what you said."
        except sr.RequestError as e:
            return False, f"Error with speech recognition service: {e}"
        except OSError as e:
            return False, f"Microphone access error: {e}"
        except Exception as e:
            return False, f"Unexpected error: {e}"
    
    def speak(self, text: str, wait: bool = True) -> bool:
        """
        Convert text to speech and speak it out loud.
        
        Args:
            text: The text to speak
            wait: If True, wait for speech to complete. If False, speak asynchronously.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  Warning: No text provided to speak")
            return False
        
        try:
            print(f"🔊 Speaking: {text}")
            self.tts_engine.say(text)
            
            if wait:
                self.tts_engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Error with text-to-speech: {e}")
            return False
    
    def stop_speaking(self):
        """
        Stop any ongoing speech immediately.
        """
        try:
            self.tts_engine.stop()
            print("⏹️  Speech stopped")
        except Exception as e:
            print(f"❌ Error stopping speech: {e}")
    
    def set_voice(self, voice_index: int = 0) -> bool:
        """
        Change the TTS voice.
        
        Args:
            voice_index: Index of the voice to use (0 = default)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            voices = self.tts_engine.getProperty('voices')
            
            if not voices:
                print("❌ No voices available")
                return False
            
            if voice_index >= len(voices):
                print(f"❌ Voice index {voice_index} out of range (max: {len(voices)-1})")
                return False
            
            self.tts_engine.setProperty('voice', voices[voice_index].id)
            print(f"✅ Voice changed to: {voices[voice_index].name}")
            return True
            
        except Exception as e:
            print(f"❌ Error changing voice: {e}")
            return False
    
    def list_available_voices(self):
        """
        Display all available TTS voices.
        """
        try:
            voices = self.tts_engine.getProperty('voices')
            
            if not voices:
                print("❌ No voices available")
                return
            
            print("\n🗣️  Available Voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name}")
                print(f"     ID: {voice.id}")
                if hasattr(voice, 'languages'):
                    print(f"     Languages: {voice.languages}")
                print()
                
        except Exception as e:
            print(f"❌ Error listing voices: {e}")
    
    def adjust_settings(self, rate: Optional[int] = None, volume: Optional[float] = None):
        """
        Adjust TTS settings on the fly.
        
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


# Create a global instance that we can import elsewhere
# This allows: from voice_engine import voice_engine
try:
    voice_engine = VoiceEngine()
except Exception as e:
    print(f"⚠️  Warning: Could not create global voice_engine instance: {e}")
    voice_engine = None


# Test function
def test_voice_engine():
    """
    Test the complete voice engine functionality.
    """
    print("\n" + "="*50)
    print("🔊 VOICE ENGINE TEST")
    print("="*50)
    
    try:
        # Create a new instance for testing
        engine = VoiceEngine()
        
        # List available voices
        engine.list_available_voices()
        
        # Test speaking first
        print("\n📢 Testing text-to-speech...")
        engine.speak("Hello! I am testing the voice engine. Please say something after the beep.")
        
        # Test listening
        print("\n🎤 Now testing speech recognition...")
        print("💡 Tip: Speak clearly after you hear the 'Listening' message")
        
        success, result = engine.listen_to_speech()
        
        if success:
            print(f"\n{'='*50}")
            print(f"✅ SUCCESS! I heard: '{result}'")
            print(f"{'='*50}")
            engine.speak(f"I heard you say: {result}")
        else:
            print(f"\n{'='*50}")
            print(f"❌ FAILED: {result}")
            print(f"{'='*50}")
            engine.speak("Sorry, I didn't catch that.")
        
        print("\n" + "="*50)
        print("✅ VOICE ENGINE TEST COMPLETE")
        print("="*50 + "\n")
        
        return success
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    try:
        success = test_voice_engine()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)