import datetime
import time
from collections import defaultdict

import dateparser
import streamlit as st
import pandas as pd
import numpy as np


class Aggregation(object):
    def __init__(self, workouts_df, group_by=None):
        self.group_by = group_by

        # These accumulators hold the values over the iterations
        total_workouts = defaultdict(lambda: 0)
        total_time = defaultdict(lambda: 0.0)
        total_distance = defaultdict(lambda: 0.0)
        total_output = defaultdict(lambda: 0.0)
        total_calories = defaultdict(lambda: 0.0)

        for _, row in workouts_df.iterrows():
            # Get the value for the group_by column
            if group_by:
                key = row[group_by]
            else:
                key = "All Time"

            # Update the accumulators
            total_workouts[key] += 1
            if not pd.isna(row["Length (minutes)"]):
                total_time[key] += row["Length (minutes)"]
            if not pd.isna(row["Distance (mi)"]):
                total_distance[key] += row["Distance (mi)"]
            if not pd.isna(row["Total Output"]):
                total_output[key] += row["Total Output"]
            if not pd.isna(row["Calories Burned"]):
                total_calories[key] += row["Calories Burned"]

        self.aggregated_df = pd.DataFrame(
            {
                "Total Workouts": pd.Series(total_workouts),
                "Total Minutes": pd.Series(total_time),
                "Total Distance": pd.Series(total_distance),
                "Total Output": pd.Series(total_output),
                "Total Calories": pd.Series(total_calories),
            }
        )


def process_workouts_df():
    # Bail out if we don't have a workouts_df on the session_state
    if "workouts_df" not in st.session_state:
        return
    workouts_df = st.session_state["workouts_df"]

    # Convert to datetime
    def parse_datetime(date_str):
        # This is necessary because some Peloton workouts contain timezones
        # like (-05) which are not well-handled by dateparser
        return dateparser.parse(date_str.replace("(-", "(GMT-").replace("(+", "(GMT+"))

    # Parse the various versions of the Workout's Timestamp
    workouts_df["c_datetime"] = workouts_df["Workout Timestamp"].apply(
        lambda x: parse_datetime(x)
    )
    workouts_df["c_datetime"] = pd.to_datetime(workouts_df["c_datetime"], utc=True)
    workouts_df["c_date"] = workouts_df["c_datetime"].apply(lambda x: x.date())
    workouts_df["c_week"] = workouts_df["c_datetime"].apply(
        lambda x: datetime.datetime.strptime(
            "{}-{}-1".format(x.year, x.isocalendar()[1]), "%Y-%W-%w"
        ).date()
    )
    workouts_df["c_month"] = workouts_df["c_datetime"].apply(
        lambda x: x.strftime("%Y-%m")
    )
    workouts_df["c_year"] = workouts_df["c_datetime"].apply(lambda x: int(x.year))

    # Calculate some exercise-level stats
    workouts_df["c_calories_per_minute"] = (
        workouts_df["Calories Burned"] / workouts_df["Length (minutes)"]
    )
    workouts_df["c_output_per_minute"] = (
        workouts_df["Total Output"] / workouts_df["Length (minutes)"]
    )

    # After processing, reassign the processed DF to session_state
    st.session_state["workouts_df"] = workouts_df
    st.session_state["workouts_aggregation_all_time"] = Aggregation(workouts_df)
    st.session_state["workouts_aggregation_by_year"] = Aggregation(
        workouts_df, "c_year"
    )
    st.session_state["workouts_aggregation_by_month"] = Aggregation(
        workouts_df, "c_month"
    )
    st.session_state["workouts_aggregation_by_week"] = Aggregation(
        workouts_df, "c_week"
    )


def render_upload_workouts():
    st.title("Upload Workouts")
    workouts_guide = """
    1. Go to https://members.onepeloton.com/profile/workouts
    2. Click 'DOWNLOAD WORKOUTS' and save your file
    3. Upload your saved workouts.csv file below
    """
    st.markdown(workouts_guide)

    workouts_help = """
    We do not save any of your personal data. To learn more, or
    to see the source code, go to https://github.com/jfkirk/pelotodos.
    """
    raw_workouts = st.file_uploader(
        "Upload your workouts",
        type=["csv"],
        help=workouts_help,
    )

    if ("workouts_df" in st.session_state) and (raw_workouts is None):
        workouts_df = st.session_state["workouts_df"]

    if raw_workouts is not None:
        workouts_df = pd.read_csv(raw_workouts)
        st.session_state["workouts_df"] = workouts_df

        # Whether-or-not we've uploaded, process the DF
        st.text("Processing your workouts...")
        process_workouts_df()
        st.text("{} workouts processed!".format(len(workouts_df)))

    if "workouts_df" in st.session_state:
        st.subheader("Workouts")
        st.dataframe(st.session_state["workouts_df"])
        print(workouts_df)


def render_all_time_stats():
    st.title("All-Time Stats")

    if "workouts_df" not in st.session_state:
        st.text("Workouts have not been uploaded. See 'Upload Workouts' to the left.")
        return

    st.dataframe(st.session_state["workouts_aggregation_all_time"].aggregated_df)


def render_stats_by_month():
    st.title("Stats By Month")

    if "workouts_df" not in st.session_state:
        st.text("Workouts have not been uploaded. See 'Upload Workouts' to the left.")
        return

    st.subheader("Total Minutes")
    st.bar_chart(
        st.session_state["workouts_aggregation_by_month"].aggregated_df["Total Minutes"]
    )

    st.subheader("Total Workouts")
    st.bar_chart(
        st.session_state["workouts_aggregation_by_month"].aggregated_df[
            "Total Workouts"
        ]
    )

    st.subheader("Total Output")
    st.bar_chart(
        st.session_state["workouts_aggregation_by_month"].aggregated_df["Total Output"]
    )

    st.subheader("Total Calories")
    st.bar_chart(
        st.session_state["workouts_aggregation_by_month"].aggregated_df[
            "Total Calories"
        ]
    )

    st.subheader("Total Distance")
    st.bar_chart(
        st.session_state["workouts_aggregation_by_month"].aggregated_df[
            "Total Distance"
        ]
    )


def render_about():
    st.title("About Pelotodos")
    st.markdown("Pelotodos is a tool for visualizing your workouts.")
    st.markdown(
        "Pelotodos is not associated with Peloton Interactive, Inc. in any way - except"
        + " as fans."
    )
    st.markdown(
        "To learn more, or to see the source code, see "
        + "[GitHub](https://github.com/jfkirk/pelotodos)."
    )


def main():
    st.sidebar.title("Pelotodos")

    pages = ["Upload Workouts", "All-Time Stats", "Stats By Month", "About"]
    app_mode = st.sidebar.radio("Tools", options=pages)
    st.session_state["app_mode"] = app_mode

    if st.session_state["app_mode"] == "Upload Workouts":
        render_upload_workouts()
    elif st.session_state["app_mode"] == "All-Time Stats":
        render_all_time_stats()
    elif st.session_state["app_mode"] == "Stats By Month":
        render_stats_by_month()
    elif st.session_state["app_mode"] == "About":
        render_about()


main()
