def test_basic_import():
    """Test basic import functionality"""
    try:
        import shared
        print("✅ Successfully imported shared package")
        assert True
    except ImportError as e:
        print(f"❌ Failed to import shared package: {e}")
        assert False

def test_config_import():
    """Test config import"""
    try:
        from shared import config
        print("✅ Successfully imported shared.config")
        assert True
    except ImportError as e:
        print(f"❌ Failed to import shared.config: {e}")
        assert False

def test_simple_function():
    """Test that basic Python functionality works"""
    result = 2 + 2
    assert result == 4
    print("✅ Basic arithmetic works")