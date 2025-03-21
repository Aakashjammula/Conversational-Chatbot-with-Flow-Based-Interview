# AI Interview Chatbot

This is an AI-powered interview chatbot named **Monika**, designed to conduct interviews for the **Frontend Developer** role. It follows a structured decision tree to navigate conversations and assess candidates based on predefined conditions.

## Features
- Loads a **tree-based conversation structure** from a JSON file.
- Uses **Gemini 2.0 Flash** from Google Generative AI for intelligent responses.
- Evaluates user input conditions to **progress through interview steps**.
- **Handles user responses dynamically** based on predefined conditions.
- Includes a **conversation history** for tracking interactions.
- The **user interface** is built using **Streamlit** for a seamless and interactive experience.
- The app is deployed using **Vercel** for easy access and scalability.

## Demo
Visit the live demo here: [Conversational Chatbot Demo](https://conversational-chatbot-with-flow-based.streamlit.app)

## Prerequisites
- Python 3.8+
- API key for **Google Generative AI** (stored in `.env`)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/Conversational-Chatbot-with-Flow-Based-Interview.git
   cd Conversational-Chatbot-with-Flow-Based-Interview
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your **Google API key**:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Add a **tree.json** file defining the interview conversation structure.

## Usage
Run the chatbot with:
```bash
streamlit run app.py
```

## Project Structure
```
project_root/
├── app.py              # Main application file
├── chatbot.py          # ChatbotBackend class
├── config.py           # Configuration and constants
├── styles.py           # CSS styles
├── ui_components.py    # UI related functions
├── tree.json           # Decision tree data (existing file)
└── .env                # Environment variables (existing file)
```

## Example Tree Structure (tree.json)
```json
[
    {
        "nodeId": "node1",
        "rootNode": true,
        "prompt": "Ask if the user is John",
        "edges": [
            {
                "condition": "user is John",
                "targetNodeId": "node2"
            },
            {
                "condition": "user is not John",
                "targetNodeId": "node8"
            }
        ]
    }
]
```

## Notes
- The chatbot **strictly follows the decision tree**.
- It **does not generate additional questions** outside the structure.
- Debugging logs are enabled to track conditions and responses.

## Outputs

## 1. User is John and Ready
![image](https://github.com/user-attachments/assets/b9bce001-0e07-4998-8ddd-c77d1a21b401)

## 2. User is John but Not Ready
![image-1](https://github.com/user-attachments/assets/bead787d-d11b-4f66-a4eb-073f59ed5ba0)

## 3. User is not John
![image-2](https://github.com/user-attachments/assets/7fb15aa5-3a94-456e-a737-f05abe895688)

## License
MIT License
