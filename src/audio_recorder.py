"""
Módulo para gravação de áudio via microfone.
Suporta tanto PyAudio quanto SoundDevice.
"""

import os
import wave
import numpy as np
from typing import Optional

try:
    import sounddevice as sd
    import soundfile as sf
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False

try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False


class AudioRecorder:
    """Classe para gravar áudio do microfone."""
    
    def __init__(self, sample_rate: int = 44100):
        """
        Inicializa o gravador de áudio.
        
        Args:
            sample_rate: Taxa de amostragem em Hz (padrão: 44100)
        """
        self.sample_rate = sample_rate
        
    def record(self, duration: int = 5, output_file: str = "audio.wav") -> str:
        """
        Grava áudio do microfone.
        
        Args:
            duration: Duração da gravação em segundos
            output_file: Caminho do arquivo de saída
            
        Returns:
            Caminho do arquivo de áudio gravado
        """
        print(f"🎤 Gravando por {duration} segundos...")
        
        if SOUNDDEVICE_AVAILABLE:
            return self._record_sounddevice(duration, output_file)
        elif PYAUDIO_AVAILABLE:
            return self._record_pyaudio(duration, output_file)
        else:
            raise RuntimeError(
                "Nenhuma biblioteca de áudio disponível. "
                "Instale 'sounddevice' ou 'pyaudio'."
            )
    
    def _record_sounddevice(self, duration: int, output_file: str) -> str:
        """Grava usando sounddevice (recomendado)."""
        recording = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        
        # Salva o arquivo
        sf.write(output_file, recording, self.sample_rate)
        print(f"✅ Áudio salvo em: {output_file}")
        return output_file
    
    def _record_pyaudio(self, duration: int, output_file: str) -> str:
        """Grava usando PyAudio."""
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        
        p = pyaudio.PyAudio()
        
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        frames = []
        
        for i in range(0, int(self.sample_rate / CHUNK * duration)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        # Salva o arquivo WAV
        wf = wave.open(output_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        print(f"✅ Áudio salvo em: {output_file}")
        return output_file


def record_audio(duration: int = 5, output_file: str = "audio.wav") -> str:
    """
    Função auxiliar para gravar áudio rapidamente.
    
    Args:
        duration: Duração em segundos
        output_file: Arquivo de saída
        
    Returns:
        Caminho do arquivo gravado
    """
    recorder = AudioRecorder()
    return recorder.record(duration, output_file)


if __name__ == "__main__":
    # Teste do módulo
    print("Testando gravação de áudio...")
    audio_file = record_audio(duration=3, output_file="test_audio.wav")
    print(f"Gravação concluída: {audio_file}")
