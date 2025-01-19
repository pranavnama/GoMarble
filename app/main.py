from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import logging
from .config import Config
from .services.llm import LLMService
from .services.scraper import ReviewScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': Config.CACHE_TIMEOUT
})

llm_service = LLMService(Config.GEMINI_API_KEY)
scraper = ReviewScraper(Config.CHROME_DRIVER_PATH, llm_service)

@app.route('/api/reviews', methods=['GET'])
@limiter.limit("10 per minute")
@cache.memoize(timeout=3600)
def get_reviews():
    url = request.args.get('page')
    
    if not url:
        return jsonify({
            "error": "Missing 'page' parameter",
            "reviews_count": 0,
            "reviews": []
        }), 400

    try:
        result = scraper.extract_reviews(url)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Review extraction failed: {str(e)}")
        return jsonify({
            "error": str(e),
            "reviews_count": 0,
            "reviews": []
        }), 500