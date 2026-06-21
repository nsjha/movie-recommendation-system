# 🎬 Movie Recommendation System

A content-based movie recommendation system built with Python and deployed as a web application. It leverages the **TMDB 5000 Movies Dataset** to suggest movies similar to a user's choice using cosine similarity on vectorized movie metadata.

---

## 🚀 Live Demo

> Deployed via Render · (https://movie-recommendation-system-ww2m.onrender.com/)

---

## 📌 Features

- 🔍 Search any movie and get top similar recommendations instantly
- 🧠 Content-based filtering using cosine similarity
- 📊 Built on the TMDB 5000 Movies & Credits dataset
- 🌐 Interactive web app powered by Streamlit / Flask (`app.py`)
- 📓 End-to-end pipeline documented in Jupyter Notebook

---

## 🗂️ Project Structure

```
movie-recommendation-system/
│
├── app.py                          # Web application (Streamlit/Flask)
├── movie-recommender-system.ipynb  # EDA, feature engineering & model building
├── movies_dict.pkl                 # Serialized movies dataframe (dictionary)
├── similarity.pkl                  # Precomputed cosine similarity matrix
├── tmdb_5000_movies.csv            # TMDB movies metadata
├── tmdb_5000_credits.csv           # TMDB cast & crew data
├── requirements.txt                # Python dependencies
├── Procfile                        # Render deployment config
└── setup.sh                        # Render server setup script
```

---

## 🧠 How It Works

1. **Data Preprocessing** — Merges the movies and credits datasets; extracts relevant features like genres, keywords, cast, crew, and overview.
2. **Feature Engineering** — Combines all features into a single "tags" column per movie.
3. **Vectorization** — Applies `CountVectorizer` (Bag of Words) to convert tags into numerical vectors.
4. **Similarity Computation** — Computes cosine similarity between all movie vectors.
5. **Recommendation** — For a selected movie, returns the top 5 most similar movies based on cosine similarity scores.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Data Processing | Pandas, NumPy |
| ML / NLP | Scikit-learn (CountVectorizer, Cosine Similarity) |
| Web App | Streamlit / Flask |
| Deployment | Render |
| Notebook | Jupyter |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/nsjha/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app locally
```bash
streamlit run app.py
# or
python app.py
```

### 4. Open in browser
```
http://localhost:8501
```

> **Note:** The `similarity.pkl` and `movies_dict.pkl` files must be present in the root directory. If missing, run the Jupyter Notebook (`movie-recommender-system.ipynb`) end-to-end to regenerate them.

---

## 📦 Dataset

- **Source:** [TMDB 5000 Movie Dataset – Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
- `tmdb_5000_movies.csv` — Movie metadata (title, genres, keywords, overview, etc.)
- `tmdb_5000_credits.csv` — Cast and crew information

---

## 📸 Screenshots

> <img width="787" height="667" alt="image" src="https://github.com/user-attachments/assets/af0cfe70-4cce-4ece-a379-ed14ef929cea" />


---

## 🚢 Deployment (Render)

This app is deployed on [Render](https://movie-recommendation-system-ww2m.onrender.com/). To deploy your own instance:

1. Push your code to GitHub
2. Go to [render.com](https://render.com) and create a **New Web Service**
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py` *(or `python app.py` for Flask)*
5. Click **Deploy** — Render handles the rest automatically

---

## 🙋‍♂️ Author

**Nishant Saurav (Jimmy)**  
B.Tech Mechanical Engineering | IIT Bhilai  
[GitHub](https://github.com/nsjha)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
