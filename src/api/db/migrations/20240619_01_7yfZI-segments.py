"""
segments
"""

from yoyo import step

__depends__ = {'20240618_03_Ds0QX-questions'}

steps = [
    step("""
        CREATE TABLE segments (
            id SERIAL PRIMARY KEY,
            project_id INTEGER NOT NULL,
            segment TEXT NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE
        )
    """),
    step("""
    ALTER TABLE questions
    ADD CONSTRAINT fk_questions_project_id
    FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE; 
    """)
]
