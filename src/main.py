import pandas as pd
import streamlit as st

from aggregation import process_workouts_df
from render_stats_by_time import render_stats_by_time
from render_stats_by_class import render_stats_by_class
from render_stats_all_time import render_stats_all_time


def render_upload_workouts():
    st.title("Upload Workouts")
    workouts_guide = """
    1. Go to https://members.onepeloton.com/profile/workouts.
    2. Click 'DOWNLOAD WORKOUTS' and save your workouts.csv file.
    3. Upload your saved workouts.csv file below.
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
        st.markdown("Processing your workouts...")
        process_workouts_df()
        st.markdown("{} workouts processed!".format(len(workouts_df)))

    if "workouts_df" in st.session_state:
        st.subheader(
            "Upload complete! Use the tools in the sidebar to analyze your workouts."
        )
        st.subheader("Cycling Workouts")
        st.dataframe(st.session_state["workouts_df"])


def render_stats_by_year():
    return render_stats_by_time(
        aggregation=st.session_state.get("workouts_aggregation_by_year", None),
        readable_time_unit="Year",
    )


def render_stats_by_month():
    return render_stats_by_time(
        aggregation=st.session_state.get("workouts_aggregation_by_month", None),
        readable_time_unit="Month",
    )


def render_stats_by_week():
    return render_stats_by_time(
        aggregation=st.session_state.get("workouts_aggregation_by_week", None),
        readable_time_unit="Week",
    )


def render_stats_by_day():
    return render_stats_by_time(
        aggregation=st.session_state.get("workouts_aggregation_by_day", None),
        readable_time_unit="Day",
    )


def render_stats_by_instructor():
    return render_stats_by_class(
        aggregation=st.session_state.get("workouts_aggregation_by_instructor", None),
        readable_class_characteristic="Instructor",
    )


def render_stats_by_class_type():
    return render_stats_by_class(
        aggregation=st.session_state.get("workouts_aggregation_by_class_type", None),
        readable_class_characteristic="Class Type",
    )


def render_stats_by_class_length():
    return render_stats_by_class(
        aggregation=st.session_state.get("workouts_aggregation_by_class_length", None),
        readable_class_characteristic="Class Length",
    )


def render_about():
    st.title("About Pelotonnes")
    st.markdown("Pelotonnes is a tool for visualizing your cycling workouts.")
    st.markdown(
        "Pelotonnes is not associated with Peloton Interactive, Inc. "
        + "- except as fans."
    )
    st.markdown("Pelotonnes does not log or save any of your personal data.")
    st.markdown(
        "To see the source code, contribute, or report an issue,"
        + " [see GitHub](https://github.com/jfkirk/pelotonnes)."
    )
    st.markdown("To learn more, [message James](https://twitter.com/Jiminy_Kirket).")


def main():
    st.set_page_config(page_title="Pelotonnes", layout="wide")
    st.sidebar.title("Pelotonnes")

    pages = {
        "Upload Workouts": render_upload_workouts,
        "All-Time Stats": render_stats_all_time,
        "Stats By Instructor": render_stats_by_instructor,
        "Stats By Class Type": render_stats_by_class_type,
        "Stats By Class Length": render_stats_by_class_length,
        "Stats By Year": render_stats_by_year,
        "Stats By Month": render_stats_by_month,
        "Stats By Week": render_stats_by_week,
        "Stats By Day": render_stats_by_day,
        "About": render_about,
    }
    app_mode = st.sidebar.radio("Tools", options=pages.keys())
    st.session_state["app_mode"] = app_mode

    # Render the selected page
    pages[app_mode]()


main()
