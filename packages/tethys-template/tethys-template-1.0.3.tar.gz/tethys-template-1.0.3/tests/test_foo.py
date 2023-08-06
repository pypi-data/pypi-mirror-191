from tethys.foobar import foo, fetch


def test_foobar():
    assert foo() == 'bar'


def test_fetch():
    status = fetch()
    assert status == 200
