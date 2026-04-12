from pyui import App, Button, Flex, Heading, Page, Text, computed, reactive

# Reactive state defined at module level for simple scoped access
count = reactive(0)
doubled = computed(lambda: count.get() * 2)


class CounterApp(App):
    count = count
    doubled = doubled

    @staticmethod
    def increment():
        count.set(count.get() + 1)

    @staticmethod
    def reset():
        count.set(0)


class HomePage(Page):
    title = "Phase 3: Reactivity Demo"
    route = "/"

    def compose(self):
        with Flex(direction="col", gap=8, align="center", justify="center").padding(20):
            Heading("PyUI Phase 3").style("lead").className("text-center")
            Text("Full-Stack Reactivity Demo").style("muted").size("sm")

            with Flex(gap=10, align="center"):
                with Flex(direction="col", align="center"):
                    Text("Base Count").style("muted").size("sm")
                    Text(
                        lambda: f"{count.get()}",
                    ).size("4xl").className("font-mono text-violet-600 font-bold")

                # Divider
                Text("|").size("4xl").style("muted").className("opacity-20")

                with Flex(direction="col", align="center"):
                    Text("Computed (x2)").style("muted").size("sm")
                    Text(
                        lambda: f"{doubled.get()}",
                    ).size("4xl").className("font-mono text-emerald-600 font-bold")

            with Flex(gap=4):
                Button("Increment").icon("plus").style("primary").size("lg").onClick(
                    CounterApp.increment
                )
                Button("Reset").icon("refresh-cw").style("ghost").onClick(CounterApp.reset)

            # Test conditional visibility
            with Flex(direction="col", align="center").padding(24, 0, 0, 0):
                Text(
                    "You've reached double digits!",
                ).style("success").className("font-medium").hidden(lambda: count.get() < 10)


class Demo(CounterApp):
    index = HomePage()


if __name__ == "__main__":
    from pyui.server.dev_server import run_dev_server

    run_dev_server(Demo, port=9015)
