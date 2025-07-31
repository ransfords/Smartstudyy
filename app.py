import os
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from ai_processor import AIProcessor

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "smartstudy-dev-key")

# Initialize AI processor
ai_processor = AIProcessor()

@app.route('/')
def index():
    """Landing page with rotating quotes"""
    quotes = ai_processor.get_educational_quotes()
    return render_template('index.html', quotes=quotes)

@app.route('/dashboard')
def dashboard():
    """Main dashboard with statistics"""
    # Get user statistics from session or default to 0
    stats = {
        'summaries': session.get('summaries_count', 0),
        'flashcards': session.get('flashcards_count', 0),
        'quizzes': session.get('quizzes_count', 0),
        'questions': session.get('questions_count', 0)
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/assistant')
def assistant():
    """AI Assistant chat interface"""
    quick_questions = ai_processor.get_quick_questions()
    chat_history = session.get('chat_history', [])
    return render_template('assistant.html', 
                         quick_questions=quick_questions,
                         chat_history=chat_history)

@app.route('/assistant/chat', methods=['POST'])
def assistant_chat():
    """Handle chat messages"""
    message = request.form.get('message', '').strip()
    if message:
        # Get AI response
        response = ai_processor.get_assistant_response(message)
        
        # Update chat history
        chat_history = session.get('chat_history', [])
        chat_history.append({'user': message, 'assistant': response})
        session['chat_history'] = chat_history[-10:]  # Keep last 10 messages
        
        # Increment questions count
        session['questions_count'] = session.get('questions_count', 0) + 1
    
    return redirect(url_for('assistant'))

@app.route('/assistant/clear')
def clear_chat():
    """Clear chat history"""
    session.pop('chat_history', None)
    return redirect(url_for('assistant'))

@app.route('/summarizer')
def summarizer():
    """Note summarizer interface"""
    return render_template('summarizer.html')

@app.route('/summarizer/process', methods=['POST'])
def process_summary():
    """Process text summarization"""
    text = request.form.get('text', '').strip()
    if text:
        summary = ai_processor.summarize_text(text)
        session['last_summary'] = summary
        session['summaries_count'] = session.get('summaries_count', 0) + 1
        
        # Save to history
        from datetime import datetime
        summary_history = session.get('summary_history', [])
        summary_history.append({
            'text': text[:100] + '...' if len(text) > 100 else text,
            'summary': summary[:200] + '...' if len(summary) > 200 else summary,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        session['summary_history'] = summary_history[-20:]  # Keep last 20
        
        return render_template('summarizer.html', text=text, summary=summary)
    return render_template('summarizer.html', error="Please enter text to summarize")

@app.route('/flashcards')
def flashcards():
    """Flashcard creator and viewer"""
    flashcard_set = session.get('current_flashcards', [])
    return render_template('flashcards.html', flashcards=flashcard_set)

@app.route('/flashcards/generate', methods=['POST'])
def generate_flashcards():
    """Generate flashcards from text"""
    text = request.form.get('text', '').strip()
    if text:
        flashcards = ai_processor.generate_flashcards(text)
        session['current_flashcards'] = flashcards
        session['flashcards_count'] = session.get('flashcards_count', 0) + len(flashcards)
        
        # Save to history
        from datetime import datetime
        flashcard_history = session.get('flashcard_history', [])
        flashcard_history.append({
            'text': text[:100] + '...' if len(text) > 100 else text,
            'count': len(flashcards),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        session['flashcard_history'] = flashcard_history[-20:]  # Keep last 20
        
        return render_template('flashcards.html', flashcards=flashcards)
    return render_template('flashcards.html', error="Please enter text to generate flashcards")

@app.route('/quiz')
def quiz():
    """Interactive quiz page"""
    return render_template('quiz.html')

@app.route('/quiz/generate', methods=['POST'])
def generate_quiz():
    """Generate a quiz"""
    topic = request.form.get('topic', 'science')
    difficulty = request.form.get('difficulty', 'medium')
    
    quiz_data = ai_processor.generate_quiz(topic, difficulty)
    session['current_quiz'] = quiz_data
    session['quiz_answers'] = {}
    
    return render_template('quiz.html', quiz=quiz_data)

@app.route('/quiz/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz answers"""
    quiz_data = session.get('current_quiz', {})
    if not quiz_data:
        return redirect(url_for('quiz'))
    
    answers = {}
    score = 0
    total = len(quiz_data.get('questions', []))
    
    for i, question in enumerate(quiz_data.get('questions', [])):
        user_answer = request.form.get(f'question_{i}')
        if user_answer is not None:
            user_answer = int(user_answer)
            answers[i] = {
                'user_answer': user_answer,
                'correct_answer': question['correct'],
                'is_correct': user_answer == question['correct'],
                'explanation': question['explanation']
            }
            if user_answer == question['correct']:
                score += 1
    
    session['quiz_results'] = {
        'score': score,
        'total': total,
        'percentage': round((score / total) * 100) if total > 0 else 0,
        'answers': answers
    }
    session['quizzes_count'] = session.get('quizzes_count', 0) + 1
    
    return render_template('quiz.html', quiz=quiz_data, results=session['quiz_results'])

@app.route('/progress')
def progress():
    """Progress tracker with charts"""
    # Generate mock activity data for the chart
    activity_data = ai_processor.get_activity_data()
    stats = {
        'summaries': session.get('summaries_count', 0),
        'flashcards': session.get('flashcards_count', 0),
        'quizzes': session.get('quizzes_count', 0),
        'questions': session.get('questions_count', 0)
    }
    return render_template('progress.html', activity_data=activity_data, stats=stats)

@app.route('/history')
def history():
    """Activity history page"""
    history_data = {
        'summaries': session.get('summary_history', []),
        'flashcards': session.get('flashcard_history', []),
        'chats': session.get('chat_history', [])
    }
    return render_template('history.html', history=history_data)

@app.route('/history/clear', methods=['POST'])
def clear_history():
    """Clear activity history"""
    activity_type = request.form.get('type', 'all')
    
    if activity_type == 'all':
        session.pop('summary_history', None)
        session.pop('flashcard_history', None)
        session.pop('chat_history', None)
    elif activity_type == 'summaries':
        session.pop('summary_history', None)
    elif activity_type == 'flashcards':
        session.pop('flashcard_history', None)
    elif activity_type == 'chats':
        session.pop('chat_history', None)
    
    return redirect(url_for('history'))

@app.route('/about')
def about():
    """Meet the developer page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
