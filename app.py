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

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    if request.method == 'POST':
        text = request.form.get('text', '')
        file = request.files.get('file')

        # Handle file upload
        if file and file.filename and file.filename.endswith('.txt'):
            try:
                file_content = file.read()
                if isinstance(file_content, bytes):
                    text = file_content.decode('utf-8')
                else:
                    text = file_content
            except UnicodeDecodeError:
                return jsonify({'error': 'Unable to decode file. Please ensure it is a valid UTF-8 text file.'}), 400
            except Exception as e:
                return jsonify({'error': f'Error reading file: {str(e)}'}), 400

        if text:
            try:
                length = request.form.get('length', 'medium')
                style = request.form.get('style', 'general')

                # Pass additional parameters to AI processor
                summary = ai_processor.summarize_text(text, length=length, style=style)
                return jsonify({'summary': summary})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        return jsonify({'error': 'No text provided'}), 400
    return render_template('summarizer.html')

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

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign in page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        # Simple authentication (in production, use proper password hashing)
        if email and password:
            session['user_email'] = email
            session['user_name'] = email.split('@')[0].title()
            session['is_authenticated'] = True

            if remember:
                session.permanent = True

            return redirect(url_for('dashboard'))
        else:
            return render_template('signin.html', error="Invalid email or password")

    return render_template('signin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign up page"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')

        # Simple validation
        if not all([name, email, password, confirm_password, terms]):
            return render_template('signup.html', error="All fields are required")

        if password != confirm_password:
            return render_template('signup.html', error="Passwords do not match")

        if len(password) < 8:
            return render_template('signup.html', error="Password must be at least 8 characters")

        # Create account (in production, hash password and store in database)
        session['user_email'] = email
        session['user_name'] = name
        session['is_authenticated'] = True

        return redirect(url_for('dashboard'))

    return render_template('signup.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    """User profile page"""
    if not session.get('is_authenticated'):
        return redirect(url_for('signin'))

    user_data = {
        'name': session.get('user_name', 'User'),
        'email': session.get('user_email', ''),
        'stats': {
            'summaries': session.get('summaries_count', 0),
            'flashcards': session.get('flashcards_count', 0),
            'quizzes': session.get('quizzes_count', 0),
            'questions': session.get('questions_count', 0)
        }
    }
    return render_template('profile.html', user=user_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)