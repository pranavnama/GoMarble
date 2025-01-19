import google.generativeai as genai
import base64
import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def get_selectors(self, html_content):
        try:
            doc_data = base64.standard_b64encode(html_content.encode('utf-8')).decode('utf-8')
            
            prompt = """
            Analyze this HTML and provide CSS selectors for:
            1. The main reviews container
            2. Individual review elements
            3. Pagination next button
            4. Review components (title, rating, content, author)
            4. Review components (title, rating, content, author)
            Return ONLY valid CSS selectors in this exact JSON format:
            {
                "reviews_container": "selector",
                "review_item": "selector",
                "next_button": "selector",
                "selectors": {
                    "title": "selector",
                    "rating": "selector",
                    "content": "selector",
                    "author": "selector"
                }
                }
            """


            response = self.model.generate_content([
                {'mime_type': 'text/html', 'data': doc_data},
                prompt
            ])

            result = response.text.strip()
            if result.startswith('```json'):
                result = result[7:-3]

            return json.loads(result)

        except Exception as e:
            logger.error(f"LLM selector extraction failed: {str(e)}")
            raise