# -*- coding: utf8 -*-
from doom.social.signature.od_signature import ODSignature
import pytest


SESSION_KEY = 'fff46634098ff79ce9a657de771fae2904f0a4d49e7553c47e4eda26c.8'


@pytest.fixture
def signature():
    return ODSignature('E36EBA56D5759286F167D45C')


def test_auth(signature):
    assert signature.auth(
        {
            'logged_user_id': '556722096996',
            'session_key': SESSION_KEY,
            'application_key': 'CBAFLHOCEBABABABA',
            'auth_key': '2606ad4a24f6ff93d93bd2a13b8d95b6'
        },
    )


def test_failed_auth(signature):
    assert signature.auth({}) == False


