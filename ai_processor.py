import re
import random
import time
import threading
from typing import List, Dict, Any
from functools import lru_cache

class AIProcessor:
    """Local AI processing for SmartStudy without external APIs"""

    def __init__(self):
        self.processing_cache = {}
        self.response_times = []
        self.educational_quotes = [
            "Education is not the learning of facts, but the training of the mind to think. – Einstein",
            "The beautiful thing about learning is that nobody can take it away from you. – B.B. King",
            "Your education is a dress rehearsal for a life that is yours to lead. – Nora Ephron",
            "Education is the most powerful weapon which you can use to change the world. – Nelson Mandela",
            "Live as if you were to die tomorrow. Learn as if you were to live forever. – Mahatma Gandhi",
            "An investment in knowledge pays the best interest. – Benjamin Franklin",
            "The expert in anything was once a beginner. – Helen Hayes",
            "Learning never exhausts the mind. – Leonardo da Vinci",
            "Education is what remains after one has forgotten what one has learned in school. – Einstein",
            "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice. – Brian Herbert"
        ]

        self.quick_questions = [
            "Explain the concept of photosynthesis",
            "What is machine learning?",
            "How do I solve quadratic equations?",
            "Explain the water cycle",
            "What is the theory of relativity?",
            "How does DNA replication work?",
            "What are the fundamentals of programming?",
            "Explain Shakespeare's writing style",
            "How do chemical reactions work?",
            "What is calculus used for?",
            "Explain the scientific method",
            "How does the human brain work?"
        ]

        self.knowledge_base = {
            # Science
            "photosynthesis": "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create oxygen and energy in the form of sugar. It occurs in the chloroplasts of plant cells and involves two main stages: light-dependent reactions and the Calvin cycle.",
            "water cycle": "The water cycle is the continuous movement of water on, above, and below Earth's surface. It includes processes like evaporation, condensation, precipitation, and collection, driven by solar energy and gravity.",
            "theory of relativity": "Einstein's theory of relativity consists of special relativity (dealing with objects moving at constant speeds) and general relativity (dealing with gravity). It shows that space and time are interconnected and relative to the observer's motion.",
            "dna replication": "DNA replication is the process by which DNA makes a copy of itself. It involves unwinding the double helix, separating the strands, and using each strand as a template to create complementary new strands.",
            "chemical reactions": "Chemical reactions involve the breaking and forming of bonds between atoms to create new substances. They follow conservation laws and can be classified as synthesis, decomposition, single or double replacement reactions.",
            "scientific method": "The scientific method is a systematic approach to understanding the natural world through observation, hypothesis formation, experimentation, analysis, and conclusion. It ensures reliable and reproducible results.",
            "human brain": "The human brain contains approximately 86 billion neurons that communicate through electrical and chemical signals. It's divided into regions like the cerebrum, cerebellum, and brainstem, each with specialized functions.",

            # Mathematics
            "quadratic equations": "Quadratic equations are polynomial equations of degree 2, typically in the form ax² + bx + c = 0. They can be solved using the quadratic formula: x = (-b ± √(b²-4ac)) / 2a, by factoring, or by completing the square.",
            "calculus": "Calculus is the mathematical study of continuous change. It includes differential calculus (rates of change and slopes) and integral calculus (accumulation of quantities and areas under curves). It's used in physics, engineering, economics, and many other fields.",
            "algebra": "Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. It includes solving equations, working with functions, and understanding mathematical relationships.",
            "geometry": "Geometry is the branch of mathematics concerned with questions of shape, size, relative position of figures, and the properties of space. It includes plane geometry (2D) and solid geometry (3D).",

            # Programming
            "machine learning": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It uses algorithms to analyze data, identify patterns, and make decisions with minimal human intervention.",
            "programming fundamentals": "Programming fundamentals include variables, data types, control structures (loops, conditionals), functions, and algorithms. These building blocks allow developers to create instructions for computers to execute.",
            "algorithms": "Algorithms are step-by-step procedures for solving problems or performing computations. They form the foundation of computer programming and are evaluated based on efficiency, correctness, and clarity.",
            "data structures": "Data structures are ways of organizing and storing data in computers so it can be accessed and modified efficiently. Common examples include arrays, linked lists, stacks, queues, trees, and graphs.",

            # English & Literature
            "shakespeare": "William Shakespeare was an English playwright and poet, widely regarded as the greatest writer in the English language. His works include tragedies like Hamlet and Macbeth, comedies like A Midsummer Night's Dream, and sonnets that explore themes of love, time, and mortality.",
            "essay writing": "Essay writing involves organizing thoughts and arguments in a structured format with an introduction, body paragraphs, and conclusion. Good essays have clear thesis statements, supporting evidence, and logical flow between ideas.",
            "grammar": "Grammar is the system of rules that governs how words are combined to form meaningful sentences. It includes parts of speech, sentence structure, punctuation, and syntax that help communicate ideas clearly."
        }

    def get_educational_quotes(self) -> List[str]:
        """Return list of educational quotes for rotation"""
        return self.educational_quotes

    def get_quick_questions(self) -> List[str]:
        """Return list of quick questions for the assistant"""
        return self.quick_questions

    @lru_cache(maxsize=100)
    def summarize_text(self, text: str, max_length=150, length='medium', style='general'):
        """Generate a summary of the given text with customizable options"""
        try:
            # Determine length parameters
            length_instructions = {
                'short': "in 2-3 sentences",
                'medium': "in 1 paragraph (4-6 sentences)",
                'long': "in 2-3 paragraphs with detailed explanations"
            }

            # Determine style parameters
            style_instructions = {
                'general': "using clear and accessible language",
                'bullet': "as a list of key bullet points",
                'academic': "in formal academic style with precise terminology",
                'simple': "using simple language suitable for beginners"
            }

            length_prompt = length_instructions.get(length, length_instructions['medium'])
            style_prompt = style_instructions.get(style, style_instructions['general'])

            # Enhanced prompt for better summaries
            prompt = f"""Please provide a comprehensive summary of the following text {length_prompt}, {style_prompt}. 
            Focus on the main points, key information, and essential concepts:

            Text: {text}

            Summary:"""

            response = self.get_assistant_response(prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    @lru_cache(maxsize=50)
    def generate_flashcards(self, text: str) -> List[Dict[str, str]]:
        """Enhanced flashcard generation with caching"""
        start_time = time.time()

        cache_key = f"flashcards_{hash(text)}"
        if cache_key in self.processing_cache:
            return self.processing_cache[cache_key]

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

        flashcards = flashcards[:10]  # Limit to 10 flashcards

        # Cache the result
        self.processing_cache[cache_key] = flashcards

        # Track performance
        processing_time = time.time() - start_time
        self.response_times.append(processing_time)

        return flashcards

    def get_assistant_response(self, question: str) -> str:
        """Enhanced AI assistant response with context awareness"""
        start_time = time.time()
        question_lower = question.lower()

        # Performance boost with caching
        cache_key = f"response_{hash(question_lower)}"
        if cache_key in self.processing_cache:
            return self.processing_cache[cache_key]

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
            response = "I'm here to help with your studies! I can assist with explanations, problem-solving, and study strategies across various subjects. What specific topic would you like to explore?"

        # Cache the response
        self.processing_cache[cache_key] = response

        # Track performance
        processing_time = time.time() - start_time
        self.response_times.append(processing_time)

        return response

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get AI processing performance statistics"""
        if not self.response_times:
            return {"avg_response_time": 0, "total_requests": 0, "cache_size": 0}

        return {
            "avg_response_time": sum(self.response_times) / len(self.response_times),
            "total_requests": len(self.response_times),
            "cache_size": len(self.processing_cache),
            "fastest_response": min(self.response_times),
            "slowest_response": max(self.response_times)
        }

    def get_activity_data(self) -> Dict[str, Any]:
        """Generate activity data for charts"""
        days = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
        activities = [0, 0, 0, 0, 0, 0, 3]  # Current activity pattern

        return {
            'labels': days,
            'data': activities,
            'total_activities': sum(activities)
        }

    def generate_quiz(self, topic: str, difficulty: str = "medium") -> dict:
        """Generate a quiz based on topic and difficulty"""
        quiz_questions = {
            "science": {
                "easy": [
                    {
                        "question": "What gas do plants take in during photosynthesis?",
                        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"],
                        "correct": 1,
                        "explanation": "Plants take in carbon dioxide and release oxygen during photosynthesis."
                    },
                    {
                        "question": "How many bones are in an adult human body?",
                        "options": ["206", "250", "186", "300"],
                        "correct": 0,
                        "explanation": "An adult human skeleton has 206 bones."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the powerhouse of the cell?",
                        "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"],
                        "correct": 1,
                        "explanation": "Mitochondria produce ATP, the energy currency of cells."
                    },
                    {
                        "question": "Which law states that energy cannot be created or destroyed?",
                        "options": ["Newton's First Law", "Law of Conservation of Energy", "Boyle's Law", "Charles's Law"],
                        "correct": 1,
                        "explanation": "The Law of Conservation of Energy states that energy can only be transformed from one form to another."
                    }
                ]
            },
            "math": {
                "easy": [
                    {
                        "question": "What is 15% of 200?",
                        "options": ["25", "30", "35", "40"],
                        "correct": 1,
                        "explanation": "15% of 200 = 0.15 × 200 = 30"
                    },
                    {
                        "question": "What is the area of a rectangle with length 8 and width 5?",
                        "options": ["13", "26", "40", "45"],
                        "correct": 2,
                        "explanation": "Area = length × width = 8 × 5 = 40"
                    }
                ],
                "medium": [
                    {
                        "question": "Solve for x: 2x + 5 = 15",
                        "options": ["5", "10", "7.5", "2.5"],
                        "correct": 0,
                        "explanation": "2x + 5 = 15, so 2x = 10, therefore x = 5"
                    },
                    {
                        "question": "What is the slope of the line y = 3x - 2?",
                        "options": ["3", "-2", "1", "0"],
                        "correct": 0,
                        "explanation": "In the equation y = mx + b, m is the slope. Here, m = 3."
                    }
                ]
            },
            "programming": {
                "easy": [
                    {
                        "question": "Which of these is a programming language?",
                        "options": ["HTML", "Python", "CSS", "JSON"],
                        "correct": 1,
                        "explanation": "Python is a programming language, while HTML and CSS are markup/styling languages."
                    },
                    {
                        "question": "What does 'print()' do in Python?",
                        "options": ["Calculates numbers", "Displays output", "Creates variables", "Loops code"],
                        "correct": 1,
                        "explanation": "The print() function displays output to the console."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the time complexity of binary search?",
                        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                        "correct": 1,
                        "explanation": "Binary search has O(log n) time complexity because it halves the search space each iteration."
                    },
                    {
                        "question": "Which data structure uses LIFO principle?",
                        "options": ["Queue", "Stack", "Array", "Tree"],
                        "correct": 1,
                        "explanation": "Stack uses Last In, First Out (LIFO) principle."
                    }
                ]
            }
        }

        topic_lower = topic.lower()
        if topic_lower in quiz_questions and difficulty in quiz_questions[topic_lower]:
            import random
            questions = quiz_questions[topic_lower][difficulty]
            return {
                "topic": topic,
                "difficulty": difficulty,
                "questions": random.sample(questions, min(len(questions), 3))
            }
        else:
            return {
                "topic": topic,
                "difficulty": difficulty,
                "questions": [
                    {
                        "question": f"What is an important concept in {topic}?",
                        "options": ["Concept A", "Concept B", "Concept C", "All of the above"],
                        "correct": 3,
                        "explanation": f"This is a general question about {topic}. Consider studying the fundamental concepts."
                    }
                ]
            }