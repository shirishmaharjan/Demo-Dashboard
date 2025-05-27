import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Urban Health Data Hub Demo")

# --- 1. Translations Dictionary ---
translations = {
    "English": {
        "hub_title": "Urban Health Data Hub",
        "filters_options": "Filters & Options",
        "select_ward": "Select Ward:",
        "all_wards": "All Wards",
        "select_indicator_bar_box": "Select Indicator for Bar/Box Plot:",
        "dashboard_title": "🏙️ Budhanilkantha Health Dashboard (Demo)",
        "dashboard_subtitle": "A prototype dashboard to visualize urban health data.",
        "key_metrics_header": "Key Metrics (Overall City)",
        "total_population": "Total Population",
        "avg_diabetes_prev": "Avg. Diabetes Prevalence",
        "avg_hypertension_prev": "Avg. Hypertension Prevalence",
        "total_clinics": "Total Clinics",
        "view_raw_data": "View Raw Data",
        "ward_comparisons": "Ward Comparisons",
        "bar_chart_title": "{indicator} by Ward (Bar Chart)", # Placeholder for indicator
        "population_distribution_pie": "Population Distribution by Ward (Pie Chart)",
        "relationships_trends": "Relationships and Trends",
        "explore_relationships_scatter": "Explore Relationships (Scatter Plot)",
        "select_x_scatter": "Select X-axis for Scatter Plot:",
        "select_y_scatter": "Select Y-axis for Scatter Plot:",
        "scatter_plot_title": "{y_axis} vs. {x_axis}", # Placeholders
        "indicator_comparison_line": "Indicator Comparison Across Wards (Line Chart)",
        "select_indicators_line": "Select indicators for Line Chart:",
        "info_select_indicator_line": "Select at least one indicator for the line chart.",
        "distribution_analysis": "Distribution Analysis",
        "distribution_by_ward_box": "Distribution of {indicator} by Ward (Box Plot)",
        "info_select_indicator_box": "Select an indicator for the box plot.",
        "frequency_distribution_hist": "Frequency Distribution (Histogram)",
        "select_indicator_hist": "Select Indicator for Histogram:",
        "hist_plot_title": "Distribution of {indicator}",
        "info_select_indicator_hist": "Select an indicator for the histogram.",
        "correlation_analysis": "Correlation Analysis",
        "correlation_matrix_title": "Correlation Matrix of Numeric Features",
        "no_numeric_cols_corr": "Not enough numeric columns for a correlation matrix.",
        "detailed_metrics_for_ward": "Detailed Metrics for {ward}",
        "diabetes_cases_metric": "Diabetes Cases",
        "hypertension_cases_metric": "Hypertension Cases",
        "flu_cases_metric": "Flu Cases",
        "access_to_sanitation_metric": "Access to Sanitation",
        "average_income_metric": "Average Income",
        "num_clinics_metric": "Number of Clinics",
        "sidebar_info": "This is a simplified demo of an Urban Health Data Hub. Real-world hubs involve complex data integration, privacy considerations, and more advanced analytics.",
        "data_load_error": "Error: The file {file_path} was not found. Make sure it's in the same directory as app.py.",
        "data_not_loaded_warning": "Data could not be loaded. Please check the CSV file.",
        "select_indicator_warning": "Please select an indicator from the sidebar to view charts.",
        # --- Keys for indicator_options (for display in selectbox) ---
        "Diabetes Prevalence": "Diabetes Prevalence",
        "Hypertension Prevalence": "Hypertension Prevalence",
        "Flu Prevalence": "Flu Prevalence",
        "Access to Sanitation (%)": "Access to Sanitation (%)",
        "Average Income (USD)": "Average Income (USD)",
        "Number of Clinics": "Number of Clinics",
        "Average Age": "Average Age",
        "Population": "Population"
    },
    "नेपाली": {
        "hub_title": "शहरी स्वास्थ्य डेटा हब",
        "filters_options": "फिल्टर र विकल्पहरू",
        "select_ward": "वार्ड छान्नुहोस्:",
        "all_wards": "सबै वार्डहरू",
        "select_indicator_bar_box": "बार/बक्स प्लटका लागि सूचक छान्नुहोस्:",
        "dashboard_title": "🏙️ बुढानिलकण्ठ स्वास्थ्य ड्यासबोर्ड (डेमो)",
        "dashboard_subtitle": "शहरी स्वास्थ्य डेटा कल्पना गर्न एक प्रोटोटाइप ड्यासबोर्ड।",
        "key_metrics_header": "मुख्य मेट्रिक्स (समग्र शहर)",
        "total_population": "कुल जनसंख्या",
        "avg_diabetes_prev": "औसत मधुमेह व्यापकता",
        "avg_hypertension_prev": "औसत उच्च रक्तचाप व्यापकता",
        "total_clinics": "कुल क्लिनिकहरू",
        "view_raw_data": "कच्चा डाटा हेर्नुहोस्",
        "ward_comparisons": "वार्ड तुलना",
        "bar_chart_title": "{indicator} वार्ड अनुसार (बार चार्ट)",
        "population_distribution_pie": "वार्ड अनुसार जनसंख्या वितरण (पाई चार्ट)",
        "relationships_trends": "सम्बन्ध र प्रवृत्तिहरू",
        "explore_relationships_scatter": "सम्बन्धहरू अन्वेषण गर्नुहोस् (स्क्याटर प्लट)",
        "select_x_scatter": "स्क्याटर प्लटका लागि X-अक्ष छान्नुहोस्:",
        "select_y_scatter": "स्क्याटर प्लटका लागि Y-अक्ष छान्नुहोस्:",
        "scatter_plot_title": "{y_axis} विरुद्ध {x_axis}",
        "indicator_comparison_line": "वार्डहरूमा सूचक तुलना (लाइन चार्ट)",
        "select_indicators_line": "लाइन चार्टका लागि सूचकहरू छान्नुहोस्:",
        "info_select_indicator_line": "लाइन चार्टका लागि कम्तिमा एक सूचक छान्नुहोस्।",
        "distribution_analysis": "वितरण विश्लेषण",
        "distribution_by_ward_box": "{indicator} को वार्ड अनुसार वितरण (बक्स प्लट)",
        "info_select_indicator_box": "बक्स प्लटका लागि एक सूचक छान्नुहोस्।",
        "frequency_distribution_hist": "आवृत्ति वितरण (हिस्टोग्राम)",
        "select_indicator_hist": "हिस्टोग्रामका लागि सूचक छान्नुहोस्:",
        "hist_plot_title": "{indicator} को वितरण",
        "info_select_indicator_hist": "हिस्टोग्रामका लागि एक सूचक छान्नुहोस्।",
        "correlation_analysis": "सहसम्बन्ध विश्लेषण",
        "correlation_matrix_title": "संख्यात्मक विशेषताहरूको सहसम्बन्ध म्याट्रिक्स",
        "no_numeric_cols_corr": "सहसम्बन्ध म्याट्रिक्सका लागि पर्याप्त संख्यात्मक स्तम्भहरू छैनन्।",
        "detailed_metrics_for_ward": "{ward} का लागि विस्तृत मेट्रिक्स",
        "diabetes_cases_metric": "मधुमेहका केसहरू",
        "hypertension_cases_metric": "उच्च रक्तचापका केसहरू",
        "flu_cases_metric": "फ्लूका केसहरू",
        "access_to_sanitation_metric": "सरसफाइमा पहुँच",
        "average_income_metric": "औसत आय",
        "num_clinics_metric": "क्लिनिक संख्या",
        "sidebar_info": "यो शहरी स्वास्थ्य डेटा हबको एक सरलीकृत डेमो हो। वास्तविक संसारका हबहरूमा जटिल डेटा एकीकरण, गोपनीयता विचारहरू, र थप उन्नत विश्लेषणहरू समावेश हुन्छन्।",
        "data_load_error": "त्रुटि: फाइल {file_path} फेला परेन। यो app.py सँगैको डाइरेक्टरीमा छ भनी सुनिश्चित गर्नुहोस्।",
        "data_not_loaded_warning": "डाटा लोड हुन सकेन। कृपया CSV फाइल जाँच गर्नुहोस्।",
        "select_indicator_warning": "चार्टहरू हेर्न कृपया साइडबारबाट सूचक चयन गर्नुहोस्।",
        # --- Keys for indicator_options (for display in selectbox) ---
        "Diabetes Prevalence": "मधुमेहको व्यापकता",
        "Hypertension Prevalence": "उच्च रक्तचापको व्यापकता",
        "Flu Prevalence": "फ्लूको व्यापकता",
        "Access to Sanitation (%)": "सरसफाइमा पहुँच (%)",
        "Average Income (USD)": "औसत आय (USD)",
        "Number of Clinics": "क्लिनिक संख्या",
        "Average Age": "औसत उमेर",
        "Population": "जनसंख्या"
    }
}

# --- 2. Initialize Session State for Language ---
if 'language' not in st.session_state:
    st.session_state.language = "English" # Default language

# --- 3. Define Callback Function for Language Change ---
def set_language():
    st.session_state.language = st.session_state.lang_select # lang_select is the key of the selectbox

# --- 4. Language Selector Widget (in Sidebar) ---
# This must be defined before the _ function if _ relies on st.session_state.language,
# and the _ function must be defined before it's used by other sidebar elements.
# So, we define the selector, then _, then the rest of the sidebar.
st.sidebar.selectbox(
    "भाषा छान्नुहोस् / Select Language", # Label is bilingual here for initial display
    options=["English", "नेपाली"],
    key="lang_select",
    on_change=set_language
)

# --- 5. Define Translation Helper Function `_` ---
def _(key, **kwargs):
    # Access language from session state, which is now guaranteed to be initialized
    lang = st.session_state.language
    return translations[lang].get(key, key).format(**kwargs)

# --- Sidebar Setup (Now using the defined _ function) ---
st.sidebar.title(_("hub_title"))
st.sidebar.markdown(f"## {_('filters_options')}")

# --- Load Data ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Diabetes_Prevalence_per_1000'] = (df['Diabetes_Cases'] / df['Population']) * 1000
        df['Hypertension_Prevalence_per_1000'] = (df['Hypertension_Cases'] / df['Population']) * 1000
        df['Flu_Prevalence_per_1000'] = (df['Flu_Cases'] / df['Population']) * 1000
        return df
    except FileNotFoundError:
        # Use the translation function for user-facing error messages
        st.error(_("data_load_error", file_path=file_path))
        return pd.DataFrame()

data = load_data("urban_health_data.csv")

# --- Sidebar Widgets (Continued) ---
# Ward Selector
all_wards_text = _("all_wards")
# Assuming ward names in the CSV are in English and don't need direct translation for filtering logic
ward_options_for_select = [all_wards_text] + (list(data['Ward'].unique()) if not data.empty else [])
selected_ward_display_name = st.sidebar.selectbox(
    _("select_ward"),
    options=ward_options_for_select,
    index=0
)
# Logic to determine the actual ward value for filtering
selected_ward = selected_ward_display_name
if selected_ward_display_name == all_wards_text:
    selected_ward = 'All Wards' # Internal value for 'All Wards'

# Health Indicator Selector (Internal keys remain English)
indicator_options_internal = {
    "Diabetes Prevalence": "Diabetes_Prevalence_per_1000",
    "Hypertension Prevalence": "Hypertension_Prevalence_per_1000",
    "Flu Prevalence": "Flu_Prevalence_per_1000",
    "Access to Sanitation (%)": "Access_to_Sanitation_Pct",
    "Average Income (USD)": "Avg_Income_USD",
    "Number of Clinics": "Num_Clinics",
    "Average Age": "Avg_Age",
    "Population": "Population"
}
# Create translated display options for the selectbox
# The keys of this map are what the user sees (translated)
# The values are the original English keys used internally
translated_indicator_display_map = {_(key): key for key in indicator_options_internal.keys()}

selected_display_indicator_name = st.sidebar.selectbox(
    _("select_indicator_bar_box"),
    options=list(translated_indicator_display_map.keys()) if not data.empty else [],
    index=0
)
# Get the original English key from the selected translated display name
selected_indicator_original_key = translated_indicator_display_map.get(selected_display_indicator_name)
selected_indicator_col = indicator_options_internal.get(selected_indicator_original_key)


# --- Main Dashboard Area ---
st.title(_("dashboard_title"))
st.markdown(_("dashboard_subtitle"))

if not data.empty and selected_indicator_col:
    # --- Key Metrics ---
    st.header(_("key_metrics_header"))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(_("total_population"), f"{data['Population'].sum():,}")
    col2.metric(_("avg_diabetes_prev"), f"{data['Diabetes_Prevalence_per_1000'].mean():.2f} per 1000")
    col3.metric(_("avg_hypertension_prev"), f"{data['Hypertension_Prevalence_per_1000'].mean():.2f} per 1000")
    col4.metric(_("total_clinics"), data['Num_Clinics'].sum())

    st.markdown("---")

    # --- Data View (Expandable) ---
    with st.expander(_("view_raw_data")):
        if selected_ward == 'All Wards':
            st.dataframe(data)
        else:
            st.dataframe(data[data['Ward'] == selected_ward])

    st.markdown("---")

    # --- Visualizations ---
    st.header(_("Visualizations")) # Assuming 'Visualizations' is a key in translations

    # Row 1: Bar Chart and Pie Chart
    st.subheader(_("ward_comparisons"))
    viz_row1_col1, viz_row1_col2 = st.columns(2)

    with viz_row1_col1:
        # Use the translated version of the original key for display
        display_key_for_bar = _(selected_indicator_original_key) if selected_indicator_original_key else ""
        st.markdown(f"**{_('bar_chart_title', indicator=display_key_for_bar)}**")
        if selected_indicator_col:
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            sns.barplot(x='Ward', y=selected_indicator_col, data=data, ax=ax_bar, palette="viridis")
            plt.xticks(rotation=45, ha='right')
            ax_bar.set_ylabel(display_key_for_bar) # Use translated key for axis label
            ax_bar.set_title(_('bar_chart_title', indicator=display_key_for_bar))
            st.pyplot(fig_bar)

    with viz_row1_col2:
        st.markdown(f"**{_('population_distribution_pie')}**")
        fig_pie = px.pie(data, values='Population', names='Ward', title=_('population_distribution_pie'),
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Row 2: Scatter Plot and Line Chart
    st.subheader(_("relationships_trends"))
    viz_row2_col1, viz_row2_col2 = st.columns(2)

    with viz_row2_col1:
        st.markdown(f"**{_('explore_relationships_scatter')}**")
        x_axis_options_internal = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
        y_axis_options_internal = x_axis_options_internal

        # For scatter plot selectors, translate the display options
        x_axis_display_map = {_(col.replace('_', ' ').title()): col for col in x_axis_options_internal}
        y_axis_display_map = {_(col.replace('_', ' ').title()): col for col in y_axis_options_internal}

        default_x_display = _('Average Income (USD)') if _('Average Income (USD)') in x_axis_display_map else (list(x_axis_display_map.keys())[0] if x_axis_display_map else None)
        default_y_display = _('Diabetes Prevalence') if _('Diabetes Prevalence') in y_axis_display_map else (list(y_axis_display_map.keys())[1] if len(y_axis_display_map) > 1 else None)


        selected_x_display = st.selectbox(_("select_x_scatter"), list(x_axis_display_map.keys()), index=list(x_axis_display_map.keys()).index(default_x_display) if default_x_display in x_axis_display_map else 0)
        selected_y_display = st.selectbox(_("select_y_scatter"), list(y_axis_display_map.keys()), index=list(y_axis_display_map.keys()).index(default_y_display) if default_y_display in y_axis_display_map else 0)

        x_axis_col = x_axis_display_map.get(selected_x_display)
        y_axis_col = y_axis_display_map.get(selected_y_display)


        if x_axis_col and y_axis_col:
            fig_scatter = px.scatter(data, x=x_axis_col, y=y_axis_col, color='Ward',
                                     title=_('scatter_plot_title', y_axis=selected_y_display, x_axis=selected_x_display),
                                     labels={x_axis_col: selected_x_display, y_axis_col: selected_y_display}, # Use translated labels
                                     hover_data=['Population'])
            st.plotly_chart(fig_scatter, use_container_width=True)

    with viz_row2_col2:
        st.markdown(f"**{_('indicator_comparison_line')}**")
        line_chart_options_internal = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col]) and col not in ['Population', 'Num_Clinics', 'Avg_Age']]
        line_chart_display_map = {_(col.replace('_', ' ').title()): col for col in line_chart_options_internal}

        selected_line_displays = st.multiselect(
            _("select_indicators_line"),
            options=list(line_chart_display_map.keys()),
            default=[_('Diabetes Prevalence'), _('Hypertension Prevalence')] if _('Diabetes Prevalence') in line_chart_display_map and _('Hypertension Prevalence') in line_chart_display_map else []
        )
        selected_line_cols = [line_chart_display_map.get(disp) for disp in selected_line_displays if line_chart_display_map.get(disp)]

        if selected_line_cols:
            line_df = data.set_index('Ward')[selected_line_cols]
            # For st.line_chart, column names become legend entries.
            # If you need translated legend, you'd rename columns in line_df before plotting
            # For simplicity, keeping internal column names for legend here.
            st.line_chart(line_df)
        else:
            st.info(_("info_select_indicator_line"))

    st.markdown("---")

    # Row 3: Box Plot and Histogram
    st.subheader(_("distribution_analysis"))
    viz_row3_col1, viz_row3_col2 = st.columns(2)

    with viz_row3_col1:
        display_key_for_box = _(selected_indicator_original_key) if selected_indicator_original_key else ""
        st.markdown(f"**{_('distribution_by_ward_box', indicator=display_key_for_box)}**")
        if selected_indicator_col:
            fig_box, ax_box = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='Ward', y=selected_indicator_col, data=data, ax=ax_box, palette="Set2")
            plt.xticks(rotation=45, ha='right')
            ax_box.set_ylabel(display_key_for_box)
            ax_box.set_title(_('distribution_by_ward_box', indicator=display_key_for_box))
            st.pyplot(fig_box)
        else:
            st.info(_("info_select_indicator_box"))

    with viz_row3_col2:
        st.markdown(f"**{_('frequency_distribution_hist')}**")
        # Re-use indicator_options_internal and translated_indicator_display_map for consistency
        selected_hist_display_name = st.selectbox(
            _("select_indicator_hist"),
            options=list(translated_indicator_display_map.keys()),
            index=list(translated_indicator_display_map.keys()).index(_("Average Age")) if _("Average Age") in translated_indicator_display_map else 0
        )
        hist_indicator_original_key = translated_indicator_display_map.get(selected_hist_display_name)
        hist_indicator_col = indicator_options_internal.get(hist_indicator_original_key)

        if hist_indicator_col:
            fig_hist, ax_hist = plt.subplots(figsize=(10, 6))
            sns.histplot(data[hist_indicator_col], kde=True, ax=ax_hist, color="skyblue")
            ax_hist.set_xlabel(selected_hist_display_name) # Use translated name for label
            ax_hist.set_ylabel(_("Frequency")) # Assuming "Frequency" is a key
            ax_hist.set_title(_('hist_plot_title', indicator=selected_hist_display_name))
            st.pyplot(fig_hist)
        else:
            st.info(_("info_select_indicator_hist"))

    st.markdown("---")

    # Correlation Matrix
    st.subheader(_("correlation_analysis"))
    if len(data.columns) > 1:
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            correlation_matrix = data[numeric_cols].corr()
            fig_corr, ax_corr = plt.subplots(figsize=(10,8))
            sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5, ax=ax_corr)
            ax_corr.set_title(_("correlation_matrix_title"))
            st.pyplot(fig_corr)
        else:
            st.write(_("no_numeric_cols_corr"))

    # Detailed view for a selected ward
    if selected_ward != 'All Wards' and selected_ward in data['Ward'].values: # Check if ward exists
        st.subheader(_("detailed_metrics_for_ward", ward=selected_ward))
        ward_data_selected = data[data['Ward'] == selected_ward].iloc[0]
        details_col1, details_col2 = st.columns(2)
        with details_col1:
            st.metric(_("Population"), f"{ward_data_selected['Population']:,}") # Translate "Population"
            st.metric(_("diabetes_cases_metric"), f"{ward_data_selected['Diabetes_Cases']} ({ward_data_selected['Diabetes_Prevalence_per_1000']:.2f} per 1000)")
            st.metric(_("hypertension_cases_metric"), f"{ward_data_selected['Hypertension_Cases']} ({ward_data_selected['Hypertension_Prevalence_per_1000']:.2f} per 1000)")
        with details_col2:
            st.metric(_("flu_cases_metric"), f"{ward_data_selected['Flu_Cases']} ({ward_data_selected['Flu_Prevalence_per_1000']:.2f} per 1000)")
            st.metric(_("access_to_sanitation_metric"), f"{ward_data_selected['Access_to_Sanitation_Pct']}%")
            st.metric(_("average_income_metric"), f"${ward_data_selected['Avg_Income_USD']:,}")
            st.metric(_("num_clinics_metric"), ward_data_selected['Num_Clinics'])
else:
    if data.empty:
        st.warning(_("data_not_loaded_warning"))
    else:
        st.info(_("select_indicator_warning"))

st.sidebar.markdown("---")
st.sidebar.info(_("sidebar_info"))