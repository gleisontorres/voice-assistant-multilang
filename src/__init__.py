"""
Voice Assistant Multi-Language Package
"""

from .voice_assistant import VoiceAssistant, create_assistant
from .audio_recorder import AudioRecorder, record_audio
from .speech_to_text import SpeechToText, transcribe_audio
from .chatgpt_client import ChatGPTClient, ask_chatgpt
from .text_to_speech import TextToSpeech, text_to_speech, play_audio

__version__ = "1.0.0"
__author__ = "Gleison"

__all__ = [
    "VoiceAssistant",
    "create_assistant",
    "AudioRecorder",
    "record_audio",
    "SpeechToText",
    "transcribe_audio",
    "ChatGPTClient",
    "ask_chatgpt",
    "TextToSpeech",
    "text_to_speech",
    "play_audio",
]
