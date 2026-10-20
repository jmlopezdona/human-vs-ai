@echo off
rem Diseña la voz del narrador con el generador de la mesa (Qwen3-TTS VoiceDesign).
set HF_HOME=D:\mesa-modelos\huggingface
set HF_HUB_OFFLINE=1
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
cd /d %~dp0
D:\hades2-dub-work\venv\qwen3tts\Scripts\python.exe disenar.py
