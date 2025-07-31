import re
import random
from typing import List, Dict, Any

class AIProcessor:
    """Local AI processing for SmartStudy without external APIs"""
    
    def __init__(self):
        self.educational_quotes = [
            "Education is not the learning of facts, but the training of the mind to think. – Albert Einstein",
            "The beautiful thing about learning is that nobody can take it away from you. – B.B. King",
            "Your education is a dress rehearsal for a life that is yours to lead. – Nora Ephron",
            "Education is the most powerful weapon which you can use to change the world. – Nelson Mandela",
            "The more that you read, the more things you will know. The more that you learn, the more places you'll go. – Dr. Seuss",
            "Live as if you were to die tomorrow. Learn as if you were to live forever. – Mahatma Gandhi",
            "Tell me and I forget, teach me and I may remember, involve me and I learn. – Benjamin Franklin",
            "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice. – Brian Herbert"
        ]
        
        self.quick_questions = [
            "Explain the concept of photosynthesis",
            "What is machine learning?",
            "How do I solve quadratic equations?",
            "Explain the water cycle",
            "What is the theory of relativity?",
            "How does DNA replication work?"
        ]
        
        self.knowledge_base = {
            "photosynthesis": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar. It occurs in the chloroplasts of plant cells and involves two main stages: light-dependent reactions and the Calvin cycle.",
            "machine learning": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions with minimal human intervention.",
            "quadratic equations": "Quadratic equations are polynomial equations of degree 2, typically in the form ax² + bx + c = 0. They can be solved using the quadratic formula: x = (-b ± √(b²-4ac)) / 2a, by factoring, or by completing the square.",
            "water cycle": "The water cycle is the continuous movement of water on, above, and below Earth's surface. It includes processes like evaporation, condensation, precipitation, and collection, driven by solar energy and gravity.",
            "theory of relativity": "Einstein's theory of relativity consists of special relativity (dealing with objects moving at constant speeds) and general relativity (dealing with gravity). It shows that space and time are interconnected and relative to the observer's motion.",
            "dna replication": "DNA replication is the process by which DNA makes a copy of itself. It involves unwinding the double helix, separating the strands, and using each strand as a template to create complementary new strands."
        }
    
    def get_educational_quotes(self) -> List[str]:
        """Return list of educational quotes for rotation"""
        return self.educational_quotes
    
    def get_quick_questions(self) -> List[str]:
        """Return list of quick questions for the assistant"""
        return self.quick_questions
    
    def summarize_text(self, text: str) -> str:
        """Simple text summarization using extractive method"""
        if len(text) < 100:
            return "Text too short to summarize effectively. Please provide longer content."
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= 3:
            return text
        
        # Simple scoring based on word frequency and position
        word_freq = {}
        words = re.findall(r'\b\w+\b', text.lower())
        for word in words:
            if len(word) > 3:  # Skip short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            score = 0
            sentence_words = re.findall(r'\b\w+\b', sentence.lower())
            for word in sentence_words:
                if word in word_freq:
                    score += word_freq[word]
            
            # Boost score for sentences at beginning and end
            if i < 2 or i >= len(sentences) - 2:
                score *= 1.2
            
            sentence_scores.append((score, sentence))
        
        # Select top sentences (roughly 1/3 of original)
        sentence_scores.sort(reverse=True)
        num_sentences = max(2, len(sentences) // 3)
        selected = sentence_scores[:num_sentences]
        
        # Sort by original order
        selected_sentences = []
        for score, sentence in selected:
            original_index = sentences.index(sentence)
            selected_sentences.append((original_index, sentence))
        
        selected_sentences.sort()
        summary = '. '.join([sent for _, sent in selected_sentences]) + '.'
        
        return summary
    
    def generate_flashcards(self, text: str) -> List[Dict[str, str]]:
        """Generate flashcards from text"""
        if len(text) < 50:
            return []
        
        # Simple keyword extraction
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        flashcards = []
        
        # Look for definition patterns
        for sentence in sentences:
            if any(word in sentence.lower() for word in ['is', 'are', 'means', 'refers to', 'defined as']):
                parts = re.split(r'\s+(?:is|are|means|refers to|defined as)\s+', sentence, 1)
                if len(parts) == 2:
                    term = parts[0].strip()
                    definition = parts[1].strip()
                    if len(term) < 50 and len(definition) > 10:
                        flashcards.append({
                            'front': f"What is {term}?",
                            'back': definition
                        })
        
        # Generate question-based flashcards from key phrases
        key_phrases = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        for phrase in key_phrases[:5]:  # Limit to 5
            if len(phrase.split()) <= 3:
                flashcards.append({
                    'front': f"Explain the concept of {phrase}",
                    'back': f"Based on the provided text: {phrase} is discussed in the context of the material you studied."
                })
        
        return flashcards[:10]  # Limit to 10 flashcards
    
    def get_assistant_response(self, question: str) -> str:
        """Generate AI assistant response"""
        question_lower = question.lower()
        
        # Check for matches in knowledge base
        for key, answer in self.knowledge_base.items():
            if key in question_lower or any(word in question_lower for word in key.split()):
                return answer
        
        # Generic responses for common question types
        if any(word in question_lower for word in ['what', 'explain', 'define']):
            return "I'd be happy to help explain that concept! Could you provide more specific details about what aspect you'd like me to focus on? I can help with topics in science, mathematics, programming, and general academic subjects."
        
        elif any(word in question_lower for word in ['how', 'solve', 'calculate']):
            return "For problem-solving questions, I recommend breaking down the problem into smaller steps. Could you share the specific problem or equation you're working with? I can guide you through the solution process."
        
        elif any(word in question_lower for word in ['why', 'reason', 'cause']):
            return "That's a great analytical question! Understanding the 'why' behind concepts is crucial for deeper learning. Could you provide more context about the specific topic you're exploring?"
        
        else:
            return "I'm here to help with your studies! I can assist with explanations, problem-solving, and study strategies across various subjects. What specific topic would you like to explore?"
    
    def get_activity_data(self) -> Dict[str, Any]:
        """Generate activity data for charts"""
        days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
        activities = [0, 0, 0, 0, 0, 0, 3]  # Current activity pattern
        
        return {
            'labels': days,
            'data': activities,
            'total_activities': sum(activities)
        }
