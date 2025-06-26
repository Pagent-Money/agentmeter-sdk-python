# Publishing Guide

Guide for publishing AgentMeter Python SDK to PyPI

## Steps
1. Build: python -m build
2. Test: twine upload --repository testpypi dist/*
3. Publish: twine upload dist/*
