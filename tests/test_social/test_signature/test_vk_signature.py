# -*- coding: utf8 -*-
from doom.social.signature.vk_signature import VKSignature
import pytest


@pytest.fixture
def signature():
    return VKSignature('secretkey')


def test_string(signature):
    assert signature.string((32134, 'uids')) == '32134_uids_' + signature.key


def test_md5(signature):
    assert signature.md5(("3126387", "32436")) == \
           "30d8dbb6aebccd7eb8ed4faed6b7b70e"


def test_auth(signature):
    uid = 'user'
    app_id = 1251235
    auth_key = signature.md5((app_id, uid))
    assert signature.auth(
        {'auth_key': auth_key, 'api_id': app_id, 'viewer_id': uid}
    )
