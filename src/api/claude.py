from anthropic import Anthropic
import re
import json
from config import CLAUDE_API_KEY, CLAUDE_MODEL_NAME


# Initialize Anthropic client
client = Anthropic()


# Make AI request to Claude API
def make_ai_request(prompt):
    """
    Send a prompt to Claude and get a trading decision response.
    
    Args:
        prompt (str): The trading analysis prompt
        
    Returns:
        dict: Response object with message content
    """
    try:
        ai_resp = client.messages.create(
            model=CLAUDE_MODEL_NAME,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return ai_resp
    except Exception as e:
        raise Exception(f"Claude API error: {e}")


# Parse AI response
def parse_ai_response(ai_response):
    """
    Extract and parse JSON trading decisions from Claude's response.
    
    Args:
        ai_response: Response object from Claude API
        
    Returns:
        list: Parsed JSON array of trading decisions
        
    Raises:
        Exception: If JSON parsing fails
    """
    try:
        # Extract text content from Claude response
        ai_content = ai_response.content[0].text.strip()
        
        # Remove markdown code blocks if present
        ai_content = re.sub(r'```json|```', '', ai_content).strip()
        
        # Parse JSON
        decisions = json.loads(ai_content)
        
        # Ensure it's a list
        if not isinstance(decisions, list):
            raise Exception("Claude response is not a JSON array")
            
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response from Claude: {ai_content}")
    
    return decisions
