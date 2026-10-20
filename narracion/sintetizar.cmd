@echo off
rem Dice las frases de un idioma con el motor indextts de la mesa.
rem Uso: sintetizar.cmd <es-ES|es-419|en> <voz.wav> [semilla]
setlocal
cd /d %~dp0
set MESA_MODELOS=D:\mesa-modelos
set PYTHONIOENCODING=utf-8
set PYTHONPATH=%~dp0lib
uv run --no-project -q --python 3.12 --with numpy --with soxr==1.1.0 --with "pydantic>=2.13.5" python sintetizar.py %1 %2 tomas-%1 %3
