from flask import Blueprint, request

category_bp = Blueprint("category", __name__, url_prefix="/category")

@category_bp.route("/", methods=["GET"])
def get_category():
    pass