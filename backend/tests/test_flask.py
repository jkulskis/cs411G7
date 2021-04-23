# basic tests to make sure that flask is working properly
import pytest

def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200

def test_404(app, client):
    res = client.get('/DNE')
    assert res.status_code == 404
