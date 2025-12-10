import streamlit as st
import requests
import random
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()


# ---------- API CONFIG ----------
API_KEY = os.getenv("OMDB_API_KEY")  # <-- put your OMDb key here
BASE_URL = "http://www.omdbapi.com/?apikey=" + API_KEY

# Mood → Genre mapping
mood_to_genre = {
    "happy": "Comedy",
    "sad": "Drama",
    "romantic": "Romance",
    "thriller": "Thriller",
    "motivated": "Sport",
    "funny": "Comedy",
    "scared": "Horror",
}


# ---------- LOGIC ----------

def fetch_movie_for_mood(
    mood: str,
    region: str,
    year_filter_mode: str,
    exact_year: int | None,
    year_range: tuple[int, int] | None,
    rating_filter_mode: str,
    rating_range: tuple[float, float] | None,
    sort_mode: str,
    last_imdb_id: str | None = None,
) -> dict:
    """
    Return one movie dict for a given mood + filters.
    Try to avoid repeating last_imdb_id if possible.
    If no movie matches, raise LookupError.
    """
    mood = mood.lower().strip()
    if mood not in mood_to_genre:
        raise ValueError(f"Unknown mood: {mood}")

    genre = mood_to_genre[mood]

    # 1) Search movies using genre keyword
    search_url = f"{BASE_URL}&s={genre}&type=movie"
    response = requests.get(search_url, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "Search" not in data:
        raise LookupError("No movies found for this mood/genre.")

    movies = data["Search"]
    random.shuffle(movies)  # mix results

    candidates: list[dict] = []

    # unpack year range and rating range safely
    if year_range is not None:
        min_year, max_year = year_range
    else:
        min_year = max_year = None

    if rating_range is not None:
        min_rating, max_rating = rating_range
    else:
        min_rating = max_rating = None

    for movie in movies:
        movie_id = movie["imdbID"]
        details_url = f"{BASE_URL}&i={movie_id}"
        details = requests.get(details_url, timeout=10).json()

        # store imdbID in details for later use
        details["imdbID"] = movie_id

        # ---------- REGION FILTER ----------
        country = (details.get("Country") or "").lower()
        if region == "Bollywood (India)":
            if "india" not in country:
                continue
        elif region == "Hollywood (USA/UK)":
            if (
                "usa" not in country
                and "united states" not in country
                and "uk" not in country
                and "united kingdom" not in country
            ):
                continue
        # "Any" → no region filter

        # ---------- YEAR PARSING ----------
        year_str = (details.get("Year") or "")
        year_int = None
        if len(year_str) >= 4 and year_str[:4].isdigit():
            year_int = int(year_str[:4])

        # ---------- YEAR FILTER ----------
        if year_filter_mode == "Exact year":
            if year_int is None or year_int != exact_year:
                continue
        elif year_filter_mode == "Between range":
            if (
                year_int is None
                or min_year is None
                or max_year is None
                or not (min_year <= year_int <= max_year)
            ):
                continue
        # "Any year" → no filter

        # ---------- RATING PARSING ----------
        rating_str = details.get("imdbRating", "N/A")
        rating_val = None
        if rating_str not in ("N/A", None, ""):
            try:
                rating_val = float(rating_str)
            except ValueError:
                rating_val = None

        # ---------- RATING FILTER ----------
        if rating_filter_mode == "Minimum only":
            if rating_val is None or min_rating is None or rating_val < min_rating:
                continue
        elif rating_filter_mode == "Between range":
            if (
                rating_val is None
                or min_rating is None
                or max_rating is None
                or not (min_rating <= rating_val <= max_rating)
            ):
                continue
        # "Any rating" → no filter

        # keep parsed helpers for sorting
        details["_year_int"] = year_int
        details["_rating_val"] = rating_val
        details["_title_lower"] = (details.get("Title") or "").lower()

        candidates.append(details)

    if not candidates:
        raise LookupError("No movies matched your filters. Try relaxing them a bit.")

    # ---------- AVOID REPEATING LAST MOVIE ----------
    original_candidates = candidates[:]
    if last_imdb_id is not None and len(candidates) > 1:
        candidates = [c for c in candidates if c.get("imdbID") != last_imdb_id]
        # if filtering removed everything, fall back to full list
        if not candidates:
            candidates = original_candidates

    # ---------- SORTING ----------
    if sort_mode == "Newest first":
        candidates.sort(key=lambda d: d.get("_year_int") or 0, reverse=True)
    elif sort_mode == "Oldest first":
        candidates.sort(key=lambda d: d.get("_year_int") or 9999)
    elif sort_mode == "Highest rating":
        candidates.sort(key=lambda d: d.get("_rating_val") or 0.0, reverse=True)
    elif sort_mode == "Alphabetical (A–Z)":
        candidates.sort(key=lambda d: d.get("_title_lower") or "")
    else:  # "Random"
        random.shuffle(candidates)

    # pick the first movie after sorting / shuffling
    return candidates[0]


# ---------- STREAMLIT APP ----------

def main():
    st.set_page_config(page_title="Mood Movie Recommender", page_icon="🎬")

    st.title("🎬 Mood-Based Movie Recommender")
    st.write("Pick your mood, tune the filters, and get a movie suggestion.")

    # initialise session state for last movie
    if "last_imdb_id" not in st.session_state:
        st.session_state["last_imdb_id"] = None

    # ---- SIDEBAR FILTERS ----
    st.sidebar.header("Filters")

    region = st.sidebar.selectbox(
        "Region",
        options=["Any", "Hollywood (USA/UK)", "Bollywood (India)"],
        index=0,
    )

    # Year filter mode
    year_filter_mode = st.sidebar.selectbox(
        "Year filter type",
        options=["Any year", "Exact year", "Between range"],
        index=0,
    )

    exact_year = None
    year_range = None
    if year_filter_mode == "Exact year":
        exact_year = st.sidebar.number_input(
            "Year",
            min_value=1960,
            max_value=2025,
            value=2020,
            step=1,
        )
    elif year_filter_mode == "Between range":
        year_range = st.sidebar.slider(
            "Release year range",
            min_value=1960,
            max_value=2025,
            value=(2000, 2025),
        )

    # Rating filter mode
    rating_filter_mode = st.sidebar.selectbox(
        "Rating filter type",
        options=["Any rating", "Minimum only", "Between range"],
        index=0,
    )

    rating_range = None
    if rating_filter_mode == "Minimum only":
        min_rating = st.sidebar.slider(
            "Minimum IMDb rating",
            min_value=0.0,
            max_value=9.9,
            value=7.0,
            step=0.1,
        )
        rating_range = (min_rating, None)
    elif rating_filter_mode == "Between range":
        rating_range = st.sidebar.slider(
            "IMDb rating range",
            min_value=0.0,
            max_value=9.9,
            value=(6.0, 9.0),
            step=0.1,
        )

    # Sort mode
    sort_mode = st.sidebar.selectbox(
        "Sort movies by",
        options=[
            "Random",
            "Newest first",
            "Oldest first",
            "Highest rating",
            "Alphabetical (A–Z)",
        ],
        index=0,
    )

    # ---- MAIN CONTROLS ----
    mood = st.selectbox(
        "How do you feel right now?",
        options=list(mood_to_genre.keys()),
        index=0,
    )

    col1, col2 = st.columns(2)
    with col1:
        suggest_clicked = st.button("Suggest a movie 🎲")
    with col2:
        another_clicked = st.button("Another suggestion for this mood 🔁")

    st.caption(
        "Tip: Adjust filters in the sidebar, then click 🎲 or 🔁 for a movie "
        "that matches your mood + filters. 🔁 will try to avoid repeating the last movie."
    )

    if suggest_clicked or another_clicked:
        try:
            details = fetch_movie_for_mood(
                mood=mood,
                region=region,
                year_filter_mode=year_filter_mode,
                exact_year=exact_year,
                year_range=year_range,
                rating_filter_mode=rating_filter_mode,
                rating_range=rating_range,
                sort_mode=sort_mode,
                last_imdb_id=st.session_state["last_imdb_id"],
            )

            # update last_imdb_id so next time we can avoid it
            st.session_state["last_imdb_id"] = details.get("imdbID")

            title = details.get("Title", "Unknown")
            year = details.get("Year", "?")
            genre = details.get("Genre", "?")
            rating = details.get("imdbRating", "?")
            plot = details.get("Plot", "No plot available.")
            poster = details.get("Poster", None)

            st.subheader(f"🎭 Mood: **{mood}**")
            st.markdown(f"### 🎥 {title} ({year})")
            st.write(f"**Genre:** {genre}")
            st.write(f"**IMDb Rating:** {rating}")
            st.write(f"**Region (Country):** {details.get('Country', 'Unknown')}")

            if poster and poster != "N/A":
                st.image(poster, caption=title, use_container_width=True)

            st.markdown("**Plot:**")
            st.write(plot)

        except ValueError as e:
            st.error(str(e))
        except LookupError as e:
            st.warning(str(e))
        except requests.RequestException as e:
            st.error(f"Network error while calling the movie API.\n\n{e}")
        except Exception as e:
            st.error(f"Something went wrong.\n\n{e}")


if __name__ == "__main__":
    main()
