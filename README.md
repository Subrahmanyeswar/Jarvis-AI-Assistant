Jarvis AI Assistant 🤖

A modular, voice-enabled AI assistant that integrates computer vision, natural conversation, productivity tools, and PC automation into one unified system.

Designed as a real-time AI-powered personal assistant, Jarvis combines face/object recognition, voice interaction, and smart automation to act as your all-in-one desktop AI.

🚀 Features
🧠 Core AI

1. Voice commands (speech-to-text)

2. Natural chat powered by Groq API (Meta LLaMA 3 model)

3. Voice replies (text-to-speech)

📅 Productivity

1. To-do list manager

2. Reminders & notifications

3. Alarms & timers

4. News updates (via API)

5. Weather reports (via API)

6. World clock & time updates

👁️ Vision (Security)

1. Face recognition (authorized / unauthorized)

2. Facial expression detection

3. Object detection (YOLOv8)

4. Unauthorized alerts + voice warnings

🖥️ PC Automation

1. Open/close applications

2. Control apps with voice

3. Voice typing anywhere

4. Smart search (Google, YouTube, Amazon, Flipkart)

5. Auto form filling & navigation

6. Scroll, click, tab switching via voice

7. Shutdown / restart / sleep via voice

⚡ Extra Smart Features

1. AI Friend conversation mode

2. Battery monitoring + alerts

🏗️ System Architecture

📂 Project Structure
Jarvis-AI-Assistant/
│── main.py                  # Runs security modules (face + object detection)
│── ai_core/                 # Core assistant logic (chat, speech, processing)
│── productivity/            # To-do, reminders, alarms, news, weather
│── pc_automation/           # App + system control modules
│── system/                  # Monitoring utilities
│── models/                  # Pretrained models (YOLO, face recognition, etc.)
│── data/                    # Training/evaluation data
│── docs/                    # Documentation + architecture diagram
│── requirements.txt
│── README.md
│── .gitignore

⚙️ Installation
# Clone the repository
git clone https://github.com/Subrahmanyeswar/Jarvis-AI-Assistant.git
cd Jarvis-AI-Assistant

# Create venv (recommended)
python -m venv .venv
.\.venv\Scripts\activate   # (Windows)

# Install dependencies
pip install -r requirements.txt

▶️ Running Jarvis
Jarvis has two modules that need to run in parallel:

1️⃣ Run Security System (Face + Object Detection)
python main.py

2️⃣ Run Jarvis Core (AI Assistant, Productivity, Automation)
python -m ai_core.main_ai

🔑 API Setup
Groq API (for natural chat):
Get your API key from Groq Console
.
Add it to an .env file:

GROQ_API_KEY=your_key_here


News API (for daily news):
Sign up at NewsAPI
.
Add key to .env:

NEWS_API_KEY=your_key_here


Weather API (for weather reports):
Use OpenWeather
.
Add key to .env:

WEATHER_API_KEY=your_key_here


📈 Future Roadmap

 1. Web dashboard for real-time monitoring

 2. Mobile companion app

 3. Multi-user support (face-based personalization)

 4. Advanced emotion recognition

 5. Cloud sync for tasks & reminders

🤝 Contribution

Pull requests are welcome. For major changes, open an issue first to discuss what you’d like to change.

📬 Contact

Developed by Subrahmanyeswar
📧 Reach me at: subrahmanyeswarkolluru@gmail.comS
🌐 GitHub: @Subrahmanyeswar
