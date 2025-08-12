import pathlib

def test_caddyfile_uses_cloudflare_dns():
    contents = pathlib.Path('Caddyfile').read_text()
    assert 'dns cloudflare' in contents
