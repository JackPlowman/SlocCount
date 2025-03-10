# /// script
# requires-python = ">=3.13"
# dependencies = ["diagrams==0.24.4"]
# ///

from diagrams import Diagram
from diagrams.c4 import (
    Person,
    Container,
    Database,
    SystemBoundary,
    Relationship,
)

with Diagram("../docs/diagrams/c4", direction="TB", graph_attr={"splines": "spline"}):
    user = Person(name="User")

    with SystemBoundary("CountSloc"):
        scanner = Container(name="Scanner", technology="Python")

        with SystemBoundary("GitHub Pages"):
            data_file = Database(
                name="Data File",
                description="File containing the data to be scanned.",
                technology="JSON",
            )
            dashboard = Container(
                name="Dashboard",
                description="Web application for viewing statistics and metrics.",
                technology="TypeScript",
            )

    user >> Relationship("Uses") >> dashboard
    scanner >> Relationship("Creates") >> data_file
    dashboard >> Relationship("Reads") >> data_file
