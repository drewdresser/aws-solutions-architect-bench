"""Tests for CDK code extraction from model outputs."""

import pytest
import sys
from pathlib import Path

# Add evals directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "evals" / "cdk_synth"))

from tasks import _extract_code, CODE_PATTERNS


class TestCodeExtractionPatterns:
    """Test that various code block formats are correctly extracted."""

    def test_python_fenced_block(self):
        """Standard ```python block should be extracted."""
        raw = '''Here's the CDK code:

```python
from aws_cdk import App, Stack
from constructs import Construct

class MyStack(Stack):
    pass

app = App()
MyStack(app, "MyStack")
app.synth()
```

This creates a simple stack.'''

        code = _extract_code(raw)
        assert "from aws_cdk import App, Stack" in code
        assert "class MyStack(Stack):" in code
        assert "app.synth()" in code
        # Should not include the markdown or explanation
        assert "Here's the CDK code" not in code
        assert "This creates a simple stack" not in code

    def test_py_fenced_block(self):
        """```py block (alternative tag) should be extracted."""
        raw = '''```py
from aws_cdk import App
app = App()
```'''

        code = _extract_code(raw)
        assert "from aws_cdk import App" in code

    def test_untagged_fenced_block(self):
        """``` block without language tag should be extracted."""
        raw = '''Here's code:

```
from aws_cdk import App
app = App()
```'''

        code = _extract_code(raw)
        assert "from aws_cdk import App" in code

    def test_capitalized_python_tag(self):
        """```Python (capitalized) should be handled by IGNORECASE."""
        raw = '''```Python
from aws_cdk import App
```'''

        code = _extract_code(raw)
        assert "from aws_cdk import App" in code

    def test_multiple_blocks_takes_largest(self):
        """When multiple code blocks exist, take the largest one."""
        raw = '''First some setup:

```python
import os
```

Then the main code:

```python
from aws_cdk import App, Stack
from constructs import Construct

class MyStack(Stack):
    def __init__(self, scope, id):
        super().__init__(scope, id)

app = App()
MyStack(app, "MyStack")
app.synth()
```

And that's it.'''

        code = _extract_code(raw)
        # Should get the larger block, not the small "import os" block
        assert "class MyStack(Stack):" in code
        assert "app.synth()" in code

    def test_fallback_removes_answer_lines(self):
        """Fallback should remove ANSWER: prefixed lines."""
        raw = '''ANSWER: The code is below
from aws_cdk import App
app = App()
ANSWER: Done'''

        code = _extract_code(raw)
        assert "from aws_cdk import App" in code
        assert "ANSWER:" not in code

    def test_empty_code_block(self):
        """Empty code block should return empty string."""
        raw = '''```python
```'''

        code = _extract_code(raw)
        assert code == ""

    def test_code_with_explanation_inside_block(self):
        """Code blocks with comments should preserve them."""
        raw = '''```python
# This creates an S3 bucket
from aws_cdk import aws_s3 as s3

# The bucket
bucket = s3.Bucket(self, "MyBucket")
```'''

        code = _extract_code(raw)
        assert "# This creates an S3 bucket" in code
        assert "# The bucket" in code

    def test_nested_backticks_in_code(self):
        """Code containing backticks should be handled."""
        raw = '''```python
doc = """
This is a docstring with `code` inside
"""
```'''

        code = _extract_code(raw)
        assert "docstring with `code` inside" in code


class TestCodeExtractionEdgeCases:
    """Test edge cases and error handling."""

    def test_no_code_block_returns_cleaned_text(self):
        """When no code block found, return cleaned text."""
        raw = '''from aws_cdk import App
app = App()'''

        code = _extract_code(raw)
        assert "from aws_cdk import App" in code

    def test_whitespace_handling(self):
        """Extracted code should be properly dedented."""
        raw = '''```python
    from aws_cdk import App
    app = App()
```'''

        code = _extract_code(raw)
        # Should be dedented
        lines = code.split('\n')
        assert not lines[0].startswith('    ')

    def test_trailing_newlines(self):
        """Trailing newlines should be stripped."""
        raw = '''```python
from aws_cdk import App


```'''

        code = _extract_code(raw)
        assert not code.endswith('\n\n')


class TestRealModelOutputPatterns:
    """Test patterns observed from real model outputs."""

    def test_claude_style_output(self):
        """Claude typically uses ```python with explanation."""
        raw = '''I'll create a CDK stack for an S3 bucket with versioning enabled.

```python
from aws_cdk import App, Stack, RemovalPolicy
from aws_cdk import aws_s3 as s3
from constructs import Construct

class S3BucketStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(
            self, "VersionedBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
        )

app = App()
S3BucketStack(app, "S3BucketStack")
app.synth()
```

This stack creates an S3 bucket with versioning enabled and a DESTROY removal policy for easy cleanup during development.'''

        code = _extract_code(raw)
        assert "class S3BucketStack(Stack):" in code
        assert "versioned=True" in code
        assert "app.synth()" in code
        assert "I'll create" not in code

    def test_gpt_style_output(self):
        """GPT sometimes uses different formatting."""
        raw = '''Here is the CDK code:

```python
#!/usr/bin/env python3
from aws_cdk import App, Stack
from constructs import Construct

class MyStack(Stack):
    pass

if __name__ == "__main__":
    app = App()
    MyStack(app, "MyStack")
    app.synth()
```
'''

        code = _extract_code(raw)
        assert "#!/usr/bin/env python3" in code
        assert 'if __name__ == "__main__":' in code


class TestPatternPriority:
    """Test that patterns are tried in correct order."""

    def test_python_preferred_over_untagged(self):
        """```python should be matched before ``` when both present."""
        raw = '''First block:
```
not python
```

Second block:
```python
from aws_cdk import App
```'''

        code = _extract_code(raw)
        # Should prefer python-tagged block
        assert "from aws_cdk import App" in code
        assert "not python" not in code
