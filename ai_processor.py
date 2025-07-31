
import random
from typing import List, Dict, Any

class AIProcessor:
    def __init__(self):
        self.educational_quotes = [
            "Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
            "The beautiful thing about learning is that no one can take it away from you. - B.B. King", 
            "Education is not preparation for life; education is life itself. - John Dewey",
            "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice. - Brian Herbert",
            "Intelligence plus character - that is the goal of true education. - Martin Luther King Jr.",
            "Education is what remains after one has forgotten what one has learned in school. - Albert Einstein",
            "The mind is not a vessel to be filled, but a fire to be kindled. - Plutarch",
            "Tell me and I forget, teach me and I may remember, involve me and I learn. - Benjamin Franklin"
        ]
        
        self.quick_questions = [
            "Explain the concept of photosynthesis",
            "What is machine learning?",
            "How do I solve quadratic equations?",
            "Explain the water cycle",
            "What is the theory of relativity?",
            "How does DNA replication work?",
            "What are the fundamentals of programming?",
            "Explain Shakespeare's writing style"
        ]

    def get_educational_quotes(self) -> List[str]:
        """Return a shuffled list of educational quotes"""
        quotes = self.educational_quotes.copy()
        random.shuffle(quotes)
        return quotes

    def get_quick_questions(self) -> List[str]:
        """Return a shuffled list of quick questions"""
        questions = self.quick_questions.copy()
        random.shuffle(questions)
        return questions

    def summarize_text(self, text: str, length: str = "medium", style: str = "general") -> str:
        """
        Enhanced text summarization with different styles and lengths
        """
        if not text or not text.strip():
            return "No text provided to summarize."

        # Split text into sentences
        sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
        
        if len(sentences) <= 1:
            return text.strip()

        # Determine summary length
        if length == "short":
            target_sentences = max(1, len(sentences) // 4)
        elif length == "long":
            target_sentences = max(2, len(sentences) // 2)
        else:  # medium
            target_sentences = max(1, len(sentences) // 3)

        # Apply style-based processing
        if style == "academic":
            # Prioritize sentences with academic keywords
            academic_keywords = ['research', 'study', 'analysis', 'theory', 'methodology', 'findings', 'conclusion']
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                score = sum(1 for keyword in academic_keywords if keyword.lower() in sentence.lower())
                score += len(sentence.split()) / 20  # Prefer longer sentences
                scored_sentences.append((score, i, sentence))
            scored_sentences.sort(reverse=True)
            selected = scored_sentences[:target_sentences]
        elif style == "technical":
            # Prioritize sentences with technical terms
            technical_keywords = ['system', 'process', 'method', 'function', 'algorithm', 'data', 'implement']
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                score = sum(1 for keyword in technical_keywords if keyword.lower() in sentence.lower())
                score += sentence.count('(') + sentence.count('[')  # Technical texts often have parentheses
                scored_sentences.append((score, i, sentence))
            scored_sentences.sort(reverse=True)
            selected = scored_sentences[:target_sentences]
        else:  # general
            # Use simple extractive summarization
            # Select sentences that are representative of the text
            word_freq = {}
            words = text.lower().split()
            for word in words:
                if len(word) > 3 and word.isalpha():
                    word_freq[word] = word_freq.get(word, 0) + 1

            # Score sentences based on word frequency
            sentence_scores = []
            for i, sentence in enumerate(sentences):
                score = 0
                words_in_sentence = sentence.lower().split()
                for word in words_in_sentence:
                    if word in word_freq:
                        score += word_freq[word]
                if len(words_in_sentence) > 0:
                    score = score / len(words_in_sentence)
                sentence_scores.append((score, i, sentence))

            # Select top sentences maintaining order
            sentence_scores.sort(reverse=True)
            selected = sentence_scores[:target_sentences]

        # Sort selected sentences by original order
        selected.sort(key=lambda x: x[1])
        
        # Join sentences and clean up
        summary = '. '.join([sentence[2] for sentence in selected])
        if not summary.endswith('.'):
            summary += '.'
            
        return summary

    def get_assistant_response(self, question: str) -> str:
        """
        Enhanced AI assistant with domain-specific responses
        """
        question_lower = question.lower()
        
        # Science responses
        if any(word in question_lower for word in ['photosynthesis', 'plant', 'chlorophyll']):
            return "Photosynthesis is the process by which plants convert light energy into chemical energy. Plants use chlorophyll to capture sunlight, combine carbon dioxide from the air with water from the roots, and produce glucose and oxygen. The equation is: 6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂. This process is essential for life on Earth as it produces oxygen and forms the base of food chains."
        
        elif any(word in question_lower for word in ['machine learning', 'ai', 'artificial intelligence']):
            return "Machine Learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. It works by identifying patterns in data and using these patterns to make predictions. Common types include supervised learning (learning from labeled examples), unsupervised learning (finding hidden patterns), and reinforcement learning (learning through trial and error)."
        
        elif any(word in question_lower for word in ['quadratic', 'equation', 'algebra']):
            return "A quadratic equation has the form ax² + bx + c = 0. To solve it, you can use: 1) Factoring (if possible), 2) Completing the square, or 3) The quadratic formula: x = [-b ± √(b² - 4ac)] / 2a. The discriminant (b² - 4ac) tells you about the solutions: positive = two real solutions, zero = one solution, negative = no real solutions."
        
        elif any(word in question_lower for word in ['water cycle', 'evaporation', 'precipitation']):
            return "The water cycle is Earth's continuous process of water movement. It includes: 1) Evaporation - water from oceans/lakes becomes vapor, 2) Condensation - vapor cools and forms clouds, 3) Precipitation - water falls as rain/snow, 4) Collection - water gathers in bodies of water, 5) Transpiration - plants release water vapor. This cycle is powered by solar energy and gravity."
        
        elif any(word in question_lower for word in ['relativity', 'einstein', 'space', 'time']):
            return "Einstein's Theory of Relativity consists of two parts: Special Relativity (1905) shows that space and time are linked as spacetime, and nothing travels faster than light. General Relativity (1915) describes gravity as the curvature of spacetime caused by mass and energy. Key insights include time dilation, length contraction, and the famous equation E=mc²."
        
        elif any(word in question_lower for word in ['dna', 'replication', 'genetics']):
            return "DNA replication is the process of copying DNA before cell division. Steps: 1) Helicase unwinds the double helix, 2) DNA polymerase adds complementary nucleotides (A with T, G with C), 3) The leading strand is synthesized continuously, while the lagging strand is made in fragments (Okazaki fragments), 4) Ligase joins the fragments. This ensures each new cell has identical genetic information."
        
        elif any(word in question_lower for word in ['programming', 'coding', 'algorithm']):
            return "Programming fundamentals include: 1) Variables (storing data), 2) Data types (numbers, text, booleans), 3) Control structures (if/else, loops), 4) Functions (reusable code blocks), 5) Arrays/Lists (storing multiple values), 6) Object-oriented concepts (classes, objects), 7) Problem-solving approach (breaking problems into smaller parts), 8) Debugging (finding and fixing errors)."
        
        elif any(word in question_lower for word in ['shakespeare', 'literature', 'writing']):
            return "Shakespeare's writing style features: 1) Iambic pentameter (rhythmic pattern), 2) Rich metaphors and imagery, 3) Wordplay and puns, 4) Soliloquies revealing inner thoughts, 5) Complex characters with psychological depth, 6) Themes of love, power, betrayal, and human nature, 7) Invented many words still used today, 8) Blank verse and rhyming couplets for different effects."
        
        # Math responses
        elif any(word in question_lower for word in ['calculus', 'derivative', 'integral']):
            return "Calculus studies continuous change through derivatives and integrals. Derivatives measure rates of change (slope of a curve), while integrals measure accumulation (area under a curve). Key concepts include limits, the fundamental theorem of calculus (connecting derivatives and integrals), and applications in physics, engineering, and economics."
        
        elif any(word in question_lower for word in ['geometry', 'triangle', 'circle']):
            return "Geometry studies shapes, sizes, and spatial relationships. Key concepts include: points, lines, angles, polygons, circles, and three-dimensional shapes. Important theorems include Pythagorean theorem (a² + b² = c²), properties of similar triangles, circle theorems, and formulas for area and volume."
        
        # General responses for common question patterns
        elif question_lower.startswith(('what is', 'what are')):
            return f"That's a great question about {question[8:]}! This is a complex topic that involves multiple concepts. I'd recommend breaking it down into smaller parts and exploring each component. Would you like me to help you understand a specific aspect of this topic?"
        
        elif question_lower.startswith(('how do', 'how does')):
            return f"Understanding how {question[7:]} works requires looking at the underlying processes and mechanisms. Let me help you break this down step by step. What specific aspect would you like to focus on first?"
        
        elif question_lower.startswith('explain'):
            return f"I'd be happy to explain {question[8:]}! This concept can be understood better when we look at its key components, real-world applications, and how it connects to other ideas. What level of detail would be most helpful for your current studies?"
        
        else:
            return "That's an interesting question! I'm here to help you understand various topics in science, mathematics, programming, and more. Could you provide more specific details about what you'd like to learn? For example, are you looking for a definition, an explanation of a process, or help with a specific problem?"

    def generate_flashcards(self, text: str) -> List[Dict[str, str]]:
        """
        Enhanced flashcard generation with better content extraction
        """
        if not text or not text.strip():
            return []

        # Split text into sentences and clean
        sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip() and len(s.strip()) > 20]
        
        if len(sentences) < 2:
            return [{
                "front": "Key Concept",
                "back": text.strip()
            }]

        flashcards = []
        
        # Generate different types of flashcards
        for i, sentence in enumerate(sentences[:8]):  # Limit to 8 cards
            words = sentence.split()
            
            if len(words) < 5:
                continue
                
            # Type 1: Definition cards (look for "is", "are", "means")
            if any(word in sentence.lower() for word in [' is ', ' are ', ' means ', ' refers to ']):
                parts = sentence.split(' is ', 1) or sentence.split(' are ', 1) or sentence.split(' means ', 1)
                if len(parts) == 2:
                    flashcards.append({
                        "front": f"What is {parts[0].strip()}?",
                        "back": parts[1].strip()
                    })
                    continue
            
            # Type 2: Process cards (look for process words)
            if any(word in sentence.lower() for word in ['process', 'steps', 'method', 'procedure']):
                flashcards.append({
                    "front": f"Describe the process mentioned in: {sentence[:50]}...",
                    "back": sentence
                })
                continue
            
            # Type 3: Fill-in-the-blank cards
            if len(words) > 10:
                # Remove a key word (usually a noun or important term)
                important_words = [w for w in words if len(w) > 6 and w.isalpha()]
                if important_words:
                    key_word = important_words[0]
                    question = sentence.replace(key_word, "______", 1)
                    flashcards.append({
                        "front": f"Fill in the blank: {question}",
                        "back": key_word
                    })
                    continue
            
            # Type 4: General comprehension cards
            flashcards.append({
                "front": f"Explain the concept described in this statement:",
                "back": sentence
            })

        # If no flashcards generated, create basic ones
        if not flashcards:
            words = text.split()
            mid_point = len(words) // 2
            flashcards.append({
                "front": "Key Information (Part 1)",
                "back": " ".join(words[:mid_point])
            })
            if mid_point < len(words):
                flashcards.append({
                    "front": "Key Information (Part 2)", 
                    "back": " ".join(words[mid_point:])
                })

        return flashcards[:6]  # Return max 6 cards

    def get_activity_data(self) -> List[Dict[str, Any]]:
        """Generate mock activity data for progress tracking"""
        import random
        from datetime import datetime, timedelta

        activities = []
        activity_types = ['summary', 'flashcard', 'quiz', 'chat']
        
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            activity_count = random.randint(0, 8)
            activities.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': activity_count,
                'type': random.choice(activity_types)
            })
        
        return list(reversed(activities))

    def generate_quiz(self, topic: str, difficulty: str = "medium") -> dict:
        """Generate a comprehensive quiz based on topic and difficulty"""
        quiz_questions = {
            "science": {
                "easy": [
                    {
                        "question": "What gas do plants take in during photosynthesis?",
                        "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"],
                        "correct": 1,
                        "explanation": "Plants take in carbon dioxide from the air and release oxygen during photosynthesis. This process converts light energy into chemical energy."
                    },
                    {
                        "question": "How many bones are in an adult human body?",
                        "options": ["206", "250", "186", "300"],
                        "correct": 0,
                        "explanation": "An adult human skeleton has 206 bones. Babies are born with about 270 bones, but many fuse together as they grow."
                    },
                    {
                        "question": "What is the center of an atom called?",
                        "options": ["Electron", "Proton", "Nucleus", "Neutron"],
                        "correct": 2,
                        "explanation": "The nucleus is the dense center of an atom containing protons and neutrons, while electrons orbit around it."
                    },
                    {
                        "question": "Which planet is closest to the Sun?",
                        "options": ["Venus", "Mercury", "Earth", "Mars"],
                        "correct": 1,
                        "explanation": "Mercury is the closest planet to the Sun, with an average distance of about 36 million miles."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the powerhouse of the cell?",
                        "options": ["Nucleus", "Mitochondria", "Ribosome", "Endoplasmic Reticulum"],
                        "correct": 1,
                        "explanation": "Mitochondria produce ATP (adenosine triphosphate), the energy currency of cells, through cellular respiration."
                    },
                    {
                        "question": "Which law states that energy cannot be created or destroyed?",
                        "options": ["Newton's First Law", "Law of Conservation of Energy", "Law of Gravity", "Ohm's Law"],
                        "correct": 1,
                        "explanation": "The Law of Conservation of Energy states that energy can only be transformed from one form to another, never created or destroyed."
                    },
                    {
                        "question": "What is the chemical formula for water?",
                        "options": ["CO2", "H2O", "NaCl", "CH4"],
                        "correct": 1,
                        "explanation": "Water has the chemical formula H2O, meaning each molecule contains two hydrogen atoms and one oxygen atom."
                    },
                    {
                        "question": "What type of bond holds the two strands of DNA together?",
                        "options": ["Ionic bonds", "Covalent bonds", "Hydrogen bonds", "Van der Waals forces"],
                        "correct": 2,
                        "explanation": "Hydrogen bonds hold the complementary base pairs together in the DNA double helix structure."
                    }
                ]
            },
            "math": {
                "easy": [
                    {
                        "question": "What is 15% of 200?",
                        "options": ["30", "25", "35", "20"],
                        "correct": 0,
                        "explanation": "To find 15% of 200: 0.15 × 200 = 30"
                    },
                    {
                        "question": "If a triangle has angles of 60° and 70°, what is the third angle?",
                        "options": ["50°", "60°", "45°", "40°"],
                        "correct": 0,
                        "explanation": "The sum of angles in a triangle is always 180°. So 180° - 60° - 70° = 50°"
                    },
                    {
                        "question": "What is the area of a rectangle with length 8 and width 5?",
                        "options": ["40", "26", "13", "35"],
                        "correct": 0,
                        "explanation": "Area of rectangle = length × width = 8 × 5 = 40 square units"
                    }
                ],
                "medium": [
                    {
                        "question": "What is the derivative of x²?",
                        "options": ["x", "2x", "x²", "2"],
                        "correct": 1,
                        "explanation": "Using the power rule: d/dx(x²) = 2x¹ = 2x"
                    },
                    {
                        "question": "Solve for x: 2x + 5 = 13",
                        "options": ["4", "3", "6", "9"],
                        "correct": 0,
                        "explanation": "2x + 5 = 13 → 2x = 8 → x = 4"
                    },
                    {
                        "question": "What is the circumference of a circle with radius 3?",
                        "options": ["6π", "9π", "3π", "12π"],
                        "correct": 0,
                        "explanation": "Circumference = 2πr = 2π(3) = 6π"
                    }
                ]
            },
            "programming": {
                "easy": [
                    {
                        "question": "Which symbol is used for comments in Python?",
                        "options": ["//", "#", "/*", "<!--"],
                        "correct": 1,
                        "explanation": "In Python, the # symbol is used for single-line comments."
                    },
                    {
                        "question": "What does HTML stand for?",
                        "options": ["High Tech Modern Language", "HyperText Markup Language", "Home Tool Markup Language", "Hyperlink and Text Markup Language"],
                        "correct": 1,
                        "explanation": "HTML stands for HyperText Markup Language, used for creating web pages."
                    },
                    {
                        "question": "Which data type would you use to store a whole number in most programming languages?",
                        "options": ["float", "string", "integer", "boolean"],
                        "correct": 2,
                        "explanation": "Integer data type is used to store whole numbers without decimal points."
                    }
                ],
                "medium": [
                    {
                        "question": "What is the time complexity of binary search?",
                        "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                        "correct": 1,
                        "explanation": "Binary search has O(log n) time complexity because it eliminates half the search space in each iteration."
                    },
                    {
                        "question": "In object-oriented programming, what is encapsulation?",
                        "options": ["Inheriting properties", "Hiding internal details", "Creating multiple objects", "Overriding methods"],
                        "correct": 1,
                        "explanation": "Encapsulation is the principle of hiding internal implementation details and exposing only necessary interfaces."
                    },
                    {
                        "question": "What does SQL stand for?",
                        "options": ["Simple Query Language", "Structured Query Language", "Standard Query Language", "Sequential Query Language"],
                        "correct": 1,
                        "explanation": "SQL stands for Structured Query Language, used for managing relational databases."
                    }
                ]
            }
        }

        topic_lower = topic.lower()
        if topic_lower in quiz_questions and difficulty in quiz_questions[topic_lower]:
            questions = quiz_questions[topic_lower][difficulty]
            selected_questions = random.sample(questions, min(len(questions), 5))
            return {
                "topic": topic,
                "difficulty": difficulty,
                "questions": selected_questions
            }
        else:
            # Fallback quiz
            return {
                "topic": topic,
                "difficulty": difficulty,
                "questions": [
                    {
                        "question": f"What is an important concept in {topic}?",
                        "options": ["Concept A", "Concept B", "Concept C", "All of the above"],
                        "correct": 3,
                        "explanation": f"This is a general question about {topic}. Consider studying the fundamental concepts and principles."
                    },
                    {
                        "question": f"Which approach is most effective for learning {topic}?",
                        "options": ["Memorization only", "Practice and understanding", "Reading alone", "Watching videos only"],
                        "correct": 1,
                        "explanation": "The most effective learning combines practice, understanding concepts, and applying knowledge."
                    }
                ]
            }
