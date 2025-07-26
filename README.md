# Sutra - Smart Class Finder

A web application that helps students find the perfect college courses through AI-powered chat interactions. This system combines course search, voice interaction, and intelligent recommendations to make course discovery intuitive and personalized.

## Features

- **AI-Powered Course Search**: Get personalized course recommendations through natural language chat
- **Voice Interaction**: Ask about classes using voice input and receive audio responses
- **MongoDB Course Database**: Access comprehensive course information with vector search capabilities
- **Multi-Modal AI**: Integration with OpenAI, Friendli.ai, Google Gemini, and Tavily for enhanced responses
- **Real-time Course Lookup**: Search through course catalogs with semantic understanding
- **Interactive Chat Interface**: Natural conversation flow for course discovery
- **Voice-to-Text & Text-to-Speech**: Seamless voice interaction using OpenAI Whisper and Rime TTS

## Technology Stack

- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: 
  - OpenAI API (GPT-4) for voice transcription and text-to-speech
  - Friendli.ai for chat completions
  - Google ADK (Agent Development Kit) for course search workflows
  - Tavily for hybrid search capabilities
- **Database**: MongoDB with vector search for course data
- **Voice Services**: Rime TTS for text-to-speech conversion

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- MongoDB Atlas account (for course database)
- API keys for various services

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Sutra
   ```

2. Create a virtual environment:
   ```bash
   conda create --name sutra python=3.12
   conda activate sutra
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API keys and environment variables:
   - Create a `.env` file in the root directory
   - Add the following API keys:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     FRIENDLI_TOKEN=your_friendli_token_here
     RIME_API_KEY=your_rime_api_key_here
     COHERE_API_KEY=your_cohere_api_key_here
     TAVILY_API_KEY=your_tavily_api_key_here
     GOOGLE_API_KEY=your_google_api_key_here
     MONGO_URI=your_mongodb_connection_string
     ```

### Running the Application

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Homepage**: Learn about the course finding features
2. **Find Classes**: Use the main chat interface to search for courses
3. **Voice Interaction**: Click the microphone button to ask questions by voice
4. **Course Recommendations**: Get personalized course suggestions based on your interests
5. **Schedule Planning**: Find courses that fit your schedule and academic goals

## API Endpoints

- `/api/chat` - Main chat interface for course queries
- `/api/transcribe` - Voice-to-text conversion using OpenAI Whisper
- `/api/text-to-speech` - Text-to-speech conversion using Rime TTS
- `/api/transition` - Phase transitions in the application

## Database Setup

The application uses MongoDB Atlas with vector search capabilities:

1. **MongoDB Atlas**: Set up a cluster and get your connection string
2. **Vector Index**: The application automatically creates a vector search index for course embeddings
3. **Course Data**: Populate the database with course information including embeddings

## AI Services Integration

### OpenAI
- **Whisper API**: Speech-to-text transcription
- **GPT-4**: Advanced language processing

### Friendli.ai
- **Chat Completions**: Primary chat interface responses

### Google ADK
- **Agent Workflows**: Course search and recommendation workflows
- **Gemini Models**: Advanced reasoning for course matching

### Tavily
- **Hybrid Search**: Combines semantic and keyword search for course discovery

### Rime
- **Text-to-Speech**: High-quality voice synthesis for responses

## Customization

### Adding New Course Data

1. **MongoDB Collection**: Add courses to the MongoDB collection with proper embeddings
2. **Vector Search**: Ensure the vector index is properly configured
3. **Course Schema**: Follow the established schema for course information

### Modifying AI Responses

- **System Prompts**: Update the system prompts in `app.py` for different AI services
- **Workflow Agents**: Modify the Google ADK agents for custom course search logic
- **Voice Settings**: Adjust TTS parameters for different voice characteristics

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for Whisper and GPT-4 | Yes |
| `FRIENDLI_TOKEN` | Friendli.ai API token for chat completions | Yes |
| `RIME_API_KEY` | Rime API key for text-to-speech | Yes |
| `COHERE_API_KEY` | Cohere API key for embeddings | Yes |
| `TAVILY_API_KEY` | Tavily API key for hybrid search | Yes |
| `GOOGLE_API_KEY` | Google API key for ADK and Gemini | Yes |
| `MONGO_URI` | MongoDB Atlas connection string | Yes |

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for Whisper and GPT-4 APIs
- Friendli.ai for chat completion services
- Google for ADK and Gemini models
- Tavily for hybrid search capabilities
- Rime for text-to-speech services
- MongoDB for vector search database