"""Main Flask application entry point."""
import logging
import os
import sys
from flask import Flask, jsonify
from dotenv import load_dotenv
from config.config import get_config
from routes import home_bp, items_bp

# Load environment variables from .env (for local dev; Render sets them natively)
load_dotenv()

# Configure logging — stdout only (Render/cloud captures stdout automatically)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory for creating and configuring the Flask app."""
    try:
        app = Flask(__name__)
        
        # Load configuration
        config = get_config()
        app.config.from_object(config)
        
        # Register blueprints
        app.register_blueprint(home_bp)
        app.register_blueprint(items_bp)
        
        # Register error handlers
        register_error_handlers(app)
        
        logger.info(f"Flask app created successfully with {app.config['FLASK_ENV']} environment")
        return app
    
    except ValueError as e:
        logger.critical(f"Configuration error: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Failed to create Flask app: {str(e)}")
        raise


def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        logger.warning(f"Bad request: {str(error)}")
        return jsonify({"error": "Bad request"}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        logger.warning(f"Resource not found: {str(error)}")
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        logger.warning(f"Method not allowed: {str(error)}")
        return jsonify({"error": "Method not allowed"}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 Internal Server errors."""
        logger.error(f"Internal server error: {str(error)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle 503 Service Unavailable errors."""
        logger.error(f"Service unavailable: {str(error)}")
        return jsonify({"error": "Service unavailable"}), 503


# Create the application
app = create_app()


if __name__ == '__main__':
    # In production, use a proper WSGI server like Gunicorn
    # This is only for development
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_ENV") == "development"
    
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    app.run(
        host=app.config['HOST'],
        port=port,
        debug=debug,
        threaded=True
    )