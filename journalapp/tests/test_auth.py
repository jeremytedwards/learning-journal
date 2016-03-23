# coding=utf-8
import os
import pytest
import webtest


@pytest.fixture()
def app():
    settings = {'sqlalchemy.url': 'sqlite:////tmp/foobar/'}
    app = main({}, settings)
    return webtest.TestApp(app)


@pytest.fixture()
def auth_env():
    from foobar.security import pwd_context
    os.environ['AUTH_USERNAME'] = pwd_context.'SecretUser'
    os.environ['AUTH_PASSWORD'] = 'SecretPwd!'


def test_secure_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403


def test_accesss_view(app):
    response = app.get('/secure', status=200)
    assert response.status_code == 200


def test_un_exist(app):
    assert os.environ.get('AUTH_USERNAME', None) is not 'SecretUser'


def test_pw_exist(app):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_check_pw_success(auth_env):
    from foobar.security import check_pw
    password = 'SecretPwd!'
    assert not check_pw(password)


def test_check_pw_fail(auth_env):
    from foobar.security import check_pw
    password = 'SecretPwd!'
    assert check_pw(password)


def test_get_login_view(app):
    response = app.get('/login')
    assert response.status_code == 200


def test_post_login_view(app, auth_env):
    data = {'username': 'SecretUser', "password": 'SecretPwd!'}
    response = app.get('/login', data)
    assert response.status_code == 200

