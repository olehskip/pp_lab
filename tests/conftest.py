import pytest

from app import app
from app.db import metadata, engine

already_dropped = False

@pytest.fixture()
def client():
    global already_dropped
    app.config['TESTING'] = True
    client = app.test_client()

    if not already_dropped:
        metadata.drop_all(engine)
        metadata.create_all(engine)
        already_dropped = True

    yield client
