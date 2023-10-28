import pytest
from app import app as flask_app
from flask import url_for
from flask_login import current_user, login_user
from werkzeug.datastructures import MultiDict


@pytest.fixture
def app():
    app = flask_app
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_valid_user(client):
    data = MultiDict([
        ('username', 'john'),
        ('password', '123'),
        ('remember_me', False)
    ])
    with flask_app.app_context():
        with flask_app.test_request_context():
            flask_app.config['WTF_CSRF_ENABLED'] = False

            response = client.post('/login', data=data, content_type='multipart/form-data', follow_redirects=True)
            assert current_user.username == 'john'
            assert response.status_code == 200