"""
Wake Word Detection System
==========================

This module implements a wake word detector for the Speak-to-Infrastructure project.
It listens continuously for a wake word (e.g., "assistant") before activating full voice mode.

Key Features:
- Continuous microphone listening with timeouts
- Speech-to-text recognition (Google API by default)
- Wake word detection and confirmation response
- Integration with EnhancedVoiceEngine for natural TTS feedback
"""

import time
import signal
import logging
from typing import Tuple
from dataclasses import dataclass

import speech_recognition as sr
from enhanced_voice_engine import EnhancedVoiceEngine


# ---------------- CONFIGURATION ----------------
DEFAULT_WAKE_WORD = "assistant"
DEFAULT_TIMEOUT = 30
LISTEN_TIMEOUT = 5
PHRASE_LIMIT = 3


# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)


# ---------------- DETECTOR CLASS ----------------
@dataclass
class WakeWordDetector:
    """
    Wake word detection system.

    Attributes:
        wake_word: The wake word to listen for.
        recognizer: Speech recognition engine instance.
        microphone: Microphone input source.
        voice_engine: Enhanced voice engine for TTS responses.
    """
    wake_word: str = DEFAULT_WAKE_WORD

    def __post_init__(self):
        self.wake_word = self.wake_word.lower()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.voice_engine = EnhancedVoiceEngine()

        logging.info(f"Wake word detector initialized")
        logging.info(f"Wake word set to: '{self.wake_word}'")
        logging.info(f"Say 'Hey {self.wake_word}' to activate")

    def listen_for_wake_word(self, timeout: int = DEFAULT_TIMEOUT) -> bool:
        """
        Listen continuously for the wake word.

        Args:
            timeout (int): Maximum time to listen (seconds).

        Returns:
            bool: True if wake word detected, False otherwise.
        """
        logging.info(f"Listening for wake word: '{self.wake_word}'")
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            try:
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=LISTEN_TIMEOUT, phrase_time_limit=PHRASE_LIMIT)

                text = self.recognizer.recognize_google(audio).lower()
                logging.debug(f"Heard: '{text}'")

                if self.wake_word in text:
                    logging.info(f"Wake word '{self.wake_word}' detected ✅")
                    self.voice_engine.speak("Yes, I'm listening. How can I help with your infrastructure?")
                    return True

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                logging.error(f"Wake word listening error: {e}", exc_info=False)
                continue

        logging.warning("Wake word timeout reached ⏰")
        return False

    def wait_for_wake_word_then_listen(self) -> Tuple[bool, str]:
        """
        Full workflow: Wait for wake word, then listen for actual command.

        Returns:
            Tuple[bool, str]: (Success flag, Command text or error message)
        """
        logging.info("Wake word mode activated")

        if not self.listen_for_wake_word(timeout=DEFAULT_TIMEOUT):
            return False, "Wake word not detected"

        self.voice_engine.speak("I'm listening for your infrastructure command.")
        success, command = self.voice_engine.listen_with_retry(max_retries=2)

        return success, command


# ---------------- TEST FUNCTIONS ----------------
def simple_wake_word_test() -> bool:
    """Quick test: only listens for wake word."""
    detector = WakeWordDetector(wake_word=DEFAULT_WAKE_WORD)
    detected = detector.listen_for_wake_word(timeout=15)

    if detected:
        logging.info("Wake word successfully detected 🎉")
        detector.voice_engine.speak("Wake word confirmed! Ready for commands.")
    else:
        logging.warning("No wake word detected within timeout ⏰")

    return detected


def full_wake_word_test():
    """Full workflow test: wake word + infrastructure command."""
    detector = WakeWordDetector(wake_word=DEFAULT_WAKE_WORD)
    success, result = detector.wait_for_wake_word_then_listen()

    if success:
        logging.info(f"SUCCESS! Command received: '{result}' ✅")
        detector.voice_engine.speak(f"Command received: {result}")
    else:
        logging.error(f"RESULT: {result} ❌")


# ---------------- MAIN EXECUTION ----------------
if __name__ == "__main__":
    try:
        logging.info("🔔 Running Wake Word Detector Test Suite")
        simple_wake_word_test()
        # Uncomment to run full test
        # full_wake_word_test()

    except KeyboardInterrupt:
        logging.info("Interrupted by user (Ctrl+C). Exiting gracefully...")
