from diagrams import Diagram








with Diagram("../docs/diagrams/c4", direction="TB", graph_attr={"splines": "spline"}):
    user = diagrams.c4.Person(name="User")

    with diagrams.c4.SystemBoundary("CountSloc"):
        scanner = diagrams.c4.Container(name="Scanner", technology="Python")

        with diagrams.c4.SystemBoundary("GitHub Pages"):
            data_file = diagrams.c4.Database(
                name="Data File",
                description="File containing the data to be scanned.",
                technology="JSON",
            )
            dashboard = diagrams.c4.Container(
                name="Dashboard",
                description="Web application for viewing statistics and metrics.",
                technology="TypeScript",
            )

    user >> diagrams.c4.Relationship("Uses") >> dashboard
    scanner >> diagrams.c4.Relationship("Creates") >> data_file
    dashboard >> diagrams.c4.Relationship("Reads") >> data_file
