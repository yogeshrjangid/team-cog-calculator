
import streamlit as st
import pandas as pd
# import time
from database import add_member, get_all_members, delete_member, update_member
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(page_title="SCY CoG Tool", page_icon="📍", layout="wide")

# --------------------------------------------------
# GEOCODER
# --------------------------------------------------

geolocator = Nominatim(user_agent="scy_cog_tool", timeout=10)

# def get_coordinates(work_location, district, state, country="India"):
#     try:
#         query = f"{work_location}, {district}, {state}, {country}"
#         location = geolocator.geocode(query)
#         if location:
#             return location.latitude, location.longitude
#     except Exception:
#         pass
#     return None, None
def get_coordinates( work_location, district, state, country):

    search_queries = [
        f"{work_location}, {district}, {state}, {country}",
        f"{district}, {state}, {country}"]

    for query in search_queries:
        try:
            location = geolocator.geocode(query)
            if location:
                return (location.latitude, location.longitude, query, True)
        except Exception:
            pass

    return (None, None, None, False)

def get_cog_location(lat, lon):
    try:
        location = geolocator.reverse(
            (lat, lon),
            exactly_one=True)
        if location:
            address = location.raw.get("address", {})
            city = (address.get("city")
                or address.get("town")
                or address.get("county")
                or address.get("state_district")
                or "Unknown")
            district = (address.get("state_district")
                or address.get("county")
                or "Unknown")
            state = (address.get("state")
                or "Unknown")
            return city, district, state
    except Exception:
        pass
    return "Unknown", "Unknown", "Unknown"

# --------------------------------------------------
# TITLE
# --------------------------------------------------
st.title("📍 SCY CoG Tool")

if "member_added" not in st.session_state:
    st.session_state.member_added = False

if "show_manual_coordinates" not in st.session_state:

    st.session_state.show_manual_coordinates = False

# ==================================================
# ADD MEMBER
# ==================================================
st.markdown("---")
st.subheader("Add Member")

with st.form("member_form", clear_on_submit=True):
    name = st.text_input("Name")
    experience = st.number_input("Domain Experience", min_value=0, max_value=50, step=1)
    work_location = st.text_input("Current Work Location")
    district = st.text_input("District")
    state = st.text_input("State")
    country = st.text_input("Country", value="India")

    submitted = st.form_submit_button("Add Member")

# if submitted:
#     lat, lon = get_coordinates(work_location, district, state, country)

#     if lat is not None:
#         add_member(
#             name, experience, work_location,
#             district, state, country, lat, lon
#         )
#         st.success("Member Added Successfully")
#         st.rerun()
#     else:
#         st.error("Unable to locate the provided location")
if submitted:
    lat, lon, found_query, success = get_coordinates( work_location, district, state, country)
    if success:
        add_member( name, experience, work_location, district, state, country, lat, lon)
        st.success(
            f"Location identified using: {found_query}")
        st.rerun()
    else:
        st.session_state.show_manual_coordinates = True
        st.warning("""
            Unable to locate your location automatically.

            Please find Latitude and Longitude
            from Google Maps and enter manually.
            """)
if st.session_state.show_manual_coordinates:
    st.markdown("---")
    st.subheader("Manual Coordinates Entry")
    st.info(
        """
        Open Google Maps.

        Right click your location.

        Copy Latitude and Longitude upto six decimal places.
        """)
    manual_lat = st.number_input("Latitude", format="%.6f" )
    manual_lon = st.number_input("Longitude", format="%.6f")
    if st.button("Save With Manual Coordinates"):
        add_member(name, experience, work_location, district, state, country, manual_lat, manual_lon)
        st.session_state.show_manual_coordinates = False
        st.session_state.member_added = True
        st.success("✅ Member Added Successfully")
        # time.sleep(2)
        st.rerun()

# ==================================================
# LOAD DATA
# ==================================================
rows = get_all_members()

df = pd.DataFrame(
    rows,
    columns=[
        "ID",
        "Name",
        "Experience",
        "Work Location",
        "District",
        "State",
        "Country",
        "Latitude",
        "Longitude"
    ]
)

if not df.empty:
    df.insert(0, "S.No", range(1, len(df)+1))

# ==================================================
# DISPLAY TABLE
# ==================================================
st.markdown("---")
st.subheader("Team Members")

if not df.empty:
    st.dataframe(
        df[[
            "S.No",
            "Name",
            "Experience",
            "Work Location",
            "State"
        ]],
        use_container_width=True,
        hide_index=True
    )
    # ==================================================
    # EDIT MEMBER
    # ==================================================
    st.markdown("---")
    st.subheader("✏️ Edit Member")

    edit_options = {
        f"{r['Name']} ({r['Work Location']})": r["ID"]
        for _, r in df.iterrows()
    }

    selected = st.selectbox(
        "Select Member To Edit",
        list(edit_options.keys())
    )

    selected_id = edit_options[selected]

    row = df[df["ID"] == selected_id].iloc[0]

    with st.form("edit_form"):
        edit_name = st.text_input("Name", value=row["Name"])
        edit_exp = st.number_input(
            "Domain Experience",
            min_value=0,
            max_value=50,
            value=int(row["Experience"])
        )
        edit_loc = st.text_input(
            "Current Work Location",
            value=row["Work Location"]
        )
        edit_district = st.text_input(
            "District",
            value=row["District"]
        )
        edit_state = st.text_input(
            "State",
            value=row["State"]
        )
        edit_country = st.text_input(
            "Country",
            value=row["Country"]
        )

        update_btn = st.form_submit_button("Update Member")

    if update_btn:
        lat, lon, found_query, success = get_coordinates(
            edit_loc,
            edit_district,
            edit_state,
            edit_country
        )

        if success:
            update_member(
                selected_id,
                edit_name,
                edit_exp,
                edit_loc,
                edit_district,
                edit_state,
                edit_country,
                lat,
                lon
            )
            st.success("Member Updated")
            st.rerun()
        else:
            st.warning(
                """
                Unable to geocode edited location.
                Please update using a valid
                District / State combination.
                """)
    # ==================================================
    # COG CALCULATION
    # ==================================================
    cog_lat = df["Latitude"].mean()
    cog_lon = df["Longitude"].mean()
    cog_city, cog_district, cog_state = get_cog_location(cog_lat, cog_lon)
    # ==================================================
    # MAP
    # ==================================================
    st.markdown("---")
    st.subheader("India Team Map")

    m = folium.Map(location=[22.5, 79.0], zoom_start=5)
    # --------------------------------------------------
    # MEMBER MARKERS
    # --------------------------------------------------

    grouped_locations = df.groupby([
        "Latitude",
        "Longitude",
        "Work Location",
        "District",
        "State",
        "Country"])

    for (
        lat,
        lon,
        work_location,
        district,
        state,
        country
        ), group in grouped_locations:

        member_names = list(group["Name"])
        tooltip_text = f"""
        <div style="
            font-size:10px;
            line-height:1.0;
            color:blue;
            font-weight:normal;
            text-align:center;
            ">
            <b>{work_location} : </b><br>
            {'<br>'.join(member_names)}
        </div>
        """

        popup_text = f"""
        <div style="font-size:10px;">
        <b>Work Location:</b> {work_location}<br>
        <b>District:</b> {district}<br>
        <b>State:</b> {state}<br>
        <b>Members:</b><br>
        {'<br>'.join(member_names)}
        </div>
        """

        folium.Marker(
            [lat, lon],
            tooltip=folium.Tooltip(
                tooltip_text,
                permanent=True,
                direction="top"
            ),
            popup=folium.Popup(
             popup_text,
             max_width=300
            )
        ).add_to(m)
    # --------------------------------------------------
    # COG MARKER
    # --------------------------------------------------
    folium.Marker(
        [cog_lat, cog_lon],
        tooltip="COG",
        popup=f"""
        <b>Center Of Gravity</b><br>
        City: {cog_city}<br>
        District: {cog_district}<br>
        State: {cog_state}
        """,
        icon=folium.Icon(color="red")
    ).add_to(m)

    st_folium(m, width=1200, height=600)
    # ==================================================
    # COG INFO
    # ==================================================
    st.markdown("---")
    st.subheader("Center Of Gravity")

    c1, c2 = st.columns(2)
    c1.metric("COG Latitude", round(cog_lat, 4))
    c2.metric("COG Longitude", round(cog_lon, 4))
    st.info(f"""
    📍 Nearest City: {cog_city}
    🏛 District: {cog_district}
    🌎 State: {cog_state}
    """)
    # ==================================================
    # DELETE
    # ==================================================
    st.markdown("---")
    st.subheader("Delete Member")

    delete_selection = st.selectbox(
        "Select Member",
        list(edit_options.keys()),
        key="delete_member"
    )

    if st.button("Delete Selected Member"):
        delete_member(edit_options[delete_selection])
        st.success("Deleted Successfully")
        st.rerun()
    # ==================================================
    # STATISTICS
    # ==================================================
    st.markdown("---")
    st.subheader("Statistics")

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("Members", len(df))
    s2.metric("Average Experience", round(df["Experience"].mean(), 2))
    s3.metric("States Covered", df["State"].nunique())
    s4.metric("Work Locations", df["Work Location"].nunique())
else:
    st.info("No members added.")
