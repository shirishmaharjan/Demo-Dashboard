import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="Urban Health Data Hub Demo")

# --- Language Setup ---
translations = {
    "English": {
        "hub_title": "Urban Health Data Hub", "filters_options": "Filters & Options",
        "select_ward": "Select Ward:", "all_wards": "All Wards",
        "select_indicator_bar_box": "Select Indicator for Bar/Box Plot:",
        "dashboard_title": "🏙️ Budhanilkantha Health Dashboard",
        "key_metrics_header": "Key Metrics (Overall City)",
        "total_population": "Total Population", "avg_diabetes_prev": "Avg. Diabetes Prevalence",
        "Diabetes Prevalence": "Diabetes Prevalence", "Hypertension Prevalence": "Hypertension Prevalence", # For indicator options
        "Flu Prevalence": "Flu Prevalence", "Access to Sanitation (%)": "Access to Sanitation (%)",
        "Average Income (USD)": "Average Income (USD)", "Number of Clinics": "Number of Clinics",
        "Average Age": "Average Age", "Population": "Population",
        "view_raw_data": "View Raw Data",
        # ... Add ALL your strings
    },
    "नेपाली": {
        "hub_title": "शहरी स्वास्थ्य डेटा हब", "filters_options": "फिल्टर र विकल्पहरू",
        "select_ward": "वार्ड छान्नुहोस्:", "all_wards": "सबै वार्डहरू",
        "select_indicator_bar_box": "बार/बक्स प्लटका लागि सूचक छान्नुहोस्:",
        "dashboard_title": "🏙️ बुढानिलकण्ठ स्वास्थ्य ड्यासबोर्ड",
        "key_metrics_header": "मुख्य मेट्रिक्स (समग्र शहर)",
        "total_population": "कुल जनसंख्या", "avg_diabetes_prev": "औसत मधुमेह व्यापकता",
        "Diabetes Prevalence": "मधुमेहको व्यापकता", "Hypertension Prevalence": "उच्च रक्तचापको व्यापकता",
        "Flu Prevalence": "फ्लूको व्यापकता", "Access to Sanitation (%)": "सरसफाइमा पहुँच (%)",
        "Average Income (USD)": "औसत आय (USD)", "Number of Clinics": "क्लिनिक संख्या",
        "Average Age": "औसत उमेर", "Population": "जनसंख्या",
        "view_raw_data": "कच्चा डाटा हेर्नुहोस्",
        # ... Add ALL your strings
    }
}

# --- Sidebar START ---
st.sidebar.title(_("hub_title", lang=st.session_state.language)) # Access language from session state
st.sidebar.markdown(f"## {_('filters_options', lang=st.session_state.language)}")
# --- Sidebar END ---

# Initialize session state for language if not already set
if 'language' not in st.session_state:
    st.session_state.language = "English" # Default language

def set_language():
    # Callback function to update language in session state
    st.session_state.language = st.session_state.lang_select

# Language selector in the sidebar (place it early)
st.sidebar.selectbox(
    "भाषा छान्नुहोस् / Select Language",
    options=["English", "नेपाली"],
    key="lang_select", # Unique key for the selectbox
    on_change=set_language # Callback when selection changes
)

def _(key, **kwargs):
    lang = st.session_state.language # Use language from session state
    return translations[lang].get(key, key).format(**kwargs)

# --- Load Data --- (Keep as is, data column names are internal)
@st.cache_data
def load_data(file_path):
    # ... your existing load_data function ...
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


# --- Sidebar CONTINUED ---
# Ward Selector
all_wards_text = _("all_wards")
ward_options_display = [all_wards_text] + (list(data['Ward'].unique()) if not data.empty else []) # Assuming Ward names in data don't need translation for filtering
selected_ward_display_name = st.sidebar.selectbox(
    _("select_ward"),
    options=ward_options_display,
    index=0
)
selected_ward = selected_ward_display_name if selected_ward_display_name != all_wards_text else 'All Wards'


# Health Indicator Selector
indicator_options_internal = { # These are internal keys, keep them consistent
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
translated_indicator_display_map = {_(key): key for key in indicator_options_internal.keys()}

selected_display_indicator_name = st.sidebar.selectbox(
    _("select_indicator_bar_box"),
    options=list(translated_indicator_display_map.keys()) if not data.empty else [],
    index=0
)
selected_indicator_key = translated_indicator_display_map.get(selected_display_indicator_name) # Original English key
selected_indicator_col = indicator_options_internal.get(selected_indicator_key)


# --- Main Dashboard Area ---
st.title(_("dashboard_title"))
# ... and so on for all text elements ...

# When using selected_indicator_key for display in titles/markdown:
if selected_indicator_key: # Make sure it's not None
    st.markdown(f"**{_(selected_indicator_key)} by Ward (Bar Chart)**") # Translate the display key
    # ... in plot titles, use _(selected_indicator_key) ...
else:
    st.warning("Please select an indicator.")


if not data.empty and selected_indicator_col:
    # --- Key Metrics ---
    st.header(_("key_metrics_header"))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(_("total_population"), f"{data['Population'].sum():,}")
    col2.metric(_("avg_diabetes_prev"), f"{data['Diabetes_Prevalence_per_1000'].mean():.2f} per 1000")
    # ... more metrics with translated labels ...

    # --- Data View (Expandable) ---
    with st.expander(_("view_raw_data")):
        if selected_ward == 'All Wards':
            st.dataframe(data)
        else:
            st.dataframe(data[data['Ward'] == selected_ward])
    # ... rest of your dashboard code, applying _() to all user-facing strings ...
    # For plot titles and labels:
    # fig_bar.set_title(_(f"{selected_indicator_key} Across Wards")) # If selected_indicator_key itself needs translation
    # fig_bar.set_ylabel(_(selected_indicator_key))
    # For plotly charts:
    # fig_pie.update_layout(title_text=_('Population Proportion by Ward'))
    # fig_scatter.update_layout(title_text=_(f'{y_axis_display} vs. {x_axis_display}'),
    #                           xaxis_title=_(x_axis_display), yaxis_title=_(y_axis_display))
    # (where x_axis_display and y_axis_display are translated versions of column names if needed)

else:
    if data.empty:
        st.warning("Data could not be loaded. Please check the CSV file.")
    else: # Implies selected_indicator_col is None
        st.info("Please select an indicator from the sidebar to view charts.")

st.sidebar.markdown("---")
st.sidebar.info(_("sidebar_info"))