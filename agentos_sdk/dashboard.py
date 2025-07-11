import time
import psutil

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box

console = Console()


class Dashboard:
    """
    Dashboard class for AgentOS - handles all UI rendering and real-time monitoring display.

    This class provides a futuristic, corporate-styled dashboard interface that displays:
    - System statistics (CPU, memory, uptime)
    - Current task status and progress
    - Available tools status
    - Real-time output from agent operations
    """

    def __init__(self, show_dashboard: bool = True):
        self.show_dashboard = show_dashboard
        self.dashboard_active = False
        self.current_task = None
        self.task_progress = 0
        self.last_output = ""
        self.tools_count = 0

    def get_system_stats(self):
        """Get current system statistics for dashboard display"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            cpu_count = psutil.cpu_count()
            boot_time = psutil.boot_time()
            uptime = time.time() - boot_time

            return {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used": memory.used // (1024**3),  # GB
                "memory_total": memory.total // (1024**3),  # GB
                "cpu_cores": cpu_count,
                "uptime_hours": uptime // 3600,
            }
        except Exception:
            return {
                "cpu_percent": 0,
                "memory_percent": 0,
                "memory_used": 0,
                "memory_total": 8,
                "cpu_cores": 4,
                "uptime_hours": 0,
            }

    def create_dashboard_layout(self):
        """Create the main dashboard layout"""
        layout = Layout()

        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )

        layout["main"].split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1),
        )

        layout["left"].split_column(
            Layout(name="task_panel", ratio=1),
            Layout(name="output_panel", ratio=2),
        )

        return layout

    def create_header_panel(self):
        """Create the futuristic header panel"""
        stats = self.get_system_stats()

        header_text = Text()
        header_text.append("◢◤ ", style="bold red")
        header_text.append(
            "SWARMS CORPORATION", style="bold bright_red"
        )
        header_text.append(" ◢◤ ", style="bold red")
        header_text.append("AGENTOS v2.1.0", style="bold white")
        header_text.append(" ◢◤ ", style="bold red")
        header_text.append(
            f"CPU: {stats['cpu_percent']:.1f}%", style="bright_green"
        )
        header_text.append(" ◢◤ ", style="bold red")
        header_text.append(
            f"MEM: {stats['memory_used']}/{stats['memory_total']}GB",
            style="bright_cyan",
        )
        header_text.append(" ◢◤ ", style="bold red")
        header_text.append(
            f"CORES: {stats['cpu_cores']}", style="bright_yellow"
        )

        return Panel(
            Align.center(header_text),
            style="bold red",
            box=box.DOUBLE_EDGE,
            border_style="bright_red",
        )

    def create_system_panel(self):
        """Create system monitoring panel"""
        stats = self.get_system_stats()

        table = Table(
            box=box.MINIMAL, show_header=False, padding=(0, 1)
        )
        table.add_column("Metric", style="bright_red", width=12)
        table.add_column("Value", style="bright_white", width=20)
        table.add_column("Bar", width=15)

        # CPU Usage
        cpu_bar = "█" * int(stats["cpu_percent"] / 10) + "░" * (
            10 - int(stats["cpu_percent"] / 10)
        )
        table.add_row(
            "◢ CPU",
            f"{stats['cpu_percent']:.1f}%",
            f"[red]{cpu_bar}[/red]",
        )

        # Memory Usage
        mem_bar = "█" * int(stats["memory_percent"] / 10) + "░" * (
            10 - int(stats["memory_percent"] / 10)
        )
        table.add_row(
            "◢ MEMORY",
            f"{stats['memory_percent']:.1f}%",
            f"[cyan]{mem_bar}[/cyan]",
        )

        # Cores
        table.add_row("◢ CORES", f"{stats['cpu_cores']} cores", "")

        # Uptime
        table.add_row("◢ UPTIME", f"{stats['uptime_hours']:.1f}h", "")

        # Tools Status
        table.add_row(
            "◢ TOOLS",
            f"{self.tools_count} active",
            "[green]●●●●●●●●●●[/green]",
        )

        return Panel(
            table,
            title="[bold red]◢◤ SYSTEM STATUS ◢◤[/bold red]",
            style="red",
            border_style="bright_red",
        )

    def create_tools_panel(self):
        """Create tools status panel"""
        tools_table = Table(box=box.MINIMAL, show_header=False)
        tools_table.add_column("Tool", style="bright_red", width=20)
        tools_table.add_column(
            "Status", style="bright_green", width=8
        )

        tool_names = [
            "Browser Agent",
            "HuggingFace Model",
            "LiteLLM Model",
            "Calculator",
            "Terminal Agent",
            "Speech Generator",
            "Video Generator",
            "File Manager",
        ]

        for tool in tool_names:
            tools_table.add_row(f"◢ {tool}", "[green]ONLINE[/green]")

        return Panel(
            tools_table,
            title="[bold red]◢◤ AVAILABLE TOOLS ◢◤[/bold red]",
            style="red",
            border_style="bright_red",
        )

    def create_task_panel(self):
        """Create current task panel"""
        if self.current_task:
            task_text = Text()
            task_text.append("◢ ACTIVE TASK: ", style="bold red")
            task_text.append(
                (
                    self.current_task[:80] + "..."
                    if len(self.current_task) > 80
                    else self.current_task
                ),
                style="bright_white",
            )

            # Progress bar - fix the markup issue
            progress_bar = "█" * int(
                self.task_progress / 10
            ) + "░" * (10 - int(self.task_progress / 10))
            task_text.append(
                f"\n◢ PROGRESS: {self.task_progress}% ",
                style="bold red",
            )
            task_text.append(progress_bar, style="red")

            content = task_text
        else:
            content = Text(
                "◢ AGENT OS ACTIVATED", style="bold bright_red"
            )

        return Panel(
            content,
            title="[bold red]◢◤ MISSION STATUS ◢◤[/bold red]",
            style="red",
            border_style="bright_red",
        )

    def create_output_panel(self):
        """Create output display panel"""
        if self.last_output and self.last_output.strip():
            # Create a Text object and add content with proper styling
            output_text = Text()

            # Split into lines and process
            lines = self.last_output.split("\n")
            for i, line in enumerate(
                lines[:25]
            ):  # Show first 25 lines
                if line.strip():
                    if line.startswith("◢"):
                        output_text.append(line, style="bold red")
                    elif "ERROR" in line.upper():
                        output_text.append(line, style="bold red")
                    elif (
                        "SUCCESS" in line.upper()
                        or "COMPLETED" in line.upper()
                    ):
                        output_text.append(line, style="bold green")
                    elif "Task Completed" in line:
                        output_text.append(line, style="bold green")
                    else:
                        output_text.append(line, style="bright_white")

                # Add newline except for last line
                if i < len(lines) - 1:
                    output_text.append("\n")

            # Add truncation notice if needed
            if len(lines) > 25:
                output_text.append(
                    "\n\n[dim]... (output truncated for display)[/dim]"
                )

        else:
            output_text = Text()
            output_text.append(
                "◢ Awaiting neural commands...\n", style="bold red"
            )
            output_text.append(
                "◢ All systems nominal and ready for deployment.",
                style="bold red",
            )

        return Panel(
            output_text,
            title="[bold red]◢◤ AGENTOS OUTPUT ◢◤[/bold red]",
            style="red",
            border_style="bright_red",
            height=15,
        )

    def create_footer_panel(self):
        """Create footer with corporation branding"""
        footer_text = Text()
        footer_text.append("◢◤◢◤◢◤ ", style="bold red")
        footer_text.append(
            "SWARMS CORPORATION", style="bold bright_red"
        )
        footer_text.append(
            " - AGENT OPERATING SYSTEM - ", style="bold white"
        )
        footer_text.append(
            "UNAUTHORIZED ACCESS PROHIBITED", style="bold red"
        )
        footer_text.append(" ◢◤◢◤◢◤", style="bold red")

        return Panel(
            Align.center(footer_text),
            style="red",
            box=box.DOUBLE_EDGE,
            border_style="bright_red",
        )

    def animate_loading(self, duration=3):
        """Show loading animation"""
        if not self.show_dashboard:
            return

        with Progress(
            SpinnerColumn(style="red"),
            TextColumn("[red]◢ Initializing AgentOS..."),
            BarColumn(
                bar_width=40, style="red", complete_style="bright_red"
            ),
            TaskProgressColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Loading", total=100)
            for i in range(100):
                time.sleep(duration / 100)
                progress.update(task, advance=1)

    def show_live_dashboard(self, task_description=""):
        """Show live updating dashboard"""
        if not self.show_dashboard:
            return None

        self.current_task = task_description
        self.dashboard_active = True

        layout = self.create_dashboard_layout()

        def update_dashboard():
            layout["header"].update(self.create_header_panel())
            layout["task_panel"].update(self.create_task_panel())
            layout["output_panel"].update(self.create_output_panel())
            layout["right"].split_column(
                Layout(self.create_system_panel(), name="system"),
                Layout(self.create_tools_panel(), name="tools"),
            )
            layout["footer"].update(self.create_footer_panel())
            return layout

        return Live(
            update_dashboard(), console=console, refresh_per_second=2
        )

    def update_task_progress(self, progress: int, output: str = ""):
        """Update task progress and output"""
        self.task_progress = progress
        if output:
            self.last_output = output

    def append_output(self, new_output: str):
        """Append new output to the existing output for real-time streaming"""
        if new_output:
            if self.last_output:
                self.last_output += "\n" + new_output
            else:
                self.last_output = new_output

    def clear_output(self):
        """Clear the current output"""
        self.last_output = ""

    def clear_screen(self):
        """Clear the console screen"""
        if self.show_dashboard:
            console.clear()

    def set_tools_count(self, count: int):
        """Set the number of available tools for display"""
        self.tools_count = count
