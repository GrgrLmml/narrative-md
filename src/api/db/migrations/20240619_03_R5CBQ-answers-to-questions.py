"""
answers to questions
"""

from yoyo import step

__depends__ = {'20240619_02_aWVuR-segments'}

steps = [
    step("""
    ALTER TABLE questions
    ADD COLUMN answer TEXT NOT NULL DEFAULT 'n/a';
    """)
]
