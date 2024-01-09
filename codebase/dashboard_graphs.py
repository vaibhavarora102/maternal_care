import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

class MaternalHealthDashboard:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint
        self.maternal_health_data = self.fetch_data()

    def fetch_data(self):
        try:
            response = requests.get(self.api_endpoint)
            if response.status_code == 200:
                data = pd.read_csv(StringIO(response.text))
                return data
            else:
                st.error(f"Failed to fetch data. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error during API request: {e}")
            return None

    def drop_all_india(self, df):
        return df[df["State/UT"] != "All India"]

    def create_bubble_chart(self):
        df = self.drop_all_india(self.maternal_health_data)
        st.subheader("Bubble Chart provides a visual representation of how well different regions have performed in achieving institutional deliveries compared to their assessed needs")
        fig = px.scatter(
            df,
            x="Need Assessed (2019-20) - (A)",
            y="Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)",
            size="% Achvt of need assessed (2019-20) - (E=(B/A)*100)",
            color="State/UT",
            hover_name="State/UT",
            labels={
                "Need Assessed (2019-20) - (A)": "Need Assessed",
                "Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)": "Achievement",
                "% Achvt of need assessed (2019-20) - (E=(B/A)*100)": "% Achievement",
            },
        )
        st.plotly_chart(fig)

    def create_pie_chart(self):
        st.subheader("Visualize the proportion of institutional deliveries across different states/union territories (UTs) during the specified period (April to June 2019-20)")
        df = self.drop_all_india(self.maternal_health_data)

        fig = px.pie(
            df,
            names="State/UT",
            values="Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)",
            labels={"Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)": "Institutional Deliveries"}
        )
        st.plotly_chart(fig)

    def get_bubble_chart_data(self):
        content = """
Bubble Chart provides a visual representation of how well different regions have performed in achieving institutional deliveries compared to their assessed needs. 

The Bubble Chart presented in the example is visualizing maternal health data, particularly focusing on the achievement of institutional deliveries in different states or union territories during the period of April to June for the year 2019-20. Let's break down what the chart is showing:

1: X-axis (horizontal axis): Need Assessed (2019-20) - (A)

This axis represents the assessed needs for maternal health in different states or union territories. Each point on the X-axis corresponds to a specific region, and the position along the axis indicates the magnitude of the assessed needs.

2: Y-axis (vertical axis): Achievement during April to June - Total Institutional Deliveries - (2019-20) - (B)

The Y-axis represents the actual achievement in terms of the number of institutional deliveries during the specified period (April to June) in the year 2019-20. Each point on the Y-axis corresponds to a specific region, and the position along the axis indicates the magnitude of the achieved institutional deliveries.

3: Bubble Size: % Achvt of need assessed (2019-20) - (E=(B/A)100)

The size of each bubble is determined by the percentage achievement of the assessed needs, calculated as % Achvt = (B/A) * 100. Larger bubbles indicate a higher percentage of achievement compared to the assessed needs, suggesting a better performance in delivering institutional healthcare.

4: Color: State/UT

Each bubble is color-coded based on the respective state or union territory it represents. Different colors distinguish between regions, making it easy to identify and compare data points for different states or union territories.

5: Hover Name: State/UT

Hovering over a bubble reveals additional information, such as the name of the state or union territory it represents. This interactive feature allows users to explore specific data points on the chart.
"""
        return content
    
    def get_pie_graph_data(self):
        content = """
visualize the proportion of institutional deliveries across different states/union territories (UTs) during the specified period (April to June 2019-20). Let's break down the components of the graph and its interpretation:

Key Components:
Slices of the Pie:

Each slice of the pie represents a specific state or UT.
Size of Slices:

The size of each slice corresponds to the proportion of institutional deliveries achieved during April to June 2019-20 for the respective state or UT.
Hover Information:

Hovering over a slice provides additional information, such as the name of the state/UT and the exact proportion of institutional deliveries."""
        return content


if __name__ == "__main__":
    api_key = "579b464db66ec23bdd00000139b0d95a6ee4441c5f37eeae13f3a0b2"
    api_endpoint = api_endpoint= f"https://api.data.gov.in/resource/6d6a373a-4529-43e0-9cff-f39aa8aa5957?api-key={api_key}&format=csv"
    dashboard = MaternalHealthDashboard(api_endpoint)

    if dashboard.maternal_health_data is not None:
        dashboard.create_bubble_chart()
        dashboard.create_stacked_bar_chart()