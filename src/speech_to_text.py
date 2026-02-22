"""
Módulo para transcrição de áudio usando Whisper (OpenAI).
"""

import whisper
from typing import Optional, Dict, Any


class SpeechToText:
    """Classe para conversão de áudio em texto usando Whisper."""
    
    def __init__(self, model_name: str = "small", language: str = "pt"):
        """
        Inicializa o modelo Whisper.
        
        Args:
            model_name: Nome do modelo ('tiny', 'base', 'small', 'medium', 'large')
            language: Código do idioma (pt, en, es, fr, etc.)
        """
        self.language = language
        self.model_name = model_name
        
        print(f"📥 Carregando modelo Whisper '{model_name}'...")
        self.model = whisper.load_model(model_name)
        print(f"✅ Modelo carregado com sucesso!")
    
    def transcribe(self, audio_file: str, language: Optional[str] = None) -> str:
        """
        Transcreve um arquivo de áudio.
        
        Args:
            audio_file: Caminho do arquivo de áudio
            language: Idioma opcional (usa o padrão se não especificado)
            
        Returns:
            Texto transcrito
        """
        lang = language or self.language
        
        print(f"🧠 Transcrevendo áudio (idioma: {lang})...")
        
        result = self.model.transcribe(
            audio_file,
            language=lang,
            fp16=False  # Compatibilidade com CPU
        )
        
        transcription = result["text"].strip()
        print(f"📝 Transcrição: {transcription}")
        
        return transcription
    
    def transcribe_detailed(self, audio_file: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcreve com informações detalhadas.
        
        Args:
            audio_file: Caminho do arquivo de áudio
            language: Idioma opcional
            
        Returns:
            Dicionário com transcrição e metadados
        """
        lang = language or self.language
        
        print(f"🧠 Transcrevendo áudio (modo detalhado)...")
        
        result = self.model.transcribe(
            audio_file,
            language=lang,
            fp16=False,
            verbose=False
        )
        
        return {
            "text": result["text"].strip(),
            "language": result.get("language", lang),
            "segments": result.get("segments", []),
        }


def transcribe_audio(audio_file: str, model: str = "small", language: str = "pt") -> str:
    """
    Função auxiliar para transcrição rápida.
    
    Args:
        audio_file: Arquivo de áudio
        model: Modelo Whisper
        language: Idioma
        
    Returns:
        Texto transcrito
    """
    stt = SpeechToText(model_name=model, language=language)
    return stt.transcribe(audio_file)


if __name__ == "__main__":
    # Teste do módulo
    import sys
    
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        text = transcribe_audio(audio_path)
        print(f"\n✅ Resultado: {text}")
    else:
        print("Uso: python speech_to_text.py <caminho_do_audio>")
