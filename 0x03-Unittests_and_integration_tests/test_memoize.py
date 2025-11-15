#!/usr/bin/env python3
"""
Tests for memoize decorator.
"""

import unittest
from unittest.mock import patch
from utils import memoize


class TestMemoize(unittest.TestCase):
    """Tests for memoization."""

    def test_memoize(self):
        """Test memoization caches returned value."""

        class TestClass:
            """Helper class for memoize test."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            first = obj.a_property
            second = obj.a_property

            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()
