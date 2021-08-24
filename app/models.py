import json
import uuid
from datetime import datetime

import bcrypt
from sqlalchemy.dialects.postgresql import UUID

from app import db


class User(db.Model):
    __tablename__ = "user_account"

    # Fields
    id = db.Column(UUID, primary_key=True)
    password = db.Column(db.LargeBinary, nullable=False)
    email_address = db.Column(db.String(256), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Relationships
    things = db.relationship("Thing", backref="user", lazy=True, passive_deletes=True)

    # Methods
    def __init__(self, email_address, password):
        self.id = str(uuid.uuid4())
        self.email_address = email_address.lower()
        self.created_at = datetime.utcnow()
        self.set_password(password)

    def __repr__(self):
        return json.dumps(self.as_dict(), separators=(",", ":"))

    def as_dict(self):
        return {
            "id": self.id,
            "email_address": self.email_address,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def list_item(self):
        return {
            "id": self.id,
            "email_address": self.email_address
        }

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("UTF-8"), self.password)


class Thing(db.Model):
    # Fields
    id = db.Column(UUID, primary_key=True)
    user_id = db.Column(
        UUID,
        db.ForeignKey("user_account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
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
