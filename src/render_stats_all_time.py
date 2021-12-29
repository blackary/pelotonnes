import streamlit as st


def render_stats_all_time():
    st.title("All-Time Stats")

    if "workouts_df" not in st.session_state:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

    workouts_df = st.session_state["workouts_df"]
    all_time_df = st.session_state["workouts_aggregation_all_time"].aggregated_df

    st.dataframe(st.session_state["workouts_aggregation_all_time"].styled_aggregated_df)

    n_workouts = all_time_df["Total Workouts"].sum()
    n_instructors = len(
        st.session_state["workouts_aggregation_by_instructor"].aggregated_df
    )
    n_live = len(workouts_df[workouts_df["Live/On-Demand"] == "Live"])
    n_on_demand = len(workouts_df[workouts_df["Live/On-Demand"] == "On Demand"])
    st.markdown(
        f"You have completed **{n_workouts}** cycling workouts"
        + f" with **{n_instructors}** different instructors. "
        + f"You have completed **{n_live}** live workouts and **{n_on_demand}** "
        + "on-demand workouts."
    )

    total_mins = all_time_df["Total Minutes"].sum()
    total_hrs = total_mins / 60
    total_days = total_hrs / 24
    total_miles = all_time_df["Total Distance"].sum()
    st.markdown(
        (
            "You have cycled for **{:.0f}** minutes (that's **{:.2f}** hours, or "
            + "**{:.2f}** whole days) and rode **{:.2f}** miles in that time at an"
            + " all-time average speed of **{:.2f}** mph."
        ).format(
            total_mins,
            total_hrs,
            total_days,
            total_miles,
            all_time_df["Avg. Speed (mph)"].mean(),
        )
    )

    total_london_to_paris = total_miles / 300
    total_pacific_coast = total_miles / 1857.6
    total_tour_de_france = total_miles / 2121.6
    total_across_usa = total_miles / 3700
    total_to_moon = total_miles / 240000
    st.markdown(
        """
    That's approximately:
    - **{:.2f}** Chunnel rides from London to Paris.
    - **{:.2f}** Pacific Coast Bike Route rides from Vancouver to Imperial Beach.
    - **{:.2f}** Tours de France.
    - **{:.2f}** Great American Rail Trail rides across the USA.
    - **{:.2f}** Apollo 11 rides to the Moon.
    """.format(
            total_london_to_paris,
            total_pacific_coast,
            total_tour_de_france,
            total_across_usa,
            total_to_moon,
        )
    )

    total_output = all_time_df["Total Output"].sum()
    total_calories = all_time_df["Total Calories"].sum()
    st.markdown(
        (
            "You've output a total of **{:.0f}** kilojoules and burned a total of"
            + " **{:.0f}** kilocalories in that time."
        ).format(total_output, total_calories)
    )

    total_iphone_years = total_output / 35.6
    total_lbs_of_fat = total_calories / 3500
    total_kg_to_orbit = total_output / 63000
    total_home_days = total_output / 105682
    st.markdown(
        """
    That's approximately:
    - Enough energy to power an iPhone for **{:.0f}** days.
    - **{:.2f}** pounds of pure body fat in kilocalories.
    - **{:.2f}**x the energy to accelerate 1kg to escape velocity from Earth.
    - Enough energy to power the average American home for **{:.2f}** days.
    """.format(
            total_iphone_years, total_lbs_of_fat, total_kg_to_orbit, total_home_days
        )
    )

    st.markdown("**Keep it up!**")
