import streamlit as st
import plotly.express as px


def render_stats_by_time(aggregation, readable_time_unit):
    st.title(f"Stats By {readable_time_unit}")

    if aggregation is None:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

    st.dataframe(aggregation.styled_aggregated_df)

    n_workouts = len(aggregation.aggregated_df)
    if n_workouts < 2:
        st.markdown(
            "Only found data for **{}** {}.".format(n_workouts, readable_time_unit)
        )
        st.markdown("Keep cycling and come back soon for more graphs!")
        return

    with st.expander("Visualize Averages", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(
                aggregation.aggregated_df["Avg. Resistance"].dropna(),
                title="Avg. Resistance (%) by {}".format(readable_time_unit),
                labels={
                    "index": f"{readable_time_unit}",
                    "value": "Avg. Resistance (%)",
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
            fig = px.line(
                aggregation.aggregated_df["Avg. Cadence (RPM)"].dropna(),
                title="Avg. Cadence (RPM) by {}".format(readable_time_unit),
                labels={
                    "index": f"{readable_time_unit}",
                    "value": "Avg. Cadence (RPM)",
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
            fig = px.line(
                aggregation.aggregated_df["Avg. Speed (mph)"].dropna(),
                title="Avg. Speed (mph) by {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Avg. Speed (mph)"},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.line(
                aggregation.aggregated_df["Avg. Heartrate"].dropna(),
                title="Avg. Heartrate by {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Avg. Heartrate"},
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
            fig = px.line(
                aggregation.aggregated_df["Total Minutes"].dropna(),
                title="Total Minutes per {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Total Minutes"},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.line(
                aggregation.aggregated_df["Total Output"].dropna(),
                title="Total Output per {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Total Output"},
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
            fig = px.line(
                aggregation.aggregated_df["Output (watts)"].dropna(),
                title="Output (watts) by {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Output (watts)"},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.line(
                aggregation.aggregated_df["Total Workouts"].dropna(),
                title="Total Workouts per {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Total Workouts"},
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
            fig = px.line(
                aggregation.aggregated_df["Total Calories"].dropna(),
                title="Total Calories per {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Total Calories"},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = px.line(
                aggregation.aggregated_df["Total Distance"].dropna(),
                title="Total Distance per {}".format(readable_time_unit),
                labels={"index": f"{readable_time_unit}", "value": "Total Distance"},
            )
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
