"""
Voice Module - Handles speech recognition, text-to-speech, and wake word detection
"""

from .speech_recognition_module import SpeechRecognizer
from .text_to_speech_module import TextToSpeech
from .wake_word_detector import WakeWordDetector

__all__ = ['SpeechRecognizer', 'TextToSpeech', 'WakeWordDetector']
