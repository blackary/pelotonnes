from collections import defaultdict
import datetime

import dateparser
import pandas as pd
import streamlit as st


def datetime_to_day_index(datetime_obj):
    return datetime_obj.date()


def datetime_to_week_index(datetime_obj):
    return datetime.datetime.strptime(
        "{}-{}-1".format(datetime_obj.isocalendar()[0], datetime_obj.isocalendar()[1]),
        "%Y-%W-%w",
    ).date()


def datetime_to_month_index(datetime_obj):
    return datetime_obj.strftime("%Y-%m")


def datetime_to_year_index(datetime_obj):
    return datetime_obj.year


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
    workouts_df["c_day"] = workouts_df["c_datetime"].apply(datetime_to_day_index)
    workouts_df["c_week"] = workouts_df["c_datetime"].apply(datetime_to_week_index)
    workouts_df["c_month"] = workouts_df["c_datetime"].apply(datetime_to_month_index)
    workouts_df["c_year"] = workouts_df["c_datetime"].apply(datetime_to_year_index)
    workouts_df["c_datetime"] = pd.to_datetime(workouts_df["c_datetime"], utc=True)

    date_range = pd.Series(
        pd.date_range(start=workouts_df["c_day"].min(), end=workouts_df["c_day"].max())
    )

    # After processing, reassign the processed DF to session_state
    st.session_state["workouts_df"] = workouts_df
    st.session_state["workouts_aggregation_all_time"] = Aggregation(workouts_df)
    st.session_state["workouts_aggregation_by_year"] = Aggregation(
        workouts_df, "c_year", extra_indices=date_range.apply(datetime_to_year_index)
    )
    st.session_state["workouts_aggregation_by_month"] = Aggregation(
        workouts_df, "c_month", extra_indices=date_range.apply(datetime_to_month_index)
    )
    st.session_state["workouts_aggregation_by_week"] = Aggregation(
        workouts_df, "c_week", extra_indices=date_range.apply(datetime_to_week_index)
    )
    st.session_state["workouts_aggregation_by_day"] = Aggregation(
        workouts_df, "c_day", extra_indices=date_range.apply(datetime_to_day_index)
    )
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
    def __init__(
        self,
        workouts_df,
        group_by=None,
        extra_indices=None,
    ):
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
        total_resistance = defaultdict(lambda: 0.0)
        total_resistance_minutes = defaultdict(lambda: 0.0)

        if extra_indices is not None:
            for index in extra_indices:
                total_workouts[index] = 0
                total_time[index] = 0.0
                total_distance[index] = 0.0
                total_output[index] = 0.0
                total_output_minutes[index] = 0.0
                total_calories[index] = 0.0
                total_calories_minutes[index] = 0.0
                total_hr[index] = 0.0
                total_hr_minutes[index] = 0.0
                total_speed[index] = 0.0
                total_speed_minutes[index] = 0.0
                total_cadence[index] = 0.0
                total_cadence_minutes[index] = 0.0
                total_resistance[index] = 0.0
                total_resistance_minutes[index] = 0.0

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
            try:
                if not pd.isna(row["Distance (mi)"]):
                    total_distance[key] += row["Distance (mi)"]
            except KeyError:
                if not pd.isna(row["Distance (km)"]):
                    total_distance[key] += row["Distance (km)"] * 0.621371

            duration = None
            if not pd.isna(row["Length (minutes)"]) and (
                row["Length (minutes)"] != "None"
            ):
                duration = int(row["Length (minutes)"])
            elif row["Length (minutes)"] == "None":
                duration = (row["Distance (mi)"] / row["Avg. Speed (mph)"]) * 60

            if duration is not None:
                total_time[key] += duration
                # These are nested inside the Length if-clause because we need to
                # weight the values by the workout length. Length is missing for scenic
                #  rides.
                if not pd.isna(row["Total Output"]):
                    total_output[key] += row["Total Output"]
                    total_output_minutes[key] += duration
                if not pd.isna(row["Calories Burned"]):
                    total_calories[key] += row["Calories Burned"]
                    total_calories_minutes[key] += duration
                if not pd.isna(row["Avg. Heartrate"]):
                    total_hr[key] += duration * row["Avg. Heartrate"]
                    total_hr_minutes[key] += duration

                try:
                    if not pd.isna(row["Avg. Speed (mph)"]):
                        total_speed[key] += duration * row["Avg. Speed (mph)"]
                        total_speed_minutes[key] += duration
                except KeyError:
                    if not pd.isna(row["Avg. Speed (kph)"]):
                        total_speed[key] += (
                            duration * row["Avg. Speed (kph)"] * 0.621371
                        )
                        total_speed_minutes[key] += duration

                if not pd.isna(row["Avg. Cadence (RPM)"]):
                    total_cadence[key] += duration * row["Avg. Cadence (RPM)"]
                    total_cadence_minutes[key] += duration
                if not pd.isna(row["Avg. Resistance"]):
                    total_resistance[key] += duration * float(
                        row["Avg. Resistance"].strip("%")
                    )
                    total_resistance_minutes[key] += duration

        self.aggregated_df = pd.DataFrame(
            {
                "Total Workouts": pd.Series(total_workouts),
                "Total Minutes": pd.Series(total_time),
                "Total Distance": pd.Series(total_distance),
                "Total Output": pd.Series(total_output),
                "Total Calories": pd.Series(total_calories),
                "Avg. Output (watts)": (100.0 / 6.0)
                * pd.Series(total_output)
                / pd.Series(total_output_minutes),
                "Avg. Output (kj/m)": pd.Series(total_output)
                / pd.Series(total_output_minutes),
                "Avg. Calories per Minute": pd.Series(total_calories)
                / pd.Series(total_calories_minutes),
                "Avg. Heartrate": pd.Series(total_hr) / pd.Series(total_hr_minutes),
                "Avg. Speed (mph)": pd.Series(total_speed)
                / pd.Series(total_speed_minutes),
                "Avg. Cadence (RPM)": pd.Series(total_cadence)
                / pd.Series(total_cadence_minutes),
                "Avg. Resistance": pd.Series(total_resistance)
                / pd.Series(total_resistance_minutes),
            }
        ).sort_index()
        self.styled_aggregated_df = self.aggregated_df.style.format(
            {
                "Total Workouts": "{:,.0f}",
                "Total Minutes": "{:,.0f}",
                "Total Distance": "{:,.2f}",
                "Total Output": "{:,.0f}",
                "Total Calories": "{:,.0f}",
                "Avg. Output (watts)": "{:,.2f}",
                "Avg. Output (kj/m)": "{:,.2f}",
                "Avg. Calories per Minute": "{:,.2f}",
                "Avg. Heartrate": "{:,.2f}",
                "Avg. Speed (mph)": "{:,.2f}",
                "Avg. Cadence (RPM)": "{:,.2f}",
            },
        )
