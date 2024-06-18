"""
questions
"""

from yoyo import step

__depends__ = {'20240618_02_nOuaN-make-project-unique'}

steps = [
    step("""
    CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            question TEXT NOT NULL,
            kind TEXT NOT NULL,
            condition TEXT,
            options TEXT,  -- storing JSON array as TEXT
            project_id INT NOT NULL
        )
    """)
]
