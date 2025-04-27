# Asha AI Chatbot

## Project Overview

Asha AI Chatbot is an intelligent virtual assistant designed for the JobsForHer Foundation platform. It helps women explore career opportunities, job listings, professional development events, and mentorship programs through natural language conversations.

## Features

- **Smart Job Search**: Find relevant job opportunities based on skills, experience, and preferences
- **Event Discovery**: Get information about upcoming workshops, networking events, and training sessions
- **Mentorship Guidance**: Explore available mentorship programs across various industries
- **Career Resources**: Access tips and guidance for resume building, interviews, and career transitions
- **Context-Aware Conversations**: Maintain natural, multi-turn conversations that remember previous interactions
- **Bias Mitigation**: Ensure inclusive, supportive responses that avoid gender stereotypes
- **Futuristic UI**: Modern, responsive glassmorphism interface with smooth animations and mobile support
- **PWA Support**: Progressive Web App capabilities for installation on mobile devices

## Project Structure

```
asha_ai_chatbot/
│
├── data/
│   ├── job_listing_data.csv        # Sample job listings
│   ├── session_details.json        # Information about events and workshops
│   └── mentorship_programs.json    # Available mentorship opportunities
│
├── prompts/
│   ├── base_prompt.txt             # Core instructions for the AI assistant
│   └── examples.jsonl              # Example conversations for training
│
├── src/
│   ├── main.py                     # Main application controller
│   ├── rag_pipeline.py             # Retrieval-augmented generation system
│   ├── context_manager.py          # Conversation history management
│   ├── fallback_module.py          # Graceful handling of edge cases
│   ├── bias_detection.py           # Prevention of gender bias
│   └── api_integrations.py         # External data source connections
│
├── app/
│   ├── app.py                      # Flask application for serving the UI
│   ├── templates/                  # HTML templates
│   │   └── index.html              # Main chat interface
│   └── static/                     # Static assets
│       ├── css/                    # Stylesheets
│       │   └── style.css           # Main CSS with glassmorphism design
│       ├── js/                     # JavaScript files
│       │   └── script.js           # Chat functionality
│       ├── img/                    # Images and icons
│       │   ├── logo.svg            # Asha logo
│       │   └── icons/              # PWA icons
│       ├── manifest.json           # PWA manifest
│       └── service-worker.js       # PWA service worker
│
├── docs/
│   └── architecture.md             # System architecture documentation
│
├── requirements.txt                # Project dependencies
└── README.md                       # Project overview and setup instructions
```

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/asha-ai-chatbot.git
   cd asha-ai-chatbot
   ```


3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```
   cd app
   python app.py
   ```
   Then open http://localhost:5000 in your browser.

## Usage

Once the application is running, you can interact with Asha AI by:

1. Typing natural language queries about jobs, careers, events, or mentorship
2. Exploring recommended opportunities based on your conversations
3. Getting information about upcoming professional development sessions
4. Receiving guidance on career advancement strategies

Example queries:
- "What tech jobs are available?"
- "I'm looking to return to work after a career break"
- "Are there any upcoming networking events?"
- "How can I improve my resume?"
- "Tell me about mentorship programs in finance"

## UI Features

The futuristic UI includes:

- **Glassmorphism Design**: Transparent, frosted glass effect for a modern look
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Layout**: Works perfectly on mobile, tablet, and desktop
- **Animated Elements**: Smooth transitions, typing indicators, and particle backgrounds
- **PWA Support**: Install as a standalone app on supported devices
- **API Integration**: Uses the Groq API with Llama 3 for intelligent responses

## Development

### Adding New Data Sources

To expand Asha's knowledge:

1. Add new data files to the `data/` directory
2. Update the RAG pipeline in `src/rag_pipeline.py` to include the new data source
3. Modify response generation in `main.py` to handle the new information type

### Training and Fine-tuning

To improve Asha's responses:

1. Add new example conversations to `prompts/examples.jsonl`
2. Update the base prompt in `prompts/base_prompt.txt` with any new guidelines
3. Run the training pipeline (see documentation in `docs/`)

### UI Customization

To modify the UI:

1. Edit the CSS in `app/static/css/style.css` for styling changes
2. Update JavaScript functionality in `app/static/js/script.js`
3. Modify the HTML template in `app/templates/index.html`

## Contributing

Contributions to improve Asha AI Chatbot are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- JobsForHer Foundation for their mission to enable women's career advancement
- Open-source NLP and AI tools that make this assistant possible