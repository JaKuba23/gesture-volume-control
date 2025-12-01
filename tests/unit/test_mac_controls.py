"""Unit tests for mac_controls module."""

import subprocess
from unittest.mock import Mock, patch

import pytest

from motus.mac_controls import (
    UnsupportedPlatformError,
    VolumeControlError,
    get_volume,
    set_volume,
)


class TestSetVolume:
    """Tests for set_volume function."""

    def test_set_volume_success(self, mock_platform_darwin, mock_subprocess_run):
        """Test successful volume setting on macOS."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            set_volume(50)

        mock_subprocess_run.assert_called_once()
        args = mock_subprocess_run.call_args[0][0]
        assert args[0] == "osascript"
        assert "50" in args[2]

    def test_set_volume_clamps_to_zero(self, mock_platform_darwin, mock_subprocess_run):
        """Test that negative volume is clamped to 0."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            set_volume(-10)

        args = mock_subprocess_run.call_args[0][0]
        assert "0" in args[2]

    def test_set_volume_clamps_to_hundred(
        self, mock_platform_darwin, mock_subprocess_run
    ):
        """Test that volume over 100 is clamped to 100."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            set_volume(150)

        args = mock_subprocess_run.call_args[0][0]
        assert "100" in args[2]

    def test_set_volume_non_darwin_logs_warning(self, mock_platform_linux, caplog):
        """Test that non-macOS platform logs warning and returns."""
        set_volume(50)
        assert "only supported on macOS" in caplog.text

    def test_set_volume_missing_osascript_raises(self, mock_platform_darwin):
        """Test that missing osascript raises VolumeControlError."""
        with patch("shutil.which", return_value=None):
            with pytest.raises(VolumeControlError, match="osascript not available"):
                set_volume(50)

    def test_set_volume_subprocess_error_raises(self, mock_platform_darwin):
        """Test that subprocess error raises VolumeControlError."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = subprocess.CalledProcessError(
                    1, "osascript", stderr=b"error"
                )
                with pytest.raises(VolumeControlError, match="osascript failed"):
                    set_volume(50)

    def test_set_volume_timeout_raises(self, mock_platform_darwin):
        """Test that timeout raises VolumeControlError."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            with patch("subprocess.run") as mock_run:
                mock_run.side_effect = subprocess.TimeoutExpired("osascript", 5)
                with pytest.raises(VolumeControlError, match="timed out"):
                    set_volume(50)


class TestGetVolume:
    """Tests for get_volume function."""

    def test_get_volume_success(self, mock_platform_darwin):
        """Test successful volume query on macOS."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value.stdout = "75\n"
                mock_run.return_value.returncode = 0

                result = get_volume()
                assert result == 75

    def test_get_volume_non_darwin_returns_none(self, mock_platform_linux):
        """Test that non-macOS platform returns None."""
        result = get_volume()
        assert result is None

    def test_get_volume_missing_osascript_raises(self, mock_platform_darwin):
        """Test that missing osascript raises VolumeControlError."""
        with patch("shutil.which", return_value=None):
            with pytest.raises(VolumeControlError):
                get_volume()

    def test_get_volume_invalid_output_raises(self, mock_platform_darwin):
        """Test that invalid output raises VolumeControlError."""
        with patch("shutil.which", return_value="/usr/bin/osascript"):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value.stdout = "invalid"

                with pytest.raises(VolumeControlError):
                    get_volume()
