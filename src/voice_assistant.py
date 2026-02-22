"""
Assistente de Voz Multi-Idiomas - Classe Principal
Integra Speech-to-Text, ChatGPT e Text-to-Speech
"""

import os
from typing import Optional
from .audio_recorder import AudioRecorder
from .speech_to_text import SpeechToText
from .chatgpt_client import ChatGPTClient
from .text_to_speech import TextToSpeech


class VoiceAssistant:
    """
    Assistente de voz inteligente que combina:
    - Gravação de áudio
    - Transcrição com Whisper
    - Processamento com ChatGPT
    - Resposta em voz com gTTS
    """
    
    def __init__(
        self,
        language: str = "pt",
        whisper_model: str = "small",
        chatgpt_model: str = "gpt-4",
        api_key: Optional[str] = None,
        system_prompt: Optional[str] = None
    ):
        """
        Inicializa o assistente de voz.
        
        Args:
            language: Idioma (pt, en, es, etc.)
            whisper_model: Modelo Whisper (tiny, base, small, medium, large)
            chatgpt_model: Modelo ChatGPT (gpt-3.5-turbo, gpt-4)
            api_key: API Key OpenAI
            system_prompt: Prompt do sistema para o ChatGPT
        """
        self.language = language
        
        print(f"🚀 Inicializando Assistente de Voz Multi-Idiomas...")
        print(f"🌍 Idioma: {language}")
        
        # Inicializa componentes
        self.recorder = AudioRecorder()
        self.speech_to_text = SpeechToText(model_name=whisper_model, language=language)
        self.chatgpt = ChatGPTClient(api_key=api_key, model=chatgpt_model)
        self.text_to_speech = TextToSpeech(language=language)
        
        # Define prompt do sistema se fornecido
        if system_prompt:
            self.chatgpt.set_system_prompt(system_prompt)
        
        print("✅ Assistente pronto para uso!\n")
    
    def listen_and_respond(
        self, 
        duration: int = 5,
        save_audio: bool = True,
        audio_dir: str = "output"
    ) -> dict:
        """
        Ciclo completo: escuta → transcreve → processa → responde.
        
        Args:
            duration: Duração da gravação em segundos
            save_audio: Se True, salva os arquivos de áudio
            audio_dir: Diretório para salvar áudios
            
        Returns:
            Dicionário com transcrição, resposta e caminhos dos áudios
        """
        # Cria diretório se necessário
        if save_audio and not os.path.exists(audio_dir):
            os.makedirs(audio_dir)
        
        # 1. Grava áudio do usuário
        print("\n" + "="*60)
        input_audio = os.path.join(audio_dir, "user_input.wav") if save_audio else "temp_input.wav"
        self.recorder.record(duration=duration, output_file=input_audio)
        
        # 2. Transcreve áudio
        print("-"*60)
        transcription = self.speech_to_text.transcribe(input_audio)
        
        # 3. Processa com ChatGPT
        print("-"*60)
        response_text = self.chatgpt.send_message(transcription)
        
        # 4. Sintetiza resposta em voz
        print("-"*60)
        output_audio = os.path.join(audio_dir, "assistant_response.wav") if save_audio else "temp_output.wav"
        self.text_to_speech.synthesize(response_text, output_file=output_audio, auto_play=True)
        
        print("="*60 + "\n")
        
        return {
            "user_input": transcription,
            "assistant_response": response_text,
            "input_audio_path": input_audio if save_audio else None,
            "output_audio_path": output_audio if save_audio else None
        }
    
    def ask(self, question: str, speak_response: bool = True) -> str:
        """
        Faz uma pergunta diretamente (sem gravação).
        
        Args:
            question: Pergunta em texto
            speak_response: Se True, sintetiza a resposta em voz
            
        Returns:
            Resposta do assistente
        """
        print(f"\n💬 Você: {question}")
        response = self.chatgpt.send_message(question)
        
        if speak_response:
            self.text_to_speech.synthesize(response, auto_play=True)
        
        return response
    
    def clear_conversation(self):
        """Limpa o histórico de conversação."""
        self.chatgpt.clear_history()
    
    def change_language(self, language: str):
        """
        Altera o idioma do assistente.
        
        Args:
            language: Novo código de idioma (pt, en, es, etc.)
        """
        self.language = language
        self.speech_to_text.language = language
        self.text_to_speech.language = language
        print(f"🌍 Idioma alterado para: {language}")


def create_assistant(
    language: str = "pt",
    model: str = "gpt-4",
    api_key: Optional[str] = None
) -> VoiceAssistant:
    """
    Função auxiliar para criar um assistente rapidamente.
    
    Args:
        language: Idioma
        model: Modelo ChatGPT
        api_key: API Key OpenAI
        
    Returns:
        Instância do VoiceAssistant
    """
    return VoiceAssistant(
        language=language,
        chatgpt_model=model,
        api_key=api_key
    )


if __name__ == "__main__":
    # Teste do assistente
    print("🧪 Testando Assistente de Voz...\n")
    
    # Cria assistente
    assistant = create_assistant(language="pt")
    
    # Teste com pergunta de texto
    assistant.ask("Olá! Como você está?", speak_response=False)
    
    print("\n✅ Teste concluído!")
