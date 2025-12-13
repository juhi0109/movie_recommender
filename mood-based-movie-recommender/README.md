# 🎬 Mood-Based Movie Recommendation App

## 📌 Project Description

The **Mood-Based Movie Recommendation App** suggests movies based on the user’s **current mood**.  
Instead of manually searching for movies, users can simply select how they feel (happy, sad, romantic, etc.) and instantly receive a movie recommendation that matches their mood.

The project evolved from a **basic Python logic-based program** into an **interactive Streamlit web application** that normal (non-technical) users can easily use through a browser.

Real-time movie data is fetched using a movie API, and users can further personalize recommendations using **filters like rating, year, and sorting preferences**.

---

## 🛠️ Tech Stack Used

### 🔹 Programming Language
- Python 3

### 🔹 Libraries & Frameworks
- Streamlit – for building the web application UI
- Requests – for API calls
- Random – for random movie selection

### 🔹 API
- OMDb API / TMDB API (for fetching real movie data)

### 🔹 Tools
- VS Code
- Git & GitHub

---

## ⚙️ How the Implementation Took Place

1. **Mood-to-Genre Mapping**
   - User moods are mapped to movie genres using Python dictionaries.

2. **API Integration**
   - Real movie data is fetched using a public movie API.
   - JSON responses are parsed to extract:
     - Movie title
     - Release year
     - Genre
     - IMDb rating
     - Plot
     - Poster image

3. **Filtering & Sorting**
   - Users can filter movies by:
     - Rating (minimum or range)
     - Release year (any, exact year, or range)
   - Sorting options include:
     - Random
     - Newest first
     - Oldest first
     - Highest rating
     - Alphabetical order

4. **Streamlit UI**
   - Converted terminal-based interaction into a web-based UI.
   - Added dropdowns, buttons, sidebar filters, and poster display.
   - Used `st.session_state` to avoid repeating the same movie when requesting another suggestion.

5. **Error Handling**
   - Gracefully handles API errors and strict filter conditions.
   - Displays user-friendly messages when no movies match the filters.

---

## 📚 What I Learned from This Project

- Working with real-world APIs
- Understanding API limitations
- Parsing and filtering JSON data
- Building interactive web apps using Streamlit
- Managing application state with `st.session_state`
- Designing user-friendly filters and sorting logic
- Importance of securing API keys
- Writing clean, modular Python code
- Using GitHub to document and showcase projects

---

## ▶️ How to Run This Project on Your System

### 🔹 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 🔹 Step 2: (Optional) Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

#### Windows
```bash
venv\Scripts\activate
```
#### macOS/ Linux
```bash
source venv/bin/activate
```
### 🔹 Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```
If multiple Python versions are installed:
```bash
python -m pip install -r requirements.txt
```

### 🔹 Step 4: Add Your API Key
Create the following file:
```bash
.streamlit/secrets.toml
```
Add:
```toml
MOVIE_API_KEY = "YOUR_API_KEY_HERE"
```
### ⚠️ Never expose your API key publicly.
---
## 📦 requirements.txt
Create a file named requirements.txt in the project root and add:
```txt
streamlit
requests
```
(Optional - with version pinning)
```txt
streamlit>=1.30.0
requests>=2.31.0
```

## ▶️ How to Install Requirements (Bash Commands)

### 🔹 For Windows (PowerShell / CMD)
```bash
pip install -r requirements.txt
```
If you are using multiple Python versions:
```bash
python -m pip install -r requirements.txt
```
### 🔹 For macOS / Linux (Terminal)
```bash
pip3 install -r requirements.txt
```
Or:
```bash
python3 -m pip install -r requirements.txt
```
### 🔹 Using a Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### 🔹 Step 5: Run the Application

```bash
streamlit run mood_movie_streamlit.py
```
The app will open automatically in your browser at:
```arduino
http://localhost:8501
```
---
## 🛠️ Tech Stack Used
- Full migration to TMDB API for better filtering and pagination
- Add user favorites and history
- Deploy publicly using Streamlit Cloud
- Add AI-based personalized recommendations
- Improve UI with card-based layout and animations
---
## 👤 Author
### Juhi Agarwal

### Python & ML Enthusiast

### GitHub: https://github.com/juhi0109
