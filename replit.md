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
- **Features**: Text summarization, educational quotes, quick questions, knowledge base
- **Implementation**: Rule-based text processing with extractive summarization
- **Rationale**: Eliminates API costs and privacy concerns while providing immediate responses

### Web Application (app.py)
- **Purpose**: Main Flask application handling routing and user interactions
- **Routes**: Landing page, dashboard, AI assistant, summarizer, flashcards
- **Session Management**: Tracks user statistics and activity history
- **Template Rendering**: Serves dynamic HTML pages with user data

### Frontend Components
- **Landing Page**: Hero section with rotating educational quotes
- **Dashboard**: Overview with activity statistics and navigation
- **AI Assistant**: Chat interface with conversation history
- **Summarizer**: Text input/output interface for note processing
- **Flashcard Creator**: Interactive card-based learning tool

## Data Flow

### User Interaction Flow
1. **Landing Page**: User views rotating quotes and accesses main features
2. **Dashboard**: Central hub showing statistics and quick access to tools
3. **AI Tools**: Users interact with summarizer, flashcards, or assistant
4. **Session Tracking**: Activities are logged and statistics are updated
5. **Local Storage**: Client preferences and history are persisted

### AI Processing Flow
1. **Input Reception**: User submits text through web forms
2. **Local Processing**: AIProcessor handles text analysis using built-in algorithms
3. **Response Generation**: Results are formatted and returned to user
4. **Activity Logging**: Actions are recorded in session for statistics

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