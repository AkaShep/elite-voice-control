@echo off
mkdir models\vosk
curl -L https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip -o models\vosk.zip
tar -xf models\vosk.zip -C models\vosk
del models\vosk.zip