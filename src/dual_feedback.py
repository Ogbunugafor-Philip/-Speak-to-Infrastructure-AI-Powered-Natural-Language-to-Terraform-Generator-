# dual_feedback.py - Enhanced Version
# Advanced visual feedback for both voice and text interactions

import time
import sys
from datetime import datetime

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False


class InteractionSession:
    """Track interaction session data."""
    
    def __init__(self):
        self.voice_inputs = []
        self.text_inputs = []
        self.start_time = datetime.now()
        self.current_mode = "text"
    
    def add_voice_input(self, text, confidence, status="success"):
        """Add voice input to history."""
        self.voice_inputs.append({
            "text": text,
            "confidence": confidence,
            "status": status,
            "timestamp": datetime.now()
        })
    
    def add_text_input(self, text, status="received"):
        """Add text input to history."""
        self.text_inputs.append({
            "text": text,
            "status": status,
            "timestamp": datetime.now(),
            "char_count": len(text)
        })
    
    def get_stats(self):
        """Get session statistics."""
        return {
            "voice_count": len(self.voice_inputs),
            "text_count": len(self.text_inputs),
            "total_inputs": len(self.voice_inputs) + len(self.text_inputs),
            "duration": (datetime.now() - self.start_time).seconds,
            "avg_voice_confidence": sum(v["confidence"] for v in self.voice_inputs) / len(self.voice_inputs) if self.voice_inputs else 0
        }


def display_voice_feedback(spoken_text, confidence=0.0, is_listening=False, status="Processing"):
    """Show enhanced visual feedback for voice interactions."""
    print("\n" + "═"*60)
    print("🎤 " + "VOICE INTERFACE".center(56) + " 🎤")
    print("═"*60)
    
    # Status indicator
    status_icons = {
        "listening": "🔴 LISTENING",
        "processing": "🔄 PROCESSING",
        "success": "✅ SUCCESS",
        "low_confidence": "⚠️  LOW CONFIDENCE",
        "error": "❌ ERROR"
    }
    
    if is_listening:
        print(f"\n{status_icons.get('listening', '🔊 ACTIVE')}")
        print("┌─────────────────────────────────────────────────────────┐")
        print("│  📢 Speak clearly into your microphone                  │")
        print("│  ⏹️  The system will detect when you're finished        │")
        print("│  💡 Tip: Speak at a normal pace                         │")
        print("└─────────────────────────────────────────────────────────┘")
    else:
        status_key = "success" if confidence >= 0.8 else "low_confidence" if confidence > 0 else "processing"
        print(f"\n{status_icons.get(status_key, '✅ COMPLETE')}")
        
        if spoken_text:
            print("\n┌─────────────────────────────────────────────────────────┐")
            print(f"│ 💬 TRANSCRIPTION:                                       │")
            print(f"│    \"{spoken_text[:50]}{'...' if len(spoken_text) > 50 else ''}\"")
            print("└─────────────────────────────────────────────────────────┘")
    
    # Confidence visualization
    if confidence > 0:
        print(f"\n📊 CONFIDENCE ANALYSIS:")
        
        # Progress bar
        bar_length = 40
        filled = int(confidence * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        # Color-coded indicator
        if confidence >= 0.9:
            indicator = "🟢 EXCELLENT"
        elif confidence >= 0.8:
            indicator = "🟡 GOOD"
        elif confidence >= 0.6:
            indicator = "🟠 FAIR"
        else:
            indicator = "🔴 POOR"
        
        print(f"   [{bar}] {confidence:.1%}")
        print(f"   {indicator}")
        
        # Recommendations
        if confidence < 0.8:
            print("\n💡 IMPROVEMENT TIPS:")
            if confidence < 0.5:
                print("   • Speak more clearly and slowly")
                print("   • Move to a quieter environment")
                print("   • Check microphone positioning")
            elif confidence < 0.7:
                print("   • Reduce background noise")
                print("   • Speak slightly louder")
            else:
                print("   • Minor clarity improvement needed")
    
    print("═"*60)


def display_text_feedback(typed_text, is_typing=False, status="received"):
    """Show enhanced visual feedback for text interactions."""
    print("\n" + "═"*60)
    print("⌨️  " + "TEXT INTERFACE".center(56) + " ⌨️")
    print("═"*60)
    
    if is_typing:
        print("\n✍️  WAITING FOR INPUT")
        print("┌─────────────────────────────────────────────────────────┐")
        print("│  ⌨️  Type your response below                            │")
        print("│  ↵  Press Enter when finished                           │")
        print("│  💡 Tip: Be clear and specific                          │")
        print("└─────────────────────────────────────────────────────────┘")
    else:
        print("\n✅ INPUT RECEIVED")
        
        if typed_text:
            print("\n┌─────────────────────────────────────────────────────────┐")
            print(f"│ 📝 YOUR INPUT:                                          │")
            print(f"│    \"{typed_text[:50]}{'...' if len(typed_text) > 50 else ''}\"")
            print("└─────────────────────────────────────────────────────────┘")
            
            # Text statistics
            print(f"\n📊 TEXT ANALYSIS:")
            print(f"   • Characters: {len(typed_text)}")
            print(f"   • Words: {len(typed_text.split())}")
            
            # Quality indicators
            if len(typed_text) < 3:
                print("   ⚠️  Very short input - consider adding details")
            elif len(typed_text) < 10:
                print("   🟡 Short input - acceptable")
            else:
                print("   🟢 Good level of detail")
    
    print("═"*60)


def show_unified_dashboard(voice_data, text_data, current_mode, show_comparison=True):
    """Display enhanced unified dashboard with both panels."""
    print("\n" + "╔"*60)
    print("║" + " 🎯 UNIFIED INTERACTION DASHBOARD ".center(118) + "║")
    print("╚"*60)
    
    # Mode indicator
    mode_display = {
        "voice": "🎤 VOICE MODE",
        "text": "⌨️  TEXT MODE",
        "hybrid": "🔄 HYBRID MODE",
        "auto": "🤖 AUTO MODE"
    }
    
    print(f"\n⚡ CURRENT MODE: {mode_display.get(current_mode, current_mode.upper())}")
    print("─"*60)
    
    # Side-by-side panels
    print("\n" + "┌" + "─"*28 + "┬" + "─"*29 + "┐")
    print("│" + " 🎤 VOICE PANEL ".center(28) + "│" + " ⌨️  TEXT PANEL ".center(29) + "│")
    print("├" + "─"*28 + "┼" + "─"*29 + "┤")
    
    # Voice panel content
    if voice_data:
        v_status = voice_data.get('status', 'N/A')[:12]
        v_text = voice_data.get('text', 'None')[:20]
        v_conf = voice_data.get('confidence', 0)
        
        print(f"│ Status: {v_status:<15} │", end="")
    else:
        print("│ ⏸️  No voice activity    │", end="")
    
    # Text panel content
    if text_data:
        t_status = text_data.get('status', 'N/A')[:12]
        t_text = text_data.get('text', 'None')[:20]
        
        print(f" Status: {t_status:<16} │")
        print(f"│ Text: {v_text:<17} │ Input: {t_text:<18} │")
        
        if voice_data:
            conf_bar = "█" * int(v_conf * 10) + "░" * (10 - int(v_conf * 10))
            print(f"│ Conf: [{conf_bar}] {v_conf:.0%} │", end="")
        else:
            print(f"│                          │", end="")
        
        t_chars = text_data.get('char_count', len(t_text))
        print(f" Chars: {t_chars:<17} │")
    else:
        print(" ⏸️  No text activity      │")
        if voice_data:
            v_text = voice_data.get('text', 'None')[:20]
            v_conf = voice_data.get('confidence', 0)
            conf_bar = "█" * int(v_conf * 10) + "░" * (10 - int(v_conf * 10))
            print(f"│ Text: {v_text:<17} │                           │")
            print(f"│ Conf: [{conf_bar}] {v_conf:.0%} │                           │")
        else:
            print("│                          │                           │")
    
    print("└" + "─"*28 + "┴" + "─"*29 + "┘")
    
    # Comparison section
    if show_comparison and voice_data and text_data:
        print("\n📊 INPUT COMPARISON:")
        print(f"   Voice: {len(voice_data.get('text', ''))} chars, {voice_data.get('confidence', 0):.0%} confidence")
        print(f"   Text:  {len(text_data.get('text', ''))} chars, 100% accuracy")
        
        # Suggest optimal mode
        if voice_data.get('confidence', 0) < 0.7:
            print("\n💡 SUGGESTION: Consider using text mode for better accuracy")
        else:
            print("\n✅ Both modes performing well!")


def animate_listening():
    """Animated listening indicator."""
    print("\n🎤 Listening", end="", flush=True)
    for _ in range(3):
        for indicator in ["   ", ".  ", ".. ", "..."]:
            print(f"\r🎤 Listening{indicator}", end="", flush=True)
            time.sleep(0.3)
    print("\r🎤 Listening... ✅")


def show_session_summary(session):
    """Display comprehensive session summary."""
    stats = session.get_stats()
    
    print("\n" + "╔"*60)
    print("║" + " 📊 SESSION SUMMARY ".center(118) + "║")
    print("╚"*60)
    
    print(f"\n⏱️  DURATION: {stats['duration']} seconds")
    print(f"📝 TOTAL INPUTS: {stats['total_inputs']}")
    
    print("\n┌─────────────────────────────────────────────────────────┐")
    print("│ INPUT BREAKDOWN:                                        │")
    print(f"│   🎤 Voice inputs: {stats['voice_count']:<35} │")
    print(f"│   ⌨️  Text inputs:  {stats['text_count']:<35} │")
    print("└─────────────────────────────────────────────────────────┘")
    
    if stats['voice_count'] > 0:
        print(f"\n📊 VOICE PERFORMANCE:")
        print(f"   Average confidence: {stats['avg_voice_confidence']:.1%}")
        
        if stats['avg_voice_confidence'] >= 0.85:
            print("   🟢 Excellent voice recognition quality!")
        elif stats['avg_voice_confidence'] >= 0.70:
            print("   🟡 Good voice recognition quality")
        else:
            print("   🔴 Voice recognition could be improved")
    
    # Show recent inputs
    print("\n📜 RECENT ACTIVITY:")
    
    if session.voice_inputs:
        print("\n  🎤 Last voice input:")
        last_voice = session.voice_inputs[-1]
        print(f"     \"{last_voice['text'][:50]}\"")
        print(f"     Confidence: {last_voice['confidence']:.1%}")
    
    if session.text_inputs:
        print("\n  ⌨️  Last text input:")
        last_text = session.text_inputs[-1]
        print(f"     \"{last_text['text'][:50]}\"")
        print(f"     Characters: {last_text['char_count']}")
    
    print("\n" + "═"*60)


def interactive_feedback_demo():
    """Interactive demonstration of the dual feedback system."""
    print("\n" + "╔"*60)
    print("║" + " 🎨 DUAL FEEDBACK VISUALIZATION SYSTEM ".center(118) + "║")
    print("╚"*60)
    
    print("\nThis system provides real-time visual feedback for both")
    print("voice and text inputs, helping you track interaction quality.")
    
    if SPEECH_AVAILABLE:
        print("\n✅ Real speech recognition is AVAILABLE")
    else:
        print("\n⚠️  Speech recognition not available (simulation mode)")
    
    print("\n" + "─"*60)
    
    session = InteractionSession()
    
    while True:
        print("\n" + "🔷"*30)
        print("   INTERACTION MENU")
        print("🔷"*30)
        print("\n  [1] Simulate voice input")
        print("  [2] Simulate text input")
        print("  [3] Show unified dashboard")
        print("  [4] View session summary")
        print("  [5] Full demo sequence")
        print("  [q] Quit")
        print("─"*60)
        
        choice = input("\nSelect option: ").strip().lower()
        
        if choice == 'q':
            break
        
        elif choice == '1':
            # Simulate voice input
            print("\n📍 VOICE INPUT SIMULATION")
            session.current_mode = "voice"
            
            user_input = input("What would you say? (or press Enter for demo): ").strip()
            if not user_input:
                user_input = "Create a database server with MySQL"
            
            # Show listening state
            display_voice_feedback("", confidence=0, is_listening=True)
            animate_listening()
            
            # Simulate processing
            confidence = float(input("\nSimulate confidence (0.0-1.0, or Enter for random): ").strip() or f"{0.75 + (hash(user_input) % 25) / 100}")
            
            # Show result
            display_voice_feedback(user_input, confidence=confidence, is_listening=False)
            
            session.add_voice_input(user_input, confidence)
        
        elif choice == '2':
            # Simulate text input
            print("\n📍 TEXT INPUT SIMULATION")
            session.current_mode = "text"
            
            display_text_feedback("", is_typing=True)
            
            user_input = input("\nYour input: ").strip()
            if not user_input:
                user_input = "Ubuntu 22.04 with 16GB RAM"
            
            display_text_feedback(user_input, is_typing=False)
            
            session.add_text_input(user_input)
        
        elif choice == '3':
            # Show unified dashboard
            voice_data = session.voice_inputs[-1] if session.voice_inputs else None
            text_data = session.text_inputs[-1] if session.text_inputs else None
            
            show_unified_dashboard(voice_data, text_data, session.current_mode)
        
        elif choice == '4':
            # Show session summary
            show_session_summary(session)
        
        elif choice == '5':
            # Full demo sequence
            print("\n🎬 RUNNING FULL DEMO SEQUENCE...")
            time.sleep(1)
            
            # Demo 1: High confidence voice
            print("\n📍 1. High Confidence Voice Input")
            time.sleep(1)
            display_voice_feedback("Create an AWS EC2 instance", confidence=0.95, is_listening=False)
            session.add_voice_input("Create an AWS EC2 instance", 0.95)
            time.sleep(2)
            
            # Demo 2: Text input
            print("\n📍 2. Text Input")
            time.sleep(1)
            display_text_feedback("t3.medium with 50GB storage", is_typing=False)
            session.add_text_input("t3.medium with 50GB storage")
            time.sleep(2)
            
            # Demo 3: Unified dashboard
            print("\n📍 3. Unified Dashboard")
            time.sleep(1)
            show_unified_dashboard(session.voice_inputs[-1], session.text_inputs[-1], "hybrid")
            time.sleep(2)
            
            # Demo 4: Low confidence voice
            print("\n📍 4. Low Confidence Voice Input")
            time.sleep(1)
            display_voice_feedback("databse servr", confidence=0.42, is_listening=False)
            session.add_voice_input("databse servr", 0.42, "low_confidence")
            time.sleep(2)
            
            # Demo 5: Final summary
            print("\n📍 5. Session Summary")
            time.sleep(1)
            show_session_summary(session)
            
            print("\n🎉 Demo sequence complete!")
        
        else:
            print("❌ Invalid option")
    
    # Final summary
    print("\n" + "╔"*60)
    print("║" + " 👋 SESSION ENDED ".center(118) + "║")
    print("╚"*60)
    
    show_session_summary(session)
    
    print("\n✨ Thank you for exploring the dual feedback system!")


if __name__ == "__main__":
    try:
        interactive_feedback_demo()
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")