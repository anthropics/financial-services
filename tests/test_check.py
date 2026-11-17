"""Unit tests for check.py script."""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def test_rel_function():
    """Test the rel() function converts paths correctly."""
    # Import after path is set up
    import check

    root = Path("/Users/test/financial-services")
    check.ROOT = root
    
    test_path = Path("/Users/test/financial-services/plugins/test/file.md")
    result = check.rel(test_path)
    
    assert result == "plugins/test/file.md"


def test_err_function():
    """Test the err() function appends to errors list."""
    import check
    
    check.errors = []
    check.err("test error")
    
    assert len(check.errors) == 1
    assert check.errors[0] == "test error"
