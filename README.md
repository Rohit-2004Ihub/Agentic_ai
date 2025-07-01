Agentic AI-Powered Case Study Generator
Turn your academic project documents into professional case studies using a multi-agent AI system powered by LangChain and Gemini API.

Problem Statement
Students often create great academic projects but face these challenges:
Struggle to summarize projects effectively for evaluations or placements.
Lack real-world benchmarking and structure in their documentation.
Miss out on compelling visuals and pitch feedback to improve presentation.



Solution Overview
This system intelligently transforms .docx project documents into structured case studies using an Agentic AI pipeline:
Project Extractor Agent → Extracts structured summary from the document.


Case Study Composer → Generates a complete case study draft.
RAG Refiner → Improves quality using Retrieval-Augmented Generation.
Visual Aid Recommender → Suggests charts/diagrams for visual impact.
Pitch Simulator → Simulates stakeholder pitch and provides feedback.
All results are saved with history tracking for user access.


 Tech Stack
Frontend: React + Tailwind CSS + Lucide Icons
Backend: Django (REST API)
AI Engine: LangChain Agents + Gemini 1.5 API
Database: MongoDB (for storing history and RAG results)
Storage: Local upload of .docx files (can be extended to cloud)



 Features
 Upload .docx project file
 Multi-agent AI pipeline to generate outputs
 Suggests visuals and simulates pitches
 Saves versioned history of results
 User signup & login functionality

Setup Instructions
1. Clone the Repository
git clone https://github.com/your-username/case-study-generator.git
cd case-study-generator


2. Backend Setup (Django)
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

Update your .env file with:
GEMINI_API_KEY=your_key_here
MONGO_URL=mongodb://localhost:27017/

3. Frontend Setup (React)
cd frontend
npm install
npm run dev

Future Scope
Export final case study as downloadable PDF
Cloud file storage and access
AI-powered improvement suggestions based on domain

Architecture
https://drive.google.com/file/d/1yafs35wzqpwDv3O6R7MgYgt5FEWX0xen/view?usp=drive_link