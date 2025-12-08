from datetime import datetime

from app import db


class GenerationHistory(db.Model):
    """Model to store generation history for SEO tools."""
    __tablename__ = 'generation_history'
    
    id = db.Column(db.Integer, primary_key=True)
    tool = db.Column(db.String(64), nullable=False)
    business_name = db.Column(db.String(256))
    business_type = db.Column(db.String(256))
    input_data = db.Column(db.Text)
    output_data = db.Column(db.Text)
    is_json = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
