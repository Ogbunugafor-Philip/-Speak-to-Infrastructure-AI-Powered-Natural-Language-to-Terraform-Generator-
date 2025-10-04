# advanced_tts_engine.py
"""
Advanced Text-to-Speech Engine with natural sounding responses
and infrastructure-specific voice personality.
"""

import pyttsx3
from typing import List, Optional, Dict
import sys
import time

class AdvancedTTSEngine:
    """
    Enhanced text-to-speech system with:
    - Natural pacing and pauses
    - Infrastructure-specific vocabulary emphasis
    - Multiple voice options
    - Response types for different situations
    - Robust error handling
    """
    
    def __init__(self, rate: int = 165, volume: float = 0.85, voice_index: int = 0):
        """
        Initialize the advanced TTS engine.
        
        Args:
            rate: Speech rate in words per minute (default: 165)
            volume: Volume level from 0.0 to 1.0 (default: 0.85)
            voice_index: Index of voice to use (default: 0)
        """
        try:
            self.engine = pyttsx3.init()
            
            # Get available voices
            self.voices = self.engine.getProperty('voices')
            
            if not self.voices:
                raise RuntimeError("No TTS voices available on this system")
            
            # Validate and set voice index
            if 0 <= voice_index < len(self.voices):
                self.current_voice_index = voice_index
            else:
                print(f"⚠️  Warning: Invalid voice index {voice_index}, using default (0)")
                self.current_voice_index = 0
            
            # Store default settings
            self.default_rate = rate
            self.default_volume = volume
            
            # Configure default voice settings for clarity
            self._configure_voice()
            
            print("🔊 Advanced TTS Engine initialized!")
            print(f"   Available voices: {len(self.voices)}")
            print(f"   Current voice: {self.voices[self.current_voice_index].name}")
            print(f"   Rate: {rate} WPM, Volume: {volume * 100:.0f}%")
            
        except Exception as e:
            print(f"❌ Error initializing TTS engine: {e}")
            raise
    
    def _configure_voice(self):
        """Configure voice settings for optimal clarity"""
        try:
            self.engine.setProperty('rate', self.default_rate)
            self.engine.setProperty('volume', self.default_volume)
            self.engine.setProperty('voice', self.voices[self.current_voice_index].id)
        except Exception as e:
            print(f"❌ Error configuring voice: {e}")
    
    def list_voices(self) -> List[Dict[str, str]]:
        """
        Display all available voices and return voice information.
        
        Returns:
            List of dictionaries containing voice information
        """
        print("\n🗣️  AVAILABLE VOICES:")
        print("-" * 50)
        
        voice_info = []
        
        for i, voice in enumerate(self.voices):
            status = "✓ CURRENT" if i == self.current_voice_index else ""
            
            # Extract voice details safely
            name = getattr(voice, 'name', 'Unknown')
            voice_id = getattr(voice, 'id', 'Unknown')
            languages = getattr(voice, 'languages', ['Not specified'])
            gender = getattr(voice, 'gender', 'Unknown')
            
            print(f"{i}: {name} {status}")
            print(f"   ID: {voice_id}")
            print(f"   Gender: {gender}")
            print(f"   Languages: {languages}")
            print()
            
            voice_info.append({
                'index': i,
                'name': name,
                'id': voice_id,
                'languages': languages,
                'gender': gender,
                'current': i == self.current_voice_index
            })
        
        return voice_info
    
    def set_voice(self, voice_index: int) -> bool:
        """
        Change to a specific voice.
        
        Args:
            voice_index: Index of the voice to use
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 0 <= voice_index < len(self.voices):
            self.current_voice_index = voice_index
            self.engine.setProperty('voice', self.voices[voice_index].id)
            print(f"✅ Voice changed to: {self.voices[voice_index].name}")
            return True
        else:
            print(f"❌ Invalid voice index: {voice_index} (valid range: 0-{len(self.voices)-1})")
            return False
    
    def speak_infrastructure_response(
        self, 
        text: str, 
        response_type: str = "normal",
        wait: bool = True
    ) -> bool:
        """
        Speak with infrastructure-appropriate tone and pacing.
        
        Args:
            text: The text to speak
            response_type: Type of response - affects tone and pacing
                - "normal": Regular confirmation
                - "warning": Important notice
                - "success": Operation completed
                - "error": Something went wrong
                - "question": Asking for input
                - "processing": System is working
            wait: If True, wait for speech to complete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  Warning: No text to speak")
            return False
        
        # Add appropriate prefixes based on response type
        prefixes = {
            "normal": "",
            "warning": "Note: ",
            "success": "Success! ",
            "error": "Error: ",
            "question": "",
            "processing": "Working on it... "
        }
        
        # Adjust speech rate based on response type
        rate_adjustments = {
            "normal": 165,
            "warning": 155,      # Slower for important info
            "success": 175,      # Slightly faster for positive news
            "error": 150,        # Slower for errors
            "question": 160,     # Clear for questions
            "processing": 160
        }
        
        prefix = prefixes.get(response_type, "")
        full_text = prefix + text
        
        # Adjust rate for this message
        try:
            original_rate = self.engine.getProperty('rate')
            self.engine.setProperty('rate', rate_adjustments.get(response_type, 165))
            
            print(f"🔊 [{response_type.upper()}] {full_text}")
            
            self.engine.say(full_text)
            
            if wait:
                self.engine.runAndWait()
            
            return True
            
        except Exception as e:
            print(f"❌ Error speaking: {e}")
            return False
            
        finally:
            # Restore original rate
            try:
                self.engine.setProperty('rate', original_rate)
            except:
                pass
    
    def speak_with_pause(
        self, 
        text: str, 
        pause_words: Optional[List[str]] = None,
        pause_duration: str = "short"
    ) -> bool:
        """
        Speak text with natural pauses after specific words.
        This makes technical content easier to understand.
        
        Args:
            text: The text to speak
            pause_words: Words after which to insert pauses
            pause_duration: "short" (...) or "long" (,,,)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            print("⚠️  Warning: No text to speak")
            return False
        
        if pause_words is None:
            pause_words = ['then', 'next', 'after', 'finally', 'important', 'however', 'therefore']
        
        # Choose pause marker based on duration
        pause_marker = "... " if pause_duration == "short" else ",,, "
        
        # Add pauses after specific words for better comprehension
        words = text.split()
        processed_text = ""
        
        for i, word in enumerate(words):
            processed_text += word
            # Add pause after specific words (but not at the end)
            clean_word = word.lower().rstrip('.,!?;:')
            if clean_word in pause_words and i < len(words) - 1:
                processed_text += pause_marker
            else:
                processed_text += " "
        
        try:
            print(f"🔊 [WITH PAUSES] {text}")
            self.engine.say(processed_text.strip())
            self.engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"❌ Error speaking with pauses: {e}")
            return False
    
    def speak_list(
        self, 
        items: List[str], 
        intro: str = "Here are the items:",
        numbered: bool = True
    ) -> bool:
        """
        Speak a list of items with clear separation.
        
        Args:
            items: List of items to speak
            intro: Introduction text
            numbered: Whether to number the items
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not items:
            print("⚠️  Warning: No items to speak")
            return False
        
        try:
            # Speak intro
            if intro:
                self.engine.say(intro)
                self.engine.runAndWait()
                time.sleep(0.3)
            
            # Speak each item with brief pause
            for i, item in enumerate(items, 1):
                if numbered:
                    text = f"Number {i}. {item}"
                else:
                    text = item
                
                print(f"🔊 {text}")
                self.engine.say(text)
                self.engine.runAndWait()
                
                # Brief pause between items (except after last)
                if i < len(items):
                    time.sleep(0.2)
            
            return True
            
        except Exception as e:
            print(f"❌ Error speaking list: {e}")
            return False
    
    def stop(self):
        """Stop any ongoing speech immediately."""
        try:
            self.engine.stop()
            print("⏹️  Speech stopped")
        except Exception as e:
            print(f"❌ Error stopping speech: {e}")
    
    def adjust_settings(
        self, 
        rate: Optional[int] = None, 
        volume: Optional[float] = None
    ) -> bool:
        """
        Adjust TTS settings dynamically.
        
        Args:
            rate: New speech rate (words per minute)
            volume: New volume level (0.0 to 1.0)
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if rate is not None:
                self.engine.setProperty('rate', rate)
                self.default_rate = rate
                print(f"✅ Speech rate set to {rate} WPM")
            
            if volume is not None:
                if 0.0 <= volume <= 1.0:
                    self.engine.setProperty('volume', volume)
                    self.default_volume = volume
                    print(f"✅ Volume set to {volume * 100:.0f}%")
                else:
                    print("❌ Volume must be between 0.0 and 1.0")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error adjusting settings: {e}")
            return False


def test_advanced_tts():
    """
    Test the advanced TTS system with various response types.
    """
    print("\n" + "="*60)
    print("🔊 ADVANCED TEXT-TO-SPEECH TEST")
    print("="*60)
    
    try:
        tts = AdvancedTTSEngine()
        
        # Show available voices
        tts.list_voices()
        
        print("\n🎧 TESTING DIFFERENT RESPONSE TYPES:")
        print("="*60)
        
        # Test different response types
        test_responses = [
            ("normal", "The VPC has been configured with three subnets"),
            ("success", "Infrastructure deployment completed successfully"),
            ("warning", "This operation may incur costs on your cloud account"),
            ("error", "Failed to connect to the cloud provider"),
            ("question", "Which region would you like to deploy to?"),
            ("processing", "Generating Terraform configuration files"),
        ]
        
        for response_type, text in test_responses:
            print(f"\n▶ Testing '{response_type}' response...")
            tts.speak_infrastructure_response(text, response_type)
            time.sleep(0.5)  # Brief pause between tests
        
        print("\n🎧 TESTING NATURAL PACING:")
        print("="*60)
        
        # Test natural pacing with technical content
        technical_text = "First I will create the VPC then configure the subnets next set up security groups and finally deploy the instances"
        print(f"Technical text: {technical_text}")
        tts.speak_with_pause(technical_text)
        
        print("\n🎧 TESTING LIST SPEAKING:")
        print("="*60)
        
        # Test list speaking
        steps = [
            "Create VPC",
            "Configure subnets",
            "Set up security groups",
            "Deploy instances"
        ]
        tts.speak_list(steps, intro="Deployment steps are as follows:", numbered=True)
        
        print("\n" + "="*60)
        print("✅ ADVANCED TTS TEST COMPLETE!")
        print("="*60 + "\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


if __name__ == "__main__":
    try:
        success = test_advanced_tts()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)