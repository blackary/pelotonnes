from collections import defaultdict
import datetime

import dateparser
import pandas as pd
import streamlit as st


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
    workouts_df["c_day"] = workouts_df["c_datetime"].apply(lambda x: x.date())
    workouts_df["c_week"] = workouts_df["c_datetime"].apply(
        lambda x: datetime.datetime.strptime(
            "{}-{}-1".format(x.year, x.isocalendar()[1]), "%Y-%W-%w"
        ).date()
    )
    workouts_df["c_month"] = workouts_df["c_datetime"].apply(
        lambda x: x.strftime("%Y-%m")
    )
    workouts_df["c_year"] = workouts_df["c_datetime"].apply(lambda x: int(x.year))

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
    st.session_state["workouts_aggregation_by_day"] = Aggregation(workouts_df, "c_day")
    st.session_state["workouts_aggregation_by_instructor"] = Aggregation(
        workouts_df, "Instructor Name"
    )
    st.session_state["workouts_aggregation_by_class_type"] = Aggregation(
        workouts_df, "Type"
    )
    st.session_state["workouts_aggregation_by_class_length"] = Aggregation(
        workouts_df, "Length (minutes)"
    )


class Aggregation(object):
    def __init__(self, workouts_df, group_by=None):
        self.group_by = group_by

        # These accumulators hold the values over the iterations
        total_workouts = defaultdict(lambda: 0)
        total_time = defaultdict(lambda: 0.0)
        total_distance = defaultdict(lambda: 0.0)
        total_output = defaultdict(lambda: 0.0)
        total_output_minutes = defaultdict(lambda: 0.0)
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
            if not pd.isna(row["Length (minutes)"]):
                total_time[key] += row["Length (minutes)"]
                # These are nested inside the Length if-clause because we need to
                # weight the values by the workout length
                if not pd.isna(row["Total Output"]):
                    total_output[key] += row["Total Output"]
                    total_output_minutes[key] += row["Length (minutes)"]
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
                "Output per Minute": pd.Series(total_output)
                / pd.Series(total_output_minutes),
                "Calories per Minute": pd.Series(total_calories)
                / pd.Series(total_calories_minutes),
                "Avg. Heartrate": pd.Series(total_hr) / pd.Series(total_hr_minutes),
                "Avg. Speed (mph)": pd.Series(total_speed)
                / pd.Series(total_speed_minutes),
                "Avg. Cadence (RPM)": pd.Series(total_cadence)
                / pd.Series(total_cadence_minutes),
            }
        ).sort_index()
