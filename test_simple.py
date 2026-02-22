"""
Script de teste simples para verificar se tudo está funcionando
Testa apenas o ChatGPT (sem áudio) para validar a API Key
"""

import os
import sys
from dotenv import load_dotenv

# Adiciona o diretório raiz ao PATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src import ChatGPTClient

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

print("=" * 60)
print("🧪 TESTE SIMPLES DO ASSISTENTE DE VOZ")
print("=" * 60)

# Verifica se a API Key está configurada
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("\n❌ ERRO: API Key não encontrada!")
    print("\n📝 Configure sua API Key no arquivo .env:")
    print("   OPENAI_API_KEY=sk-sua_chave_aqui")
    print("\n💡 Ou crie o arquivo .env copiando o .env.example")
    sys.exit(1)

print(f"\n✅ API Key encontrada: {api_key[:20]}...")

# Testa a conexão com ChatGPT
try:
    print("\n🔄 Testando conexão com ChatGPT...")
    
    # Cria o cliente (usando gpt-3.5-turbo que é mais rápido e barato)
    chat = ChatGPTClient(model="gpt-3.5-turbo")
    
    # Faz uma pergunta simples
    pergunta = "Olá! Me conte uma curiosidade interessante sobre Python em uma frase."
    print(f"\n💬 Pergunta: {pergunta}")
    print("\n⏳ Aguarde a resposta...")
    
    resposta = chat.send_message(pergunta)
    
    print("\n" + "=" * 60)
    print("✅ TESTE BEM-SUCEDIDO!")
    print("=" * 60)
    print(f"\n🤖 Resposta do ChatGPT:\n{resposta}")
    print("\n" + "=" * 60)
    print("\n🎉 Tudo funcionando! Agora você pode:")
    print("   1. Testar os exemplos: python examples/usage_examples.py")
    print("   2. Rodar o assistente: python src/main.py")
    print("=" * 60)
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ ERRO NO TESTE")
    print("=" * 60)
    print(f"\n{e}")
    print("\n💡 Possíveis soluções:")
    print("   1. Verifique se sua API Key está correta")
    print("   2. Confira se você tem créditos na conta OpenAI")
    print("   3. Tente instalar novamente: pip install openai")
    print("=" * 60)
    sys.exit(1)
