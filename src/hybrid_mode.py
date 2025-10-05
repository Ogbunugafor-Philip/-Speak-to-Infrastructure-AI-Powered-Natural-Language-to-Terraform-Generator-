# hybrid_mode.py - Enhanced Version with REAL Speech Recognition
# Seamless voice/text mode switching with actual microphone input

import time
import random

# Try to import speech recognition library
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    recognizer = sr.Recognizer()
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  Speech recognition not available. Install with: pip install SpeechRecognition pyaudio")
    print("Running in simulation mode...")



class InteractionMode:
    """Manage interaction mode state and preferences."""
    
    def __init__(self):
        self.current_mode = "text"
        self.mode_history = []
        self.auto_switch_enabled = False
        self.voice_confidence_threshold = 0.8
        
    def get_mode(self):
        """Get current interaction mode."""
        return self.current_mode
    
    def set_mode(self, mode):
        """Set interaction mode and track history."""
        if mode in ["text", "voice", "auto"]:
            self.mode_history.append(self.current_mode)
            self.current_mode = mode
            return True
        return False
    
    def toggle_mode(self):
        """Toggle between voice and text modes."""
        if self.current_mode == "voice":
            self.set_mode("text")
        else:
            self.set_mode("voice")
    
    def get_mode_icon(self):
        """Get icon for current mode."""
        icons = {
            "text": "⌨️",
            "voice": "🎤",
            "auto": "🔄"
        }
        return icons.get(self.current_mode, "❓")


class InfrastructureConfig:
    """Store infrastructure configuration."""
    
    def __init__(self):
        self.cloud_provider = None
        self.resource_type = None
        self.details = {}
        self.mode_used = []
    
    def reset(self):
        """Reset configuration."""
        self.cloud_provider = None
        self.resource_type = None
        self.details = {}
        self.mode_used = []
    
    def add_mode_tracking(self, mode):
        """Track which mode was used for each input."""
        self.mode_used.append(mode)
    
    def display_summary(self):
        """Display configuration summary."""
        print("\n" + "="*60)
        print("   CONFIGURATION SUMMARY")
        print("="*60)
        print(f"Cloud Provider: {self.cloud_provider or 'Not set'}")
        print(f"Resource Type:  {self.resource_type or 'Not set'}")
        
        if self.details:
            print("\nDetails:")
            for key, value in self.details.items():
                print(f"  • {key}: {value}")
        
        if self.mode_used:
            print(f"\nInput modes used: {' → '.join(self.mode_used)}")
        
        print("="*60)


def display_mode_status(mode_manager):
    """Display current mode status bar."""
    mode = mode_manager.get_mode()
    icon = mode_manager.get_mode_icon()
    
    print("\n" + "─"*60)
    print(f"│ {icon} MODE: {mode.upper():<20} │ Press 'm' to switch modes │")
    print("─"*60)


def mode_selection_menu(current_mode):
    """Display mode selection menu."""
    print("\n" + "="*60)
    print("   🔄 INTERACTION MODE SELECTION")
    print("="*60)
    print(f"\nCurrent mode: {current_mode.upper()}")
    print("\nAvailable modes:\n")
    print("  [1/t] ⌨️  TEXT MODE - Type your commands")
    print("  [2/v] 🎤 VOICE MODE - Speak your commands (simulated)")
    print("  [3/a] 🔄 AUTO MODE - System chooses best mode")
    print("  [4/k] ✅ Keep current mode")
    print("-"*60)
    
    choice = input("\nSelect mode: ").strip().lower()
    
    mode_map = {
        '1': 'text', 't': 'text',
        '2': 'voice', 'v': 'voice',
        '3': 'auto', 'a': 'auto',
        '4': 'keep', 'k': 'keep'
    }
    
    return mode_map.get(choice, 'keep')


def simulate_voice_input(prompt):
    """
    Real voice input using microphone if available, otherwise simulation.
    """
    print(f"\n🎤 {prompt}")
    print("─"*60)
    
    if SPEECH_AVAILABLE:
        return real_voice_input(prompt)
    else:
        return simulated_voice_input(prompt)


def real_voice_input(prompt):
    """
    Actual speech recognition using microphone.
    """
    print("🎙️  Real microphone input enabled")
    print("\n💡 Get ready to speak into your microphone")
    
    # Wait for user to be ready
    ready = input("\n✅ Press Enter when ready to speak (or 'c' to cancel): ").strip().lower()
    
    if ready == 'c':
        print("❌ Voice input cancelled")
        return None
    
    try:
        with sr.Microphone() as source:
            print("\n🔴 RECORDING NOW - Speak clearly into your microphone!")
            print("─"*60)
            print("🎤 Listening... (will auto-stop after silence)")
            print("💡 Speak naturally - the system will detect when you're done")
            print("─"*60)
            
            # Adjust for ambient noise
            print("\n🔧 Calibrating for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Calibration complete!\n")
            
            print("🔊 [●REC] SPEAK NOW!\n")
            
            # Listen for speech (will automatically stop after silence)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            
            print("\n✅ Recording complete!")
        
        # Convert speech to text
        print("🔄 Converting speech to text...")
        print("⏳ Processing... please wait...")
        
        try:
            # Using Google's speech recognition
            text = recognizer.recognize_google(audio)
            
            print(f"\n📝 Transcription: \"{text}\"")
            
            # Verify with user
            verify = input("\n✅ Is this correct? (y/n/edit): ").lower()
            
            if verify == 'y':
                return text
            elif verify == 'edit':
                print("\n✏️  Edit the transcription:")
                edited = input(f"[{text}]: ").strip()
                return edited if edited else text
            else:
                print("\n🔄 Would you like to try recording again?")
                retry = input("(y/n): ").lower()
                if retry == 'y':
                    return real_voice_input(prompt)
                return None
                
        except sr.UnknownValueError:
            print("\n❌ Could not understand the audio")
            print("💡 Tips: Speak clearly, reduce background noise, speak louder")
            retry = input("\nTry again? (y/n): ").lower()
            if retry == 'y':
                return real_voice_input(prompt)
            return None
            
        except sr.RequestError as e:
            print(f"\n❌ Speech recognition service error: {e}")
            print("⚠️  Falling back to text input mode")
            return input("\nPlease type your input: ").strip()
    
    except Exception as e:
        print(f"\n❌ Microphone error: {e}")
        print("💡 Make sure your microphone is connected and permissions are granted")
        
        fallback = input("\nSwitch to text input? (y/n): ").lower()
        if fallback == 'y':
            return input("Your input: ").strip()
        return None


def simulated_voice_input(prompt):
    """
    Simulated voice input when speech recognition is not available.
    """
    print("🎙️  SIMULATION MODE (microphone not available)")
    print("💡 Install speech recognition: pip install SpeechRecognition pyaudio")
    print("\n📝 Type what you would say:")
    
    # Wait for user to be ready
    ready = input("\n✅ Press Enter when ready to 'speak' (or 'c' to cancel): ").strip().lower()
    
    if ready == 'c':
        print("❌ Voice input cancelled")
        return None
    
    print("\n" + "🔴 'RECORDING' IN PROGRESS...")
    print("─"*60)
    print("🎤 Type your speech now! Press Enter when finished")
    print("💡 Simulate what you would say out loud")
    print("─"*60)
    
    print("\n🔊 [●REC] ", end='', flush=True)
    voice_text = input().strip()
    
    if not voice_text:
        print("\n❌ No input detected")
        retry = input("Try again? (y/n): ").lower()
        if retry == 'y':
            return simulated_voice_input(prompt)
        return None
    
    print("\n✅ 'Recording' complete!")
    print(f"📝 Transcription: \"{voice_text}\"")
    
    return voice_text


def get_hybrid_input(prompt, mode_manager, config, allow_mode_switch=True):
    """
    Get user input in current mode with option to switch.
    
    Args:
        prompt: Prompt to display
        mode_manager: InteractionMode instance
        config: InfrastructureConfig instance
        allow_mode_switch: Whether to allow mode switching
    
    Returns:
        User input string or None if cancelled
    """
    mode = mode_manager.get_mode()
    
    print(f"\n{mode_manager.get_mode_icon()} [{mode.upper()} MODE] {prompt}")
    
    if allow_mode_switch:
        print("💡 Tip: Type 'm' to switch modes, 'b' to go back, 'q' to quit")
    
    if mode == "voice":
        result = simulate_voice_input(prompt)
        if result:
            config.add_mode_tracking("voice")
        return result
        
    elif mode == "auto":
        # Auto mode: detect if voice would be better
        print("🤖 AUTO MODE: Analyzing best input method...")
        time.sleep(0.5)
        
        # Simple heuristic: long descriptions benefit from voice
        if "describe" in prompt.lower() or "explain" in prompt.lower():
            print("→ Switching to VOICE for this input")
            result = simulate_voice_input(prompt)
            if result:
                config.add_mode_tracking("voice(auto)")
            return result
        else:
            print("→ Using TEXT for this input")
            result = input("Your input: ").strip()
            config.add_mode_tracking("text(auto)")
            return result
    
    else:  # text mode
        result = input("Your input: ").strip()
        
        # Check for mode switch command
        if result.lower() == 'm' and allow_mode_switch:
            new_mode = mode_selection_menu(mode)
            if new_mode != 'keep':
                mode_manager.set_mode(new_mode)
                print(f"\n✅ Switched to {new_mode.upper()} mode")
                display_mode_status(mode_manager)
            return get_hybrid_input(prompt, mode_manager, config, allow_mode_switch)
        
        if result:
            config.add_mode_tracking("text")
        return result


def quick_mode_switch(mode_manager):
    """Quick mode switching without full menu."""
    current = mode_manager.get_mode()
    
    print(f"\n🔄 Quick Mode Switch (currently: {current.upper()})")
    print("  [t] Text  [v] Voice  [a] Auto  [c] Cancel")
    
    choice = input("\nSwitch to: ").strip().lower()
    
    mode_map = {'t': 'text', 'v': 'voice', 'a': 'auto'}
    
    if choice in mode_map:
        mode_manager.set_mode(mode_map[choice])
        print(f"✅ Switched to {mode_map[choice].upper()} mode")
        return True
    
    return False


def natural_language_parser(text):
    """
    Parse natural language input into structured commands.
    Simulates AI understanding of voice/text commands.
    """
    text_lower = text.lower()
    
    # Parse cloud provider
    cloud_provider = None
    if 'aws' in text_lower or 'amazon' in text_lower:
        cloud_provider = 'AWS'
    elif 'azure' in text_lower or 'microsoft' in text_lower:
        cloud_provider = 'Azure'
    elif 'gcp' in text_lower or 'google' in text_lower:
        cloud_provider = 'GCP'
    
    # Parse resource type
    resource_type = None
    if 'server' in text_lower or 'compute' in text_lower or 'vm' in text_lower:
        resource_type = 'Compute'
    elif 'database' in text_lower or 'db' in text_lower:
        resource_type = 'Database'
    elif 'storage' in text_lower or 'bucket' in text_lower or 's3' in text_lower:
        resource_type = 'Storage'
    elif 'network' in text_lower or 'vpc' in text_lower:
        resource_type = 'Networking'
    
    return {
        'cloud_provider': cloud_provider,
        'resource_type': resource_type,
        'raw_text': text
    }


def voice_command_mode(mode_manager, config):
    """
    Natural language voice command processing.
    User can describe entire setup in one go.
    """
    print("\n" + "="*60)
    print("   🎤 VOICE COMMAND MODE")
    print("="*60)
    print("\n💬 Describe what you want to create in natural language")
    print("Example: 'Create a medium web server on AWS with 100GB storage'")
    print("-"*60)
    
    command = get_hybrid_input(
        "Describe your infrastructure:",
        mode_manager,
        config,
        allow_mode_switch=False
    )
    
    if not command:
        return False
    
    # Parse the natural language command
    print("\n🤖 Processing your request...")
    time.sleep(1)
    
    parsed = natural_language_parser(command)
    
    print("\n📋 Understood:")
    if parsed['cloud_provider']:
        print(f"  • Cloud: {parsed['cloud_provider']}")
        config.cloud_provider = parsed['cloud_provider']
    if parsed['resource_type']:
        print(f"  • Resource: {parsed['resource_type']}")
        config.resource_type = parsed['resource_type']
    
    if not parsed['cloud_provider'] or not parsed['resource_type']:
        print("\n⚠️  Need more information")
        return False
    
    print("\n✅ Configuration captured from voice command!")
    return True


def main_hybrid_flow():
    """Main hybrid mode flow with full integration."""
    print("\n" + "="*60)
    print("   🚀 HYBRID INFRASTRUCTURE SYSTEM")
    print("   Voice + Text Seamless Integration")
    print("="*60)
    
    mode_manager = InteractionMode()
    config = InfrastructureConfig()
    
    # Initial mode selection
    initial_mode = mode_selection_menu(mode_manager.get_mode())
    if initial_mode != 'keep':
        mode_manager.set_mode(initial_mode)
    
    print("\n✅ System ready!")
    print("💡 You can switch modes anytime during the process")
    
    while True:
        display_mode_status(mode_manager)
        
        print("\n" + "="*60)
        print("   MAIN MENU")
        print("="*60)
        print("\n  [1] Create infrastructure (step-by-step)")
        print("  [2] Create infrastructure (voice command)")
        print("  [3] View mode statistics")
        print("  [4] Switch mode")
        print("  [q] Quit")
        print("-"*60)
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Thank you for using Hybrid Mode!")
            break
            
        elif choice == '1':
            # Step-by-step with hybrid input
            print("\n📝 Step-by-step configuration")
            
            # Step 1: Cloud provider
            cloud = get_hybrid_input(
                "Which cloud provider? (AWS/Azure/GCP)",
                mode_manager,
                config
            )
            
            if cloud:
                config.cloud_provider = cloud.upper()
                print(f"✅ Cloud: {config.cloud_provider}")
            
            # Step 2: Resource type
            resource = get_hybrid_input(
                "What resource type? (Compute/Database/Storage/Networking)",
                mode_manager,
                config
            )
            
            if resource:
                config.resource_type = resource.capitalize()
                print(f"✅ Resource: {config.resource_type}")
            
            # Step 3: Details
            details = get_hybrid_input(
                "Any additional details?",
                mode_manager,
                config
            )
            
            if details:
                config.details['Additional Info'] = details
            
            # Summary and confirmation
            config.display_summary()
            
            confirm = input("\n✅ Create this infrastructure? (y/n): ").lower()
            if confirm == 'y':
                print("\n🚀 Creating infrastructure...")
                time.sleep(2)
                print("✅ Infrastructure created successfully!")
                
                # Show mode usage stats
                print(f"\n📊 You used: {', '.join(set(config.mode_used))} mode(s)")
            
            config.reset()
            
        elif choice == '2':
            # Voice command mode
            if voice_command_mode(mode_manager, config):
                config.display_summary()
                
                confirm = input("\n✅ Create this infrastructure? (y/n): ").lower()
                if confirm == 'y':
                    print("\n🚀 Creating infrastructure...")
                    time.sleep(2)
                    print("✅ Infrastructure created successfully!")
            
            config.reset()
            
        elif choice == '3':
            # Mode statistics
            print("\n" + "="*60)
            print("   📊 MODE USAGE STATISTICS")
            print("="*60)
            print(f"Current mode: {mode_manager.get_mode().upper()}")
            print(f"Mode switches: {len(mode_manager.mode_history)}")
            if mode_manager.mode_history:
                print(f"History: {' → '.join(mode_manager.mode_history[-5:])}")
            print("="*60)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Switch mode
            quick_mode_switch(mode_manager)
            
        else:
            print("❌ Invalid option")
    
    # Final statistics
    print("\n" + "="*60)
    print("   SESSION SUMMARY")
    print("="*60)
    print(f"Total mode switches: {len(mode_manager.mode_history)}")
    print(f"Final mode: {mode_manager.get_mode().upper()}")
    print("="*60)


if __name__ == "__main__":
    try:
        main_hybrid_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")