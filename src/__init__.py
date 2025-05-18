from src.integration.elite_integration import EliteIntegration, EliteStatusHandler
from src.integration.ship_state import ShipState
from src.integration.events import EliteJournalHandler, EventTypes
from src.voice.tts.tts_engine import TtsEngine
from src.voice.tts.tts_settings import TTS_SETTINGS, TTS_SAMPLE_RATE, TTS_DEVICE
from src.voice.stt.speech_recognition import SpeechRecognizer
from src.voice.stt.stt_settings import SAMPLE_RATE, DEFAULT_DURATION, DEVICE