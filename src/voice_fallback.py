# voice_fallback.py - Enhanced Version
# Intelligent automatic fallback with retry logic and error recovery

import random
import time

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    recognizer = sr.Recognizer()
except ImportError:
    SPEECH_AVAILABLE = False


class VoiceRecognitionResult:
    """Store voice recognition results with metadata."""
    
    def __init__(self, success, text=None, confidence=None, error=None, method="voice"):
        self.success = success
        self.text = text
        self.confidence = confidence
        self.error = error
        self.method = method  # 'voice', 'text_fallback', 'manual_correction'
    
    def __repr__(self):
        if self.success:
            return f"Success: {self.text} ({self.confidence:.0%} confidence)"
        return f"Failed: {self.error}"


def real_voice_recognition(timeout=10):
    """
    Actual voice recognition using microphone.
    Returns VoiceRecognitionResult object.
    """
    if not SPEECH_AVAILABLE:
        return VoiceRecognitionResult(
            success=False,
            error="Speech recognition library not installed",
            method="unavailable"
        )
    
    try:
        with sr.Microphone() as source:
            print("\n🔧 Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("🔊 [●REC] Listening... Speak now!")
            
            # Listen with timeout
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            
            print("✅ Audio captured!")
        
        # Convert to text
        print("🔄 Processing speech...")
        
        try:
            text = recognizer.recognize_google(audio)
            
            # Google doesn't provide confidence score directly
            # Estimate based on text length and clarity
            confidence = min(0.95, 0.7 + (len(text) / 100))
            
            return VoiceRecognitionResult(
                success=True,
                text=text,
                confidence=confidence,
                method="voice"
            )
            
        except sr.UnknownValueError:
            return VoiceRecognitionResult(
                success=False,
                error="Could not understand audio - speech unclear",
                method="voice"
            )
            
        except sr.RequestError as e:
            return VoiceRecognitionResult(
                success=False,
                error=f"API service error: {str(e)}",
                method="voice"
            )
    
    except sr.WaitTimeoutError:
        return VoiceRecognitionResult(
            success=False,
            error="Timeout - no speech detected",
            method="voice"
        )
    
    except Exception as e:
        return VoiceRecognitionResult(
            success=False,
            error=f"Microphone error: {str(e)}",
            method="voice"
        )


def simulate_voice_recognition(user_input):
    """
    Simulate voice recognition with realistic failure scenarios.
    Used when real speech recognition is not available.
    """
    # Various realistic scenarios
    scenarios = [
        {"success": True, "text": user_input, "confidence": 0.95, "error": None},
        {"success": True, "text": user_input, "confidence": 0.92, "error": None},
        {"success": True, "text": user_input, "confidence": 0.78, "error": None},
        {"success": False, "text": None, "confidence": None, "error": "Background noise too loud"},
        {"success": False, "text": None, "confidence": None, "error": "Speech too fast - please slow down"},
        {"success": False, "text": None, "confidence": None, "error": "Unclear pronunciation detected"},
        {"success": False, "text": None, "confidence": None, "error": "Microphone connection lost"},
        {"success": True, "text": user_input, "confidence": 0.85, "error": None},
    ]
    
    # Higher chance of success (70%)
    scenario = random.choices(
        scenarios,
        weights=[15, 15, 10, 5, 5, 5, 5, 10],
        k=1
    )[0]
    
    # Simulate processing time
    time.sleep(random.uniform(0.5, 1.5))
    
    return VoiceRecognitionResult(
        success=scenario["success"],
        text=scenario["text"],
        confidence=scenario["confidence"],
        error=scenario["error"],
        method="simulated_voice"
    )


def voice_input_with_smart_fallback(prompt, max_retries=2, auto_fallback=True):
    """
    Intelligent voice input with automatic fallback and retry logic.
    
    Args:
        prompt: The prompt to show user
        max_retries: Maximum voice recognition attempts before fallback
        auto_fallback: Automatically fall back to text on failure
    
    Returns:
        Tuple of (text, method_used)
    """
    print("\n" + "="*60)
    print(f"🎤 VOICE INPUT: {prompt}")
    print("="*60)
    
    attempt = 0
    
    while attempt < max_retries:
        attempt += 1
        
        if attempt > 1:
            print(f"\n🔄 Retry attempt {attempt} of {max_retries}")
        
        # Wait for user to be ready
        ready = input("\n✅ Press Enter when ready to speak (or 't' for text, 'c' to cancel): ").strip().lower()
        
        if ready == 'c':
            print("❌ Input cancelled")
            return None, "cancelled"
        
        if ready == 't':
            print("⌨️  User chose text input")
            return text_input_fallback(prompt)
        
        # Try voice recognition
        if SPEECH_AVAILABLE:
            result = real_voice_recognition()
        else:
            # Simulation mode
            print("🔊 [SIMULATION] Listening...")
            what_user_said = input("(Type what you would say): ").strip()
            
            if not what_user_said:
                print("❌ No input provided")
                continue
            
            result = simulate_voice_recognition(what_user_said)
        
        # Handle result
        if result.success:
            print(f"\n✅ Voice recognized!")
            print(f"📝 Transcription: \"{result.text}\"")
            print(f"📊 Confidence: {result.confidence:.0%}")
            
            # Low confidence - ask for verification
            if result.confidence < 0.80:
                print("\n⚠️  Low confidence detected")
                print("💡 Please verify the transcription")
                
                verify = input(f"\nIs this correct: '{result.text}'? (y/n/edit): ").lower()
                
                if verify == 'y':
                    return result.text, "voice_verified"
                
                elif verify == 'edit':
                    print("\n✏️  Manual correction:")
                    corrected = input(f"[{result.text}]: ").strip()
                    final_text = corrected if corrected else result.text
                    return final_text, "voice_corrected"
                
                else:
                    if attempt < max_retries:
                        print(f"\n🔄 Let's try again ({max_retries - attempt} attempts remaining)")
                        continue
                    else:
                        if auto_fallback:
                            print("\n⚠️  Max retries reached - switching to text input")
                            return text_input_fallback(prompt)
                        return None, "max_retries"
            
            else:
                # High confidence - accept immediately
                return result.text, "voice"
        
        else:
            # Voice recognition failed
            print(f"\n❌ Voice recognition failed!")
            print(f"📛 Error: {result.error}")
            
            # Show helpful tips based on error
            show_troubleshooting_tips(result.error)
            
            if attempt < max_retries:
                retry = input(f"\n🔄 Try again? ({max_retries - attempt} attempts remaining) (y/n): ").lower()
                if retry != 'y':
                    if auto_fallback:
                        print("\n⌨️  Switching to text input...")
                        return text_input_fallback(prompt)
                    return None, "user_cancelled"
            else:
                if auto_fallback:
                    print(f"\n⚠️  Max retries ({max_retries}) reached")
                    print("🔄 Automatic fallback to text input...")
                    return text_input_fallback(prompt)
                return None, "max_retries"
    
    # Should not reach here, but just in case
    if auto_fallback:
        return text_input_fallback(prompt)
    return None, "failed"


def show_troubleshooting_tips(error):
    """Show context-specific troubleshooting tips."""
    tips = {
        "noise": [
            "💡 Move to a quieter location",
            "💡 Close windows and doors",
            "💡 Mute notifications and other apps"
        ],
        "unclear": [
            "💡 Speak more clearly and slowly",
            "💡 Move closer to the microphone",
            "💡 Avoid mumbling or trailing off"
        ],
        "timeout": [
            "💡 Start speaking immediately after the beep",
            "💡 Don't pause for too long mid-sentence",
            "💡 Keep responses concise"
        ],
        "microphone": [
            "💡 Check microphone is connected",
            "💡 Check microphone permissions",
            "💡 Try a different microphone"
        ],
        "fast": [
            "💡 Slow down your speech",
            "💡 Pause between words",
            "💡 Enunciate clearly"
        ]
    }
    
    error_lower = error.lower()
    
    print("\n💡 TROUBLESHOOTING TIPS:")
    
    if "noise" in error_lower:
        for tip in tips["noise"]:
            print(f"   {tip}")
    elif "unclear" in error_lower or "understand" in error_lower:
        for tip in tips["unclear"]:
            print(f"   {tip}")
    elif "timeout" in error_lower:
        for tip in tips["timeout"]:
            print(f"   {tip}")
    elif "microphone" in error_lower or "connection" in error_lower:
        for tip in tips["microphone"]:
            print(f"   {tip}")
    elif "fast" in error_lower:
        for tip in tips["fast"]:
            print(f"   {tip}")
    else:
        print("   💡 Speak clearly and slowly")
        print("   💡 Reduce background noise")
        print("   💡 Check microphone connection")


def text_input_fallback(prompt):
    """
    Text input fallback mode.
    Returns tuple of (text, method).
    """
    print("\n" + "="*60)
    print("⌨️  TEXT INPUT FALLBACK MODE")
    print("="*60)
    print(f"\n{prompt}")
    print("💡 Type your response below:")
    
    text = input("\nYour input: ").strip()
    
    if text:
        print(f"\n✅ Text input received: \"{text}\"")
        return text, "text_fallback"
    else:
        print("\n❌ No input provided")
        return None, "empty"


def display_input_statistics(stats):
    """Display statistics about input methods used."""
    print("\n" + "="*60)
    print("   📊 INPUT METHODS STATISTICS")
    print("="*60)
    
    total = sum(stats.values())
    
    if total == 0:
        print("No inputs recorded yet")
        return
    
    print(f"\nTotal inputs: {total}\n")
    
    methods = {
        "voice": "🎤 Voice (high confidence)",
        "voice_verified": "🎤 Voice (user verified)",
        "voice_corrected": "✏️  Voice (manually corrected)",
        "text_fallback": "⌨️  Text fallback",
        "cancelled": "❌ Cancelled"
    }
    
    for method, count in stats.items():
        if count > 0:
            percentage = (count / total) * 100
            label = methods.get(method, method)
            print(f"  {label}: {count} ({percentage:.1f}%)")
    
    # Calculate success rate
    voice_success = stats.get("voice", 0) + stats.get("voice_verified", 0) + stats.get("voice_corrected", 0)
    if total > 0:
        success_rate = (voice_success / total) * 100
        print(f"\n✅ Voice recognition success rate: {success_rate:.1f}%")
    
    print("="*60)


def main_fallback_flow():
    """Main flow with smart fallback system."""
    print("\n" + "="*60)
    print("   🎤 SMART VOICE FALLBACK SYSTEM")
    print("   Automatic Text Fallback on Voice Failure")
    print("="*60)
    
    # Check speech recognition availability
    if SPEECH_AVAILABLE:
        print("\n✅ Real speech recognition ENABLED")
        print("💡 Your microphone will be used for voice input")
    else:
        print("\n⚠️  Speech recognition not available")
        print("💡 Install: pip install SpeechRecognition pyaudio")
        print("📝 Running in SIMULATION mode")
    
    print("\n" + "="*60)
    
    # Statistics tracking
    input_stats = {
        "voice": 0,
        "voice_verified": 0,
        "voice_corrected": 0,
        "text_fallback": 0,
        "cancelled": 0
    }
    
    # Configuration
    print("\n⚙️  FALLBACK SETTINGS:")
    print("  • Max voice retries: 2")
    print("  • Auto text fallback: Enabled")
    print("  • Confidence threshold: 80%")
    
    input("\n✅ Press Enter to start...")
    
    session_count = 0
    
    while True:
        session_count += 1
        print("\n" + "🔷"*30)
        print(f"   SESSION #{session_count}")
        print("🔷"*30)
        
        # Get infrastructure request
        infrastructure, method = voice_input_with_smart_fallback(
            "Describe the infrastructure you need",
            max_retries=2,
            auto_fallback=True
        )
        
        if infrastructure:
            input_stats[method] = input_stats.get(method, 0) + 1
            print(f"\n🎯 CAPTURED: \"{infrastructure}\"")
            print(f"📝 Method used: {method}")
        else:
            print("\n❌ No input captured")
            input_stats["cancelled"] = input_stats.get("cancelled", 0) + 1
        
        # Ask if user wants to continue
        print("\n" + "─"*60)
        continue_choice = input("\n➡️  Continue with another input? (y/stats/quit): ").lower()
        
        if continue_choice == 'stats':
            display_input_statistics(input_stats)
            continue_choice = input("\nContinue? (y/n): ").lower()
        
        if continue_choice != 'y':
            break
    
    # Final statistics
    print("\n" + "="*60)
    print("   SESSION COMPLETE")
    print("="*60)
    
    display_input_statistics(input_stats)
    
    print("\n👋 Thank you for testing the smart fallback system!")


if __name__ == "__main__":
    try:
        main_fallback_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")