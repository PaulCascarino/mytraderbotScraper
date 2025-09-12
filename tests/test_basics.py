def test_import():
    import mytraderbotScraper
    assert hasattr(mytraderbotScraper, "__version__")
