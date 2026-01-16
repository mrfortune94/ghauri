#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghauri Android App - Kivy-based GUI for SQL Injection Testing

Author  : Nasir Khan (r0ot h3x49)
License : MIT
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window
from kivy.clock import Clock
import threading
import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr

# Import Ghauri modules
GHAURI_IMPORT_ERROR = None
ORBOT_IMPORT_ERROR = None
try:
    import ghauri
    from ghauri.logger.colored_logger import logger
except ImportError as e:
    GHAURI_IMPORT_ERROR = str(e)
    ghauri = None

# Import Orbot integration module
try:
    from ghauri.common.orbot import (
        orbot_manager,
        enable_tor_routing,
        disable_tor_routing,
        get_tor_status,
        get_tor_proxy_for_requests,
        OrbotNotRunningError,
        TorNetworkError,
        DEFAULT_ORBOT_HOST,
        DEFAULT_ORBOT_PORT,
    )
except ImportError as e:
    ORBOT_IMPORT_ERROR = str(e)
    orbot_manager = None


class GhauriApp(App):
    """Main Ghauri Kivy Application"""
    
    def build(self):
        """Build the application UI"""
        self.title = "Ghauri - SQL Injection Tool"
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title_label = Label(
            text='[b]Ghauri SQL Injection Tool[/b]',
            markup=True,
            size_hint=(1, 0.08),
            color=(0.2, 0.4, 0.8, 1),
            font_size='20sp'
        )
        main_layout.add_widget(title_label)
        
        # Create tabbed interface
        tab_panel = TabbedPanel(do_default_tab=False, tab_width=150)
        
        # Basic Tab
        basic_tab = TabbedPanelItem(text='Basic')
        basic_tab.add_widget(self.create_basic_tab())
        tab_panel.add_widget(basic_tab)
        
        # Advanced Tab
        advanced_tab = TabbedPanelItem(text='Advanced')
        advanced_tab.add_widget(self.create_advanced_tab())
        tab_panel.add_widget(advanced_tab)
        
        # Results Tab
        results_tab = TabbedPanelItem(text='Results')
        results_tab.add_widget(self.create_results_tab())
        tab_panel.add_widget(results_tab)
        
        # Tor Settings Tab
        tor_tab = TabbedPanelItem(text='Tor')
        tor_tab.add_widget(self.create_tor_tab())
        tab_panel.add_widget(tor_tab)
        
        main_layout.add_widget(tab_panel)
        
        return main_layout
    
    def create_basic_tab(self):
        """Create the basic configuration tab"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ScrollView for scrollable content
        scroll = ScrollView(size_hint=(1, 1))
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Target URL
        url_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        url_layout.add_widget(Label(text='Target URL:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.url_input = TextInput(
            hint_text='http://example.com/vuln.php?id=1',
            multiline=False,
            size_hint_x=0.7
        )
        url_layout.add_widget(self.url_input)
        scroll_layout.add_widget(url_layout)
        
        # POST Data
        data_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        data_layout.add_widget(Label(text='POST Data:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.data_input = TextInput(
            hint_text='id=1&name=test (optional)',
            multiline=False,
            size_hint_x=0.7
        )
        data_layout.add_widget(self.data_input)
        scroll_layout.add_widget(data_layout)
        
        # Cookie
        cookie_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        cookie_layout.add_widget(Label(text='Cookie:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.cookie_input = TextInput(
            hint_text='PHPSESSID=abc123 (optional)',
            multiline=False,
            size_hint_x=0.7
        )
        cookie_layout.add_widget(self.cookie_input)
        scroll_layout.add_widget(cookie_layout)
        
        # DBMS Selection
        dbms_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        dbms_layout.add_widget(Label(text='DBMS:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.dbms_spinner = Spinner(
            text='Auto Detect',
            values=('Auto Detect', 'MySQL', 'PostgreSQL', 'Microsoft SQL Server', 'Oracle', 'Microsoft Access'),
            size_hint_x=0.7
        )
        dbms_layout.add_widget(self.dbms_spinner)
        scroll_layout.add_widget(dbms_layout)
        
        # Technique Selection
        tech_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        tech_layout.add_widget(Label(text='Technique:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.tech_spinner = Spinner(
            text='BEST',
            values=('BEST', 'B', 'E', 'T', 'S'),
            size_hint_x=0.7
        )
        tech_layout.add_widget(self.tech_spinner)
        scroll_layout.add_widget(tech_layout)
        
        # Action Selection
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        action_layout.add_widget(Label(text='Action:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.action_spinner = Spinner(
            text='Test Injection',
            values=('Test Injection', 'Get Banner', 'Get Current User', 'Get Current DB', 
                   'Get Hostname', 'List Databases', 'List Tables', 'Dump Data'),
            size_hint_x=0.7
        )
        self.action_spinner.bind(text=self.on_action_change)
        action_layout.add_widget(self.action_spinner)
        scroll_layout.add_widget(action_layout)
        
        # Database name (conditional)
        self.db_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=0)
        self.db_layout.add_widget(Label(text='Database:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.db_input = TextInput(hint_text='database_name', multiline=False, size_hint_x=0.7)
        self.db_layout.add_widget(self.db_input)
        scroll_layout.add_widget(self.db_layout)
        
        # Table name (conditional)
        self.table_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=0)
        self.table_layout.add_widget(Label(text='Table:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.table_input = TextInput(hint_text='table_name', multiline=False, size_hint_x=0.7)
        self.table_layout.add_widget(self.table_input)
        scroll_layout.add_widget(self.table_layout)
        
        # Columns (conditional)
        self.cols_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=0)
        self.cols_layout.add_widget(Label(text='Columns:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.cols_input = TextInput(hint_text='col1,col2 (optional)', multiline=False, size_hint_x=0.7)
        self.cols_layout.add_widget(self.cols_input)
        scroll_layout.add_widget(self.cols_layout)
        
        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)
        
        # Run button
        self.run_button = Button(
            text='Run Scan',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='18sp'
        )
        self.run_button.bind(on_press=self.run_scan)
        layout.add_widget(self.run_button)
        
        return layout
    
    def create_advanced_tab(self):
        """Create the advanced options tab"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # User Agent
        ua_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        ua_layout.add_widget(Label(text='User-Agent:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.ua_input = TextInput(hint_text='Custom User-Agent (optional)', multiline=False, size_hint_x=0.7)
        ua_layout.add_widget(self.ua_input)
        scroll_layout.add_widget(ua_layout)
        
        # Proxy
        proxy_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        proxy_layout.add_widget(Label(text='Proxy:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.proxy_input = TextInput(hint_text='http://127.0.0.1:8080 (optional)', multiline=False, size_hint_x=0.7)
        proxy_layout.add_widget(self.proxy_input)
        scroll_layout.add_widget(proxy_layout)
        
        # Timeout
        timeout_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        timeout_layout.add_widget(Label(text='Timeout (sec):', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.timeout_input = TextInput(text='30', multiline=False, size_hint_x=0.7, input_filter='int')
        timeout_layout.add_widget(self.timeout_input)
        scroll_layout.add_widget(timeout_layout)
        
        # Delay
        delay_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        delay_layout.add_widget(Label(text='Delay (sec):', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.delay_input = TextInput(text='0', multiline=False, size_hint_x=0.7, input_filter='int')
        delay_layout.add_widget(self.delay_input)
        scroll_layout.add_widget(delay_layout)
        
        # Level
        level_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        level_layout.add_widget(Label(text='Level (1-3):', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.level_spinner = Spinner(text='1', values=('1', '2', '3'), size_hint_x=0.7)
        level_layout.add_widget(self.level_spinner)
        scroll_layout.add_widget(level_layout)
        
        # Threads
        threads_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        threads_layout.add_widget(Label(text='Threads:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.threads_input = TextInput(text='1', multiline=False, size_hint_x=0.7, input_filter='int')
        threads_layout.add_widget(self.threads_input)
        scroll_layout.add_widget(threads_layout)
        
        # Batch mode
        batch_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        batch_layout.add_widget(Label(text='Batch Mode:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.batch_checkbox = CheckBox(active=True, size_hint_x=0.7)
        batch_layout.add_widget(self.batch_checkbox)
        scroll_layout.add_widget(batch_layout)
        
        # Random Agent
        random_agent_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        random_agent_layout.add_widget(Label(text='Random Agent:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.random_agent_checkbox = CheckBox(active=False, size_hint_x=0.7)
        random_agent_layout.add_widget(self.random_agent_checkbox)
        scroll_layout.add_widget(random_agent_layout)
        
        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)
        
        return layout
    
    def create_results_tab(self):
        """Create the results display tab"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Results output
        self.results_output = TextInput(
            text='Results will appear here...',
            readonly=True,
            multiline=True,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='12sp'
        )
        layout.add_widget(self.results_output)
        
        # Clear button
        clear_btn = Button(
            text='Clear Results',
            size_hint=(1, 0.1),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        clear_btn.bind(on_press=lambda x: setattr(self.results_output, 'text', ''))
        layout.add_widget(clear_btn)
        
        return layout
    
    def create_tor_tab(self):
        """Create the Tor/Orbot settings tab"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))
        
        # Tor Settings Header
        header_label = Label(
            text='[b]Orbot / Tor Settings[/b]',
            markup=True,
            size_hint_y=None,
            height=40,
            color=(0.2, 0.4, 0.8, 1),
            font_size='16sp'
        )
        scroll_layout.add_widget(header_label)
        
        # Info text
        info_label = Label(
            text='Route traffic through Orbot (official Tor app) for anonymity.\n'
                 'Ensure Orbot is installed and running before enabling.',
            size_hint_y=None,
            height=60,
            color=(0.3, 0.3, 0.3, 1),
            font_size='12sp',
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        info_label.bind(size=lambda *x: setattr(info_label, 'text_size', (info_label.width, None)))
        scroll_layout.add_widget(info_label)
        
        # Enable Tor Routing
        tor_enable_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        tor_enable_layout.add_widget(Label(text='Enable Tor Routing:', size_hint_x=0.5, color=(0, 0, 0, 1)))
        self.tor_enabled_checkbox = CheckBox(active=False, size_hint_x=0.5)
        self.tor_enabled_checkbox.bind(active=self.on_tor_toggle)
        tor_enable_layout.add_widget(self.tor_enabled_checkbox)
        scroll_layout.add_widget(tor_enable_layout)
        
        # Fail-Closed Mode
        fail_closed_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        fail_closed_layout.add_widget(Label(text='Fail-Closed Mode:', size_hint_x=0.5, color=(0, 0, 0, 1)))
        self.fail_closed_checkbox = CheckBox(active=True, size_hint_x=0.5)
        fail_closed_layout.add_widget(self.fail_closed_checkbox)
        scroll_layout.add_widget(fail_closed_layout)
        
        # Fail-closed info
        fail_info_label = Label(
            text='(Block network if Tor disconnects)',
            size_hint_y=None,
            height=25,
            color=(0.5, 0.5, 0.5, 1),
            font_size='11sp'
        )
        scroll_layout.add_widget(fail_info_label)
        
        # SOCKS Host
        host_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        host_layout.add_widget(Label(text='SOCKS Host:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.tor_host_input = TextInput(
            text='127.0.0.1',
            multiline=False,
            size_hint_x=0.7
        )
        host_layout.add_widget(self.tor_host_input)
        scroll_layout.add_widget(host_layout)
        
        # SOCKS Port
        port_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        port_layout.add_widget(Label(text='SOCKS Port:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.tor_port_input = TextInput(
            text='9050',
            multiline=False,
            size_hint_x=0.7,
            input_filter='int'
        )
        port_layout.add_widget(self.tor_port_input)
        scroll_layout.add_widget(port_layout)
        
        # Status indicator
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        status_layout.add_widget(Label(text='Status:', size_hint_x=0.3, color=(0, 0, 0, 1)))
        self.tor_status_label = Label(
            text='Disabled',
            size_hint_x=0.7,
            color=(0.5, 0.5, 0.5, 1),
            halign='left'
        )
        self.tor_status_label.bind(size=lambda *x: setattr(self.tor_status_label, 'text_size', (self.tor_status_label.width, None)))
        status_layout.add_widget(self.tor_status_label)
        scroll_layout.add_widget(status_layout)
        
        scroll.add_widget(scroll_layout)
        layout.add_widget(scroll)
        
        # Test Connection button
        test_btn = Button(
            text='Test Tor Connection',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.5, 0.7, 1),
            color=(1, 1, 1, 1)
        )
        test_btn.bind(on_press=self.test_tor_connection)
        layout.add_widget(test_btn)
        
        # Save Settings button
        save_btn = Button(
            text='Save Tor Settings',
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.save_tor_settings)
        layout.add_widget(save_btn)
        
        return layout
    
    def on_tor_toggle(self, checkbox, value):
        """Handle Tor routing toggle."""
        if orbot_manager is None:
            self.update_tor_status("Error: Orbot module not available", error=True)
            checkbox.active = False
            return
        
        if value:
            self.update_tor_status("Enabled (not verified)", warning=True)
        else:
            self.update_tor_status("Disabled")
            disable_tor_routing()
    
    def update_tor_status(self, text, error=False, warning=False, success=False):
        """Update Tor status label (thread-safe)."""
        def update(dt):
            self.tor_status_label.text = text
            if error:
                self.tor_status_label.color = (0.8, 0.2, 0.2, 1)
            elif warning:
                self.tor_status_label.color = (0.8, 0.6, 0.2, 1)
            elif success:
                self.tor_status_label.color = (0.2, 0.7, 0.2, 1)
            else:
                self.tor_status_label.color = (0.5, 0.5, 0.5, 1)
        Clock.schedule_once(update)
    
    def test_tor_connection(self, instance):
        """Test Tor/Orbot connection."""
        if orbot_manager is None:
            self.update_tor_status("Error: Orbot module not available", error=True)
            self.append_to_results("\n[TOR] Error: Orbot module not loaded. Install PySocks.")
            return
        
        # Run test in background thread
        thread = threading.Thread(target=self._test_tor_thread)
        thread.daemon = True
        thread.start()
    
    def _test_tor_thread(self):
        """Test Tor connection in background thread."""
        try:
            host = self.tor_host_input.text.strip() or "127.0.0.1"
            port_text = self.tor_port_input.text.strip() or "9050"
            
            try:
                port = int(port_text)
                if port < 1 or port > 65535:
                    raise ValueError("Port out of range")
            except ValueError:
                self.update_tor_status("Invalid port number", error=True)
                self.append_to_results(f"\n[TOR] Error: Invalid port '{port_text}'. Port must be between 1-65535.")
                return
            
            self.update_tor_status("Testing connection...", warning=True)
            self.append_to_results(f"\n[TOR] Testing Orbot connection at {host}:{port}...")
            
            # Configure orbot manager for testing
            orbot_manager.host = host
            orbot_manager.port = port
            orbot_manager.fail_closed = False  # Don't fail during test
            
            # Test Orbot proxy
            if orbot_manager.verify_orbot_running():
                self.append_to_results("[TOR] Orbot SOCKS5 proxy is accessible!")
                
                # Test Tor network connection
                if orbot_manager.verify_tor_connection():
                    self.update_tor_status("Connected to Tor!", success=True)
                    self.append_to_results("[TOR] Successfully verified Tor network connection!")
                else:
                    self.update_tor_status("Orbot running, Tor not verified", warning=True)
                    self.append_to_results("[TOR] Warning: Orbot accessible but Tor network not verified.")
            else:
                self.update_tor_status("Orbot not running", error=True)
                self.append_to_results(f"[TOR] Error: Cannot connect to Orbot at {host}:{port}")
                self.append_to_results("[TOR] Please ensure Orbot is installed and running.")
                
        except OrbotNotRunningError as e:
            self.update_tor_status("Orbot not running", error=True)
            self.append_to_results(f"[TOR] Error: {str(e)}")
        except TorNetworkError as e:
            self.update_tor_status("Tor network error", error=True)
            self.append_to_results(f"[TOR] Error: {str(e)}")
    
    def save_tor_settings(self, instance):
        """Save and apply Tor settings."""
        if orbot_manager is None:
            self.update_tor_status("Error: Orbot module not available", error=True)
            self.append_to_results("\n[TOR] Error: Orbot module not loaded.")
            return
        
        host = self.tor_host_input.text.strip() or "127.0.0.1"
        port_text = self.tor_port_input.text.strip() or "9050"
        
        try:
            port = int(port_text)
            if port < 1 or port > 65535:
                raise ValueError("Port out of range")
        except ValueError:
            self.update_tor_status("Invalid port number", error=True)
            self.append_to_results(f"\n[TOR] Error: Invalid port '{port_text}'. Port must be between 1-65535.")
            return
        
        enabled = self.tor_enabled_checkbox.active
        fail_closed = self.fail_closed_checkbox.active
        
        try:
            if enabled:
                try:
                    enable_tor_routing(host=host, port=port, fail_closed=fail_closed)
                    self.update_tor_status("Tor routing enabled", success=True)
                    self.append_to_results(f"\n[TOR] Tor routing enabled via {host}:{port}")
                    if fail_closed:
                        self.append_to_results("[TOR] Fail-closed mode: Network blocked if Tor disconnects")
                except OrbotNotRunningError as e:
                    self.update_tor_status("Orbot not running", error=True)
                    self.append_to_results(f"\n[TOR] Error: {str(e)}")
                    self.tor_enabled_checkbox.active = False
            else:
                disable_tor_routing()
                self.update_tor_status("Disabled")
                self.append_to_results("\n[TOR] Tor routing disabled")
        except TorNetworkError as e:
            self.update_tor_status("Tor network error", error=True)
            self.append_to_results(f"\n[TOR] Error: {str(e)}")

    def on_action_change(self, spinner, text):
        """Handle action selection changes to show/hide relevant fields"""
        # Reset all conditional layouts
        self.db_layout.height = 0
        self.table_layout.height = 0
        self.cols_layout.height = 0
        
        if text == 'List Tables':
            self.db_layout.height = 40
        elif text == 'Dump Data':
            self.db_layout.height = 40
            self.table_layout.height = 40
            self.cols_layout.height = 40
    
    def append_to_results(self, text):
        """Append text to results output (thread-safe)"""
        def update(dt):
            current = self.results_output.text
            if current == 'Results will appear here...':
                self.results_output.text = text
            else:
                self.results_output.text = current + '\n' + text
        Clock.schedule_once(update)
    
    def update_button_state(self, enabled):
        """Enable or disable the run button"""
        def update(dt):
            self.run_button.disabled = not enabled
            self.run_button.text = 'Run Scan' if enabled else 'Running...'
        Clock.schedule_once(update)
    
    def run_scan(self, instance):
        """Run the Ghauri scan in a separate thread"""
        if not ghauri:
            error_msg = f"Error: Ghauri module not loaded\n{GHAURI_IMPORT_ERROR if GHAURI_IMPORT_ERROR else 'Unknown import error'}"
            self.append_to_results(error_msg)
            return
        
        url = self.url_input.text.strip()
        if not url:
            self.append_to_results("Error: Please enter a target URL")
            return
        
        # Disable button during scan
        self.update_button_state(False)
        self.append_to_results(f"\n{'='*50}\nStarting scan on: {url}\n{'='*50}")
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._run_scan_thread)
        thread.daemon = True
        thread.start()
    
    def _run_scan_thread(self):
        """Execute Ghauri scan in background thread"""
        try:
            # Check if Tor routing is enabled and verify connection
            if orbot_manager is not None and orbot_manager.enabled:
                try:
                    orbot_manager.ensure_tor_or_fail()
                    self.append_to_results("[TOR] Routing traffic through Tor network...")
                except (OrbotNotRunningError, TorNetworkError) as e:
                    self.append_to_results(f"[TOR] Error: {str(e)}")
                    self.append_to_results("[TOR] Scan aborted due to fail-closed mode.")
                    return
            
            # Prepare arguments
            url = self.url_input.text.strip()
            data = self.data_input.text.strip() or None
            cookie = self.cookie_input.text.strip() or ""
            proxy = self.proxy_input.text.strip() or ""
            user_agent = self.ua_input.text.strip() or ""
            
            # Use Tor proxy if enabled and no custom proxy specified
            if orbot_manager is not None and orbot_manager.enabled and not proxy:
                proxy = orbot_manager.socks_proxy_url
                self.append_to_results(f"[TOR] Using SOCKS5 proxy: {proxy}")
            
            # Get DBMS
            dbms_map = {
                'MySQL': 'MySQL',
                'PostgreSQL': 'PostgreSQL',
                'Microsoft SQL Server': 'Microsoft SQL Server',
                'Oracle': 'Oracle',
                'Microsoft Access': 'Microsoft Access',
                'Auto Detect': None
            }
            dbms = dbms_map.get(self.dbms_spinner.text)
            
            # Get other parameters
            technique = self.tech_spinner.text
            timeout = int(self.timeout_input.text) if self.timeout_input.text.isdigit() else 30
            delay = int(self.delay_input.text) if self.delay_input.text.isdigit() else 0
            level = int(self.level_spinner.text) if self.level_spinner.text.isdigit() else 1
            threads = int(self.threads_input.text) if self.threads_input.text.isdigit() else 1
            batch = self.batch_checkbox.active
            random_agent = self.random_agent_checkbox.active
            
            # Perform injection test (without capturing all output to avoid interfering with Kivy)
            self.append_to_results("Testing for SQL injection vulnerabilities...")
            
            try:
                resp = ghauri.perform_injection(
                    url=url,
                    data=data,
                    cookies=cookie,
                    proxy=proxy,
                    user_agent=user_agent,
                    dbms=dbms,
                    level=level,
                    verbosity=1,
                    techniques=technique,
                    batch=batch,
                    timeout=timeout,
                    delay=delay,
                    threads=threads,
                    random_agent=random_agent,
                    host="",
                    header="",
                    headers="",
                    referer="",
                    requestfile="",
                    flush_session=False,
                    force_ssl=False,
                    timesec=5,
                    testparameter=None,
                    retries=3,
                    prefix=None,
                    suffix=None,
                    code=200,
                    string=None,
                    not_string=None,
                    text_only=False,
                    skip_urlencoding=False,
                    confirm_payloads=False,
                    safe_chars=None,
                    fetch_using=None,
                    test_filter=None,
                    sql_shell=False,
                    fresh_queries=False,
                    update=False,
                    ignore_code="",
                    bulkfile=False,
                    mobile=False,
                )
                
                if resp and resp.is_injected:
                        self.append_to_results("\n[SUCCESS] SQL injection found!")
                        self.append_to_results(f"Parameter: {resp.parameter}")
                        self.append_to_results(f"Backend: {resp.backend}")
                        self.append_to_results(f"Injection Type: {resp.injection_type}")
                        
                        # Perform requested action
                        action = self.action_spinner.text
                        target = ghauri.Ghauri(
                            url=resp.url,
                            data=resp.data,
                            vector=resp.vector,
                            backend=resp.backend,
                            parameter=resp.parameter,
                            headers=resp.headers,
                            base=resp.base,
                            injection_type=resp.injection_type,
                            proxy=resp.proxy,
                            filepaths=resp.filepaths,
                            is_multipart=resp.is_multipart,
                            timeout=timeout,
                            delay=delay,
                            timesec=5,
                            attack=resp.attack,
                            match_string=resp.match_string,
                            vectors=resp.vectors,
                        )
                        
                        if action == 'Get Banner':
                            result = target.extract_banner()
                            if result and result.ok:
                                self.append_to_results(f"\nBanner: {result.result}")
                        elif action == 'Get Current User':
                            result = target.extract_current_user()
                            if result and result.ok:
                                self.append_to_results(f"\nCurrent User: {result.result}")
                        elif action == 'Get Current DB':
                            result = target.extract_current_db()
                            if result and result.ok:
                                self.append_to_results(f"\nCurrent Database: {result.result}")
                        elif action == 'Get Hostname':
                            result = target.extract_hostname()
                            if result and result.ok:
                                self.append_to_results(f"\nHostname: {result.result}")
                        elif action == 'List Databases':
                            result = target.extract_dbs()
                            if result and result.ok:
                                self.append_to_results(f"\nDatabases: {result.result}")
                        elif action == 'List Tables':
                            db = self.db_input.text.strip()
                            if db:
                                result = target.extract_tables(database=db)
                                if result and result.ok:
                                    self.append_to_results(f"\nTables in {db}: {result.result}")
                            else:
                                self.append_to_results("\nError: Database name required")
                        elif action == 'Dump Data':
                            db = self.db_input.text.strip()
                            table = self.table_input.text.strip()
                            cols = self.cols_input.text.strip() or ""
                            if db and table:
                                result = target.extract_records(database=db, table=table, columns=cols)
                                if result and result.ok:
                                    self.append_to_results(f"\nDumped data from {db}.{table}:\n{result.result}")
                            else:
                                self.append_to_results("\nError: Database and table names required")
                else:
                    self.append_to_results("\n[INFO] No SQL injection found or unable to detect.")
                    
            except Exception as e:
                self.append_to_results(f"\nError during scan: {str(e)}")
                self.append_to_results(traceback.format_exc())
            
            self.append_to_results(f"\n{'='*50}\nScan completed\n{'='*50}")
            
        except Exception as e:
            self.append_to_results(f"\nFatal error: {str(e)}")
            self.append_to_results(traceback.format_exc())
        finally:
            # Re-enable button
            self.update_button_state(True)


def main():
    """Main entry point"""
    GhauriApp().run()


if __name__ == '__main__':
    main()
