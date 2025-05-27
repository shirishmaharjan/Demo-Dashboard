import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px # For more interactive charts like pie charts

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Urban Health Data Hub Demo")

# --- Load Data ---
@st.cache_data # Cache the data loading to improve performance
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        # Calculate prevalence rates (per 1000 people for example)
        df['Diabetes_Prevalence_per_1000'] = (df['Diabetes_Cases'] / df['Population']) * 1000
        df['Hypertension_Prevalence_per_1000'] = (df['Hypertension_Cases'] / df['Population']) * 1000
        df['Flu_Prevalence_per_1000'] = (df['Flu_Cases'] / df['Population']) * 1000
        return df
    except FileNotFoundError:
        st.error(f"Error: The file {file_path} was not found. Make sure it's in the same directory as app.py.")
        return pd.DataFrame()

data = load_data("urban_health_data.csv")

# --- Sidebar ---
st.sidebar.title("Urban Health Data Hub")
st.sidebar.markdown("## Filters & Options")

# Ward Selector
selected_ward = st.sidebar.selectbox(
    "Select Ward (for detailed view & some charts):",
    options=['All Wards'] + list(data['Ward'].unique()) if not data.empty else ['All Wards'],
    index=0
)

# Health Indicator Selector for general charts
indicator_options = {
    "Diabetes Prevalence": "Diabetes_Prevalence_per_1000",
    "Hypertension Prevalence": "Hypertension_Prevalence_per_1000",
    "Flu Prevalence": "Flu_Prevalence_per_1000",
    "Access to Sanitation (%)": "Access_to_Sanitation_Pct",
    "Average Income (USD)": "Avg_Income_USD",
    "Number of Clinics": "Num_Clinics",
    "Average Age": "Avg_Age",
    "Population": "Population"
}
selected_indicator_key = st.sidebar.selectbox(
    "Select Indicator for Bar/Box Plot:",
    options=list(indicator_options.keys()) if not data.empty else [],
    index=0
)
selected_indicator_col = indicator_options.get(selected_indicator_key) # Use .get for safety

# --- Main Dashboard Area ---
st.title("🏙️ Budhanilkantha Municipality - Health Dashboard (Demo)")
st.markdown("A prototype dashboard to visualize urban health data.")

if not data.empty and selected_indicator_col: # Ensure data and indicator are loaded
    # --- Key Metrics ---
    st.header("Key Metrics (Overall City)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Population", f"{data['Population'].sum():,}")
    col2.metric("Avg. Diabetes Prevalence", f"{data['Diabetes_Prevalence_per_1000'].mean():.2f} per 1000")
    col3.metric("Avg. Hypertension Prevalence", f"{data['Hypertension_Prevalence_per_1000'].mean():.2f} per 1000")
    col4.metric("Total Clinics", data['Num_Clinics'].sum())

    st.markdown("---")

    # --- Data View (Expandable) ---
    with st.expander("View Raw Data"):
        if selected_ward == 'All Wards':
            st.dataframe(data)
        else:
            st.dataframe(data[data['Ward'] == selected_ward])

    st.markdown("---")

    # --- Visualizations ---
    st.header("Visualizations")

    # Row 1: Bar Chart and Pie Chart
    st.subheader("Ward Comparisons")
    viz_row1_col1, viz_row1_col2 = st.columns(2)

    with viz_row1_col1:
        st.markdown(f"**{selected_indicator_key} by Ward (Bar Chart)**")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        sns.barplot(x='Ward', y=selected_indicator_col, data=data, ax=ax_bar, palette="viridis")
        plt.xticks(rotation=45, ha='right')
        plt.ylabel(selected_indicator_key)
        plt.title(f"{selected_indicator_key} Across Wards")
        st.pyplot(fig_bar)

    with viz_row1_col2:
        st.markdown("**Population Distribution by Ward (Pie Chart)**")
        fig_pie = px.pie(data, values='Population', names='Ward', title='Population Proportion by Ward',
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Row 2: Scatter Plot and Line Chart
    st.subheader("Relationships and Trends")
    viz_row2_col1, viz_row2_col2 = st.columns(2)

    with viz_row2_col1:
        st.markdown("**Explore Relationships (Scatter Plot)**")
        # Scatter plot options
        x_axis_options = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
        y_axis_options = x_axis_options

        x_axis = st.selectbox("Select X-axis for Scatter Plot:", x_axis_options, index=x_axis_options.index('Avg_Income_USD') if 'Avg_Income_USD' in x_axis_options else 0)
        y_axis = st.selectbox("Select Y-axis for Scatter Plot:", y_axis_options, index=y_axis_options.index('Diabetes_Prevalence_per_1000') if 'Diabetes_Prevalence_per_1000' in y_axis_options else 1)

        if x_axis and y_axis:
            fig_scatter = px.scatter(data, x=x_axis, y=y_axis, color='Ward',
                                     title=f'{y_axis} vs. {x_axis}',
                                     labels={x_axis: x_axis.replace('_', ' '), y_axis: y_axis.replace('_', ' ')},
                                     hover_data=['Population'])
            st.plotly_chart(fig_scatter, use_container_width=True)

    with viz_row2_col2:
        st.markdown("**Indicator Comparison Across Wards (Line Chart)**")
        # Multi-select for line chart indicators
        line_chart_indicators = st.multiselect(
            "Select indicators for Line Chart:",
            options=[col for col in data.columns if pd.api.types.is_numeric_dtype(data[col]) and col not in ['Population', 'Num_Clinics', 'Avg_Age']], # Exclude some less comparable ones
            default=['Diabetes_Prevalence_per_1000', 'Hypertension_Prevalence_per_1000']
        )
        if line_chart_indicators:
            line_df = data.set_index('Ward')[line_chart_indicators]
            st.line_chart(line_df) # Streamlit's native line chart
        else:
            st.info("Select at least one indicator for the line chart.")


    st.markdown("---")

    # Row 3: Box Plot and Histogram
    st.subheader("Distribution Analysis")
    viz_row3_col1, viz_row3_col2 = st.columns(2)

    with viz_row3_col1:
        st.markdown(f"**Distribution of {selected_indicator_key} by Ward (Box Plot)**")
        fig_box, ax_box = plt.subplots(figsize=(10, 6))
        # For a box plot to be meaningful across wards with single values per ward,
        # we'd typically compare distributions if we had multiple data points per ward.
        # Here, we'll show it, but it will look like single lines unless we had more granular data.
        # A more typical use would be: sns.boxplot(x='SomeCategory', y='Value', data=df_with_multiple_obs_per_category)
        # For this demo, we'll use it to compare the single values, which isn't its strongest use case but demonstrates the plot type.
        # A better use for this data would be if selected_indicator_col represented individual patient data, grouped by ward.
        # Since we only have aggregate data per ward, we'll plot the values directly for comparison.
        if selected_indicator_col:
            sns.boxplot(x='Ward', y=selected_indicator_col, data=data, ax=ax_box, palette="Set2")
            # sns.swarmplot(x='Ward', y=selected_indicator_col, data=data, color=".25", ax=ax_box) # Optionally overlay points
            plt.xticks(rotation=45, ha='right')
            plt.ylabel(selected_indicator_key)
            plt.title(f"Distribution of {selected_indicator_key}")
            st.pyplot(fig_box)
        else:
            st.info("Select an indicator for the box plot.")


    with viz_row3_col2:
        st.markdown("**Frequency Distribution (Histogram)**")
        hist_indicator_key = st.selectbox(
            "Select Indicator for Histogram:",
            options=list(indicator_options.keys()),
            index=list(indicator_options.keys()).index('Avg_Age') # Default to Avg_Age
        )
        hist_indicator_col = indicator_options.get(hist_indicator_key)
        if hist_indicator_col:
            fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
            sns.histplot(data[hist_indicator_col], kde=True, ax=ax_hist, color="skyblue")
            plt.xlabel(hist_indicator_key)
            plt.ylabel("Frequency")
            plt.title(f"Distribution of {hist_indicator_key}")
            st.pyplot(fig_hist)
        else:
            st.info("Select an indicator for the histogram.")

    st.markdown("---")

    # Correlation Matrix (kept from previous example)
    st.subheader("Correlation Analysis")
    if len(data.columns) > 1:
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            correlation_matrix = data[numeric_cols].corr()
            fig_corr, ax_corr = plt.subplots(figsize=(10,8)) # Increased size
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5, ax=ax_corr)
            plt.title("Correlation Matrix of Numeric Features")
            st.pyplot(fig_corr)
        else:
            st.write("Not enough numeric columns for a correlation matrix.")

    # Detailed view for a selected ward
    if selected_ward != 'All Wards':
        st.subheader(f"Detailed Metrics for {selected_ward}")
        ward_data_selected = data[data['Ward'] == selected_ward].iloc[0]
        details_col1, details_col2 = st.columns(2)
        with details_col1:
            st.metric("Population", f"{ward_data_selected['Population']:,}")
            st.metric("Diabetes Cases", f"{ward_data_selected['Diabetes_Cases']} ({ward_data_selected['Diabetes_Prevalence_per_1000']:.2f} per 1000)")
            st.metric("Hypertension Cases", f"{ward_data_selected['Hypertension_Cases']} ({ward_data_selected['Hypertension_Prevalence_per_1000']:.2f} per 1000)")
        with details_col2:
            st.metric("Flu Cases", f"{ward_data_selected['Flu_Cases']} ({ward_data_selected['Flu_Prevalence_per_1000']:.2f} per 1000)")
            st.metric("Access to Sanitation", f"{ward_data_selected['Access_to_Sanitation_Pct']}%")
            st.metric("Average Income", f"${ward_data_selected['Avg_Income_USD']:,}")
            st.metric("Number of Clinics", ward_data_selected['Num_Clinics'])

else:
    st.warning("Data could not be loaded or indicator not selected. Please check the CSV file and selections.")

st.sidebar.markdown("---")
st.sidebar.info(
    "This is a simplified demo of an Urban Health Data Hub. "
    "Real-world hubs involve complex data integration, privacy considerations, "
    "and more advanced analytics."
)