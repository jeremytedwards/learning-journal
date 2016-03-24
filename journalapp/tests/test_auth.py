# coding=utf-8
import os


def test_un_exist(auth_env):
    assert os.environ.get('AUTH_USERNAME', None) is not None


def test_pw_exist(auth_env):
    assert os.environ.get('AUTH_PASSWORD', None) is not None


def test_password_is_encrypted(auth_env):
    """Test the password is encrypted."""
    assert os.environ.get('AUTH_PASSWORD', None) != 'SecretPwd!'


def test_check_pw_success(auth_env):
    from journalapp.security import is_admin_pw
    password = 'SecretPwd!'
    assert is_admin_pw(password)


def test_check_pw_fail(auth_env):
    from journalapp.security import is_admin_pw
    password = '!dwPterceS'
    assert not is_admin_pw(password)


def test_secure_view(app):
    response = app.get('/secure', status=403)
    assert response.status_code == 403


def test_accesss_view(app):
    response = app.get('/secure', status=200)
    assert response.status_code == 200


def test_get_login_view(app):
    response = app.get('/login/')
    assert response.status_code == 200


def test_post_login_view(app, auth_env):
    data = {'username': 'SecretUser', "password": 'SecretPwd!'}
    response = app.get('/login/', data)
    assert response.status_code == 200


def test_add_no_permission(dbtransaction, app):
    """Test that add route returns a 403 if not permitted."""
    response = app.get('/new/', status='4*')
    assert response.status_code == 403


def test_add_with_permission(dbtransaction, authenticated_app):
    """Test that add route returns a 200 if authenticated."""
    response = authenticated_app.get('/new/')
    assert response.status_code == 200