from scr.integration.elite_integration import EliteIntegration, EliteStatusHandler
from scr.integration.ship_state import ShipState
from scr.integration.events import EliteJournalHandler, EventTypes
from scr.voice.tts.tts_engine import TtsEngine
from scr.voice.tts.tts_settings import TTS_SETTINGS, TTS_SAMPLE_RATE, TTS_DEVICE
from scr.voice.stt.speech_recognition import SpeechRecognizer
from scr.voice.stt.stt_settings import SAMPLE_RATE, DEFAULT_DURATION, DEVICE