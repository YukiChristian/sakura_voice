"""Prueba interactiva de openWakeWord con un micrófono seleccionado."""
import sys
import time

import numpy as np
import pyaudio
from openwakeword.model import Model

RATE = 16000
CHUNK = 1280  # 80 ms
THRESHOLD = 0.5


def main():
    audio = pyaudio.PyAudio()
    stream = None
    try:
        inputs = []
        print("Entradas de micrófono disponibles:")
        default_index = audio.get_default_input_device_info().get("index")
        for index in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(index)
            if info.get("maxInputChannels", 0) > 0:
                inputs.append((index, info))
                default = " (predeterminado)" if index == default_index else ""
                print(f"  [{index}] {info['name']} — {int(info['maxInputChannels'])} canal(es){default}")
        if not inputs:
            print("No se encontraron entradas de micrófono.")
            return 1

        choice = input("\nÍndice a usar (Enter = predeterminado): ").strip()
        device_index = int(choice) if choice else default_index
        selected = next((info for index, info in inputs if index == device_index), None)
        if selected is None:
            print("Ese índice no corresponde a una entrada de micrófono.")
            return 2

        print(f"\nUsando: {selected['name']} (índice {device_index})")
        print("Cargando el modelo hey_mycroft...")
        model = Model(wakeword_models=["hey_mycroft_v0.1.onnx"], inference_framework="onnx")
        print("Modelo listo. Di ‘hey mycroft’ cerca del micrófono. Ctrl+C para salir.\n")

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=CHUNK,
        )
        frames = 0
        last_detection = 0.0
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            samples = np.frombuffer(data, dtype=np.int16)
            rms = float(np.sqrt(np.mean(samples.astype(np.float32) ** 2)))
            scores = model.predict(samples)
            score = max((float(value) for value in scores.values()), default=0.0)
            frames += 1
            if frames % 5 == 0:
                level = "sin señal / muy bajo" if rms < 30 else f"nivel {rms:.0f}"
                print(f"\r{level} | hey_mycroft: {score:.4f}   ", end="", flush=True)
            if score >= THRESHOLD and time.monotonic() - last_detection > 2:
                print(f"\n¡DETECTADO! hey mycroft (score {score:.3f})")
                last_detection = time.monotonic()
    except KeyboardInterrupt:
        print("\nPrueba finalizada.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"\nNo se pudo abrir o leer ese micrófono: {exc}")
        return 3
    finally:
        if stream is not None:
            stream.stop_stream()
            stream.close()
        audio.terminate()


if __name__ == "__main__":
    sys.exit(main())

