# ruff: noqa: S101, D100, D101, D102, D103
"""Tests for core.utils module."""

from src.core.utils import split_path


class TestSplitPath:
    """Tests for the split_path function."""

    def test_absolute_path_with_multiple_segments(self):
        """Test splitting an absolute path with multiple segments."""
        result = split_path("/electronics/laptops")
        assert result == ["/", "/electronics", "/electronics/laptops"]

    def test_absolute_path_with_single_segment(self):
        """Test splitting an absolute path with a single segment."""
        result = split_path("/electronics")
        assert result == ["/", "/electronics"]

    def test_root_path(self):
        """Test splitting the root path."""
        result = split_path("/")
        assert result == ["/"]

    def test_relative_path_with_multiple_segments(self):
        """Test splitting a relative path with multiple segments."""
        result = split_path("electronics/laptops/gaming")
        assert result == ["electronics", "electronics/laptops", "electronics/laptops/gaming"]

    def test_relative_path_with_single_segment(self):
        """Test splitting a relative path with a single segment."""
        result = split_path("electronics")
        assert result == ["electronics"]

    def test_path_with_current_directory(self):
        """Test splitting a path starting with current directory marker."""
        result = split_path("./electronics/laptops")
        # Path normalizes away the current directory marker
        assert result == ["electronics", "electronics/laptops"]

    def test_path_with_parent_directory(self):
        """Test splitting a path with parent directory markers."""
        result = split_path("../electronics/laptops")
        assert result == ["..", "../electronics", "../electronics/laptops"]

    def test_empty_string(self):
        """Test splitting an empty string."""
        result = split_path("")
        # Path("") has no parts, so accumulate returns an empty list
        assert result == []

    def test_path_with_trailing_slash(self):
        """Test splitting a path with a trailing slash."""
        result = split_path("/electronics/laptops/")
        # Path normalizes trailing slashes, so this should be same as without trailing slash
        assert result == ["/", "/electronics", "/electronics/laptops"]

    def test_deep_nested_path(self):
        """Test splitting a deeply nested path."""
        result = split_path("/a/b/c/d/e")
        assert result == ["/", "/a", "/a/b", "/a/b/c", "/a/b/c/d", "/a/b/c/d/e"]

    def test_relative_deep_nested_path(self):
        """Test splitting a deeply nested relative path."""
        result = split_path("a/b/c/d")
        assert result == ["a", "a/b", "a/b/c", "a/b/c/d"]

    def test_path_with_special_characters(self):
        """Test splitting a path with special characters in names."""
        result = split_path("/products/coffee-beans/premium_blend")
        assert result == [
            "/",
            "/products",
            "/products/coffee-beans",
            "/products/coffee-beans/premium_blend",
        ]
