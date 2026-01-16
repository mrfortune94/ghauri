#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=R,W,E,C

"""
Orbot (Tor) Integration Module for Ghauri Android App

This module provides integration with Orbot (official Tor app for Android)
to route all network traffic through the Tor network.

Features:
- SOCKS5 proxy routing through Orbot
- Fail-closed behavior (block network if Tor disconnects)
- App-level Tor routing (not system-wide)
- Connection verification

Author  : Nasir Khan (r0ot h3x49)
Github  : https://github.com/r0oth3x49
License : MIT

Copyright (c) 2016-2025 Nasir Khan (r0ot h3x49)
"""

import socket
from collections import namedtuple
from urllib.request import ProxyHandler
from urllib.parse import urlparse
import socks  # PySocks library for SOCKS proxy support

# Default Orbot SOCKS5 proxy settings
DEFAULT_ORBOT_HOST = "127.0.0.1"
DEFAULT_ORBOT_PORT = 9050

# Tor connection test endpoints
TOR_CHECK_HOSTS = [
    ("check.torproject.org", 443),
    ("www.torproject.org", 443),
]

# Named tuple for Orbot configuration
OrbotConfig = namedtuple(
    "OrbotConfig",
    [
        "enabled",
        "host",
        "port",
        "fail_closed",
        "verified",
    ]
)


class OrbotConnectionError(Exception):
    """Exception raised when Orbot/Tor connection fails."""
    pass


class OrbotNotRunningError(OrbotConnectionError):
    """Exception raised when Orbot is not running or not accessible."""
    pass


class TorNetworkError(OrbotConnectionError):
    """Exception raised when traffic cannot be routed through Tor."""
    pass


class OrbotManager:
    """
    Manager class for Orbot/Tor integration.
    
    Provides functionality to:
    - Configure SOCKS5 proxy for Orbot
    - Verify Orbot connection
    - Enforce fail-closed behavior
    - Route app traffic through Tor
    """

    def __init__(
        self,
        host=DEFAULT_ORBOT_HOST,
        port=DEFAULT_ORBOT_PORT,
        fail_closed=True,
        enabled=False,
    ):
        """
        Initialize OrbotManager.

        Args:
            host: Orbot SOCKS5 proxy host (default: 127.0.0.1)
            port: Orbot SOCKS5 proxy port (default: 9050)
            fail_closed: If True, block all network access if Tor is unavailable
            enabled: If True, enable Tor routing
        """
        self._host = host
        self._port = port
        self._fail_closed = fail_closed
        self._enabled = enabled
        self._verified = False
        self._original_socket = None

    @property
    def host(self):
        """Get Orbot SOCKS5 proxy host."""
        return self._host

    @host.setter
    def host(self, value):
        """Set Orbot SOCKS5 proxy host."""
        self._host = value
        self._verified = False

    @property
    def port(self):
        """Get Orbot SOCKS5 proxy port."""
        return self._port

    @port.setter
    def port(self, value):
        """Set Orbot SOCKS5 proxy port."""
        self._port = int(value)
        self._verified = False

    @property
    def fail_closed(self):
        """Get fail-closed mode status."""
        return self._fail_closed

    @fail_closed.setter
    def fail_closed(self, value):
        """Set fail-closed mode."""
        self._fail_closed = bool(value)

    @property
    def enabled(self):
        """Get Tor routing enabled status."""
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        """Set Tor routing enabled status."""
        self._enabled = bool(value)
        if not self._enabled:
            self._restore_socket()

    @property
    def verified(self):
        """Get connection verification status."""
        return self._verified

    @property
    def config(self):
        """Get current Orbot configuration as OrbotConfig namedtuple."""
        return OrbotConfig(
            enabled=self._enabled,
            host=self._host,
            port=self._port,
            fail_closed=self._fail_closed,
            verified=self._verified,
        )

    @property
    def socks_proxy_url(self):
        """Get SOCKS5 proxy URL for use with requests library."""
        return f"socks5h://{self._host}:{self._port}"

    @property
    def proxy_dict(self):
        """Get proxy dictionary for use with requests library."""
        if self._enabled:
            proxy_url = self.socks_proxy_url
            return {
                "http": proxy_url,
                "https": proxy_url,
            }
        return {}

    def get_urllib_proxy_handler(self):
        """
        Get ProxyHandler for urllib.
        
        Returns:
            ProxyHandler configured for Orbot SOCKS5 proxy
        """
        if self._enabled:
            proxy_url = self.socks_proxy_url
            return ProxyHandler({
                "http": proxy_url,
                "https": proxy_url,
            })
        return None

    def verify_orbot_running(self):
        """
        Verify that Orbot SOCKS5 proxy is accessible.

        Returns:
            bool: True if Orbot is running and accessible

        Raises:
            OrbotNotRunningError: If Orbot is not running and fail_closed is True
        """
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(5)
            result = test_socket.connect_ex((self._host, self._port))
            test_socket.close()
            
            if result == 0:
                return True
            else:
                if self._fail_closed:
                    raise OrbotNotRunningError(
                        f"Orbot SOCKS5 proxy not accessible at {self._host}:{self._port}. "
                        "Please ensure Orbot is running and configured correctly. "
                        "Network access blocked due to fail-closed mode."
                    )
                return False
        except socket.error as e:
            if self._fail_closed:
                raise OrbotNotRunningError(
                    f"Cannot connect to Orbot at {self._host}:{self._port}: {str(e)}. "
                    "Network access blocked due to fail-closed mode."
                )
            return False

    def verify_tor_connection(self):
        """
        Verify that traffic is actually being routed through Tor.
        
        This performs a connection test through the SOCKS proxy to verify
        that the Tor network is accessible.

        Returns:
            bool: True if Tor connection is verified

        Raises:
            TorNetworkError: If Tor network is not accessible and fail_closed is True
        """
        if not self.verify_orbot_running():
            return False

        try:
            # Create a SOCKS5 socket
            test_socket = socks.socksocket()
            test_socket.set_proxy(socks.SOCKS5, self._host, self._port)
            test_socket.settimeout(10)
            
            # Try to connect to a Tor check endpoint
            for host, port in TOR_CHECK_HOSTS:
                try:
                    test_socket.connect((host, port))
                    test_socket.close()
                    self._verified = True
                    return True
                except Exception:
                    continue
            
            test_socket.close()
            
            if self._fail_closed:
                raise TorNetworkError(
                    "Unable to verify Tor network connection. "
                    "Network access blocked due to fail-closed mode."
                )
            return False
            
        except socks.ProxyConnectionError as e:
            if self._fail_closed:
                raise TorNetworkError(
                    f"Tor proxy connection failed: {str(e)}. "
                    "Network access blocked due to fail-closed mode."
                )
            return False
        except Exception as e:
            if self._fail_closed:
                raise TorNetworkError(
                    f"Tor connection verification failed: {str(e)}. "
                    "Network access blocked due to fail-closed mode."
                )
            return False

    def configure_socket_for_tor(self):
        """
        Configure the default socket to route through Tor.
        
        This patches the socket module to use SOCKS5 proxy for all connections.
        Call restore_socket() to revert to normal behavior.
        """
        if not self._enabled:
            return
        
        if self._fail_closed:
            # Verify Orbot is running before configuring
            self.verify_orbot_running()
        
        # Store original socket for restoration
        if self._original_socket is None:
            self._original_socket = socket.socket

        # Configure PySocks to use Orbot SOCKS5 proxy
        socks.set_default_proxy(socks.SOCKS5, self._host, self._port)
        socket.socket = socks.socksocket

    def _restore_socket(self):
        """Restore the original socket behavior."""
        if self._original_socket is not None:
            socket.socket = self._original_socket
            self._original_socket = None

    def restore_socket(self):
        """
        Restore the original socket behavior.
        
        Call this when you want to disable Tor routing.
        """
        self._restore_socket()

    def get_status(self):
        """
        Get current Orbot/Tor status.

        Returns:
            dict: Status information
        """
        orbot_running = False
        tor_connected = False
        
        try:
            orbot_running = self.verify_orbot_running()
        except OrbotNotRunningError:
            pass
        
        if orbot_running:
            try:
                tor_connected = self.verify_tor_connection()
            except TorNetworkError:
                pass
        
        return {
            "enabled": self._enabled,
            "fail_closed": self._fail_closed,
            "orbot_running": orbot_running,
            "tor_connected": tor_connected,
            "verified": self._verified,
            "host": self._host,
            "port": self._port,
        }

    def ensure_tor_or_fail(self):
        """
        Ensure Tor is available and verified, or raise an exception.
        
        This should be called before any network operation when fail_closed is True.

        Raises:
            OrbotNotRunningError: If Orbot is not running
            TorNetworkError: If Tor network is not accessible
        """
        if not self._enabled:
            return
        
        if self._fail_closed:
            if not self.verify_orbot_running():
                raise OrbotNotRunningError(
                    "Orbot is not running. Network access blocked due to fail-closed mode."
                )
            if not self._verified:
                self.verify_tor_connection()


# Global Orbot manager instance
orbot_manager = OrbotManager()


def is_tor_enabled():
    """Check if Tor routing is enabled."""
    return orbot_manager.enabled


def enable_tor_routing(
    host=DEFAULT_ORBOT_HOST,
    port=DEFAULT_ORBOT_PORT,
    fail_closed=True,
):
    """
    Enable Tor routing through Orbot.

    Args:
        host: Orbot SOCKS5 proxy host
        port: Orbot SOCKS5 proxy port
        fail_closed: If True, block network if Tor unavailable

    Raises:
        OrbotNotRunningError: If Orbot is not running and fail_closed is True
    """
    orbot_manager.host = host
    orbot_manager.port = port
    orbot_manager.fail_closed = fail_closed
    orbot_manager.enabled = True
    
    if fail_closed:
        orbot_manager.verify_orbot_running()


def disable_tor_routing():
    """Disable Tor routing and restore normal socket behavior."""
    orbot_manager.enabled = False
    orbot_manager.restore_socket()


def get_tor_proxy_for_requests():
    """
    Get proxy dictionary for use with requests library.

    Returns:
        dict: Proxy configuration for requests, or empty dict if Tor disabled
    """
    if orbot_manager.enabled:
        orbot_manager.ensure_tor_or_fail()
        return orbot_manager.proxy_dict
    return {}


def get_tor_status():
    """
    Get current Tor/Orbot status.

    Returns:
        dict: Status information
    """
    return orbot_manager.get_status()
