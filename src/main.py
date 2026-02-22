#!/usr/bin/env python3
"""
Script principal do Assistente de Voz Multi-Idiomas
"""

import os
import sys
from dotenv import load_dotenv
from voice_assistant import VoiceAssistant

# Carrega variáveis de ambiente
load_dotenv()


def print_banner():
    """Exibe banner do assistente."""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║     🎤 ASSISTENTE DE VOZ MULTI-IDIOMAS 🌍              ║
    ║                                                          ║
    ║     Powered by Whisper + ChatGPT + gTTS                 ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Exibe menu de opções."""
    print("\n" + "="*60)
    print("OPÇÕES:")
    print("="*60)
    print("1. 🎤 Falar com o assistente (gravação de voz)")
    print("2. ✍️  Enviar mensagem de texto")
    print("3. 🌍 Alterar idioma")
    print("4. 🗑️  Limpar histórico de conversação")
    print("5. ❌ Sair")
    print("="*60)


def get_language_choice():
    """Solicita escolha de idioma."""
    print("\n🌍 Idiomas disponíveis:")
    languages = {
        "1": ("pt", "Português"),
        "2": ("en", "English"),
        "3": ("es", "Español"),
        "4": ("fr", "Français"),
        "5": ("de", "Deutsch"),
        "6": ("it", "Italiano"),
        "7": ("ja", "日本語"),
        "8": ("zh", "中文"),
    }
    
    for key, (code, name) in languages.items():
        print(f"{key}. {name} ({code})")
    
    choice = input("\nEscolha o idioma (1-8): ").strip()
    return languages.get(choice, ("pt", "Português"))[0]


def main():
    """Função principal."""
    print_banner()
    
    # Verifica API Key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ ERRO: API Key não encontrada!")
        print("Configure a variável OPENAI_API_KEY no arquivo .env")
        sys.exit(1)
    
    # Configurações iniciais
    language = os.getenv("DEFAULT_LANGUAGE", "pt")
    model = os.getenv("DEFAULT_MODEL", "gpt-4")
    whisper_model = os.getenv("WHISPER_MODEL", "small")
    
    # Cria o assistente
    try:
        assistant = VoiceAssistant(
            language=language,
            whisper_model=whisper_model,
            chatgpt_model=model,
            api_key=api_key
        )
    except Exception as e:
        print(f"❌ Erro ao inicializar assistente: {e}")
        sys.exit(1)
    
    # Loop principal
    while True:
        print_menu()
        choice = input("\nEscolha uma opção (1-5): ").strip()
        
        if choice == "1":
            # Gravação de voz
            print("\n🎤 Prepare-se para falar...")
            duration = int(os.getenv("RECORDING_DURATION", "5"))
            
            try:
                result = assistant.listen_and_respond(duration=duration)
                print(f"\n✅ Processamento concluído!")
                print(f"📝 Você disse: {result['user_input']}")
                print(f"🤖 Assistente: {result['assistant_response']}")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif choice == "2":
            # Mensagem de texto
            message = input("\n✍️  Digite sua mensagem: ").strip()
            if message:
                try:
                    response = assistant.ask(message, speak_response=True)
                    print(f"\n🤖 Assistente: {response}")
                except Exception as e:
                    print(f"❌ Erro: {e}")
        
        elif choice == "3":
            # Alterar idioma
            new_language = get_language_choice()
            assistant.change_language(new_language)
        
        elif choice == "4":
            # Limpar histórico
            assistant.clear_conversation()
            print("✅ Histórico limpo!")
        
        elif choice == "5":
            # Sair
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)
