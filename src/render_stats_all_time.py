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

    st.markdown(
        f"You have completed **{all_time_df['Total Workouts'].sum()}** cycling workouts with **{len(st.session_state['workouts_aggregation_by_instructor'].aggregated_df)}** different instructors."
    )

    total_mins = all_time_df["Total Minutes"].sum()
    total_hrs = total_mins / 60
    total_days = total_hrs / 24
    total_miles = all_time_df["Total Distance"].sum()
    st.markdown(
        "You have cycled for **{:.0f}** minutes (that's **{:.2f}** hours, or **{:.2f}** whole days) and rode **{:.2f}** miles in that time.".format(
            total_mins, total_hrs, total_days, total_miles
        )
    )

    st.markdown(
        "That makes for an all-time average speed of **{:.2f}** mph.".format(
            all_time_df["Avg. Speed (mph)"].mean()
        )
    )

    n_live = len(workouts_df[workouts_df["Live/On-Demand"] == "Live"])
    n_on_demand = len(workouts_df[workouts_df["Live/On-Demand"] == "On Demand"])
    st.markdown(
        "You have completed **{}** live workouts and **{}** on-demand workouts.".format(
            n_live, n_on_demand
        )
    )

    total_calories = all_time_df["Total Calories"].sum()
    total_pizzas = total_calories / 2240
    total_lbs_of_fat = total_calories / 3500
    st.markdown(
        "You've burned a total of **{:.0f}** calories in that time - that's equivalent to **{:.2f}** Large Pepperoni Pizzas from Domino's or **{:.2f}lbs** of body fat.".format(
            total_calories, total_pizzas, total_lbs_of_fat
        )
    )

    st.markdown("Keep it up!")

    st.dataframe(st.session_state["workouts_aggregation_all_time"].styled_aggregated_df)
