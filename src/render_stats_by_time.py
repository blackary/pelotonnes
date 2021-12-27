import streamlit as st
import plotly.express as px


def render_stats_by_time(aggregation, readable_time_unit):
    st.title(f"Stats By {readable_time_unit}")

    if "workouts_df" not in st.session_state:
        st.markdown(
            "Workouts have not been uploaded. See 'Upload Workouts' to the left."
        )
        return

    st.dataframe(aggregation.aggregated_df)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total Minutes per {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Total Minutes"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Total Minutes"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Total Output per {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Total Output"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Total Output"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Output per Minute by Day")
        fig = px.line(
            aggregation.aggregated_df["Output per Minute"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Output per Minute"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Total Workouts per {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Total Workouts"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Total Workouts"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Total Calories per {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Total Calories"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Total Calories"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Total Distance per {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Total Distance"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Total Distance"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Avg. Heartrate by {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Avg. Heartrate"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Avg. Heartrate"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Avg. Speed (mph) by {}".format(readable_time_unit))
        fig = px.line(
            aggregation.aggregated_df["Avg. Speed (mph)"].dropna(),
            labels={"index": f"{readable_time_unit}", "value": "Avg. Speed (mph)"},
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
