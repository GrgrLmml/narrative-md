"""
project
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE project (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """),
]
