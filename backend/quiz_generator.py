from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class QuizGenerator:
    """Generates quiz questions using LLM from Wikipedia article content"""

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.7,
            convert_system_message_to_human=True
        )

        # Define prompt templates
        self.quiz_prompt = self._create_quiz_prompt()
        self.related_topics_prompt = self._create_related_topics_prompt()

    def _create_quiz_prompt(self) -> PromptTemplate:
        """
        Create the prompt template for quiz generation
        Optimized for grounding in article content and minimizing hallucination
        """
        template = """You are an expert quiz creator. Based on the Wikipedia article provided, create a high-quality quiz.

ARTICLE TITLE: {title}

ARTICLE CONTENT:
{content}

INSTRUCTIONS:
1. Create exactly {num_questions} multiple-choice questions based ONLY on the information in the article above
2. Questions should cover different aspects and sections of the article
3. Include a mix of difficulty levels: easy (basic facts), medium (understanding), and hard (deeper analysis)
4. Each question must have:
   - A clear, specific question
   - Four plausible options (A, B, C, D)
   - The correct answer (must be one of the four options)
   - A brief explanation citing which part of the article contains the answer
   - A difficulty level (easy, medium, or hard)

CRITICAL RULES:
- DO NOT make up facts - only use information explicitly stated in the article
- Ensure all options are plausible but only one is correct
- Make sure the correct answer is clearly supported by the article text
- Vary the position of correct answers (don't always make it option B)
- Questions should test comprehension, not just recall

OUTPUT FORMAT (respond with valid JSON only):
{{
  "questions": [
    {{
      "question": "Question text here?",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option B",
      "difficulty": "medium",
      "explanation": "The article states in the [section name] that..."
    }}
  ]
}}

Generate the quiz now:"""

        return PromptTemplate(
            input_variables=["title", "content", "num_questions"],
            template=template
        )

    def _create_related_topics_prompt(self) -> PromptTemplate:
        """
        Create the prompt template for suggesting related topics
        """
        template = """Based on the Wikipedia article about "{title}", suggest related topics that would be interesting for further reading.

ARTICLE SUMMARY:
{summary}

ARTICLE SECTIONS:
{sections}

INSTRUCTIONS:
Suggest 5-8 related Wikipedia topics that:
1. Are directly related to the main topic
2. Would help deepen understanding of the subject
3. Are specific enough to be actual Wikipedia articles
4. Cover different aspects (people, events, concepts, places, etc.)

OUTPUT FORMAT (respond with valid JSON only):
{{
  "related_topics": [
    "Topic 1",
    "Topic 2",
    "Topic 3"
  ]
}}

Generate the related topics now:"""

        return PromptTemplate(
            input_variables=["title", "summary", "sections"],
            template=template
        )

    def generate_quiz(self, title: str, content: str, num_questions: int = 7) -> List[Dict]:
        """
        Generate quiz questions from article content
        
        Args:
            title: Article title
            content: Full article text
            num_questions: Number of questions to generate (default 7)
        
        Returns:
            List of question dictionaries
        """
        try:
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=self.quiz_prompt)
            
            # Generate quiz
            result = chain.run(
                title=title,
                content=content,
                num_questions=num_questions
            )
            
            # Parse JSON response
            # Clean the response to extract JSON
            result = result.strip()
            if result.startswith('```json'):
                result = result[7:]
            if result.startswith('```'):
                result = result[3:]
            if result.endswith('```'):
                result = result[:-3]
            result = result.strip()
            
            quiz_data = json.loads(result)
            questions = quiz_data.get('questions', [])
            
            # Validate and ensure each question has required fields
            validated_questions = []
            for q in questions:
                if all(key in q for key in ['question', 'options', 'answer', 'difficulty', 'explanation']):
                    # Ensure options is a list of 4 items
                    if isinstance(q['options'], list) and len(q['options']) == 4:
                        # Ensure answer is one of the options
                        if q['answer'] in q['options']:
                            validated_questions.append(q)
            
            return validated_questions
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {result}")
            return self._generate_fallback_quiz(title, content, num_questions)
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._generate_fallback_quiz(title, content, num_questions)

    def generate_related_topics(self, title: str, summary: str, sections: List[str]) -> List[str]:
        """
        Generate related topic suggestions
        
        Args:
            title: Article title
            summary: Article summary
            sections: List of article sections
        
        Returns:
            List of related topic names
        """
        try:
            # Create chain
            chain = LLMChain(llm=self.llm, prompt=self.related_topics_prompt)
            
            # Generate related topics
            sections_text = ', '.join(sections[:5])  # Use first 5 sections
            result = chain.run(
                title=title,
                summary=summary,
                sections=sections_text
            )
            
            # Parse JSON response
            result = result.strip()
            if result.startswith('```json'):
                result = result[7:]
            if result.startswith('```'):
                result = result[3:]
            if result.endswith('```'):
                result = result[:-3]
            result = result.strip()
            
            topics_data = json.loads(result)
            topics = topics_data.get('related_topics', [])
            
            return topics[:8]  # Limit to 8 topics
            
        except Exception as e:
            print(f"Error generating related topics: {e}")
            return self._generate_fallback_topics(title, sections)

    def _generate_fallback_quiz(self, title: str, content: str, num_questions: int) -> List[Dict]:
        """Generate a basic fallback quiz if LLM fails"""
        return [
            {
                "question": f"What is the main subject of this article?",
                "options": [title, "Unknown", "Not specified", "Other"],
                "answer": title,
                "difficulty": "easy",
                "explanation": "This is the title of the article."
            }
        ]

    def _generate_fallback_topics(self, title: str, sections: List[str]) -> List[str]:
        """Generate fallback related topics"""
        topics = [f"{title} - {section}" for section in sections[:5]]
        return topics if topics else ["History", "Biography", "Science"]
