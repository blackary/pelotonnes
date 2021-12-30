import streamlit as st
import plotly.express as px

from aggregation import Aggregation


def render_stats_by_class(aggregation: Aggregation, readable_class_characteristic: str):
    st.title("Stats By {}".format(readable_class_characteristic))

    if aggregation is None:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

    st.dataframe(aggregation.styled_aggregated_df)

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
            "Use a logarithmic scale if you have a large number of workouts of some "
            + "types and very few workouts of other types."
        )

    # When slicing by Instructor, this helps visualize without as much crowding
    scatter_text = aggregation.aggregated_df.index.to_series()
    if readable_class_characteristic == "Instructor":
        scatter_text = scatter_text.apply(lambda x: x.split(" ")[0])

    with st.expander("Visualize Output and Performance", expanded=True):

        c1, c2 = st.columns([3, 2])
        with c1:
            fig = px.scatter(
                aggregation.aggregated_df,
                x="Total Minutes",
                y="Output (watts)",
                text=scatter_text,
                log_x=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_traces(textposition="top center", marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Output (watts) vs Total Minutes")
            st.markdown(
                "This plot shows which classes you spend the most time in vs how hard"
                + " you work in those workouts. "
            )
            st.markdown(
                "Classes in the top-left make you work hard, but you have not spent "
                + "much time in them. Maybe try them out some more!"
            )

            st.markdown(
                "Classes in the bottom-right are ones you spend a lot of time in, but "
                + "don't push you as hard. You may want to phase these out of your "
                + "routines."
            )

        c1, c2 = st.columns([3, 2])
        with c1:
            fig = px.scatter(
                aggregation.aggregated_df,
                x="Avg. Cadence (RPM)",
                y="Avg. Resistance",
                text=scatter_text,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_traces(textposition="top center", marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Avg. Resistance (%) vs Avg. Cadence (RPM)")
            st.markdown(
                "This plot shows how hard you work in a class vs how fast you pedal "
                + "in it."
            )
            st.markdown(
                "Classes at the top-left get you pedaling slowly and working hard at a "
                + "high resistance - good for putting the work in."
            )
            st.markdown(
                "Classes at the bottom-right get you pedaling quickly but working at "
                + "a low resistance - good for stretching your legs."
            )

        c1, c2 = st.columns(2)
        with c1:
            fig = px.scatter(
                aggregation.aggregated_df,
                title="Calories per Minute vs Total Minutes",
                x="Total Minutes",
                y="Calories per Minute",
                text=scatter_text,
                log_x=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_traces(textposition="top center", marker_size=20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.scatter(
                aggregation.aggregated_df,
                title="Calories per Minute vs Avg. Cadence (RPM)",
                x="Avg. Cadence (RPM)",
                y="Calories per Minute",
                text=scatter_text,
                log_x=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_traces(textposition="top center", marker_size=20)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sorted_opm = aggregation.aggregated_df["Output (watts)"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_opm,
                title="Output (watts) by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Output (watts)",
                },
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            sorted_cpm = aggregation.aggregated_df["Calories per Minute"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_cpm,
                title="Calories per Minute by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Calories per Minute",
                },
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sorted_distance = (
                aggregation.aggregated_df["Avg. Speed (mph)"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_distance,
                title="Avg. Speed (mph) by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Speed (mph)",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            sorted_calories = (
                aggregation.aggregated_df["Avg. Heartrate"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_calories,
                title="Avg. Heartrate by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Heartrate",
                },
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sorted_resistance = (
                aggregation.aggregated_df["Avg. Resistance"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_resistance,
                title="Avg. Resistance (%) by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Resistance (%)",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            sorted_cadence = (
                aggregation.aggregated_df["Avg. Cadence (RPM)"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_cadence,
                title="Avg. Cadence (RPM) by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Avg. Cadence (RPM)",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with st.expander("Visualize Totals", expanded=True):

        c1, c2 = st.columns(2)
        with c1:
            sorted_minutes = aggregation.aggregated_df["Total Minutes"].sort_values(
                ascending=False
            )
            fig = px.bar(
                sorted_minutes,
                title="Total Minutes by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Minutes",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            sorted_workouts = (
                aggregation.aggregated_df["Total Workouts"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_workouts,
                title="Total Workouts by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Workouts",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sorted_output = (
                aggregation.aggregated_df["Total Output"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_output,
                title="Total Output by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Output",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            sorted_calories = (
                aggregation.aggregated_df["Total Calories"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_calories,
                title="Total Calories by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Calories",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            sorted_distance = (
                aggregation.aggregated_df["Total Distance"]
                .sort_values(ascending=False)
                .dropna()
            )
            fig = px.bar(
                sorted_distance,
                title="Total Distance by {}".format(readable_class_characteristic),
                labels={
                    "index": readable_class_characteristic,
                    "value": "Total Distance",
                },
                log_y=log_scale,
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.empty()
