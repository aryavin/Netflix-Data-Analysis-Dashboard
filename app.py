import streamlit as st
import pandas as pd
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="🎬",
    layout="wide"
)


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "netflix_titles.csv"
    return pd.read_csv(data_path)


df = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("🎬 Netflix Analytics Dashboard")

st.write(
    "Explore Netflix Movies and TV Shows using interactive data analysis."
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Filters")


# -------------------------
# Type Filter
# -------------------------

selected_type = st.sidebar.selectbox(
    "Select Type",
    ["All", "Movie", "TV Show"]
)


# -------------------------
# Country Filter
# -------------------------

country_list = (
    df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .dropna()
    .unique()
)

country_list = sorted(country_list)


selected_country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + country_list
)


# -------------------------
# Release Year Filter
# -------------------------

min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())


selected_year = st.sidebar.slider(
    "Release Year",
    min_year,
    max_year,
    (min_year, max_year)
)


# -------------------------
# Rating Filter
# -------------------------

rating_list = sorted(
    df["rating"].dropna().unique()
)


selected_rating = st.sidebar.selectbox(
    "Select Rating",
    ["All"] + rating_list
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


# Type Filter

if selected_type != "All":

    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]


# Country Filter

if selected_country != "All":

    filtered_df = filtered_df[
        filtered_df["country"]
        .fillna("")
        .str.contains(
            selected_country,
            case=False,
            na=False
        )
    ]


# Release Year Filter

filtered_df = filtered_df[
    filtered_df["release_year"].between(
        selected_year[0],
        selected_year[1]
    )
]


# Rating Filter

if selected_rating != "All":

    filtered_df = filtered_df[
        filtered_df["rating"] == selected_rating
    ]


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_titles = len(filtered_df)

total_movies = (
    filtered_df["type"] == "Movie"
).sum()

total_tv_shows = (
    filtered_df["type"] == "TV Show"
).sum()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


col1.metric(
    "🎬 Total Titles",
    total_titles
)


col2.metric(
    "🎥 Movies",
    total_movies
)


col3.metric(
    "📺 TV Shows",
    total_tv_shows
)


# =========================================================
# PREPARE DATA FOR CHARTS
# =========================================================


# Type

type_count = (
    filtered_df["type"]
    .value_counts()
)


# Countries

country_data = (
    filtered_df["country"]
    .dropna()
    .str.split(", ")
    .explode()
)

country_count = (
    country_data
    .value_counts()
    .head(10)
)


# Genres

genre_data = (
    filtered_df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
)

genre_count = (
    genre_data
    .value_counts()
    .head(10)
)


# Release Year

year_count = (
    filtered_df["release_year"]
    .value_counts()
    .sort_index()
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "🔎 Explore",
        "🎲 Recommendation"
    ]
)


# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tab1:

    st.subheader("📊 Netflix Overview")

    st.write(
        f"Showing **{len(filtered_df)}** records based on your filters."
    )


    # -------------------------
    # Movies vs TV + Countries
    # -------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("🎬 Movies vs TV Shows")

        st.bar_chart(
            type_count
        )


    with col2:

        st.subheader("🌍 Top 10 Countries")

        st.bar_chart(
            country_count
        )


    # -------------------------
    # Genres + Release Year
    # -------------------------

    col3, col4 = st.columns(2)


    with col3:

        st.subheader("🎭 Top 10 Genres")

        st.bar_chart(
            genre_count
        )


    with col4:

        st.subheader("📈 Content by Release Year")

        st.line_chart(
            year_count
        )


    # -------------------------
    # Dataset
    # -------------------------

    st.subheader("📋 Filtered Dataset")

    st.dataframe(
        filtered_df,
        width="stretch"
    )


# =========================================================
# TAB 2 — EXPLORE
# =========================================================

with tab2:

    st.subheader("🔎 Search Netflix")


    search = st.text_input(
        "Search Movie or TV Show",
        placeholder="Enter title..."
    )


    if search:

        search_result = filtered_df[
            filtered_df["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]


        st.write(
            f"Found **{len(search_result)}** result(s)"
        )


        if len(search_result) > 0:

            st.dataframe(
                search_result,
                width="stretch"
            )

        else:

            st.warning(
                "No matching titles found."
            )


    # -------------------------
    # Data Summary
    # -------------------------

    st.subheader("📌 Data Summary")


    summary_col1, summary_col2 = st.columns(2)


    with summary_col1:

        if len(filtered_df) > 0:

            most_common_rating = (
                filtered_df["rating"]
                .mode()
            )

            if len(most_common_rating) > 0:

                st.write(
                    f"⭐ **Most Common Rating:** "
                    f"{most_common_rating.iloc[0]}"
                )


    with summary_col2:

        if len(country_count) > 0:

            top_country = country_count.index[0]

            st.write(
                f"🌍 **Top Country:** "
                f"{top_country}"
            )


    # -------------------------
    # Top Genre
    # -------------------------

    if len(genre_count) > 0:

        top_genre = genre_count.index[0]

        st.write(
            f"🎭 **Top Genre:** {top_genre}"
        )


    # -------------------------
    # Latest Release
    # -------------------------

    if len(filtered_df) > 0:

        latest_year = filtered_df[
            "release_year"
        ].max()

        st.write(
            f"📅 **Latest Release Year:** "
            f"{latest_year}"
        )


# =========================================================
# TAB 3 — RECOMMENDATION
# =========================================================

with tab3:

    st.subheader("🎲 Surprise Me")


    if len(filtered_df) > 0:

        st.write(
            "Click the button to get a random Netflix recommendation."
        )


        if st.button(
            "🎲 Give Me a Netflix Pick"
        ):

            random_show = (
                filtered_df
                .sample(1)
                .iloc[0]
            )


            st.success(
                f"🎬 {random_show['title']}"
            )


            st.write(
                f"**Type:** {random_show['type']}"
            )


            st.write(
                f"**Release Year:** "
                f"{random_show['release_year']}"
            )


            st.write(
                f"**Rating:** "
                f"{random_show['rating']}"
            )


            st.write(
                f"**Genre:** "
                f"{random_show['listed_in']}"
            )


            st.write(
                f"**Country:** "
                f"{random_show['country']}"
            )


            st.write(
                f"**Description:** "
                f"{random_show['description']}"
            )


    else:

        st.warning(
            "No titles available for the selected filters."
        )


# =========================================================
# DYNAMIC INSIGHTS
# =========================================================

st.divider()

st.subheader("📌 Key Insights")


if len(filtered_df) > 0:

    # Movies vs TV Shows

    if total_movies > total_tv_shows:

        st.write(
            f"🎬 Movies dominate the selected dataset "
            f"with **{total_movies}** titles."
        )

    elif total_tv_shows > total_movies:

        st.write(
            f"📺 TV Shows dominate the selected dataset "
            f"with **{total_tv_shows}** titles."
        )

    else:

        st.write(
            "🎬 Movies and TV Shows have equal representation."
        )


    # Top Country

    if len(country_count) > 0:

        st.write(
            f"🌍 The leading country in the selected data is "
            f"**{country_count.index[0]}**."
        )


    # Top Genre

    if len(genre_count) > 0:

        st.write(
            f"🎭 The most common genre is "
            f"**{genre_count.index[0]}**."
        )


    # Latest Year

    latest_year = filtered_df[
        "release_year"
    ].max()

    st.write(
        f"📅 The latest release year in the selected data is "
        f"**{latest_year}**."
    )


else:

    st.warning(
        "No data available. Try changing the filters."
    )