import json
import requests
from typing import Dict, List, Any
from config import config

class InsightExtractionService:
    def __init__(self):
        self.ollama_url = f"{config.OLLAMA_BASE_URL}/api/generate"
        self.model = config.OLLAMA_MODEL
    
    def _query_ollama(self, prompt: str) -> str:
        """Query Ollama LLM"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "top_p": 0.9
            }
        }
        
        response = requests.post(self.ollama_url, json=payload)
        response.raise_for_status()
        
        return response.json()["response"]
    
    async def extract_action_items(self, transcript: str) -> List[Dict[str, Any]]:
        """Extract action items from transcript"""
        prompt = f"""
        Analyze the following meeting transcript and extract all action items. 
        Return the result as a JSON array where each item has the structure:
        {{"description": "task description", "assignee": "person name or null", "priority": "high/medium/low", "due_date": "mentioned date or null"}}
        
        Transcript:
        {transcript}
        
        Action items (JSON only):
        """
        
        response = self._query_ollama(prompt)
        try:
            # Clean the response to extract JSON
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return []
    
    async def extract_decisions(self, transcript: str) -> List[Dict[str, Any]]:
        """Extract key decisions from transcript"""
        prompt = f"""
        Analyze the following meeting transcript and extract all key decisions made.
        Return as JSON array with structure: {{"decision": "description", "context": "background", "impact": "potential impact"}}
        
        Transcript:
        {transcript}
        
        Decisions (JSON only):
        """
        
        response = self._query_ollama(prompt)
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return []
    
    async def identify_participants(self, transcript: str) -> List[str]:
        """Identify meeting participants"""
        prompt = f"""
        Identify all unique speakers/participants mentioned in this meeting transcript.
        Return only a JSON array of names: ["Name1", "Name2", ...]
        
        Transcript:
        {transcript}
        
        Participants (JSON only):
        """
        
        response = self._query_ollama(prompt)
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return []
    
    async def extract_key_topics(self, transcript: str) -> List[str]:
        """Extract main topics discussed"""
        prompt = f"""
        Identify the main topics and themes discussed in this meeting.
        Return as JSON array: ["Topic 1", "Topic 2", ...]
        
        Transcript:
        {transcript}
        
        Key topics (JSON only):
        """
        
        response = self._query_ollama(prompt)
        try:
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return []