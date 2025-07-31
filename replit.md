# replit.md

## Overview

SmartStudy is a modern AI-powered educational web application built with Flask that helps students enhance their learning through intelligent study tools. The app provides local AI processing capabilities without requiring external API keys, making it self-contained and privacy-focused.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: HTML5 with Tailwind CSS for responsive, modern UI design
- **JavaScript**: Vanilla JavaScript for client-side interactivity
- **Design Pattern**: Component-based templates using Jinja2 templating
- **Styling**: Gradient-based dark theme with purple/blue accent colors
- **Icons**: Font Awesome for consistent iconography

### Backend Architecture
- **Framework**: Flask (Python) with session-based state management
- **AI Processing**: Local AIProcessor class for text processing without external APIs
- **Routing**: RESTful routes with template rendering and JSON API endpoints
- **Session Management**: Flask sessions for user state and activity tracking

### Data Storage Strategy
- **Session Storage**: Flask sessions for temporary user data and activity tracking
- **Local Storage**: Browser localStorage for client-side preferences and history
- **File System**: Static file serving for CSS/JS assets
- **No Database**: Currently uses in-memory data structures and session storage

## Key Components

### AI Processing Engine (ai_processor.py)
- **Purpose**: Provides local AI functionality without external API dependencies
- **Features**: Text summarization, educational quotes, quick questions, comprehensive knowledge base, quiz generation
- **Implementation**: Rule-based text processing with extractive summarization and interactive quiz system
- **Quiz System**: Multi-subject quizzes (Science, Math, Programming) with difficulty levels and detailed explanations
- **Knowledge Base**: Expanded coverage including algebra, geometry, calculus, chemistry, biology, programming concepts, and literature
- **Rationale**: Eliminates API costs and privacy concerns while providing immediate responses and assessments

### Web Application (app.py)
- **Purpose**: Main Flask application handling routing and user interactions
- **Routes**: Landing page, dashboard, AI assistant, summarizer, flashcards, interactive quiz, activity history
- **Session Management**: Tracks user statistics, activity history with timestamps, and quiz results
- **History Tracking**: Comprehensive logging of summaries, flashcards, and chat conversations
- **Quiz Management**: Handles quiz generation, submission, scoring, and detailed feedback
- **Template Rendering**: Serves dynamic HTML pages with user data and interactive features

### Frontend Components
- **Landing Page**: Hero section with rotating educational quotes and comprehensive navigation
- **Dashboard**: Overview with activity statistics and feature cards for all tools
- **AI Assistant**: Chat interface with conversation history and quick questions
- **Summarizer**: Text input/output interface for note processing with history tracking
- **Flashcard Creator**: Interactive card-based learning tool with history tracking
- **Interactive Quiz**: Multi-subject quiz system with scoring and explanations
- **Activity History**: Comprehensive tracking of all user activities with timestamps

## Data Flow

### User Interaction Flow
1. **Landing Page**: User views rotating quotes and accesses main features
2. **Dashboard**: Central hub showing statistics and quick access to tools
3. **AI Tools**: Users interact with summarizer, flashcards, quiz, or assistant
4. **Session Tracking**: Activities are logged with timestamps and statistics are updated
5. **History Management**: Detailed activity history with filtering and clearing options
6. **Quiz System**: Interactive assessments with immediate feedback and explanations

### AI Processing Flow
1. **Input Reception**: User submits text through web forms or quiz selections
2. **Local Processing**: AIProcessor handles text analysis, quiz generation using built-in algorithms
3. **Response Generation**: Results are formatted and returned with explanations
4. **Activity Logging**: Actions are recorded in session with timestamps for comprehensive history
5. **Knowledge Base**: Comprehensive coverage of Science, Math, Programming, and English topics

## External Dependencies

### Frontend Dependencies
- **Tailwind CSS**: CDN-hosted utility-first CSS framework
- **Font Awesome**: Icon library for UI elements
- **Chart.js**: Data visualization for progress tracking

### Backend Dependencies
- **Flask**: Core web framework
- **Python Standard Library**: Built-in modules for text processing and utilities

### No External APIs
- **Design Choice**: All AI functionality is handled locally
- **Benefits**: No API keys required, better privacy, no usage costs
- **Trade-offs**: Limited AI capabilities compared to cloud-based solutions

## Deployment Strategy

### Development Environment
- **Server**: Flask development server with debug mode
- **Host**: Runs on 0.0.0.0:5000 for local access
- **Static Files**: Served directly by Flask

### Production Considerations
- **WSGI Server**: Should be deployed with Gunicorn or similar
- **Environment Variables**: SESSION_SECRET for production security
- **Static Files**: Consider CDN or separate static file server
- **Database Migration**: Future versions may need persistent storage

### Replit Deployment
- **Entry Point**: main.py runs the Flask application
- **Port Configuration**: Uses port 5000 with host binding for Replit
- **Static Assets**: All frontend assets are served from static/ directory
- **Template System**: Jinja2 templates in templates/ directory

## Technical Decisions

### Local AI Processing
- **Problem**: Need AI functionality without external API dependencies
- **Solution**: Custom AIProcessor class with rule-based text processing
- **Benefits**: No API costs, better privacy, instant responses
- **Limitations**: Less sophisticated than cloud AI services

### Session-Based Storage
- **Problem**: Need user state persistence without database complexity
- **Solution**: Flask sessions and browser localStorage
- **Benefits**: Simple implementation, no database setup required
- **Trade-offs**: Data is temporary and not shared across devices

### Component-Based Templates
- **Problem**: Need consistent UI across multiple pages
- **Solution**: Jinja2 template inheritance with base.html
- **Benefits**: DRY principle, consistent navigation, easy maintenance
- **Implementation**: Shared sidebar navigation and common styling

### Tailwind CSS Integration
- **Problem**: Need modern, responsive UI without custom CSS complexity
- **Solution**: CDN-hosted Tailwind CSS with custom CSS overrides
- **Benefits**: Rapid development, consistent design system, responsive by default
- **Customization**: Additional CSS in static/style.css for specific needs