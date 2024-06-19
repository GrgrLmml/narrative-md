"""
segments update
"""

from yoyo import step

__depends__ = {'20240619_01_7yfZI-segments'}

steps = [
    step("""
    ALTER TABLE segments
    ADD COLUMN updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ADD COLUMN processed BOOLEAN NOT NULL DEFAULT FALSE;
    """)
]
