#!/usr/bin/env python3
"""
VARTAPRAVAH - AI Marathi Script Generator (Powered by Groq)
Converts news to clean, professional Marathi language scripts using AI
Ready for TTS (Text-to-Speech) engine
"""

import logging
import os
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

logger = logging.getLogger(__name__)


# ============================================================================
# GROQ AI-POWERED MARATHI SCRIPT GENERATOR
# ============================================================================

def get_groq_client():
    """Get or create Groq client with API key from environment"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("⚠️ GROQ_API_KEY not found. Set it in .env file or environment variable")
    return Groq(api_key=api_key)


def generate_marathi_script(news_list: List[Dict], bulletin_type: str = "सकाळ") -> str:
    """
    Generate professional Marathi news script using Groq AI
    
    Args:
        news_list: List of news dictionaries with title, description, source
        bulletin_type: Type of bulletin (सकाळ, मध्य, संध्या, प्राइम, रात्र)
    
    Returns:
        Professional Marathi script ready for TTS
    
    Example:
        news = [
            {"title": "...", "description": "...", "source": "PTI"},
            ...
        ]
        script = generate_marathi_script(news, "सकाळ")
    """
    
    if not HAS_GROQ:
        logger.warning("⚠️ Groq not available, returning fallback script")
        return generate_marathi_script_fallback(news_list, bulletin_type)
    
    try:
        client = get_groq_client()
        
        # Build news context
        news_text = ""
        for i, n in enumerate(news_list, 1):
            title = n.get('title', 'बातमी')
            description = n.get('description', '')
            source = n.get('source', 'अज्ञात')
            news_text += f"{i}. {title}\n   {description}\n   (स्रोत: {source})\n\n"
        
        # Craft the prompt
        prompt = f"""खालील बातम्या वापरून शुद्ध, व्यावसायिक मराठी न्यूज स्क्रिप्ट तयार करा.

बुलेटिन प्रकार: {bulletin_type}

नियम:
- फक्त मराठी भाषा, कोणतेही इंग्रजी नकोत (अपवाद: नाव, ठिकाणे)
- न्यूज अँकर स्टाइल - औपचारिक, व्यावसायिक टोन
- परिचय आणि समपन करणे समाविष्ट करा
- प्रत्येक बातमीसाठी 2-3 वाक्य
- संपूर्ण विराम वापरा (।)
- रेडिओ / टीव्ही न्यूज स्टाइल

बातम्या:
{news_text}

शुद्ध मराठी स्क्रिप्ट तयार करा:"""

        logger.info("🧠 Generating Marathi script with Groq AI...")
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2048
        )
        
        script = response.choices[0].message.content
        logger.info(f"✅ Generated AI script: {len(script)} characters")
        
        return script
    
    except Exception as e:
        logger.error(f"❌ Groq generation error: {str(e)}")
        logger.info("⚠️ Falling back to simple template")
        return generate_marathi_script_fallback(news_list, bulletin_type)


def generate_marathi_script_fallback(news_list: List[Dict], bulletin_type: str = "सकाळ") -> str:
    """
    Fallback simple script generation (no AI, template-based)
    Used when Groq is unavailable
    """
    intro = f"{bulletin_type} बुलेटिन - वार्ताप्रवाह मध्ये आपले स्वागत आहे।\n\n"
    
    script = intro
    
    for i, news in enumerate(news_list, 1):
        title = news.get('title', 'बातमी')
        description = news.get('description', '')
        source = news.get('source', 'अज्ञात')
        
        script += f"{i}. {title}।\n"
        
        if description:
            script += f"{description}।\n"
        
        script += f"ही बातमी {source} कडून प्राप्त झाली आहे।\n\n"
    
    outro = "ही होती आत्तापर्यंतची प्रमुख बातमी। अधिक अपडेटसाठी पाहत रहा वार्ताप्रवाह।"
    
    return script + outro


# ============================================================================
# BULLETIN TYPES (Marathi)
# ============================================================================

BULLETIN_TYPES = {
    "सकाळ": "Morning Bulletin",
    "मध्य": "Noon Bulletin", 
    "संध्या": "Evening Bulletin",
    "प्राइम": "Prime Time Bulletin",
    "रात्र": "Night Bulletin"
}


class BulletinScript(BaseModel):
    """Generated bulletin script"""
    bullet_number: int
    original_title: str
    marathi_title: str
    marathi_description: str
    original_language: str = "en"
    target_language: str = "mr"
    category: str
    timestamp: str
    tts_ready_text: str  # Clean text for TTS


class ScriptGenerator:
    """
    Advanced script generator using Groq AI for professional Marathi scripts
    """
    
    def __init__(self, use_groq: bool = True):
        """
        Initialize script generator
        
        Args:
            use_groq: Use Groq AI for generation (default: True)
        """
        self.use_groq = use_groq and HAS_GROQ
        self.groq_client = None
        
        if self.use_groq:
            try:
                self.groq_client = get_groq_client()
                logger.info("✅ Groq AI client initialized")
            except Exception as e:
                logger.warning(f"⚠️ Groq not available: {str(e)}")
                self.use_groq = False
    
    def generate_bulletin_script(
        self,
        news_dict: Dict[str, List],
        max_bullets: int = 5,
        bulletin_type: str = "सकाळ"
    ) -> Dict:
        """
        Generate complete bulletin with Groq AI
        
        Args:
            news_dict: Dict with categories -> article lists (from NewsFetcher)
            max_bullets: Max bullets per category
            bulletin_type: Type of bulletin
        
        Returns:
            Complete bulletin structure ready for TTS
        """
        logger.info(f"🧠 Generating AI bulletin script ({max_bullets} bullets)...")
        
        # Convert NewsArticle objects to dicts if needed
        simple_news = []
        for category, articles in news_dict.items():
            for article in articles[:max_bullets]:
                # Handle both dict and NewsArticle objects
                if hasattr(article, 'title'):
                    simple_news.append({
                        'title': article.title,
                        'description': article.description or '',
                        'source': article.source,
                        'category': category
                    })
                else:
                    simple_news.append(article)
        
        # Generate AI script
        if self.use_groq:
            full_script = generate_marathi_script(simple_news, bulletin_type)
        else:
            full_script = generate_marathi_script_fallback(simple_news, bulletin_type)
        
        # Build bulletin dict
        bulletin = {
            "intro": full_script.split('\n\n')[0] if '\n\n' in full_script else "",
            "full_script": full_script,
            "bullets": [
                {
                    "bullet_number": i,
                    "original_title": n.get('title', ''),
                    "marathi_title": n.get('title', ''),
                    "marathi_description": n.get('description', ''),
                    "category": n.get('category', ''),
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "tts_ready_text": f"{n.get('title', '')}। {n.get('description', '')}"
                }
                for i, n in enumerate(simple_news, 1)
            ],
            "outro": "अधिक अपडेटसाठी पाहत रहा वार्ताप्रवाह।",
            "total_bullets": len(simple_news),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        logger.info(f"✅ Generated {len(simple_news)} bullet scripts with AI")
        return bulletin
    
    def generate_full_narration(self, bulletin: Dict) -> str:
        """
        Generate complete narration text for TTS
        """
        return bulletin.get('full_script', '')


def get_script_generator(use_groq: bool = True) -> ScriptGenerator:
    """Factory function to create ScriptGenerator instance with Groq AI"""
    return ScriptGenerator(use_groq=use_groq)


if __name__ == "__main__":
    # Test the AI script generator
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test with simple news list
    test_news = [
        {
            "title": "Maharashtra announces new education policy",
            "description": "The state government has approved a comprehensive education reform plan",
            "source": "PTI",
            "category": "Maharashtra"
        },
        {
            "title": "Railway announces new routes",
            "description": "Indian Railways launches express routes connecting major cities",
            "source": "ANI",
            "category": "India"
        }
    ]
    
    print("\n" + "=" * 70)
    print("🧠 VARTAPRAVAH - AI Marathi Script Generator (Powered by Groq)")
    print("=" * 70)
    
    # Test simple function
    print("\n📄 Testing simple function API:")
    print("-" * 70)
    script = generate_marathi_script(test_news, "सकाळ")
    print(script[:500] + "...\n" if len(script) > 500 else script)
    
    print("\n" + "=" * 70)
