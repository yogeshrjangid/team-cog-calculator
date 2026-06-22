import streamlit as st
import pandas as pd

from database import (
    add_member,
    get_all_members,
    delete_member,
    update_member
)

from geopy.geocoders import Nominatim
from rapidfuzz import process
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Team COG Calculator",
    page_icon="📍",
    layout="wide"
)

# --------------------------------------------------
# GEOCODER
# --------------------------------------------------

geolocator = Nominatim(
    user_agent="cog_app_v2"
)

COMMON_CITIES = [
    "Pune",
    "Mumbai",
    "Delhi",
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Ahmedabad",
    "Jaipur",
    "Lucknow",
    "Nagpur",
    "Indore",
    "Surat",
    "Patna",
    "Bhopal"
]


def get_coordinates(city_name):

    match = process.extractOne(
        city_name,
        COMMON_CITIES
    )

    if match and match[1] >= 80:
        city_name = match[0]

    try:

        location = geolocator.geocode(
            city_name + ", India"
        )

        if location:

            return (
                location.latitude,
                location.longitude,
                city_name
            )

    except Exception:
        pass

    return None, None, city_name


def get_nearest_city(lat, lon):

    try:

        location = geolocator.reverse(
            (lat, lon),
            exactly_one=True
        )

        if location:

            address = location.raw.get(
                "address",
                {}
            )

            return (
                address.get("city")
                or address.get("town")
                or address.get("county")
                or address.get("state_district")
                or address.get("state")
                or "Unknown"
            )

    except Exception:
        pass

    return "Unknown"


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📍 Team COG Calculator")

# ==================================================
# ADD MEMBER
# ==================================================

st.markdown("---")

st.subheader("Add Member")

with st.form(
    "member_form",
    clear_on_submit=True
):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Name")

        age = st.number_input(
            "Age",
            min_value=0,
            max_value=100,
            step=1
        )

    with col2:

        experience = st.number_input(
            "Domain Experience",
            min_value=0,
            max_value=50,
            step=1
        )

        city = st.text_input("City")

    submitted = st.form_submit_button(
        "Add Member"
    )

if submitted:

    lat, lon, corrected_city = get_coordinates(
        city
    )

    if lat is not None:

        add_member(
            name,
            age,
            experience,
            corrected_city,
            lat,
            lon
        )

        st.success(
            f"✅ Member Added. City detected as: {corrected_city}"
        )

        st.rerun()

    else:

        st.error(
            "❌ Unable to locate city."
        )

# ==================================================
# LOAD DATA
# ==================================================

rows = get_all_members()

df = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Name",
        "Age",
        "Experience",
        "City",
        "Latitude",
        "Longitude"
    ]
)

if not df.empty:

    df.insert(
        0,
        "S.No",
        range(
            1,
            len(df) + 1
        )
    )

# ==================================================
# DISPLAY TABLE
# ==================================================

st.markdown("---")

st.subheader("Team Members")

if not df.empty:

    st.dataframe(
        df[
            [
                "S.No",
                "Name",
                "Age",
                "Experience",
                "City"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No members added.")

# ==================================================
# EDIT MEMBER
# ==================================================

if not df.empty:

    st.markdown("---")

    st.subheader("✏️ Edit Member")

    edit_options = {

        f"{row['Name']} ({row['City']})":
        row["ID"]

        for _, row in df.iterrows()
    }

    selected_edit = st.selectbox(
        "Select Member To Edit",
        edit_options.keys(),
        key="edit_member_select"
    )

    selected_id = edit_options[selected_edit]

    selected_row = df[
        df["ID"] == selected_id
    ].iloc[0]

    with st.form("edit_member_form"):

        edit_name = st.text_input(
            "Name",
            value=selected_row["Name"]
        )

        edit_age = st.number_input(
            "Age",
            min_value=0,
            max_value=100,
            value=int(selected_row["Age"])
        )

        edit_experience = st.number_input(
            "Domain Experience",
            min_value=0,
            max_value=50,
            value=int(selected_row["Experience"])
        )

        edit_city = st.text_input(
            "City",
            value=selected_row["City"]
        )

        update_btn = st.form_submit_button(
            "Update Member"
        )

    if update_btn:

        lat, lon, corrected_city = get_coordinates(
            edit_city
        )

        if lat is not None:

            update_member(
                selected_id,
                edit_name,
                edit_age,
                edit_experience,
                corrected_city,
                lat,
                lon
            )

            st.success(
                f"✅ Member Updated. City detected as: {corrected_city}"
            )

            st.rerun()

        else:

            st.error(
                "❌ Unable to locate city."
            )
# ==================================================
# COG CALCULATION
# ==================================================

if not df.empty:

    cog_lat = df["Latitude"].mean()

    cog_lon = df["Longitude"].mean()

    cog_city = get_nearest_city(
        cog_lat,
        cog_lon
    )

# ==================================================
# MAP
# ==================================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "India Team Map"
    )

    m = folium.Map(
        location=[22.5, 79.0],
        zoom_start=5
    )

    # --------------------------------------------------
    # MEMBER MARKERS
    # --------------------------------------------------

    for _, row in df.iterrows():

        folium.Marker(
            [
                row["Latitude"],
                row["Longitude"]
            ],
            popup=f"""
            <b>{row['Name']}</b><br>
            City: {row['City']}<br>
            Age: {row['Age']}<br>
            Experience: {row['Experience']}
            """
        ).add_to(m)

        # Permanent name label

        folium.map.Marker(
            [
                row["Latitude"],
                row["Longitude"]
            ],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size:12px;
                    color:blue;
                    font-weight:bold;
                    white-space: nowrap;
                ">
                    {row['Name']}
                </div>
                """
            )
        ).add_to(m)

    # --------------------------------------------------
    # COG MARKER
    # --------------------------------------------------

    folium.Marker(
        [
            cog_lat,
            cog_lon
        ],
        tooltip="COG",
        popup=f"""
        <b>Center Of Gravity</b><br>
        Nearest City: {cog_city}
        """,
        icon=folium.Icon(
            color="red",
            icon="star"
        )
    ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=600
    )

# ==================================================
# COG INFO
# ==================================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "Center Of Gravity"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "COG Latitude",
            round(
                cog_lat,
                4
            )
        )

    with col2:

        st.metric(
            "COG Longitude",
            round(
                cog_lon,
                4
            )
        )

    with col3:

        st.metric(
            "Nearest City",
            cog_city
        )

# ==================================================
# DELETE
# ==================================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "Delete Member"
    )

    options = {

        f"{row['Name']} ({row['City']})":
        row["ID"]

        for _, row in df.iterrows()
    }

    selected = st.selectbox(
        "Select Member",
        options.keys()
    )

    if st.button(
        "Delete Selected Member"
    ):

        delete_member(
            options[selected]
        )

        st.success(
            "✅ Deleted Successfully"
        )

        st.rerun()

# ==================================================
# STATISTICS
# ==================================================

if not df.empty:

    st.markdown("---")

    st.subheader(
        "Statistics"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Members",
        len(df)
    )

    c2.metric(
        "Average Age",
        round(
            df["Age"].mean(),
            2
        )
    )

    c3.metric(
        "Average Experience",
        round(
            df["Experience"].mean(),
            2
        )
    )

    c4.metric(
        "Cities",
        df["City"].nunique()
    )