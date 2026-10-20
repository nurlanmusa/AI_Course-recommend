import httpx 

from app.core.config import get_settings

settings = get_settings()

def generate_answer(
    question: str,
    context: str,)-> str:
    
    system_prompt = ( 
        "You are a course recommendation assistant. "
        "Answer only using the supplied course context. "
        "Do not invent courses, providers, or URLs."
    )

    user_prompt = f"""
    User question:
    {question}
    Available courses:
    {context}

    Recommend the most relevant courses and briefly explain why.
    """
    response = httpx.post(f"{settings.ollama_base_url}/api/chat",
    json = {
        "model": settings.ollama_model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "stream": False,
        "thinking": False,
        "options": {
            "temperature": 0.1,
        },
    },
    timeout=180,)

    response.raise_for_status()
    response_data = response.json()
    
    return response_data["message"]["content"]
