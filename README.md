# Sakura Voice

Configuración experimental para probar localmente la detección de la palabra de activación **“hey mycroft”** con openWakeWord y ONNX.

## Estado

Esta publicación contiene una prueba de micrófono y detección en tiempo real. No reconoce “Oye, Sakura”, no usa un modelo personalizado y todavía no activa Open WebUI. El detector principal requiere integrar y validar esos pasos por separado.

## Requisitos

- Windows 10/11
- Python 3.11
- Un micrófono habilitado en Windows

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Probar el micrófono

Desde la carpeta del proyecto, ejecuta:

```powershell
python test_mic_oww.py
```

El programa muestra las entradas disponibles. Presiona Enter para elegir la entrada predeterminada o escribe el índice de otro micrófono. Luego di **“hey mycroft”** en inglés cerca del micrófono. Un score de 0.5 o más indica una detección. Presiona Ctrl+C para salir.

El script también muestra el nivel de audio. Si aparece **“sin señal / muy bajo”**, revisa que el dispositivo correcto esté seleccionado, que no esté silenciado y que Windows permita el acceso al micrófono. Los índices de dispositivo pueden cambiar entre equipos o sesiones.

## Modelos

La prueba usa el modelo preentrenado `hey_mycroft_v0.1.onnx` que openWakeWord carga desde sus recursos instalados. No se incluyen modelos personalizados ni grabaciones de voz.

## Privacidad

La captura y la inferencia de esta prueba se realizan localmente. El script no guarda ni transmite audio.

## Licencias

Revisa las licencias de openWakeWord y de sus modelos antes de redistribuirlos. Este repositorio no redistribuye esos archivos.
