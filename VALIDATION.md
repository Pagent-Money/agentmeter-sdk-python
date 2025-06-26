# AgentMeter Package Validation

This document describes how to validate the published AgentMeter package to ensure it works correctly for end users.

## Overview

We provide two validation methods:
1. **Comprehensive Test Suite** - Full pytest-based validation
2. **Standalone Validator** - Quick validation script

## Quick Validation (Recommended)

After publishing to PyPI, run this quick validation:

```bash
# Install the published package
pip install agentmeter

# Run standalone validation
python validate_published_package.py
```

This will output a comprehensive checklist showing what works and what doesn't.

## Comprehensive Test Suite

For detailed testing with pytest:

```bash
# Install the published package
pip install agentmeter

# Install testing dependencies
pip install pytest

# Run the comprehensive test suite
python -m pytest tests/test_published_package.py -v
```

## What Gets Validated

### Core Functionality
- ✅ Package import and version
- ✅ Core classes (AgentMeterClient, AgentMeterTracker, etc.)
- ✅ Payment models (APIRequestPayEvent, TokenBasedPayEvent, InstantPayEvent)
- ✅ Convenience functions (create_client, quick_* functions)
- ✅ Decorators (meter_api_request_pay, meter_token_based_pay, etc.)
- ✅ Context managers (track_* functions)
- ✅ Error classes and exception handling

### Integration Features
- ✅ LangChain integration (optional)
- ✅ CLI entry point
- ✅ Type hints (py.typed)
- ✅ Dependency management

### User Experience
- ✅ Common import patterns
- ✅ Realistic usage scenarios
- ✅ Package installation validation
- ✅ Python version compatibility

## Clean Environment Testing

For the most accurate validation, test in a clean environment:

```bash
# Create a clean virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install only the published package
pip install agentmeter

# Run validation
python validate_published_package.py
```

## Expected Output

Successful validation should show:

```
🔍 AgentMeter Package Validation
==================================================
✅ Basic Import
✅ Version Format
✅ Core Classes
✅ Payment Models
✅ Convenience Functions
✅ Decorators
✅ Context Managers
ℹ️  LangChain Integration skipped (optional dependency)
✅ CLI Entry Point
✅ Dependencies
✅ Error Handling
✅ Common Usage Patterns

==================================================
📊 Test Summary:
   ✅ Passed: 11
   ❌ Failed: 0
   📈 Success Rate: 100.0%

🎉 All tests passed! The agentmeter package is working correctly.
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
❌ Failed to import package: No module named 'agentmeter'
```
Solution: Make sure the package is installed: `pip install agentmeter`

**Version Issues:**
```bash
❌ Version Format: Version should be 0.2.0+, got 0.1.0
```
Solution: Check you have the latest version: `pip install --upgrade agentmeter`

**Dependency Issues:**
```bash
❌ Dependencies: Required dependency not available: httpx
```
Solution: Dependencies should install automatically. Try: `pip install --force-reinstall agentmeter`

### Development vs Published Package

If you're testing during development:

```bash
# Test local development version
pip install -e .
python validate_published_package.py

# Test published version (after uploading to PyPI)
pip uninstall agentmeter
pip install agentmeter
python validate_published_package.py
```

## CI/CD Integration

You can integrate this validation into your CI/CD pipeline:

```yaml
# Example GitHub Actions step
- name: Validate Published Package
  run: |
    pip install agentmeter
    python validate_published_package.py
```

## Publishing Checklist

Before publishing to PyPI, ensure:

1. ✅ All local tests pass
2. ✅ Package builds successfully (`python -m build`)
3. ✅ Package passes twine check (`twine check dist/*`)
4. ✅ Test on TestPyPI first
5. ✅ Validate published package with this script
6. ✅ Update documentation with new version

## Support

If validation fails:
1. Check the error messages for specific issues
2. Verify all dependencies are correctly specified
3. Test in a clean environment
4. Check the package installation location
5. Report issues at: https://github.com/Pagent-Money/agentmeter-sdk-python/issues 