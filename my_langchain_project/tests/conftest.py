import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv

# Add project root to Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

@pytest.fixture(scope="session", autouse=True)
def setup_env():
    load_dotenv()
    # Set asyncio fixture scope
    pytest.asyncio_default_fixture_scope = "function"
    return
