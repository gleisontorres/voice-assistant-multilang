"""
Módulo para integração com a API do ChatGPT (OpenAI).
"""

import os
import openai
from typing import List, Dict, Optional


class ChatGPTClient:
    """Cliente para interação com a API do ChatGPT."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Inicializa o cliente ChatGPT.
        
        Args:
            api_key: Chave da API OpenAI (usa variável de ambiente se None)
            model: Modelo a ser usado (gpt-3.5-turbo, gpt-4, etc.)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API Key não encontrada! "
                "Configure a variável OPENAI_API_KEY ou passe como parâmetro."
            )
        
        openai.api_key = self.api_key
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
        
        print(f"✅ Cliente ChatGPT inicializado (modelo: {model})")
    
    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """
        Envia uma mensagem para o ChatGPT.
        
        Args:
            message: Mensagem do usuário
            system_prompt: Prompt do sistema (opcional)
            
        Returns:
            Resposta do ChatGPT
        """
        messages = []
        
        # Adiciona prompt do sistema se fornecido
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Adiciona histórico de conversação
        messages.extend(self.conversation_history)
        
        # Adiciona nova mensagem
        messages.append({"role": "user", "content": message})
        
        print(f"💬 Enviando para ChatGPT: {message}")
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            
            assistant_message = response.choices[0].message.content
            
            # Atualiza histórico
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            print(f"🤖 Resposta: {assistant_message}")
            return assistant_message
            
        except Exception as e:
            print(f"❌ Erro ao comunicar com ChatGPT: {e}")
            raise
    
    def clear_history(self):
        """Limpa o histórico de conversação."""
        self.conversation_history = []
        print("🗑️ Histórico limpo")
    
    def set_system_prompt(self, prompt: str):
        """
        Define um prompt de sistema padrão.
        
        Args:
            prompt: Prompt do sistema
        """
        self.conversation_history.insert(0, {"role": "system", "content": prompt})


def ask_chatgpt(question: str, model: str = "gpt-4", api_key: Optional[str] = None) -> str:
    """
    Função auxiliar para perguntas rápidas ao ChatGPT.
    
    Args:
        question: Pergunta
        model: Modelo ChatGPT
        api_key: API Key (opcional)
        
    Returns:
        Resposta do ChatGPT
    """
    client = ChatGPTClient(api_key=api_key, model=model)
    return client.send_message(question)


if __name__ == "__main__":
    # Teste do módulo
    import sys
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        answer = ask_chatgpt(question)
        print(f"\n✅ Resposta: {answer}")
    else:
        print("Uso: python chatgpt_client.py <sua pergunta>")
