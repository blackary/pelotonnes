import streamlit as st
import plotly.express as px

from aggregation import Aggregation


def render_stats_by_class(aggregation: Aggregation, readable_class_characteristic: str):
    st.title("Stats By {}".format(readable_class_characteristic))

    if "workouts_df" not in st.session_state:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

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
            "Use a logarithmic scale if you have a large number of workouts of some types and few workouts of other types."
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
            This plot shows which classes you spend the most time in vs how hard you work in those workouts. 
            
            Classes in the top-left make you work hard, but you have not spent much time in them.

            Classes in the bottom-right are ones you spend a lot of time in, but don't push you as hard.
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
            This plot shows how hard you work in a class vs how fast you pedal in it.

            Classes at the top-left get you working hard and pedaling slowly - usually at high resistance.

            Classes at the bottom-right get you pedaling your quickest but not working very hard.
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
            st.subheader(
                "Output per Minute by {}".format(readable_class_characteristic)
            )
            sorted_opm = aggregation.aggregated_df["Output per Minute"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_opm,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Output per Minute",
                },
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader(
                "Calories per Minute by {}".format(readable_class_characteristic)
            )
            sorted_cpm = aggregation.aggregated_df["Calories per Minute"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_cpm,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Calories per Minute",
                },
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Avg. Speed (mph) by {}".format(readable_class_characteristic))
            sorted_distance = (
                aggregation.aggregated_df["Avg. Speed (mph)"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_distance,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Speed (mph)",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Avg. Heartrate by {}".format(readable_class_characteristic))
            sorted_calories = (
                aggregation.aggregated_df["Avg. Heartrate"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_calories,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Heartrate",
                },
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("Visualize Totals", expanded=True):

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Minutes by {}".format(readable_class_characteristic))
            sorted_minutes = aggregation.aggregated_df["Total Minutes"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_minutes,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Minutes",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Total Workouts by {}".format(readable_class_characteristic))
            sorted_workouts = (
                aggregation.aggregated_df["Total Workouts"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_workouts,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Workouts",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Output by {}".format(readable_class_characteristic))
            sorted_output = (
                aggregation.aggregated_df["Total Output"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_output,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Output",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            st.subheader("Total Calories by {}".format(readable_class_characteristic))
            sorted_calories = (
                aggregation.aggregated_df["Total Calories"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_calories,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Calories",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Total Distance by {}".format(readable_class_characteristic))
            sorted_distance = (
                aggregation.aggregated_df["Total Distance"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_distance,
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Distance",
                },
                log_y=log_scale,
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.empty()
