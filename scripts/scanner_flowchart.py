# /// script
# requires-python = ">=3.13"
# dependencies = ["diagrams==0.24.4"]
# ///

from diagrams import Diagram
from diagrams.programming.flowchart import StartEnd, Database, Action
from diagrams.c4 import SystemBoundary

# Define node attributes to ensure text appears inside shapes
node_attrs = {
    "fontsize": "12",
    "fontname": "Arial",
    "shape": "plaintext",  # Changed from "box" to "plaintext"
    "style": "filled",
    "fillcolor": "white",
    "labelloc": "c"  # Center the label within the shape
}

with Diagram("../docs/diagrams/scanner_flowchart", direction="TB",
             graph_attr={"splines": "spline"},
             node_attr=node_attrs):
    with SystemBoundary("SlocCount"):
        with SystemBoundary("Scanner"):

            start = StartEnd("Start", **node_attrs)
            end = StartEnd("End", **node_attrs)
            data_file = Database("Data File", **node_attrs)
            save_to_file = Action("Save to File", **node_attrs)

            start >> save_to_file >> end
            save_to_file >> data_file
