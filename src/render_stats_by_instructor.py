import streamlit as st
import plotly.express as px


def render_stats_by_instructor():
    st.title("Stats By Instructor")

    if "workouts_df" not in st.session_state:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

    aggregation = st.session_state["workouts_aggregation_by_instructor"]
    st.dataframe(aggregation.aggregated_df)

    with st.expander("Visualization Options"):
        log_scale = st.checkbox(
            "Use a logarithmic scale for cumulative statistics",
            value=(
                True
                if aggregation.aggregated_df["Total Workouts"].max() >= 100
                else False
            ),
        )
        st.markdown(
            "Use a logarithmic scale if you have a large number of workouts with your "
            + "top instructors and few workouts with others."
        )

    with st.expander("Visualize Output and Performance", expanded=True):

        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                aggregation.aggregated_df,
                x="Total Minutes",
                y="Output per Minute",
                text=aggregation.aggregated_df.index,
                log_x=log_scale,
            )
            fig.update_traces(marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Output per Minute vs Total Minutes")
            st.markdown(
                """
            This plot shows which instructors you spend the most time with vs how hard you work in their workouts. 
            
            Instructors in the top-left make you work hard, but you have not spent much time with them.

            Instructors in the bottom-right are ones you spend a lot of time with, but don't push you as hard.
            """
            )

        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                aggregation.aggregated_df,
                x="Avg. Cadence (RPM)",
                y="Output per Minute",
                text=aggregation.aggregated_df.index,
            )
            fig.update_traces(marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Output per Minute vs Avg. Cadence (RPM)")
            st.markdown(
                """
            This plot shows how hard you work with an instructor vs how fast you pedal with them.

            Instructors at the top-left get you working hard and pedaling slowly - usually at high resistance.

            Instructors at the bottom-right get you pedaling your quickest but not working very hard.
            """
            )

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
            fig.update_traces(marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Calories per Minute vs Avg. Cadence (RPM)")
            fig = px.scatter(
                aggregation.aggregated_df,
                x="Avg. Cadence (RPM)",
                y="Calories per Minute",
                text=aggregation.aggregated_df.index,
                log_x=log_scale,
            )
            fig.update_traces(marker_size=20)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Output per Minute by Instructor")
            sorted_opm = aggregation.aggregated_df["Output per Minute"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_opm, labels={"index": "Instructor", "value": "Output per Minute"}
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Calories per Minute by Instructor")
            sorted_cpm = aggregation.aggregated_df["Calories per Minute"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_cpm,
                labels={"index": "Instructor", "value": "Calories per Minute"},
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Avg. Speed (mph) by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Avg. Heartrate by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("Visualize Totals", expanded=True):

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Minutes by Instructor")
            sorted_minutes = aggregation.aggregated_df["Total Minutes"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_minutes,
                labels={"index": "Instructor", "value": "Total Minutes"},
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Total Workouts by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Output by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Total Calories by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Distance by Instructor")
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
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.empty()
