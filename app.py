import streamlit as st
from pathlib import Path
from st_pages import Page, add_page_title, get_nav_from_toml
from PIL import Image



image_path = logo = "Media\earth.jpg"  # The path to the image
img = Image.open(image_path)

st.markdown(
    """
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    </head>
    """, unsafe_allow_html=True
)

# Inject custom CSS for sidebar styling and background image
st.markdown(
    """
    <style>
    /* Set background image */
    .stApp {
        background: url("https://www.toxel.com/wp-content/uploads/2014/02/icebergs09.jpg");
        background-size: 100%;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: local;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    /* Sidebar background color */
    .css-1d391kg {
        background-color: #d1f1c7;  /* Light green background */
        color: #333333;  /* Dark text color */
    }

    /* Sidebar header (optional) */
    .css-1d391kg h2 {
        color: #333333;  /* Dark text color */
    }

    /* Sidebar background color */
    .css-1d391kg {
        background-color: #d1f1c7;  /* Light green background */
        color: #333333;  /* Dark text color */
    }

    /* Sidebar header (optional) */
    .css-1d391kg h2 {
        color: #333333;  /* Dark text color */
    }

    /* Style the sidebar image */
    .css-1d391kg .stSidebar {
        padding: 20px 0;
        display: flex;
        justify-content: center;
    }

    /* Style for the social media section */
    .social-links {
        display: flex;
        justify-content: start;
        gap: 10px;
        padding-top: 10px;
    }

    .social-links a {
        color: #0073b1;  /* LinkedIn color */
        font-size: 20px;
    }

    .social-links a:hover {
        color: #0a66c2;  /* LinkedIn hover color */
    }


    /* Bottom white divider */
    .css-1d391kg .stSidebar .stButton {
        margin-top: 10px;
        border-top: 2px solid #ffffff;
    }

    </style>
    """, unsafe_allow_html=True
)
# Display the image in the sidebar
st.sidebar.image(img, use_container_width=True)

# Team members and information in the sidebar
st.sidebar.markdown("### Promotion Continuous Data Analyst May - 2024")
st.sidebar.markdown("**Team members social accounts:**")
st.sidebar.markdown(
    'Maria  |  <a href="https://www.linkedin.com/in/maria-januszka-9a564a6b/" target="_blank"><i class="fab fa-linkedin" style="font-size:20px;"></i></a> | <a href="https://github.com/timea-prejbean/World_Temperature_Project" target="_blank"><i class="fab fa-github" style="font-size:20px;"></i></a>', 
    unsafe_allow_html=True
)
st.sidebar.markdown(
    'David  |  <a href="https://www.linkedin.com" target="_blank"><i class="fab fa-linkedin" style="font-size:20px;"></i></a> | <a href="https://github.com/timea-prejbean/World_Temperature_Project" target="_blank"><i class="fab fa-github" style="font-size:20px;"></i></a>', 
    unsafe_allow_html=True
)
st.sidebar.markdown(
    'Timea  |  <a href="https://www.linkedin.com/in/prejbean-timea-313b13b7/" target="_blank"><i class="fab fa-linkedin" style="font-size:20px;"></i></a> | <a href="https://github.com/timea-prejbean/World_Temperature_Project" target="_blank"><i class="fab fa-github" style="font-size:20px;"></i></a>', 
    unsafe_allow_html=True
)


# Automatically load pages from .streamlit/pages.toml here we have the sidebar visual design from the *.toml file
toml_path = Path.cwd() / ".streamlit" / "pages.toml"

# Debugging output
#st.write("Current working directory:", Path.cwd())
#st.write("Constructed TOML path:", toml_path)

# Load navigation
if not toml_path.exists():
    st.error(f"TOML file not found at: {toml_path}")
else:
    #st.success(f"TOML file found at: {toml_path}")
    nav = get_nav_from_toml(str(toml_path))
    pg = st.navigation(nav)
    add_page_title(pg)
    pg.run()

# Image sources from URLs
st.sidebar.markdown("<hr>",unsafe_allow_html=True)
st.sidebar.markdown("""  
    <p style="text-align: left; font-size: 12px;">
        Image source - earth JPG: <a href="https://karmawallet.io/blog/wp-content/uploads/2024/04/concept-illustration-global-warming-around-the-royalty-free-image-1707420637-2048x1098.jpg" target="_blank">earth_global_warming</a>
    </p>
    """,
    unsafe_allow_html=True)