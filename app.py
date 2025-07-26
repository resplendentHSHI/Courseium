from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
import json
import requests  # For Rhyme API calls
from openai import OpenAI  # Friendli AI client import
from datetime import datetime
from dotenv import load_dotenv
import tempfile
from llama_index.llms.openai import OpenAI as LlamaOpenAI
import markdown
# We avoid a direct LlamaIndex Evaluator base to eliminate import issues on some versions.

import os
os.environ["COHERE_API_KEY"] = "g67wQFvUOFrNsx5XjnoaE4tQAXe5Xb7cYfcu0UH4"
from tavily import TavilyClient
import json
import pandas as pd
tavily_client = TavilyClient(api_key="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")

import pymongo


def get_mongo_client(mongo_uri):
    """Establish and validate connection to the MongoDB."""

    client = pymongo.MongoClient(mongo_uri, appname="devrel.showcase.tavily_mongodb")

    # Validate the connection
    ping_result = client.admin.command("ping")
    if ping_result.get("ok") == 1.0:
        # Connection successful
        print("Connection to MongoDB successful")
        return client
    print("Connection to MongoDB failed")
    return None

MONGO_URI = "mongodb+srv://admin:admin123@college-rag.0e6k9ug.mongodb.net/?retryWrites=true&w=majority&appName=college-rag"

mongo_client = get_mongo_client(MONGO_URI)

DB_NAME = "ucla"
COLLECTION_NAME = "chris"

# Create or get the database
db = mongo_client[DB_NAME]

# Create or get the collections
collection = db[COLLECTION_NAME]

from pymongo.operations import SearchIndexModel
import time

index_name = "vector_index"
index_definition = {
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 1024,
                "similarity": "cosine",
            }
        ]
    }

new_vector_search_index_model = SearchIndexModel(
    definition=index_definition, name=index_name, type="vectorSearch"
)


from tavily import TavilyHybridClient

hybrid_rag = TavilyHybridClient(
    api_key="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", 
    db_provider="mongodb",
    collection=collection,
    index=index_name,
    embeddings_field="embedding",
    content_field="raw_content",
)


# --- Import all necessary libraries for our entire adventure ---
import os
import re
import asyncio
from IPython.display import display, Markdown
import google.generativeai as genai
from google.adk.agents import Agent, SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools import google_search, ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part
from getpass import getpass

print("✅ All libraries are ready to go!")


# --- Securely Configure Your API Key ---

# Prompt the user for their API key securely
#api_key = getpass('Enter your Google API Key: ')
# --- Securely Configure Your API Key ---

# Hardcode the API key directly
api_key = "AIzaSyD-k0nRSwJGYHAK7VlJsvIiF-7u2wfgvsM"

# Get Your API Key HERE 👉 https://codelabs.developers.google.com/onramp/instructions#0
# Configure the generative AI library with the provided key
genai.configure(api_key=api_key)

# Set the API key as an environment variable for ADK to use
os.environ['GOOGLE_API_KEY'] = api_key

print("✅ API Key configured successfully! Let the fun begin.")


# --- A Helper Function to Run Our Agents ---
# We'll use this function throughout the notebook to make running queries easy.

async def run_agent_query(agent: Agent, query: str, session: Session, user_id: str, is_router: bool = False):
    """Initializes a runner and executes a query for a given agent and session."""
    print(f"\n🚀 Running query for agent: '{agent.name}' in session: '{session.id}'...")

    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name=agent.name
    )

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user")
        ):
            if not is_router:
                # Let's see what the agent is thinking!
                print(f"EVENT: {event}")
            if event.is_final_response():
                final_response = event.content.parts[0].text
    except Exception as e:
        final_response = f"An error occurred: {e}"

    if not is_router:
     print("\n" + "-"*50)
     print("✅ Final Response:")
     display(Markdown(final_response))
     print("-"*50 + "\n")

    return final_response

# --- Initialize our Session Service ---
# This one service will manage all the different sessions in our notebook.
session_service = InMemorySessionService()
my_user_id = "adk_adventurer_001"


# -----------------------------------------------------------------------------
# 🆕  Mongo‑powered Course Lookup + RAG Agents for **agent_test**
# -----------------------------------------------------------------------------
# 1)  A reusable ADK *function tool* `search_courses_mongo` that performs a
#     full‑text query on a MongoDB collection called **courses** and writes the
#     raw results into the shared `state` under the key `course_results`.
# 2)  A **Parallel → Synthesis** workflow that first fetches the data and then
#     summarises it for the user.
# 3)  A single‑agent RAG pattern that always runs the Mongo tool before
#     answering – this copies the "human‑approval" scaffold but replaces the
#     human step with retrieval.
# -----------------------------------------------------------------------------
# Prerequisites (once per runtime):
#   !pip install pymongo motor
#   export MONGO_URI="mongodb+srv://<user>:<pass>@cluster.mongodb.net/?retryWrites=true&w=majority"
# -----------------------------------------------------------------------------

import os
import asyncio
import pymongo
from typing import List

from google.adk.tools import ToolContext
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

# -----------------------------------------------------------------------------
# 1️⃣  Mongo search tool (a plain async function is enough for ADK)            
# -----------------------------------------------------------------------------

async def search_courses_mongo(question: str, tool_context: ToolContext):
    results = hybrid_rag.search("Which professor is best for Math 32A?", max_local=5, max_foreign=1)
    return {"courses": results}

# -----------------------------------------------------------------------------
# 2️⃣  Parallel + Synthesis workflow                                           
# -----------------------------------------------------------------------------

course_search_agent = Agent(
    name="course_search_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a DB specialist. You MUST call the `search_courses_mongo` "
        "tool to fetch matching courses, then finish without extra chatter."
    ),
    tools=[search_courses_mongo],
    output_key="course_results",
)

course_synthesis_agent = Agent(
    name="course_synthesis_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are an academic adviser summarising course options. Using the "
        "JSON list in {course_results}, produce a concise bullet list with "
        "title, key topics, and why each might interest the student."
    ),
)

parallel_course_research_agent = ParallelAgent(
    name="parallel_course_research_agent",
    sub_agents=[course_search_agent],
)

course_lookup_workflow = SequentialAgent(
    name="course_lookup_workflow",
    sub_agents=[parallel_course_research_agent, course_synthesis_agent],
    description="Look up relevant courses in MongoDB and summarise them.",
)

# -----------------------------------------------------------------------------
# 3️⃣  Single‑agent RAG pattern (always retrieves first)                       
# -----------------------------------------------------------------------------

rag_course_agent = Agent(
    name="rag_course_agent",
    model="gemini-2.5-flash",
    tools=[search_courses_mongo],
    instruction=(
        "You are a Retrieval‑Augmented course assistant. For **every** user "
        "query you MUST:\n  1. Call `search_courses_mongo` with the full "
        "query.\n  2. Read state['course_results'].\n  3. Craft a "
        "helpful answer citing specific course attributes (title, level, "
        "prerequisites, etc.)."
    ),
)

# -----------------------------------------------------------------------------
# Example usage (inside an async context):
# -----------------------------------------------------------------------------
# session = await session_service.create_session(app_name=course_lookup_workflow.name, user_id=my_user_id)
# await run_agent_query(course_lookup_workflow, "I need an intro AI course with a project", session, my_user_id)
#
# rag_session = await session_service.create_session(app_name=rag_course_agent.name, user_id=my_user_id)
# await run_agent_query(rag_course_agent, "Any advanced genomics courses next quarter?", rag_session, my_user_id)
# -----------------------------------------------------------------------------

# --- Let's Test the Parallel Workflow! ---

# 1️⃣ – make the workflow return the string
async def run_mongo_workflow(query: str) -> str:
    print(f"\n{'='*60}\n🗣️  Processing Query: '{query}'\n{'='*60}")
    session = await session_service.create_session(
        app_name=rag_course_agent.name, user_id=my_user_id
    )
    # Capture the response text
    response_text = await run_agent_query(
        rag_course_agent, query, session, my_user_id
    )
    print(f"\n--- ✅ '{rag_course_agent.name}' Workflow Complete ---")
    return response_text      # ← return it!

# 2️⃣ – test helper now receives that string
async def test_query():
    return await run_mongo_workflow(
        "this is just a test run to make sure this function is working"
    )

# 3️⃣ – back at top level
final_result = asyncio.run(test_query())
print(final_result)           # ← plain old print



class RubricGrader:
    """Custom LlamaIndex evaluator implementing rubric grading."""
    def evaluate(self, query: str, response: str):  # type: ignore[override]
        prompt = grading_prompt_template.format(
            clinical_accuracy=rubric["Clinical Accuracy"],
            reasoning_quality=rubric["Reasoning Quality"],
            empathy=rubric["Empathy / Communication"],
            student_response=response,
        )
        completion = llm_grader.complete(prompt)
        raw = completion.text if hasattr(completion, "text") else str(completion)
        try:
            import json as _json
            result_dict = _json.loads(raw)
        except Exception:
            # Fallback: attempt eval if JSON fails
            result_dict = eval(raw)  # noqa: S307  (controlled LLM output)
        return result_dict

grader = RubricGrader()
# ---------------------------------------------------------------

# OpenAI configuration - load API key from environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# ------------------- Application & LLM setup (restored) -------------------
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Rime API Configuration - Loaded from environment variables (TTS only)
RIME_API_KEY = os.getenv("RIME_API_KEY")
RIME_TTS_ENDPOINT = os.getenv("RIME_TTS_ENDPOINT", "https://api.rime.ai/v1/tts")

# Friendli.ai client for simulation chat
friendli_client = OpenAI(api_key=os.getenv("FRIENDLI_TOKEN"), base_url="https://api.friendli.ai/serverless/v1")

# OpenAI client for voice transcription
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Rubric + grading model setup
rubric = {
    "Clinical Accuracy": "Does the student provide correct facts and interpretations?",
    "Reasoning Quality": "Is there clear and logical medical reasoning?",
    "Empathy / Communication": "Does the response show patient-centered communication?"
}

grading_prompt_template = (
    """
You are a clinical evaluator. Grade the student's response based on the following rubric:

Rubric:
- Clinical Accuracy: {clinical_accuracy}
- Reasoning Quality: {reasoning_quality}
- Empathy: {empathy}

Student Response:
{student_response}

Output JSON format:
{{
  \"Clinical Accuracy (1-5)\": <score>,
  \"Reasoning Quality (1-5)\": <score>,
  \"Empathy (1-5)\": <score>,
  \"Feedback\": \"<explanation>\"
}}
"""
)

llm_grader = LlamaOpenAI(model="gpt-4", temperature=0)
# -------------------------------------------------------------------------

# Register data directory for serving static files
@app.route('/static/data/<path:filename>')
def serve_data(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)

# Load patient cases from JSON
def load_patient_cases():
    with open('data/patient_cases.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cases')
def cases():
    # Initialize session for class finding
    session['start_time'] = datetime.now().isoformat()
    session['interactions'] = []
    return render_template('cases.html')

# Removed complex simulation route - now using simple chat interface

@app.route('/api/chat', methods=['POST'])
#Text Completion
# Flask ≥ 2.2 lets view functions be async                        👇  route decorator as usual
async def chat():
    data          =  request.get_json()        # use await in async view
    user_message  = data.get("message", "")

    # ─── Log the user’s message ──────────────────────────────────────────────
    session.setdefault("interactions", []).append(
        {"role": "user", "content": user_message,
         "timestamp": datetime.now().isoformat()}
    )

    # ─── 1️⃣  Try Mongo / RAG first ──────────────────────────────────────────
    try:
        mongo_answer: str = await run_mongo_workflow(user_message)
        # If your RAG agent can legitimately return "", treat that as “no hit”
        if mongo_answer.strip():
            response_text = mongo_answer
        else:
            raise ValueError("No Mongo result")

    # ─── 2️⃣  Fall back to the Friendli LLM ──────────────────────────────────
    except Exception as mongo_err:
        system_prompt = (
            "You are a helpful college class‑finding assistant. "
            "Help students find courses that match their interests, schedule, "
            "and academic goals. Provide practical, specific recommendations. "
            "Ask clarifying questions when needed. Be friendly and concise."
        )

        # Friendli / OpenAI client is *blocking* → off‑load to a thread
        loop = asyncio.get_running_loop()
        try:
            response_text = await loop.run_in_executor(
                None,                                        # default ThreadPool
                lambda: (
                    friendli_client.chat.completions.create(
                        model="meta-llama-3.1-8b-instruct",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user",   "content": user_message},
                        ],
                    ).choices[0].message.content
                ),
            )
        except Exception as llm_err:
            # Absolute worst‑case fallback
            response_text = (
                "I'm here to help you find the perfect classes! "
                "Could you tell me a bit more about what you’re looking for?"
            )

    # ─── Track assistant reply ───────────────────────────────────────────────
    session["interactions"].append(
        {"role": "assistant", "content": response_text,
         "timestamp": datetime.now().isoformat()}
    )

    return jsonify({"response": response_text})


@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Endpoint to transcribe speech to text using OpenAI Whisper API
    """
    try:
        # Check if audio file was provided
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        
        # Save the audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name
        
        try:
            # Use OpenAI's Whisper API for transcription (STT)
            with open(temp_audio_path, 'rb') as audio:
                transcript = openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio
                )
            
            # Clean up temporary file
            os.unlink(temp_audio_path)
            
            return jsonify({"text": transcript.text})
            
        except Exception as e:
            # Clean up temporary file in case of error
            if os.path.exists(temp_audio_path):
                os.unlink(temp_audio_path)
            
            print(f"OpenAI Whisper API error: {str(e)}")
            return jsonify({"error": "Failed to transcribe audio", "details": str(e)}), 500
    
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route('/api/text-to-speech', methods=['POST'])
def text_to_speech():
    """
    Endpoint to convert text to speech using Rime TTS API
    """
    try:
        data = request.json
        text = data.get('text')
        voice = data.get('voice', 'default')  # Default voice for Rime
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Call Rime TTS API using correct endpoint and format from docs
        if RIME_API_KEY:
            headers = {
                'Accept': 'audio/mp3',
                'Authorization': f'Bearer {RIME_API_KEY}',
                'Content-Type': 'application/json'
            }
            payload = {
                'speaker': 'celeste',  # Rime flagship voice
                'text': text,
                'modelId': 'arcana'    # Rime's newest model
            }
            
            try:
                rime_response = requests.post(
                    'https://users.rime.ai/v1/rime-tts',  # CORRECT endpoint from docs
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                if rime_response.status_code == 200:
                    # Save audio to temporary file and return it
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                        temp_audio.write(rime_response.content)
                        temp_audio_path = temp_audio.name
                    
                    return send_from_directory(
                        os.path.dirname(temp_audio_path),
                        os.path.basename(temp_audio_path),
                        as_attachment=True,
                        download_name="response.mp3",
                        mimetype="audio/mpeg"
                    )
                else:
                    print(f"Rime TTS API error: {rime_response.status_code} - {rime_response.text}")
                    raise Exception(f"Rime TTS API returned status {rime_response.status_code}")
            
            except Exception as rime_error:
                print(f"Rime TTS error: {rime_error}")
                # Fallback response
                return jsonify({"message": f"TTS would generate audio for: {text} (Rime API error)"})
        else:
            # Placeholder when API key not configured
            return jsonify({"message": f"TTS would generate audio for: {text} (Please configure Rime API key)"})
    
    except Exception as e:
        print(f"TTS error: {str(e)}")
        return jsonify({"error": "Failed to generate speech", "details": str(e)}), 500

@app.route('/api/transition', methods=['POST'])
def transition_phase():
    # Transition from learn to diagnosis phase
    session['phase'] = 'diagnosis'
    return jsonify({"success": True, "phase": "diagnosis"})



def get_clinical_reasoning_score(case, interactions):
    """
    Uses the rubric-based grader to evaluate each student message and
    returns an averaged 0-100 score along with qualitative feedback.
    """
    try:
        # Extract student (user) messages only
        user_msgs = [i["content"] for i in interactions if i["role"] == "user"]
        if not user_msgs:
            return 0, []

        scores, feedback = [], []
        for msg in user_msgs:
            try:
                eval_result = grader.evaluate("", msg)
                ca = int(eval_result.get("Clinical Accuracy (1-5)", 0))
                rq = int(eval_result.get("Reasoning Quality (1-5)", 0))
                em = int(eval_result.get("Empathy (1-5)", 0))
                # Convert average (out of 5) to percentage
                scores.append((ca + rq + em) / 15 * 100)
                feedback.append(eval_result.get("Feedback", ""))
            except Exception as e:
                print(f"Rubric grading error: {e}")
        overall = int(sum(scores) / len(scores)) if scores else 75
        return overall, feedback
    except Exception as e:
        print(f"Error in rubric grading: {e}")
        return 75, []

@app.route('/results/<case_id>')
def results(case_id):
    # Calculate and display results
    start_time = datetime.fromisoformat(session.get('start_time', datetime.now().isoformat()))
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60  # in minutes
    
    interactions = session.get('interactions', [])
    user_messages = [i for i in interactions if i['role'] == 'user']
    
    # Load the patient case for displaying the correct diagnosis and data
    patient_cases = load_patient_cases()
    case = next((c for c in patient_cases if c['id'] == case_id), None)
    
    if not case:
        return "Case not found", 404
    
    # Get clinical reasoning score from AI
    clinical_reasoning_score, feedback_list = get_clinical_reasoning_score(case, interactions)
    
    results_data = {
        "duration": round(duration, 1),
        "num_questions": len(user_messages),
        "efficiency_score": min(100, max(0, 100 - (len(user_messages) - 10) * 5)),  # Simple efficiency score based on number of questions
        "clinical_reasoning_score": clinical_reasoning_score,  # Rubric-based clinical reasoning score
        "clinical_feedback": feedback_list,  # List of qualitative feedback strings
        "case": case  # Pass the entire case for display in the results page
    }
    
    return render_template('results.html', results=results_data)

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/case1', exist_ok=True)
    
    # Create a sample patient case file if it doesn't exist
    if not os.path.exists('data/patient_cases.json'):
        sample_cases = [
            {
                "id": "case001",
                "name": "Alicia Smith",
                "age": 33,
                "gender": "Female",
                "chief_complaint": "Right lower quadrant pain",
                "condition": "Appendicitis",
                "symptoms": [
                    "Right lower quadrant pain",
                    "Mild anorexia",
                    "No nausea",
                    "Low-grade fever"
                ],
                "history": "No significant past medical history",
                "diagnosis": "Acute appendicitis",
                "imaging_needed": "CT scan of abdomen"
            },
            {
                "id": "case002",
                "name": "James Wilson",
                "age": 57,
                "gender": "Male",
                "chief_complaint": "Chest pain and shortness of breath",
                "condition": "Myocardial Infarction",
                "symptoms": [
                    "Substernal chest pain",
                    "Pain radiating to left arm",
                    "Shortness of breath",
                    "Diaphoresis"
                ],
                "history": "Hypertension, Hyperlipidemia, Smoker",
                "diagnosis": "Acute myocardial infarction",
                "imaging_needed": "ECG, Cardiac enzymes"
            }
        ]
        
        with open('data/patient_cases.json', 'w') as f:
            json.dump(sample_cases, f, indent=2)
    
    app.run(debug=True) 