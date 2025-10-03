"""
Processador NLP - Motor do chatbot
"""
import spacy
import re
import unicodedata
from typing import List, Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .config import get_settings

settings = get_settings()


class NLPProcessor:
    """Processador de linguagem natural"""
    
    def __init__(self):
        """Inicializa o processador NLP"""
        try:
            self.nlp = spacy.load(settings.SPACY_MODEL)
        except OSError:
            print(f"Modelo {settings.SPACY_MODEL} não encontrado. Baixando...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", settings.SPACY_MODEL])
            self.nlp = spacy.load(settings.SPACY_MODEL)
        
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            ngram_range=(1, 2),
            stop_words=self._get_stop_words()
        )
        self.intents_data: Dict = {}
        self.patterns_vectorized = None
    
    def _get_stop_words(self) -> List[str]:
        """Retorna lista de stop words em português"""
        return [
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
            'em', 'no', 'na', 'nos', 'nas', 'por', 'para', 'com', 'sem',
            'e', 'ou', 'mas', 'que', 'se', 'ele', 'ela', 'eles', 'elas'
        ]
    
    def preprocess_text(self, text: str) -> str:
        """
        Pré-processa o texto
        
        Args:
            text: Texto para processar
            
        Returns:
            Texto processado
        """
        # Lowercase
        text = text.lower()
        
        # Remove acentos
        text = ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )
        
        # Remove caracteres especiais mantendo espaços
        text = re.sub(r'[^a-z0-9\s]', '', text)
        
        # Remove espaços múltiplos
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokeniza o texto
        
        Args:
            text: Texto para tokenizar
            
        Returns:
            Lista de tokens
        """
        doc = self.nlp(text)
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        return tokens
    
    def lemmatize(self, text: str) -> str:
        """
        Lematiza o texto
        
        Args:
            text: Texto para lematizar
            
        Returns:
            Texto lematizado
        """
        doc = self.nlp(text)
        lemmas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(lemmas)
    
    def load_intents(self, intents: Dict):
        """
        Carrega intenções e treina o modelo
        
        Args:
            intents: Dicionário com intenções {name: {patterns: [], responses: []}}
        """
        self.intents_data = intents
        
        # Criar lista de todos os patterns
        all_patterns = []
        pattern_to_intent = []
        
        for intent_name, intent_data in intents.items():
            for pattern in intent_data.get('patterns', []):
                processed = self.preprocess_text(pattern)
                all_patterns.append(processed)
                pattern_to_intent.append(intent_name)
        
        # Vetorizar patterns
        if all_patterns:
            self.patterns_vectorized = self.vectorizer.fit_transform(all_patterns)
            self.pattern_to_intent = pattern_to_intent
    
    def detect_intent(self, message: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Detecta intenção(ões) na mensagem
        
        Args:
            message: Mensagem do usuário
            top_k: Número de intenções para retornar
            
        Returns:
            Lista de tuplas (intent, confidence)
        """
        # Preprocessar mensagem
        processed_message = self.preprocess_text(message)
        
        # Vetorizar mensagem
        message_vector = self.vectorizer.transform([processed_message])
        
        # Calcular similaridade com todos os patterns
        similarities = cosine_similarity(message_vector, self.patterns_vectorized)[0]
        
        # Pegar top K matches
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Agrupar por intenção e pegar maior confiança
        intent_scores = {}
        for idx in top_indices:
            intent = self.pattern_to_intent[idx]
            score = float(similarities[idx])
            
            if score < settings.CONFIDENCE_THRESHOLD:
                continue
            
            if intent not in intent_scores or score > intent_scores[intent]:
                intent_scores[intent] = score
        
        # Converter para lista ordenada
        results = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Se nenhuma intenção detectada, retornar "unknown"
        if not results:
            results = [("unknown", 0.0)]
        
        return results[:top_k]
    
    def split_multiple_intents(self, message: str) -> List[str]:
        """
        Divide mensagem com múltiplas intenções
        
        Args:
            message: Mensagem do usuário
            
        Returns:
            Lista de sub-mensagens
        """
        # Dividir por conectores
        separators = [' e ', ', ', ' mas ', ' porém ', ' também ']
        
        segments = [message]
        for sep in separators:
            new_segments = []
            for segment in segments:
                new_segments.extend(segment.split(sep))
            segments = new_segments
        
        # Filtrar segmentos vazios
        segments = [s.strip() for s in segments if s.strip()]
        
        return segments if len(segments) > 1 else [message]


# Singleton global
nlp_processor = NLPProcessor()