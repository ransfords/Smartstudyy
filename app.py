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
        return render_template('flashcards.html', flashcards=flashcards)
    return render_template('flashcards.html', error="Please enter text to generate flashcards")

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

@app.route('/about')
def about():
    """Meet the developer page"""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
