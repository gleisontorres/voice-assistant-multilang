"""
Exemplos de uso do Assistente de Voz Multi-Idiomas
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import create_assistant

from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


def exemplo_basico():
    """Exemplo básico de uso."""
    print("=" * 60)
    print("EXEMPLO 1: Uso Básico")
    print("=" * 60)
    
    # Cria assistente
    assistant = create_assistant(language="pt", model="gpt-4")
    
    # Faz uma pergunta
    resposta = assistant.ask("Qual é a capital do Brasil?", speak_response=False)
    print(f"Resposta: {resposta}\n")


def exemplo_multilinguagem():
    """Exemplo com múltiplos idiomas."""
    print("=" * 60)
    print("EXEMPLO 2: Multi-Idiomas")
    print("=" * 60)
    
    assistant = create_assistant(language="pt")
    
    # Português
    print("\n🇧🇷 Português:")
    assistant.ask("Olá! Como você está?", speak_response=False)
    
    # Inglês
    print("\n🇺🇸 English:")
    assistant.change_language("en")
    assistant.ask("What is Python?", speak_response=False)
    
    # Espanhol
    print("\n🇪🇸 Español:")
    assistant.change_language("es")
    assistant.ask("¿Cuál es la capital de España?", speak_response=False)


def exemplo_com_voz():
    """Exemplo com gravação de voz."""
    print("=" * 60)
    print("EXEMPLO 3: Interação por Voz")
    print("=" * 60)
    
    assistant = create_assistant(language="pt")
    
    print("\nVocê tem 5 segundos para falar...")
    print("Após a gravação, o sistema irá:")
    print("1. Transcrever sua fala")
    print("2. Processar com ChatGPT")
    print("3. Responder em voz")
    
    # Grava, processa e responde
    resultado = assistant.listen_and_respond(duration=5)
    
    print(f"\n📝 Transcrição: {resultado['user_input']}")
    print(f"🤖 Resposta: {resultado['assistant_response']}")


def exemplo_personalizacao():
    """Exemplo com personalização."""
    print("=" * 60)
    print("EXEMPLO 4: Assistente Personalizado")
    print("=" * 60)
    
    from src import VoiceAssistant
    
    # Cria assistente com prompt personalizado
    system_prompt = """
    Você é um assistente financeiro especializado em investimentos.
    Responda de forma clara e objetiva, focando em educação financeira.
    """
    
    assistant = VoiceAssistant(
        language="pt",
        chatgpt_model="gpt-4",
        system_prompt=system_prompt
    )
    
    # Faz perguntas sobre finanças
    perguntas = [
        "O que é Tesouro Direto?",
        "Vale a pena investir em ações?",
        "Como começar a investir?"
    ]
    
    for pergunta in perguntas:
        print(f"\n💬 Pergunta: {pergunta}")
        resposta = assistant.ask(pergunta, speak_response=False)
        print(f"🤖 Resposta: {resposta[:150]}...")


def exemplo_modulos_separados():
    """Exemplo usando módulos separadamente."""
    print("=" * 60)
    print("EXEMPLO 5: Usando Módulos Individualmente")
    print("=" * 60)
    
    from src import SpeechToText, ChatGPTClient, TextToSpeech
    
    # 1. Apenas transcrição
    print("\n1️⃣ Apenas transcrição de áudio:")
    # stt = SpeechToText(model_name="small", language="pt")
    # texto = stt.transcribe("audio.wav")
    print("(Requer arquivo de áudio)")
    
    # 2. Apenas ChatGPT
    print("\n2️⃣ Apenas ChatGPT:")
    chat = ChatGPTClient(model="gpt-4")
    resposta = chat.send_message("Conte uma piada curta")
    print(f"Resposta: {resposta}")
    
    # 3. Apenas síntese de voz
    print("\n3️⃣ Apenas síntese de voz:")
    tts = TextToSpeech(language="pt")
    audio_file = tts.synthesize("Olá, este é um teste!", output_file="teste.wav")
    print(f"Áudio salvo em: {audio_file}")


if __name__ == "__main__":
    print("\n🧪 EXEMPLOS DE USO DO ASSISTENTE DE VOZ\n")
    
    # Executa exemplos
    try:
        exemplo_basico()
        print("\n")
        
        exemplo_multilinguagem()
        print("\n")
        
        exemplo_personalizacao()
        print("\n")
        
        exemplo_modulos_separados()
        print("\n")
        
        print("✅ Todos os exemplos executados com sucesso!")
        
        # Exemplo com voz (comentado por padrão)
        # exemplo_com_voz()
        
    except Exception as e:
        print(f"❌ Erro ao executar exemplos: {e}")
