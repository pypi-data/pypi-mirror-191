from byb.platforms import get_platform, InstagramPost


def test_get_instagram_post():
    assert get_platform("instagram_post") == InstagramPost
