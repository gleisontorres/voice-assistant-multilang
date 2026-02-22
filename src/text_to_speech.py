"""
Módulo para síntese de voz usando gTTS (Google Text-to-Speech).
"""

import os
from gtts import gTTS
from typing import Optional
try:
    from IPython.display import Audio, display
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False


class TextToSpeech:
    """Classe para conversão de texto em voz."""
    
    def __init__(self, language: str = "pt", slow: bool = False):
        """
        Inicializa o sintetizador de voz.
        
        Args:
            language: Código do idioma (pt, en, es, etc.)
            slow: Se True, fala mais devagar
        """
        self.language = language
        self.slow = slow
    
    def synthesize(
        self, 
        text: str, 
        output_file: str = "response.wav",
        language: Optional[str] = None,
        auto_play: bool = False
    ) -> str:
        """
        Converte texto em áudio.
        
        Args:
            text: Texto para sintetizar
            output_file: Arquivo de saída
            language: Idioma (usa o padrão se não especificado)
            auto_play: Se True, toca o áudio automaticamente (apenas em notebooks)
            
        Returns:
            Caminho do arquivo de áudio
        """
        lang = language or self.language
        
        print(f"🔊 Sintetizando voz (idioma: {lang})...")
        
        try:
            # Cria objeto gTTS
            tts = gTTS(text=text, lang=lang, slow=self.slow)
            
            # Salva o arquivo
            tts.save(output_file)
            print(f"✅ Áudio salvo em: {output_file}")
            
            # Reproduz automaticamente se solicitado (apenas em notebooks)
            if auto_play and IPYTHON_AVAILABLE:
                display(Audio(output_file, autoplay=True))
            
            return output_file
            
        except Exception as e:
            print(f"❌ Erro ao sintetizar voz: {e}")
            raise
    
    def speak(self, text: str, language: Optional[str] = None):
        """
        Sintetiza e reproduz o áudio (em notebooks).
        
        Args:
            text: Texto para falar
            language: Idioma opcional
        """
        output_file = "temp_speech.wav"
        self.synthesize(text, output_file, language, auto_play=True)


def text_to_speech(
    text: str, 
    output_file: str = "output.wav", 
    language: str = "pt"
) -> str:
    """
    Função auxiliar para síntese rápida.
    
    Args:
        text: Texto para sintetizar
        output_file: Arquivo de saída
        language: Idioma
        
    Returns:
        Caminho do arquivo de áudio
    """
    tts = TextToSpeech(language=language)
    return tts.synthesize(text, output_file)


def play_audio(audio_file: str):
    """
    Reproduz um arquivo de áudio (apenas em notebooks).
    
    Args:
        audio_file: Caminho do arquivo
    """
    if IPYTHON_AVAILABLE:
        display(Audio(audio_file, autoplay=True))
    else:
        print(f"⚠️ Reprodução automática disponível apenas em notebooks Jupyter")
        print(f"📁 Arquivo salvo em: {audio_file}")


if __name__ == "__main__":
    # Teste do módulo
    import sys
    
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        audio_file = text_to_speech(text, language="pt")
        print(f"\n✅ Áudio gerado: {audio_file}")
    else:
        # Teste padrão
        text = "Olá! Este é um teste de síntese de voz em português."
        audio_file = text_to_speech(text)
        print(f"\n✅ Teste concluído: {audio_file}")
