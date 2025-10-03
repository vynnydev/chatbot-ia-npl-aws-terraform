interface Intent {
    intent: string;
    confidence: number;
  }
  
  interface IntentDisplayProps {
    intents: Intent[];
  }
  
  export default function IntentDisplay({ intents }: IntentDisplayProps) {
    if (!intents || intents.length === 0) return null;
  
    const getIntentIcon = (intentName: string): string => {
      const icons: { [key: string]: string } = {
        compra: '🛒',
        cardapio: '📋',
        preco: '💰',
        entrega: '🚗',
        agradecimento: '🙏',
        reclamacao: '😔',
        cumprimento: '👋',
        despedida: '👋',
        personalizacao: '⚙️',
        duvida: '❓',
        unknown: '🤔',
      };
      return icons[intentName] || '💬';
    };
  
    const getIntentLabel = (intentName: string): string => {
      const labels: { [key: string]: string } = {
        compra: 'Compra',
        cardapio: 'Cardápio',
        preco: 'Preço',
        entrega: 'Entrega',
        agradecimento: 'Agradecimento',
        reclamacao: 'Reclamação',
        cumprimento: 'Cumprimento',
        despedida: 'Despedida',
        personalizacao: 'Personalização',
        duvida: 'Dúvida',
        unknown: 'Não identificado',
      };
      return labels[intentName] || intentName;
    };
  
    const getConfidenceColor = (confidence: number): string => {
      if (confidence >= 0.8) return 'bg-green-100 text-green-700 border-green-300';
      if (confidence >= 0.6) return 'bg-yellow-100 text-yellow-700 border-yellow-300';
      return 'bg-red-100 text-red-700 border-red-300';
    };
  
    return (
      <div className="mt-3 pt-3 border-t border-gray-200">
        <p className="text-xs font-semibold mb-2 text-gray-600 flex items-center gap-1">
          <span>🎯</span>
          <span>Intenções Detectadas:</span>
        </p>
        <div className="space-y-2">
          {intents.map((intent, idx) => (
            <div 
              key={idx} 
              className={`flex justify-between items-center p-2 rounded-lg border ${getConfidenceColor(intent.confidence)}`}
            >
              <div className="flex items-center gap-2">
                <span className="text-base">{getIntentIcon(intent.intent)}</span>
                <span className="text-xs font-medium">
                  {getIntentLabel(intent.intent)}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-16 bg-white bg-opacity-50 rounded-full h-2 overflow-hidden">
                  <div
                    className="bg-current h-full transition-all duration-300"
                    style={{ width: `${intent.confidence * 100}%` }}
                  />
                </div>
                <span className="text-xs font-bold min-w-[45px] text-right">
                  {(intent.confidence * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
}