"""Item CRUD routes."""
from flask import Blueprint, request, jsonify
from services.db_service import ItemService, DatabaseError
from utils.validators import validate_item_name, validate_item_id
import logging

logger = logging.getLogger(__name__)

items_bp = Blueprint('items', __name__, url_prefix='/api')


@items_bp.route('/items', methods=['GET'])
def get_items():
    """
    Fetch all items.
    
    Returns:
        JSON list of items
    """
    try:
        items = ItemService.get_all_items()
        return jsonify(items), 200
    except DatabaseError as e:
        logger.error(f"Database error fetching items: {str(e)}")
        return jsonify({"error": "Failed to fetch items"}), 500
    except Exception as e:
        logger.error(f"Unexpected error fetching items: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@items_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for load balancers."""
    try:
        items = ItemService.get_all_items()
        return jsonify({"status": "ok", "database": "connected"}), 200
    except:
        return jsonify({"status": "error", "database": "disconnected"}), 503


@items_bp.route('/add', methods=['POST'])
def add_item():
    """
    Create a new item.
    
    Request JSON:
        {
            "name": "item name"
        }
    
    Returns:
        JSON object with created item
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        name = data.get('name')
        
        # Validate input
        name = validate_item_name(name)
        
        result = ItemService.create_item(name)
        return jsonify(result), 201
    
    except ValueError as e:
        logger.warning(f"Validation error creating item: {str(e)}")
        return jsonify({"error": str(e)}), 400
    except DatabaseError as e:
        logger.error(f"Database error creating item: {str(e)}")
        return jsonify({"error": "Failed to create item"}), 500
    except Exception as e:
        logger.error(f"Unexpected error creating item: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@items_bp.route('/update/<item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Update an existing item.
    
    Request JSON:
        {
            "name": "updated item name"
        }
    
    Args:
        item_id: ID of the item to update
    
    Returns:
        JSON object with updated item
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400
        
        # Validate inputs
        item_id = validate_item_id(item_id)
        name = data.get('name')
        name = validate_item_name(name)
        
        result = ItemService.update_item(item_id, name)
        return jsonify(result), 200
    
    except ValueError as e:
        error_msg = str(e)
        status_code = 404 if "not found" in error_msg.lower() else 400
        logger.warning(f"Validation error updating item {item_id}: {error_msg}")
        return jsonify({"error": error_msg}), status_code
    except DatabaseError as e:
        logger.error(f"Database error updating item {item_id}: {str(e)}")
        return jsonify({"error": "Failed to update item"}), 500
    except Exception as e:
        logger.error(f"Unexpected error updating item {item_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@items_bp.route('/delete/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete an item.
    
    Args:
        item_id: ID of the item to delete
    
    Returns:
        JSON object confirming deletion
    """
    try:
        # Validate input
        item_id = validate_item_id(item_id)
        
        result = ItemService.delete_item(item_id)
        return jsonify(result), 200
    
    except ValueError as e:
        error_msg = str(e)
        status_code = 404 if "not found" in error_msg.lower() else 400
        logger.warning(f"Validation error deleting item {item_id}: {error_msg}")
        return jsonify({"error": error_msg}), status_code
    except DatabaseError as e:
        logger.error(f"Database error deleting item {item_id}: {str(e)}")
        return jsonify({"error": "Failed to delete item"}), 500
    except Exception as e:
        logger.error(f"Unexpected error deleting item {item_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
