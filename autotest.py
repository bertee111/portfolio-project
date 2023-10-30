import pytest
from app import app as flask_app
from flask_login import current_user, login_user
from werkzeug.datastructures import MultiDict
from datetime import datetime



@pytest.fixture
def app():
    app = flask_app
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_valid_user(client):
    user_data = MultiDict([
        ('username', 'john'),
        ('password', '123'),
        ('remember_me', False)
    ])
    with flask_app.app_context():
        with flask_app.test_request_context():
            flask_app.config['WTF_CSRF_ENABLED'] = False
            response = client.post('/login', data=user_data, content_type='multipart/form-data', follow_redirects=True)
            assert current_user.username == 'john'
            assert response.status_code == 200


    # event_data = MultiDict([
    #         ('user_id', 2),
    #         ('title', 'skateboarding'),
    #         ('date', datetime.today())
    # ])
    # with flask_app.app_context():
    #     with flask_app.test_request_context():
    #         create_event_response = client.post('/create_event', data=event_data, follow_redirects=True)
