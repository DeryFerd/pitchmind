import os
import sys
from collections.abc import Generator

from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages", "db"))

from pitchmind_db.base import get_session_factory


def get_db() -> Generator[Session, None, None]:
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()
