"""
voice_question_templates.py - Final Standalone Version with Voice
-----------------------------------------------------------------
Fully self-contained intelligent question generator with integrated TTS.
No external dependencies like advanced_tts_engine.py are required.
"""

import random
import time
from datetime import datetime
import pyttsx3


class VoiceQuestionTemplates:
    """Handles dynamic spoken question generation with tone and context awareness."""

    def __init__(self, tone="friendly", use_name=True, user_name="Philip", voice_enabled=True):
        self.tone = tone
        self.use_name = use_name
        self.user_name = user_name
        self.voice_enabled = voice_enabled
        self.question_history = []

        # Initialize pyttsx3 engine only if voice mode is enabled
        self.tts_engine = pyttsx3.init() if voice_enabled else None
        if self.tts_engine:
            self.tts_engine.setProperty("rate", 175)
            self.tts_engine.setProperty("volume", 0.9)

        # Templates organized by tone
        self.templates = {
            "provider": {
                "friendly": [
                    "Let's get started! Which cloud provider would you like to use?",
                    "Great! Now, which platform should we build on — AWS, Azure, or GCP?",
                    "I'm excited to help! Which cloud provider do you prefer?"
                ],
                "professional": [
                    "Which cloud provider would you like to use?",
                    "Please specify your preferred cloud platform."
                ]
            },
            "region": {
                "friendly": [
                    "Perfect! Where would you like to deploy your infrastructure?",
                    "Awesome! Which region should we set this up in?"
                ],
                "professional": [
                    "Which region would you like to deploy in?",
                    "Please specify your preferred deployment region."
                ]
            },
            "compute": {
                "friendly": [
                    "Let's talk compute! What instance type do you need?",
                    "How much processing power should we allocate?"
                ],
                "professional": [
                    "Please specify your compute requirements.",
                    "Which instance size best matches your workload?"
                ]
            },
            "database": {
                "friendly": [
                    "Great! Now, which database should we set up?",
                    "Perfect! What database engine works for you?"
                ],
                "professional": [
                    "Which database engine would you like to deploy?",
                    "Please specify your preferred database service."
                ]
            },
            "confirmation": {
                "friendly": [
                    "Perfect! Does this look good to you?",
                    "Great! Is this what you're looking for?"
                ],
                "professional": [
                    "Is this configuration correct?",
                    "Would you like to proceed with these settings?"
                ]
            }
        }

    def _personalize(self, question):
        if self.use_name and self.user_name and random.random() < 0.4:
            return f"{self.user_name}, {question.lower()}"
        return question

    def speak(self, text):
        """Speak text aloud if voice mode is active."""
        if self.voice_enabled and self.tts_engine:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

    def get_question(self, context_type):
        """Generate and optionally speak a question."""
        tone_templates = self.templates.get(context_type, {}).get(self.tone, [])
        if not tone_templates:
            question = f"Could you please provide details about {context_type}?"
        else:
            question = random.choice(tone_templates)

        question = self._personalize(question)
        self.question_history.append({"context": context_type, "text": question})

        print(f"\n🗣️  {question}")
        self.speak(question)
        time.sleep(0.4)
        return question

    def display_statistics(self):
        """Show summary of all questions asked."""
        stats = {}
        for q in self.question_history:
            stats[q["context"]] = stats.get(q["context"], 0) + 1

        print("\n" + "=" * 70)
        print("📊 QUESTION TEMPLATE STATISTICS".center(70))
        print("=" * 70)
        print(f"\n🗂️  Total questions asked: {len(self.question_history)}")
        for ctx, count in stats.items():
            print(f"   • {ctx}: {count}")
        if stats:
            most = max(stats, key=stats.get)
            print(f"\n⭐ Most asked context: {most}")
        print("=" * 70)


def demo():
    """Demonstrate the question and voice flow."""
    print("\n" + "=" * 70)
    print("🎙️  VOICE QUESTION TEMPLATE DEMO (BUILT-IN TTS)".center(70))
    print("=" * 70)

    q = VoiceQuestionTemplates(tone="friendly", use_name=True, user_name="Philip", voice_enabled=True)
    contexts = ["provider", "region", "compute", "database", "confirmation"]

    for context in contexts:
        q.get_question(context)

    q.display_statistics()
    print("\n✅ Voice demo complete!\n")


if __name__ == "__main__":
    try:
        demo()
    except KeyboardInterrupt:
        print("\n⚠️  Demo interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
