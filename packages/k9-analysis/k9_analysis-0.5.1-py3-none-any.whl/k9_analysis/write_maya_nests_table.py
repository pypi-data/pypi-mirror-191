from .count_burrows_detection import (
    make_summary_maya_2022_number_of_nest_marked,
    make_summary_of_marked_nests_by_year,
)

from .group_effort_and_distance import make_summary_of_effort_and_distance

import pandas as pd
import typer


app = typer.Typer()


@app.command()
def write_maya_nests_table(
    start_date: str = "2022-01-01",
    end_date: str = "2023-01-29",
    input_path: str = "data/processed/registros_rastros_de_gatos_k9_guadalupe_ISO8601.csv",
    output_path: str = "reports/tables/maya_nests_table.csv",
):
    k9_data = pd.read_csv(input_path)
    summary = make_summary_maya_2022_number_of_nest_marked(k9_data, start_date, end_date)
    summary.to_csv(output_path, index=False)


@app.command()
def write_summary_of_marked_nests_by_year(
    input_path: str = "data/processed/registros_rastros_de_gatos_k9_guadalupe_ISO8601.csv",
    output_path: str = "reports/tables/maya_nests_table.csv",
):
    k9_data = pd.read_csv(input_path)
    summary = make_summary_of_marked_nests_by_year(k9_data)
    summary.to_csv(output_path, index=False)


@app.command()
def write_total_time_and_distance_k9(
    input_path: str = "data/processed/esfuerzos_k9_gatos_guadalupe_ISO8601.csv",
    output_path: str = "data/processed/total_time_and_distance_k9.csv",
    start_date: str = "2021-01-01",
    end_date: str = "2022-12-31",
):
    k9_data = pd.read_csv(input_path)
    summary = make_summary_of_effort_and_distance(k9_data, start_date, end_date)
    summary.to_csv(output_path, index=False)
