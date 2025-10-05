# voice_text_editor.py - Enhanced Version
# Advanced manual text editing of voice-recognized inputs with diff visualization

import time
import difflib

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
    recognizer = sr.Recognizer()
except ImportError:
    SPEECH_AVAILABLE = False


class EditHistory:
    """Track editing history and changes."""
    
    def __init__(self):
        self.edits = []
    
    def add_edit(self, original, edited, edit_type):
        """Record an edit."""
        self.edits.append({
            "original": original,
            "edited": edited,
            "type": edit_type,
            "changes": self.count_changes(original, edited)
        })
    
    def count_changes(self, original, edited):
        """Count the number of changes made."""
        if not original or not edited:
            return 0
        
        # Simple character difference count
        matcher = difflib.SequenceMatcher(None, original, edited)
        return sum(1 for tag, _, _, _, _ in matcher.get_opcodes() if tag != 'equal')
    
    def get_stats(self):
        """Get editing statistics."""
        if not self.edits:
            return {"total_edits": 0, "avg_changes": 0}
        
        total_changes = sum(e["changes"] for e in self.edits)
        return {
            "total_edits": len(self.edits),
            "avg_changes": total_changes / len(self.edits) if self.edits else 0,
            "edit_types": {e["type"]: 1 for e in self.edits}
        }


def show_text_diff(original, edited):
    """Display visual diff between original and edited text."""
    print("\n" + "═"*60)
    print("   📊 CHANGES VISUALIZATION")
    print("═"*60)
    
    if original == edited:
        print("\n✅ No changes made - text accepted as-is")
        return
    
    # Show side-by-side comparison
    print("\n┌─────────────── ORIGINAL ───────────────┐")
    print(f"│ {original[:40]:<40} │")
    print("└────────────────────────────────────────┘")
    
    print("                    ⬇️")
    print("              [EDITED TO]")
    print("                    ⬇️")
    
    print("┌──────────────── EDITED ────────────────┐")
    print(f"│ {edited[:40]:<40} │")
    print("└────────────────────────────────────────┘")
    
    # Character-level diff
    print("\n🔍 DETAILED CHANGES:")
    
    matcher = difflib.SequenceMatcher(None, original, edited)
    changes_found = False
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            changes_found = True
            print(f"   🔄 Replaced: '{original[i1:i2]}' → '{edited[j1:j2]}'")
        elif tag == 'delete':
            changes_found = True
            print(f"   ❌ Deleted: '{original[i1:i2]}'")
        elif tag == 'insert':
            changes_found = True
            print(f"   ➕ Added: '{edited[j1:j2]}'")
    
    if not changes_found:
        print("   ✅ No significant changes detected")
    
    print("═"*60)


def get_real_voice_input():
    """Get actual voice input from microphone."""
    if not SPEECH_AVAILABLE:
        return None, "unavailable"
    
    try:
        with sr.Microphone() as source:
            print("\n🔧 Calibrating microphone...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            print("🔴 Recording... Speak now!")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("✅ Audio captured!")
        
        print("🔄 Converting speech to text...")
        text = recognizer.recognize_google(audio)
        confidence = 0.85  # Google doesn't provide actual confidence
        
        return text, confidence
        
    except sr.WaitTimeoutError:
        return None, "timeout"
    except sr.UnknownValueError:
        return None, "unclear"
    except Exception as e:
        return None, f"error: {e}"


def simulate_voice_recognition(user_input):
    """Simulate voice recognition with realistic confidence."""
    if not user_input:
        return None, 0.0
    
    # Simulate confidence based on input characteristics
    base_confidence = 0.65
    
    # Longer inputs tend to have lower confidence
    length_factor = max(0, 0.3 - (len(user_input) / 200))
    
    # Simple words have higher confidence
    word_count = len(user_input.split())
    complexity_factor = 0.15 if word_count < 5 else 0.05
    
    confidence = min(base_confidence + length_factor + complexity_factor, 0.95)
    
    # Simulate occasional recognition errors
    import random
    if random.random() < 0.2:  # 20% chance of minor error
        words = user_input.split()
        if words:
            # Introduce small error
            idx = random.randint(0, len(words) - 1)
            if len(words[idx]) > 3:
                words[idx] = words[idx][:-1]  # Remove last letter
            user_input = " ".join(words)
            confidence *= 0.7  # Lower confidence for errors
    
    return user_input, confidence


def advanced_text_editor(text, prompt="Edit text"):
    """Advanced in-place text editor with multiple options."""
    print("\n" + "═"*60)
    print("   ✏️  ADVANCED TEXT EDITOR")
    print("═"*60)
    
    print(f"\n📝 Current text:\n   \"{text}\"")
    print("\n" + "─"*60)
    print("EDITING OPTIONS:")
    print("  [1] Quick edit - Replace entire text")
    print("  [2] Word-by-word edit - Fix specific words")
    print("  [3] Append - Add to the end")
    print("  [4] Prepend - Add to the beginning")
    print("  [5] Find & Replace")
    print("  [6] Accept as-is")
    print("─"*60)
    
    choice = input("\nSelect editing option (1-6): ").strip()
    
    if choice == '1':
        # Quick edit - replace all
        print("\n✏️  QUICK EDIT MODE")
        print(f"Original: \"{text}\"")
        new_text = input("Enter new text: ").strip()
        
        if new_text:
            show_text_diff(text, new_text)
            confirm = input("\n✅ Keep these changes? (y/n): ").lower()
            if confirm == 'y':
                return new_text, "full_edit"
        
        return text, "no_change"
    
    elif choice == '2':
        # Word-by-word editing
        print("\n✏️  WORD-BY-WORD EDIT MODE")
        words = text.split()
        
        print("\nWords in text:")
        for i, word in enumerate(words, 1):
            print(f"  {i}. {word}")
        
        print("\nEnter word numbers to edit (comma-separated, or 'done'):")
        to_edit = input("> ").strip()
        
        if to_edit.lower() == 'done':
            return text, "no_change"
        
        try:
            indices = [int(x.strip()) - 1 for x in to_edit.split(',')]
            
            for idx in indices:
                if 0 <= idx < len(words):
                    print(f"\nWord {idx + 1}: '{words[idx]}'")
                    new_word = input(f"Replace with: ").strip()
                    if new_word:
                        words[idx] = new_word
            
            new_text = " ".join(words)
            show_text_diff(text, new_text)
            
            confirm = input("\n✅ Keep these changes? (y/n): ").lower()
            if confirm == 'y':
                return new_text, "word_edit"
        
        except (ValueError, IndexError):
            print("❌ Invalid input")
        
        return text, "no_change"
    
    elif choice == '3':
        # Append
        print("\n✏️  APPEND MODE")
        addition = input("Text to add at end: ").strip()
        
        if addition:
            new_text = f"{text} {addition}"
            show_text_diff(text, new_text)
            return new_text, "append"
        
        return text, "no_change"
    
    elif choice == '4':
        # Prepend
        print("\n✏️  PREPEND MODE")
        addition = input("Text to add at beginning: ").strip()
        
        if addition:
            new_text = f"{addition} {text}"
            show_text_diff(text, new_text)
            return new_text, "prepend"
        
        return text, "no_change"
    
    elif choice == '5':
        # Find & Replace
        print("\n✏️  FIND & REPLACE MODE")
        find = input("Find: ").strip()
        
        if find in text:
            replace = input(f"Replace '{find}' with: ").strip()
            new_text = text.replace(find, replace)
            
            count = text.count(find)
            print(f"\n📊 Found {count} occurrence(s)")
            
            show_text_diff(text, new_text)
            return new_text, "find_replace"
        else:
            print(f"❌ '{find}' not found in text")
        
        return text, "no_change"
    
    else:
        # Accept as-is
        print("\n✅ Text accepted without changes")
        return text, "accepted"


def voice_input_with_editing(prompt, edit_history=None, attempt=1, max_attempts=3):
    """
    Get voice input with comprehensive editing options.
    
    Args:
        prompt: The prompt to show
        edit_history: EditHistory object to track changes
        attempt: Current attempt number
        max_attempts: Maximum voice recognition attempts
    
    Returns:
        Tuple of (text, method)
    """
    if edit_history is None:
        edit_history = EditHistory()
    
    print("\n" + "╔"*60)
    print("║" + f" 🎤 VOICE INPUT: {prompt} ".center(118) + "║")
    print("╚"*60)
    
    if attempt > 1:
        print(f"\n🔄 Attempt {attempt} of {max_attempts}")
    
    # Mode selection
    print("\n📍 INPUT METHOD:")
    print("  [v] Voice input (speak)")
    print("  [t] Text input (type)")
    print("  [c] Cancel")
    
    mode = input("\nSelect: ").strip().lower()
    
    if mode == 'c':
        return None, "cancelled"
    
    if mode == 't':
        # Direct text input
        print("\n⌨️  TEXT INPUT MODE")
        text = input(f"{prompt}: ").strip()
        
        if text:
            return text, "text_direct"
        return None, "cancelled"
    
    # Voice input
    print("\n🎤 VOICE INPUT MODE")
    
    if SPEECH_AVAILABLE:
        print("💡 Using real microphone input")
        ready = input("\n✅ Press Enter when ready to speak (or 'c' to cancel): ").strip().lower()
        
        if ready == 'c':
            return None, "cancelled"
        
        voice_text, result = get_real_voice_input()
        
        if result == "timeout":
            print("❌ Timeout - no speech detected")
            if attempt < max_attempts:
                return voice_input_with_editing(prompt, edit_history, attempt + 1, max_attempts)
            return None, "timeout"
        
        elif result == "unclear":
            print("❌ Could not understand speech")
            if attempt < max_attempts:
                retry = input(f"Try again? ({max_attempts - attempt} attempts left) (y/n): ").lower()
                if retry == 'y':
                    return voice_input_with_editing(prompt, edit_history, attempt + 1, max_attempts)
            return None, "unclear"
        
        elif voice_text is None:
            print(f"❌ Voice input failed: {result}")
            return None, "error"
        
        confidence = result
        
    else:
        # Simulation mode
        print("💡 SIMULATION MODE (no microphone)")
        print("🔊 Listening... (type what you would say)")
        
        voice_text = input("\n[Voice simulation]: ").strip()
        
        if not voice_text:
            return None, "cancelled"
        
        voice_text, confidence = simulate_voice_recognition(voice_text)
    
    # Display recognition result
    print("\n" + "═"*60)
    print("   📊 VOICE RECOGNITION RESULT")
    print("═"*60)
    print(f"\n✅ Recognized: \"{voice_text}\"")
    print(f"📊 Confidence: {confidence:.0%}")
    
    # Confidence visualization
    bar_length = 40
    filled = int(confidence * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\n[{bar}] {confidence:.1%}")
    
    # Determine if editing is needed
    needs_review = confidence < 0.80
    
    if needs_review:
        print("\n⚠️  LOW CONFIDENCE - Review recommended")
    else:
        print("\n✅ HIGH CONFIDENCE - Looks good!")
    
    print("\n" + "─"*60)
    print("NEXT STEPS:")
    print("  [1] ✅ Accept as-is")
    print("  [2] ✏️  Edit text (advanced editor)")
    print("  [3] 🔍 Quick fix (simple correction)")
    print("  [4] 🔄 Re-record voice")
    print("  [5] ❌ Cancel input")
    print("─"*60)
    
    choice = input("\nSelect option: ").strip()
    
    if choice == '1':
        # Accept as-is
        print("\n✅ Text accepted without changes")
        return voice_text, "voice_accepted"
    
    elif choice == '2':
        # Advanced editor
        edited_text, edit_type = advanced_text_editor(voice_text, prompt)
        
        if edit_type != "no_change":
            edit_history.add_edit(voice_text, edited_text, edit_type)
            return edited_text, f"voice_{edit_type}"
        
        return voice_text, "voice_accepted"
    
    elif choice == '3':
        # Quick fix
        print("\n✏️  QUICK FIX MODE")
        print(f"Original: \"{voice_text}\"")
        corrected = input("Corrected text: ").strip()
        
        if corrected and corrected != voice_text:
            show_text_diff(voice_text, corrected)
            edit_history.add_edit(voice_text, corrected, "quick_fix")
            return corrected, "voice_edited"
        
        return voice_text, "voice_accepted"
    
    elif choice == '4':
        # Re-record
        if attempt < max_attempts:
            print("\n🔄 Re-recording...")
            return voice_input_with_editing(prompt, edit_history, attempt + 1, max_attempts)
        else:
            print(f"\n⚠️  Maximum attempts ({max_attempts}) reached")
            return voice_text, "voice_max_attempts"
    
    else:
        # Cancel
        print("❌ Input cancelled")
        return None, "cancelled"


def infrastructure_configuration_flow():
    """Enhanced infrastructure configuration with advanced editing."""
    print("\n" + "╔"*60)
    print("║" + " 🎤 VOICE-TO-TEXT EDITING SYSTEM ".center(118) + "║")
    print("║" + " Speak naturally, then edit with precision! ".center(118) + "║")
    print("╚"*60)
    
    if SPEECH_AVAILABLE:
        print("\n✅ Real microphone input ENABLED")
    else:
        print("\n⚠️  Simulation mode (install SpeechRecognition for real voice)")
    
    print("\n💡 This system allows you to:")
    print("   • Speak or type your inputs")
    print("   • Review voice recognition results")
    print("   • Edit with advanced tools (word-by-word, find/replace, etc.)")
    print("   • See visual diffs of your changes")
    
    input("\n✅ Press Enter to begin...")
    
    configurations = []
    edit_history = EditHistory()
    
    while True:
        print("\n" + "🔷"*30)
        print(f"   CONFIGURATION #{len(configurations) + 1}")
        print("🔷"*30)
        
        # Get resource type
        resource, method = voice_input_with_editing(
            "What type of resource do you need?",
            edit_history
        )
        
        if not resource:
            print("\n❌ Configuration cancelled")
            break
        
        print(f"\n✅ Resource type captured: \"{resource}\"")
        print(f"   Method: {method}")
        
        # Get specifications
        specs, spec_method = voice_input_with_editing(
            f"Describe the {resource} specifications",
            edit_history
        )
        
        if not specs:
            print("\n❌ Specifications cancelled")
            break
        
        print(f"\n✅ Specifications captured: \"{specs}\"")
        print(f"   Method: {spec_method}")
        
        # Store configuration
        config = {
            "resource": resource,
            "specifications": specs,
            "resource_method": method,
            "spec_method": spec_method,
            "timestamp": time.strftime("%H:%M:%S")
        }
        configurations.append(config)
        
        print("\n" + "─"*60)
        print("📋 CURRENT CONFIGURATION:")
        print(f"   Resource: {resource}")
        print(f"   Specs: {specs}")
        print("─"*60)
        
        # Continue or finish
        print("\n➡️  NEXT ACTION:")
        print("  [1] Add another resource")
        print("  [2] View all configurations")
        print("  [3] Finish and view summary")
        
        next_action = input("\nSelect: ").strip()
        
        if next_action == '2':
            # Show current configs
            print("\n" + "═"*60)
            print("   📊 ALL CONFIGURATIONS SO FAR")
            print("═"*60)
            
            for i, cfg in enumerate(configurations, 1):
                print(f"\n{i}. {cfg['resource'].upper()}")
                print(f"   Specs: {cfg['specifications']}")
                print(f"   Time: {cfg['timestamp']}")
            
            input("\nPress Enter to continue...")
        
        elif next_action == '3':
            break
    
    # Final summary
    if not configurations:
        print("\n❌ No configurations created")
        return
    
    print("\n" + "╔"*60)
    print("║" + " 🎯 FINAL CONFIGURATION SUMMARY ".center(118) + "║")
    print("╚"*60)
    
    for i, config in enumerate(configurations, 1):
        print(f"\n━━━ Configuration #{i} ━━━")
        print(f"🏷️  Resource: {config['resource']}")
        print(f"⚙️  Specifications: {config['specifications']}")
        print(f"📝 Input methods: {config['resource_method']} → {config['spec_method']}")
        print(f"🕐 Created: {config['timestamp']}")
    
    # Statistics
    print("\n" + "═"*60)
    print("   📊 SESSION STATISTICS")
    print("═"*60)
    
    total = len(configurations)
    
    # Count editing methods
    voice_count = sum(1 for c in configurations if 'voice' in c['resource_method'] or 'voice' in c['spec_method'])
    text_count = sum(1 for c in configurations if 'text' in c['resource_method'] or 'text' in c['spec_method'])
    edited_count = sum(1 for c in configurations if 'edit' in c['resource_method'] or 'edit' in c['spec_method'])
    
    print(f"\n📝 Total configurations: {total}")
    print(f"🎤 Voice inputs: {voice_count}")
    print(f"⌨️  Text inputs: {text_count}")
    print(f"✏️  Edited inputs: {edited_count}")
    
    if edited_count > 0:
        edit_rate = (edited_count / (voice_count + text_count)) * 100 if (voice_count + text_count) > 0 else 0
        print(f"📊 Edit rate: {edit_rate:.1f}%")
    
    # Edit history stats
    edit_stats = edit_history.get_stats()
    if edit_stats["total_edits"] > 0:
        print(f"\n✏️  Total edits made: {edit_stats['total_edits']}")
        print(f"📈 Average changes per edit: {edit_stats['avg_changes']:.1f}")
    
    print("\n" + "═"*60)
    print("\n✨ Thank you for using the Voice-to-Text Editor!")


if __name__ == "__main__":
    try:
        infrastructure_configuration_flow()
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")