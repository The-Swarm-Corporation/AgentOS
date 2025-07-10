#!/usr/bin/env python3
"""
Test script to verify workspace functionality.
"""

import os
import tempfile

# Import the workspace functionality
from agentos_sdk.workspace import Workspace, get_workspace


def test_workspace_creation():
    """Test basic workspace creation and directory structure."""
    print("🧪 Testing workspace creation...")

    # Test with custom path
    with tempfile.TemporaryDirectory() as temp_dir:
        custom_workspace = Workspace(workspace_path=temp_dir)

        # Check main directory exists
        assert os.path.exists(custom_workspace.get_workspace_path())

        # Check subdirectories exist
        subdirs = [
            "videos",
            "audio",
            "images",
            "documents",
            "generated",
            "temp",
        ]
        for subdir in subdirs:
            subdir_path = os.path.join(
                custom_workspace.get_workspace_path(), subdir
            )
            assert os.path.exists(
                subdir_path
            ), f"Subdir {subdir} not created"

        print("✅ Workspace creation test passed!")


def test_environment_variable_support():
    """Test workspace creation with environment variables."""
    print("🧪 Testing environment variable support...")

    # Test with WORKSPACE_DIR env var
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["WORKSPACE_DIR"] = temp_dir

        workspace = Workspace()
        expected_path = temp_dir
        actual_path = workspace.get_workspace_path()

        assert (
            actual_path == expected_path
        ), f"Expected {expected_path}, got {actual_path}"

        # Clean up
        del os.environ["WORKSPACE_DIR"]

    # Test with ARTIFACTS_DIR env var
    with tempfile.TemporaryDirectory() as temp_dir:
        os.environ["ARTIFACTS_DIR"] = temp_dir

        workspace = Workspace()
        expected_path = temp_dir
        actual_path = workspace.get_workspace_path()

        assert (
            actual_path == expected_path
        ), f"Expected {expected_path}, got {actual_path}"

        # Clean up
        del os.environ["ARTIFACTS_DIR"]

    print("✅ Environment variable support test passed!")


def test_file_path_generation():
    """Test file path generation for different file types."""
    print("🧪 Testing file path generation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        workspace = Workspace(workspace_path=temp_dir)

        # Test different file types
        test_cases = [
            ("test.mp4", "videos"),
            ("test.mp3", "audio"),
            ("test.jpg", "images"),
            ("test.pdf", "documents"),
            ("test.txt", "generated"),
            ("temp.log", "temp"),
        ]

        for filename, file_type in test_cases:
            file_path = workspace.get_file_path(filename, file_type)
            expected_dir = os.path.join(temp_dir, file_type)
            expected_path = os.path.join(expected_dir, filename)

            assert (
                file_path == expected_path
            ), f"Expected {expected_path}, got {file_path}"

        print("✅ File path generation test passed!")


def test_global_workspace():
    """Test global workspace functionality."""
    print("🧪 Testing global workspace functionality...")

    # Get global workspace
    workspace1 = get_workspace()
    workspace2 = get_workspace()

    # Should be the same instance
    assert (
        workspace1 is workspace2
    ), "Global workspace should be singleton"

    # Should have valid paths
    assert os.path.exists(workspace1.get_workspace_path())

    print("✅ Global workspace test passed!")


def test_mock_file_generation():
    """Test mock file generation to workspace directories."""
    print("🧪 Testing mock file generation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Set environment variable to use temp directory
        os.environ["WORKSPACE_DIR"] = temp_dir

        workspace = get_workspace()

        # Test creating mock files in each directory
        test_files = {
            "videos": "test_video.mp4",
            "audio": "test_audio.mp3",
            "images": "test_image.jpg",
            "documents": "test_doc.pdf",
            "generated": "test_output.txt",
            "temp": "test_temp.log",
        }

        for file_type, filename in test_files.items():
            file_path = workspace.get_file_path(filename, file_type)

            # Create mock file
            with open(file_path, "w") as f:
                f.write(f"Test content for {filename}")

            # Verify file exists
            assert os.path.exists(
                file_path
            ), f"File {file_path} was not created"

            # Verify content
            with open(file_path, "r") as f:
                content = f.read()
                assert f"Test content for {filename}" in content

        # Clean up environment variable
        del os.environ["WORKSPACE_DIR"]

        print("✅ Mock file generation test passed!")


def main():
    """Run all tests."""
    print("🚀 Starting workspace functionality tests...\n")

    try:
        test_workspace_creation()
        test_environment_variable_support()
        test_file_path_generation()
        test_global_workspace()
        test_mock_file_generation()

        print("\n🎉 All workspace tests passed!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()
