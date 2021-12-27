import datetime
from collections import defaultdict

import dateparser
import numpy as np
import plotly.express as px
import pandas as pd
import streamlit as st
from traitlets.traitlets import default


class Aggregation(object):
    def __init__(self, workouts_df, group_by=None):
        self.group_by = group_by

        # These accumulators hold the values over the iterations
        total_workouts = defaultdict(lambda: 0)
        total_time = defaultdict(lambda: 0.0)
        total_distance = defaultdict(lambda: 0.0)
        total_output = defaultdict(lambda: 0.0)
        total_calories = defaultdict(lambda: 0.0)
        total_calories_minutes = defaultdict(lambda: 0.0)
        total_hr = defaultdict(lambda: 0.0)
        total_hr_minutes = defaultdict(lambda: 0.0)
        total_speed = defaultdict(lambda: 0.0)
        total_speed_minutes = defaultdict(lambda: 0.0)
        total_cadence = defaultdict(lambda: 0.0)
        total_cadence_minutes = defaultdict(lambda: 0.0)

        for _, row in workouts_df.iterrows():
            # Get the value for the group_by column
            if group_by:
                key = row[group_by]

                # Skip rows with an invalid key
                if pd.isnull(key):
                    continue
            else:
                key = "All Time"

            # Update the accumulators
            total_workouts[key] += 1
            if not pd.isna(row["Distance (mi)"]):
                total_distance[key] += row["Distance (mi)"]
            if not pd.isna(row["Total Output"]):
                total_output[key] += row["Total Output"]
            if not pd.isna(row["Length (minutes)"]):
                total_time[key] += row["Length (minutes)"]
                # These are nested inside the Length if-clause because we need to
                # weight the values by the workout length
                if not pd.isna(row["Calories Burned"]):
                    total_calories[key] += row["Calories Burned"]
                    total_calories_minutes[key] += row["Length (minutes)"]
                if not pd.isna(row["Avg. Heartrate"]):
                    total_hr[key] += row["Length (minutes)"] * row["Avg. Heartrate"]
                    total_hr_minutes[key] += row["Length (minutes)"]
                if not pd.isna(row["Avg. Speed (mph)"]):
                    total_speed[key] += (
                        row["Length (minutes)"] * row["Avg. Speed (mph)"]
                    )
                    total_speed_minutes[key] += row["Length (minutes)"]
                if not pd.isna(row["Avg. Cadence (RPM)"]):
                    total_cadence[key] += (
                        row["Length (minutes)"] * row["Avg. Cadence (RPM)"]
                    )
                    total_cadence_minutes[key] += row["Length (minutes)"]

        self.aggregated_df = pd.DataFrame(
            {
                "Total Workouts": pd.Series(total_workouts),
                "Total Minutes": pd.Series(total_time),
                "Total Distance": pd.Series(total_distance),
                "Total Output": pd.Series(total_output),
                "Total Calories": pd.Series(total_calories),
                "Calories per Minute": pd.Series(total_calories)
                / pd.Series(total_calories_minutes),
                "Avg. Heartrate": pd.Series(total_hr) / pd.Series(total_hr_minutes),
                "Avg. Speed (mph)": pd.Series(total_speed)
                / pd.Series(total_speed_minutes),
                "Avg. Cadence (RPM)": pd.Series(total_cadence)
                / pd.Series(total_cadence_minutes),
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
    st.session_state["workouts_aggregation_by_instructor"] = Aggregation(
        workouts_df, "Instructor Name"
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
    We do not log or save any of your personal data. To learn more, or
    to see the source code, go to https://github.com/jfkirk/pelotonnes.
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
        workouts_df = workouts_df[workouts_df["Fitness Discipline"] == "Cycling"]
        st.session_state["workouts_df"] = workouts_df

        # Whether-or-not we've uploaded, process the DF
        st.text("Processing your workouts...")
        process_workouts_df()
        st.text("{} workouts processed!".format(len(workouts_df)))

    if "workouts_df" in st.session_state:
        st.subheader("Cycling Workouts")
        st.dataframe(st.session_state["workouts_df"])


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


def render_stats_by_instructor():
    st.title("Stats By Instructor")

    if "workouts_df" not in st.session_state:
        st.text("Workouts have not been uploaded. See 'Upload Workouts' to the left.")
        return

    aggregation = st.session_state["workouts_aggregation_by_instructor"]
    st.dataframe(aggregation.aggregated_df)

    with st.expander("Visualization Options"):
        log_scale = st.checkbox(
            "Use logarithmic scale for cumulative statistics",
            value=(
                True
                if aggregation.aggregated_df["Total Workouts"].max() >= 100
                else False
            ),
        )
        st.text(
            "Use logarithmic scale if you have a large number of workouts with your "
            + "top instructors and few workouts with others."
        )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total Minutes")
        sorted_minutes = aggregation.aggregated_df["Total Minutes"].sort_values(
            ascending=False
        )
        fig = px.bar(
            sorted_minutes,
            labels={"index": "Instructor", "value": "Total Minutes"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    with c2:
        st.subheader("Calories per Minute")
        sorted_cpm = aggregation.aggregated_df["Calories per Minute"].sort_values(
            ascending=False
        )
        fig = px.bar(
            sorted_cpm, labels={"index": "Instructor", "value": "Calories per Minute"}
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Calories per Minute vs Total Minutes")
        fig = px.scatter(
            aggregation.aggregated_df,
            x="Total Minutes",
            y="Calories per Minute",
            text=aggregation.aggregated_df.index,
            log_x=log_scale,
        )
        fig.update_traces(marker_size=10)
        st.plotly_chart(fig)

    with c2:
        st.subheader("")
        st.markdown(
            """
        **Note:**
        
        This plot shows which instructors you spend the most time with vs how hard you work in their workouts. 
        
        Instructors in the top-left make you work hard, but you have not spent much time with them.

        Instructors in the bottom-right are ones you spend a lot of time with, but don't push you as hard.
        """
        )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total Output")
        sorted_output = (
            aggregation.aggregated_df["Total Output"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_output,
            labels={"index": "Instructor", "value": "Total Output"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    with c2:
        st.subheader("Total Workouts")
        sorted_workouts = (
            aggregation.aggregated_df["Total Workouts"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_workouts,
            labels={"index": "Instructor", "value": "Total Workouts"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total Calories")
        sorted_calories = (
            aggregation.aggregated_df["Total Calories"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_calories,
            labels={"index": "Instructor", "value": "Total Calories"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    with c2:
        st.subheader("Total Distance")
        sorted_distance = (
            aggregation.aggregated_df["Total Distance"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_distance,
            labels={"index": "Instructor", "value": "Total Distance"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Avg. Heartrate")
        sorted_calories = (
            aggregation.aggregated_df["Avg. Heartrate"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_calories,
            labels={"index": "Instructor", "value": "Avg. Heartrate"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    with c2:
        st.subheader("Avg. Speed (mph)")
        sorted_distance = (
            aggregation.aggregated_df["Avg. Speed (mph)"]
            .sort_values(ascending=False)
            .dropna()
        )
        fig = px.bar(
            sorted_distance,
            labels={"index": "Instructor", "value": "Avg. Speed (mph)"},
            log_y=log_scale,
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Calories per Minute vs Avg. Cadence (RPM)")
        fig = px.scatter(
            aggregation.aggregated_df,
            x="Avg. Cadence (RPM)",
            y="Calories per Minute",
            text=aggregation.aggregated_df.index,
        )
        fig.update_traces(marker_size=10)
        st.plotly_chart(fig)

    with c2:
        st.subheader("")
        st.markdown(
            """
        **Note:**
        
        This plot shows how hard an instructor has you working vs how fast they have you pedaling.

        Instructors at the top-left have you working hard but pedaling slowly.

        Instructors at the bottom-right have you pedaling quickly, but not working very hard.
        """
        )


def render_about():
    st.title("About Pelotonnes")
    st.markdown("Pelotonnes is a tool for visualizing your workouts.")
    st.markdown(
        "Pelotonnes is not associated with Peloton Interactive, Inc. "
        + "in any way - except as fans."
    )
    st.markdown(
        "To learn more, or to see the source code, see "
        + "[GitHub](https://github.com/jfkirk/pelotonnes)."
    )


def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Pelotonnes")

    pages = {
        "Upload Workouts": render_upload_workouts,
        "All-Time Stats": render_all_time_stats,
        "Stats By Instructor": render_stats_by_instructor,
        "Stats By Month": render_stats_by_month,
        "About": render_about,
    }
    app_mode = st.sidebar.radio("Tools", options=pages.keys())
    st.session_state["app_mode"] = app_mode

    # Render the selected page
    pages[app_mode]()


main()
