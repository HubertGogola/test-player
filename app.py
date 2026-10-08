"""Dynamic Player DNA — entrypoint and always-visible navigation.

The public application's navigation deliberately uses explicit page links
instead of Streamlit's collapsible built-in sidebar. This preserves the
three requested groups and never renders a View more / View less control.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src import theme, components

st.set_page_config(
    page_title="Dynamic Player DNA",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme.inject_css()

# Keep the information architecture consistent with the research workflow.
# Page objects are shared by the router and the fully-visible custom menu.
pages = {
    "Start": [
        st.Page("pages/overview.py", title="Overview", default=True),
    ],
    "Player analysis": [
        st.Page("pages/player_dna.py", title="Player DNA"),
        st.Page("pages/player_comparison.py", title="Player comparison"),
        st.Page("pages/cohort_analysis.py", title="Cohort analysis"),
    ],
    "Modelling & reference": [
        st.Page("pages/modelling.py", title="Modelling"),
        st.Page("pages/reference.py", title="Reference"),
    ],
}

# Hidden router keeps valid page URLs and active page highlighting, while
# explicit links avoid Streamlit 1.38's View more / View less truncation.
current_page = st.navigation(pages, position="hidden")

components.sidebar_chrome()
with st.sidebar:
    for group, entries in pages.items():
        st.markdown(
            f'<div class="dp-nav-group">{group}</div>',
            unsafe_allow_html=True,
        )
        for page in entries:
            st.page_link(page, label=page.title, use_container_width=True)

components.sidebar_footer_note()
current_page.run()
