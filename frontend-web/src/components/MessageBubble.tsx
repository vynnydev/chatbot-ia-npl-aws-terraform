import IntentDisplay from './IntentDisplay';

interface Intent {
  intent: string;
  confidence: number;
}

interface MessageBubbleProps {
  text: string;
  sender: 'user' | 'bot';
  intents?: Intent[];
  timestamp: Date;
}

export default function MessageBubble({
  text,
  sender,
  intents,
  timestamp,
}: MessageBubbleProps) {
  const isUser = sender === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[70%] rounded-2xl p-4 shadow-md transition-all duration-200 hover:shadow-lg ${
          isUser
            ? 'bg-gradient-to-br from-primary to-accent text-white rounded-br-none'
            : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
        }`}
      >
        {!isUser && (
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xl">🤖</span>
            <span className="text-xs font-semibold text-gray-500">El Sabor Bot</span>
          </div>
        )}

        <p className="whitespace-pre-wrap text-sm leading-relaxed">{text}</p>

        {!isUser && intents && intents.length > 0 && (
          <IntentDisplay intents={intents} />
        )}

        <p className={`text-xs mt-2 ${isUser ? 'text-white opacity-70' : 'text-gray-500'}`}>
          {timestamp.toLocaleTimeString('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </p>
      </div>
    </div>
  );
}