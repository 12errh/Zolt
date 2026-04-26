"""
PyUI Example — Analytics Dashboard

Run with: pyui run examples/dashboard/app.py
"""

from pyui import (
    Alert, App, Badge, Button, Chart, Flex, Grid,
    Heading, Nav, Page, Stat, Table, Text, reactive,
)


class DashboardPage(Page):
    title = "Dashboard"
    route = "/"
    layout = "default"

    def compose(self) -> None:
        Nav(items=[
            ("Dashboard", "/"), ("Reports", "/reports"), ("Settings", "/settings"),
        ])

        with Flex(direction="col", gap=8):
            with Flex(align="center", justify="between"):
                Heading("Analytics Dashboard", level=1)
                Badge("Live", variant="success")

            # KPI stats
            with Grid(cols=4, gap=6):
                Stat("Total Users",    "24,521", trend="+12%",  trend_up=True)
                Stat("Revenue",        "$84,200", trend="+6%",  trend_up=True)
                Stat("Active Sessions","1,429",   trend="+3%",  trend_up=True)
                Stat("Churn Rate",     "2.4%",    trend="-0.8%",trend_up=False)

            # Chart
            Chart(
                type="line",
                labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                datasets=[{
                    "label": "Revenue ($k)",
                    "data": [42, 55, 61, 70, 78, 84],
                    "borderColor": "#6C63FF",
                }],
            )

            # Alert
            Alert("System healthy", "All services are operating normally.", variant="success")

            # Recent activity table
            Heading("Recent Activity", level=2)
            Table(
                headers=["User", "Action", "Time", "Status"],
                rows=[
                    ["Alice Smith",  "Login",   "2 min ago",  "Success"],
                    ["Bob Jones",    "Export",  "5 min ago",  "Success"],
                    ["Carol White",  "Upload",  "12 min ago", "Pending"],
                    ["Dan Brown",    "Delete",  "1 hr ago",   "Failed"],
                    ["Eve Davis",    "Login",   "2 hr ago",   "Success"],
                ],
            ).striped()


class ReportsPage(Page):
    title = "Reports"
    route = "/reports"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Reports", level=1)
            Text("Select a report to view detailed analytics.").style("muted")
            with Grid(cols=3, gap=4):
                for name in ["Monthly Revenue", "User Growth", "Churn Analysis",
                             "Conversion Funnel", "Traffic Sources", "Retention"]:
                    with Flex(direction="col", gap=2).className(
                        "p-5 bg-white border border-gray-100 rounded-2xl "
                        "shadow-sm hover:shadow-md transition-shadow cursor-pointer"
                    ):
                        Text(name).className("font-semibold text-gray-900")
                        Text("View report →").style("muted")


class SettingsPage(Page):
    title = "Settings"
    route = "/settings"

    def compose(self) -> None:
        with Flex(direction="col", gap=6):
            Heading("Settings", level=1)
            Alert("Changes are saved automatically.", variant="info")
            with Flex(direction="col", gap=4).className(
                "bg-white border border-gray-100 rounded-2xl p-6"
            ):
                Heading("Notifications", level=3)
                Text("Configure how you receive alerts.").style("muted")
                Button("Save Settings").style("primary")


class DashboardApp(App):
    name = "Analytics Dashboard"
    description = "A PyUI analytics dashboard example."
    theme = "light"

    home = DashboardPage()
    reports = ReportsPage()
    settings = SettingsPage()
