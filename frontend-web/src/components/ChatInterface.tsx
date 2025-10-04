/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import MessageBubble from './MessageBubble';

const API_URL = 'http://el-sabor-prod-alb-380735521.us-east-1.elb.amazonaws.com';

interface Intent {
  intent: string;
  confidence: number;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  intents?: Intent[];
  timestamp: Date;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const [isTyping, setIsTyping] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    const welcomeMessage: Message = {
      id: uuidv4(),
      text: '¡Hola! Bem-vindo ao El Sabor! 🌮\n\nSou seu assistente virtual e estou aqui para te ajudar!\n\nVocê pode:\n• Ver nosso cardápio\n• Fazer pedidos\n• Consultar preços\n• Tirar dúvidas\n\nComo posso te ajudar hoje?',
      sender: 'bot',
      timestamp: new Date(),
    };
    setMessages([welcomeMessage]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: uuidv4(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setIsTyping(true);
    setError(null);

    try {
      const response = await axios.post(
        `${API_URL}/api/chat`,
        {
          message: input,
          session_id: sessionId,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
          timeout: 10000,
        }
      );

      await new Promise((resolve) => setTimeout(resolve, 500));

      const botMessage: Message = {
        id: uuidv4(),
        text: response.data.response,
        sender: 'bot',
        intents: response.data.intents,
        timestamp: new Date(response.data.timestamp),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err: any) {
      console.error('Error sending message:', err);

      let errorText = 'Desculpe, ocorreu um erro ao processar sua mensagem. 😔';
      
      if (err.code === 'ECONNABORTED') {
        errorText = 'A requisição demorou muito. Tente novamente!';
      } else if (err.response?.status === 503) {
        errorText = 'O serviço está temporariamente indisponível. Aguarde um momento e tente novamente.';
      } else if (err.response?.data?.detail) {
        errorText = `Erro: ${err.response.data.detail}`;
      }

      setError(errorText);

      const errorMessage: Message = {
        id: uuidv4(),
        text: errorText,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
      setIsTyping(false);
      inputRef.current?.focus();
    }
  }

  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  const quickActions = [
    { icon: '📋', text: 'Ver cardápio', message: 'Quero ver o cardápio' },
    { icon: '💰', text: 'Preços', message: 'Quais são os preços?' },
    { icon: '🛒', text: 'Fazer pedido', message: 'Quero fazer um pedido' },
    { icon: '🚗', text: 'Tempo de entrega', message: 'Quanto tempo demora a entrega?' },
  ];

  return (
    <div className="flex flex-col h-full">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 mx-4 mt-4 rounded">
          <p className="text-sm">{error}</p>
          <button
            onClick={() => setError(null)}
            className="text-xs underline mt-1"
          >
            Fechar
          </button>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        <div className="max-w-4xl mx-auto">
          {messages.map((message) => (
            <MessageBubble
              text={message.text}
              key={message.id}
              sender={message.sender}
              intents={message.intents}
              timestamp={message.timestamp}
            />
          ))}

          {isTyping && (
            <div className="flex justify-start mb-4">
              <div className="bg-white rounded-2xl p-4 shadow-md rounded-bl-none border border-gray-200">
                <div className="flex items-center gap-2">
                  <span className="text-xl">🤖</span>
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {messages.length <= 1 && (
        <div className="px-4 pb-2">
          <div className="max-w-4xl mx-auto">
            <p className="text-xs text-gray-500 mb-2 text-center">Ações rápidas:</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {quickActions.map((action, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setInput(action.message);
                    inputRef.current?.focus();
                  }}
                  className="flex items-center justify-center gap-2 p-3 bg-white border border-gray-200 rounded-lg hover:border-primary hover:bg-orange-50 transition-all text-sm"
                  disabled={loading}
                >
                  <span>{action.icon}</span>
                  <span className="text-xs font-medium">{action.text}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto flex gap-2">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e: { target: { value: any; }; }) => setInput(e.target.value)}
            onKeyDown={(e: { key: any; }) => handleKeyPress(e as any)}
            placeholder="Digite sua mensagem..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
            disabled={loading}
            rows={1}
            style={{ minHeight: '48px', maxHeight: '120px' }}
          />
          <button
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            className="px-6 py-3 bg-primary text-white rounded-full hover:bg-accent transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-md hover:shadow-lg"
          >
            {loading ? '⏳' : '📤'}
          </button>
        </div>
      </div>
    </div>
  );
}