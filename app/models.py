import json
import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from app import db


class Thing(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    name = db.Column(db.String(32), nullable=False, index=True)
    colour = db.Column(db.String(), nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Methods
    def __init__(self, name, colour):
        self.id = str(uuid.uuid4())
        self.name = name.title().strip()
        self.colour = colour
        self.created_at = datetime.utcnow()

    def __repr__(self):
        return json.dumps(self.as_dict(), separators=(",", ":"))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "colour": self.colour,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def list_item(self):
        return {
            "id": self.id,
            "name": self.name,
            "colour": self.colour,
        }
