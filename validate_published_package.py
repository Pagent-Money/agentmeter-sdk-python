#!/usr/bin/env python3
"""
Standalone validation script for the published agentmeter package.

This script can be run independently to validate that the published 
package from PyPI works correctly. It's designed to be run in a clean 
environment after installing the package via `pip install agentmeter`.

Usage:
    # In a clean environment
    pip install agentmeter
    python validate_published_package.py
"""

import sys
import traceback
from typing import List, Tuple, Callable


class PackageValidator:
    """Validates the published agentmeter package functionality."""
    
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results: List[Tuple[str, bool, str]] = []
    
    def run_test(self, test_name: str, test_func: Callable) -> bool:
        """Run a single test and track results."""
        try:
            test_func()
            self.tests_passed += 1
            self.test_results.append((test_name, True, ""))
            print(f"✅ {test_name}")
            return True
        except Exception as e:
            self.tests_failed += 1
            error_msg = f"{type(e).__name__}: {str(e)}"
            self.test_results.append((test_name, False, error_msg))
            print(f"❌ {test_name}: {error_msg}")
            return False
    
    def test_basic_import(self):
        """Test basic package import."""
        import agentmeter
        assert agentmeter is not None
        assert hasattr(agentmeter, '__version__')
    
    def test_version_format(self):
        """Test package version format."""
        import agentmeter
        version = agentmeter.__version__
        parts = version.split('.')
        assert len(parts) >= 2
        assert int(parts[0]) >= 0
        assert int(parts[1]) >= 2  # Should be 0.2.0+
    
    def test_core_classes(self):
        """Test core classes are available."""
        from agentmeter import (
            AgentMeterClient,
            AgentMeterTracker,
            AgentMeterConfig,
            AgentMeterError,
            RateLimitError
        )
        
        # Test client instantiation
        client = AgentMeterClient(
            api_key="test_key",
            project_id="test_project",
            agent_id="test_agent"
        )
        assert client.api_key == "test_key"
        
        # Test tracker instantiation
        tracker = AgentMeterTracker(
            client=client,
            project_id="test_project",
            agent_id="test_agent"
        )
        assert tracker.client == client
    
    def test_payment_models(self):
        """Test payment model classes."""
        from agentmeter import (
            PaymentType,
            APIRequestPayEvent,
            TokenBasedPayEvent,
            InstantPayEvent
        )
        
        # Test PaymentType enum
        assert PaymentType.API_REQUEST_PAY == "api_request_pay"
        assert PaymentType.TOKEN_BASED_PAY == "token_based_pay"
        assert PaymentType.INSTANT_PAY == "instant_pay"
        
        # Test event creation
        api_event = APIRequestPayEvent(
            project_id="test",
            agent_id="test",
            user_id="test",
            api_calls=1,
            unit_price=0.001
        )
        assert api_event.api_calls == 1
        
        token_event = TokenBasedPayEvent(
            project_id="test",
            agent_id="test",
            user_id="test",
            tokens_in=100,
            tokens_out=50,
            input_token_price=0.000004,
            output_token_price=0.000001
        )
        assert token_event.tokens_in == 100
        
        instant_event = InstantPayEvent(
            project_id="test",
            agent_id="test",
            user_id="test",
            amount=5.99,
            description="Test"
        )
        assert instant_event.amount == 5.99
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        from agentmeter import (
            create_client,
            quick_api_request_pay,
            quick_token_based_pay,
            quick_instant_pay
        )
        
        # Test create_client
        client = create_client(
            api_key="test_key",
            project_id="test_project",
            agent_id="test_agent"
        )
        assert client.api_key == "test_key"
        
        # Check functions are callable
        assert callable(quick_api_request_pay)
        assert callable(quick_token_based_pay)
        assert callable(quick_instant_pay)
    
    def test_decorators(self):
        """Test decorator functions."""
        from agentmeter import (
            meter_api_request_pay,
            meter_token_based_pay,
            meter_instant_pay,
            meter_function,
            meter_agent,
            AgentMeterClient
        )
        
        client = AgentMeterClient(
            api_key="test_key",
            project_id="test_project",
            agent_id="test_agent"
        )
        
        # Test decorator application (without calling)
        @meter_api_request_pay(client, unit_price=0.1)
        def test_func(query: str, user_id: str):
            return f"result: {query}"
        
        assert hasattr(test_func, '__wrapped__')
        assert test_func.__name__ == "test_func"
    
    def test_context_managers(self):
        """Test context manager functions."""
        from agentmeter import (
            track_api_request_pay,
            track_token_based_pay,
            track_instant_pay,
            track_usage,
            AgentMeterClient
        )
        
        client = AgentMeterClient(
            api_key="test_key",
            project_id="test_project",
            agent_id="test_agent"
        )
        
        # Test context manager creation (without entering context)
        api_cm = track_api_request_pay(client, "proj", "agent", unit_price=0.1)
        token_cm = track_token_based_pay(client, "proj", "agent")
        instant_cm = track_instant_pay(client, "proj", "agent", amount=1.0)
        generic_cm = track_usage(client, "proj", "agent")
        
        # All should be context managers
        assert hasattr(api_cm, '__enter__')
        assert hasattr(token_cm, '__enter__')
        assert hasattr(instant_cm, '__enter__')
        assert hasattr(generic_cm, '__enter__')
    
    def test_langchain_integration(self):
        """Test LangChain integration (optional)."""
        try:
            from agentmeter import LangChainAgentMeterCallback
            assert LangChainAgentMeterCallback is not None
        except ImportError:
            # LangChain is optional dependency
            print("ℹ️  LangChain integration skipped (optional dependency)")
    
    def test_cli_entry_point(self):
        """Test CLI entry point."""
        import agentmeter.cli
        assert hasattr(agentmeter.cli, 'main')
        assert callable(agentmeter.cli.main)
    
    def test_dependencies(self):
        """Test required dependencies are available."""
        import httpx
        import pydantic
        
        # Basic functionality check
        assert httpx is not None
        assert pydantic is not None
        
        # Check versions are compatible
        import pydantic
        # Get version as string, convert to tuple for comparison
        version_str = pydantic.VERSION
        if isinstance(version_str, str):
            version_parts = tuple(map(int, version_str.split('.')))
        else:
            version_parts = version_str
        assert version_parts >= (2, 0, 0), f"Pydantic version too old: {version_str}"
    
    def test_error_handling(self):
        """Test error classes work correctly."""
        from agentmeter import AgentMeterError, RateLimitError
        
        # Test error creation and inheritance
        base_error = AgentMeterError("Base error")
        assert str(base_error) == "Base error"
        assert isinstance(base_error, Exception)
        
        rate_error = RateLimitError("Rate limit error")
        assert str(rate_error) == "Rate limit error"
        assert isinstance(rate_error, AgentMeterError)
        assert isinstance(rate_error, Exception)
    
    def test_common_usage_patterns(self):
        """Test common usage patterns work."""
        # Test typical import pattern
        from agentmeter import (
            create_client,
            meter_api_request_pay,
            track_token_based_pay,
            PaymentType,
            APIRequestPayEvent
        )
        
        # Test client creation
        client = create_client(
            api_key="sk-test-12345",
            project_id="proj_abc123",
            agent_id="agent_xyz789"
        )
        
        # Test event creation with realistic data
        event = APIRequestPayEvent(
            project_id="proj_abc123",
            agent_id="agent_xyz789",
            user_id="user_123",
            api_calls=1,
            unit_price=0.01,
            metadata={"endpoint": "/api/search", "method": "POST"}
        )
        
        assert event.project_id == "proj_abc123"
        assert event.metadata["endpoint"] == "/api/search"
    
    def run_all_tests(self):
        """Run all validation tests."""
        print("🔍 AgentMeter Package Validation")
        print("=" * 50)
        
        tests = [
            ("Basic Import", self.test_basic_import),
            ("Version Format", self.test_version_format),
            ("Core Classes", self.test_core_classes),
            ("Payment Models", self.test_payment_models),
            ("Convenience Functions", self.test_convenience_functions),
            ("Decorators", self.test_decorators),
            ("Context Managers", self.test_context_managers),
            ("LangChain Integration", self.test_langchain_integration),
            ("CLI Entry Point", self.test_cli_entry_point),
            ("Dependencies", self.test_dependencies),
            ("Error Handling", self.test_error_handling),
            ("Common Usage Patterns", self.test_common_usage_patterns),
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Print summary
        print("\n" + "=" * 50)
        print(f"📊 Test Summary:")
        print(f"   ✅ Passed: {self.tests_passed}")
        print(f"   ❌ Failed: {self.tests_failed}")
        print(f"   📈 Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed)) * 100:.1f}%")
        
        if self.tests_failed > 0:
            print(f"\n❌ Failed Tests:")
            for test_name, passed, error in self.test_results:
                if not passed:
                    print(f"   • {test_name}: {error}")
            return False
        else:
            print(f"\n🎉 All tests passed! The agentmeter package is working correctly.")
            return True


def main():
    """Main validation function."""
    print("🚀 AgentMeter Published Package Validator")
    print("This script validates the agentmeter package installed from PyPI")
    print()
    
    # Check if package is installed
    try:
        import agentmeter
        print(f"📦 Found agentmeter package (version {agentmeter.__version__})")
        package_path = agentmeter.__file__
        print(f"📍 Package location: {package_path}")
        
        if 'site-packages' not in package_path and 'dist-packages' not in package_path:
            print("⚠️  Warning: Package not installed in site-packages")
            print("   This might be a development installation")
        
    except ImportError:
        print("❌ agentmeter package not found!")
        print()
        print("💡 Please install the package first:")
        print("   pip install agentmeter")
        print()
        print("   Or if testing from source:")
        print("   pip install -e .")
        return 1
    
    print()
    
    # Run validation
    validator = PackageValidator()
    success = validator.run_all_tests()
    
    if success:
        print("\n✅ Validation completed successfully!")
        print("The agentmeter package is ready for production use.")
        return 0
    else:
        print("\n❌ Validation failed!")
        print("Some issues were found with the package installation.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
