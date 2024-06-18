"""
make project unique
"""

from yoyo import step

__depends__ = {'20240618_01_fQsgI-project'}

steps = [
    step("""
    ALTER TABLE project
    ADD CONSTRAINT name_unique UNIQUE (name);
    """)
]
