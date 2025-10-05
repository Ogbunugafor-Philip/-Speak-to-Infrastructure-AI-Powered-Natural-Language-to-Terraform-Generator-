"""
voice_prompt_cloud_provider.py - Enhanced Version
---------------------------------
Advanced voice-based prompting for cloud provider selection.
Features: Smart recognition, fuzzy matching, text fallback, and confirmation.
"""

import time

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  SpeechRecognition not available. Install: pip install SpeechRecognition pyaudio")

# Try to import text-to-speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("⚠️  pyttsx3 not available. Install: pip install pyttsx3")


class EnhancedVoiceEngine:
    """Enhanced voice recognition engine with fallback options."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer() if SPEECH_AVAILABLE else None
        self.mic_available = self._check_microphone()
        
    def _check_microphone(self):
        """Check if microphone is available."""
        if not SPEECH_AVAILABLE:
            return False
        
        try:
            with sr.Microphone() as source:
                return True
        except Exception:
            return False
    
    def listen(self, timeout=10, phrase_limit=15, prompt="Listening..."):
        """
        Listen for speech input with timeout and error handling.
        
        Returns:
            Tuple of (success, text, confidence, error_message)
        """
        if not SPEECH_AVAILABLE or not self.mic_available:
            return False, None, 0.0, "Microphone not available"
        
        try:
            with sr.Microphone() as source:
                print(f"\n🎤 {prompt}")
                print("🔧 Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("🔴 Speak now!")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
                
                print("✅ Audio captured! Processing...")
            
            # Convert to text
            text = self.recognizer.recognize_google(audio)
            confidence = 0.85  # Google doesn't provide confidence
            
            return True, text, confidence, None
            
        except sr.WaitTimeoutError:
            return False, None, 0.0, "Timeout - no speech detected"
        except sr.UnknownValueError:
            return False, None, 0.0, "Could not understand speech"
        except sr.RequestError as e:
            return False, None, 0.0, f"API error: {e}"
        except Exception as e:
            return False, None, 0.0, f"Error: {e}"


class AdvancedTTSEngine:
    """Advanced text-to-speech engine with fallback to text display."""
    
    def __init__(self):
        self.engine = None
        self.tts_enabled = False
        
        if TTS_AVAILABLE:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)  # Speed
                self.engine.setProperty('volume', 0.9)  # Volume
                self.tts_enabled = True
            except Exception as e:
                print(f"⚠️  TTS initialization failed: {e}")
    
    def speak(self, text, also_print=True):
        """
        Speak text using TTS, with fallback to text display.
        
        Args:
            text: Text to speak
            also_print: Whether to also print the text
        """
        if also_print or not self.tts_enabled:
            print(f"\n🔊 {text}")
        
        if self.tts_enabled and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"⚠️  TTS error: {e}")


class VoiceConfirmationSystem:
    """System for confirming voice inputs with multiple methods."""
    
    def __init__(self, voice_engine, tts_engine):
        self.voice_engine = voice_engine
        self.tts_engine = tts_engine
    
    def get_confirmation(self, prompt="Is that correct?", allow_text_fallback=True):
        """
        Get yes/no confirmation via voice or text.
        
        Returns:
            Tuple of (confirmed: bool, method: str)
        """
        self.tts_engine.speak(prompt)
        
        # Try voice first
        success, response, confidence, error = self.voice_engine.listen(
            timeout=5,
            prompt="Say 'yes' or 'no'"
        )
        
        if success and response:
            response_lower = response.lower().strip()
            
            # Check for affirmative responses
            if any(word in response_lower for word in ['yes', 'yeah', 'yep', 'correct', 'right', 'confirm']):
                return True, "voice"
            
            # Check for negative responses
            if any(word in response_lower for word in ['no', 'nope', 'wrong', 'incorrect', 'cancel']):
                return False, "voice"
            
            # Unclear response
            self.tts_engine.speak("I didn't understand. Please say yes or no clearly.")
            return self.get_confirmation(prompt, allow_text_fallback)
        
        # Voice failed, try text fallback
        if allow_text_fallback:
            self.tts_engine.speak("I couldn't hear you. Let me ask via text.")
            print("\n⌨️  Text fallback mode")
            text_response = input("Is that correct? (y/n): ").strip().lower()
            
            if text_response in ['y', 'yes', 'yeah', 'yep']:
                return True, "text_fallback"
            elif text_response in ['n', 'no', 'nope']:
                return False, "text_fallback"
            else:
                print("❌ Invalid response. Please enter 'y' or 'n'.")
                return self.get_confirmation(prompt, allow_text_fallback)
        
        return False, "error"


class CloudProviderSelector:
    """Main class for cloud provider selection with voice and text support."""
    
    def __init__(self):
        self.voice_engine = EnhancedVoiceEngine()
        self.tts_engine = AdvancedTTSEngine()
        self.confirmation_system = VoiceConfirmationSystem(self.voice_engine, self.tts_engine)
        
        # Provider mapping with fuzzy matching support
        self.provider_map = {
            # AWS variations
            "aws": "AWS",
            "amazon": "AWS",
            "amazon web services": "AWS",
            "amazon web service": "AWS",
            
            # Azure variations
            "azure": "Azure",
            "microsoft azure": "Azure",
            "microsoft": "Azure",
            "asher": "Azure",  # Common misrecognition
            "easier": "Azure",  # Common misrecognition
            
            # GCP variations
            "gcp": "GCP",
            "google cloud": "GCP",
            "google cloud platform": "GCP",
            "google": "GCP",
            "g c p": "GCP",
        }
        
        self.provider_info = {
            "AWS": {
                "full_name": "Amazon Web Services",
                "description": "The most widely used cloud platform",
                "icon": "🟧"
            },
            "Azure": {
                "full_name": "Microsoft Azure",
                "description": "Microsoft's cloud computing platform",
                "icon": "🔵"
            },
            "GCP": {
                "full_name": "Google Cloud Platform",
                "description": "Google's cloud infrastructure",
                "icon": "🔴"
            }
        }
        
        self.max_retries = 3
    
    def show_provider_options(self, show_voice=True):
        """Display available cloud provider options."""
        print("\n" + "═"*60)
        print("   ☁️  CLOUD PROVIDER SELECTION")
        print("═"*60)
        print("\nAvailable providers:\n")
        
        for i, (key, info) in enumerate(self.provider_info.items(), 1):
            print(f"  {info['icon']} {i}. {key} - {info['full_name']}")
            print(f"      {info['description']}")
        
        if show_voice:
            print("\n💡 Say: 'AWS', 'Azure', or 'GCP'")
            print("   Or: 'Amazon', 'Microsoft', or 'Google'")
        
        print("═"*60)
    
    def parse_provider_response(self, response):
        """
        Parse user response to determine cloud provider.
        
        Args:
            response: User's voice or text input
        
        Returns:
            Provider name (AWS/Azure/GCP) or None
        """
        if not response:
            return None
        
        response_lower = response.lower().strip()
        
        # Direct match
        for key, provider in self.provider_map.items():
            if key in response_lower:
                return provider
        
        # Fuzzy match for common misrecognitions
        if "amaz" in response_lower or "a w s" in response_lower:
            return "AWS"
        if "asure" in response_lower or "azur" in response_lower:
            return "Azure"
        if "googl" in response_lower or "gee" in response_lower:
            return "GCP"
        
        return None
    
    def ask_with_voice(self, attempt=1):
        """
        Ask for cloud provider using voice input.
        
        Returns:
            Tuple of (success, provider, method)
        """
        if attempt > self.max_retries:
            self.tts_engine.speak(f"Maximum attempts ({self.max_retries}) reached. Switching to text input.")
            return False, None, "max_retries"
        
        if attempt > 1:
            print(f"\n🔄 Attempt {attempt} of {self.max_retries}")
        
        # Ask the question
        self.tts_engine.speak("Which cloud provider would you like to use? You can say AWS, Azure, or GCP.")
        
        # Listen for response
        success, response, confidence, error = self.voice_engine.listen(
            timeout=10,
            prompt="Listening for your choice..."
        )
        
        if not success:
            print(f"❌ Voice input failed: {error}")
            
            if attempt < self.max_retries:
                self.tts_engine.speak("I didn't hear you clearly. Let's try again.")
                time.sleep(1)
                return self.ask_with_voice(attempt + 1)
            else:
                return False, None, "voice_failed"
        
        # Parse the response
        print(f"\n📝 You said: \"{response}\"")
        print(f"📊 Confidence: {confidence:.0%}")
        
        selected_provider = self.parse_provider_response(response)
        
        if not selected_provider:
            print("❌ Could not identify a valid cloud provider")
            self.tts_engine.speak("I didn't catch a valid cloud provider. Please say AWS, Azure, or GCP.")
            
            if attempt < self.max_retries:
                time.sleep(1)
                return self.ask_with_voice(attempt + 1)
            else:
                return False, None, "invalid_response"
        
        # Confirm the selection
        info = self.provider_info[selected_provider]
        print(f"\n✅ Recognized: {info['icon']} {selected_provider} - {info['full_name']}")
        
        self.tts_engine.speak(f"You selected {selected_provider}. Is that correct?")
        
        confirmed, confirm_method = self.confirmation_system.get_confirmation()
        
        if confirmed:
            self.tts_engine.speak(f"Great! {selected_provider} selected.")
            return True, selected_provider, f"voice_{confirm_method}"
        else:
            self.tts_engine.speak("Okay, let's try again.")
            time.sleep(1)
            return self.ask_with_voice(attempt + 1)
    
    def ask_with_text(self):
        """
        Ask for cloud provider using text input.
        
        Returns:
            Tuple of (success, provider, method)
        """
        print("\n⌨️  TEXT INPUT MODE")
        self.show_provider_options(show_voice=False)
        
        print("\n💡 Enter: 'AWS', 'Azure', 'GCP', or the number (1-3)")
        
        while True:
            response = input("\nYour choice: ").strip()
            
            # Check for number input
            if response in ['1']:
                selected_provider = 'AWS'
            elif response in ['2']:
                selected_provider = 'Azure'
            elif response in ['3']:
                selected_provider = 'GCP'
            else:
                # Parse text input
                selected_provider = self.parse_provider_response(response)
            
            if not selected_provider:
                print("❌ Invalid input. Please enter AWS, Azure, GCP, or 1-3.")
                continue
            
            # Confirm selection
            info = self.provider_info[selected_provider]
            print(f"\n✅ You selected: {info['icon']} {selected_provider} - {info['full_name']}")
            
            confirm = input("Is this correct? (y/n): ").strip().lower()
            
            if confirm in ['y', 'yes']:
                return True, selected_provider, "text_direct"
            elif confirm in ['n', 'no']:
                print("\n🔄 Let's try again...")
                continue
            else:
                print("❌ Please enter 'y' or 'n'")
    
    def ask_cloud_provider(self, prefer_voice=True):
        """
        Main method to ask for cloud provider with hybrid approach.
        
        Args:
            prefer_voice: Whether to try voice first
        
        Returns:
            Selected cloud provider (AWS/Azure/GCP)
        """
        print("\n" + "╔"*60)
        print("║" + " ☁️  CLOUD PROVIDER SELECTION ".center(118) + "║")
        print("╚"*60)
        
        # Check if voice is available
        if prefer_voice and SPEECH_AVAILABLE and self.voice_engine.mic_available:
            print("\n🎤 Voice input is AVAILABLE")
            print("💡 You can speak or type your choice")
            
            choice = input("\n❓ Use voice input? (y/n/skip): ").strip().lower()
            
            if choice in ['y', 'yes']:
                self.show_provider_options(show_voice=True)
                success, provider, method = self.ask_with_voice()
                
                if success:
                    return provider
                
                # Voice failed, offer text fallback
                print("\n⚠️  Voice input unsuccessful")
                fallback = input("Switch to text input? (y/n): ").strip().lower()
                
                if fallback in ['y', 'yes']:
                    success, provider, method = self.ask_with_text()
                    return provider
                else:
                    print("❌ Provider selection cancelled")
                    return None
        
        # Use text input
        print("\n⌨️  Using text input mode")
        success, provider, method = self.ask_with_text()
        return provider


def ask_cloud_provider():
    """Main function to ask for cloud provider."""
    selector = CloudProviderSelector()
    return selector.ask_cloud_provider(prefer_voice=True)


if __name__ == "__main__":
    print("\n" + "╔"*60)
    print("║" + " 🎤 VOICE-ENABLED CLOUD PROVIDER SELECTION ".center(118) + "║")
    print("╚"*60)
    
    try:
        provider = ask_cloud_provider()
        
        if provider:
            print("\n" + "═"*60)
            print("   ✅ SELECTION COMPLETE")
            print("═"*60)
            print(f"\n☁️  Selected Cloud Provider: {provider}")
            
            selector = CloudProviderSelector()
            info = selector.provider_info[provider]
            print(f"📋 Full Name: {info['full_name']}")
            print(f"📝 Description: {info['description']}")
            print("\n" + "═"*60)
        else:
            print("\n❌ No provider selected")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Selection cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")