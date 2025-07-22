import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    from json import loads
    from pandas import DataFrame

    import pandas as pd

    with open("/Users/jackplowman/Projects/Personal/SlocCount/scanner/output.json") as f:
        file_contents = loads(f.read())

    df = DataFrame(file_contents["repositories"])
    df

    return


if __name__ == "__main__":
    app.run()
