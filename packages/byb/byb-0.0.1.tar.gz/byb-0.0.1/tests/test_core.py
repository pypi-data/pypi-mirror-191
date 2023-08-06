from byb.core import Platform


def test_name():
    class TestPlatform(Platform):
        foo = "bar"
    
    assert TestPlatform().name == "test_platform"