# 🎬 Netflix Analytics Dashboard

An interactive Streamlit dashboard to explore Netflix Movies and TV Shows.

## Features
- **Filters:** type, country, release year range, and rating
- **KPI cards:** total titles, movies, TV shows
- **Overview tab:** Movies vs TV Shows, top 10 countries, top 10 genres, releases by year
- **Explore tab:** title search and data summary
- **Recommendation tab:** random "Surprise Me" pick based on your filters
- **Key insights** that update dynamically with the filters

## Tech Stack
Python · Pandas · Streamlit

## Dataset
[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) from Kaggle (`data/netflix_titles.csv`).

## Project Structure
```
netflix-analytics-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── netflix_titles.csv
└── notebooks/
    └── preprocessing.ipynb
```

## Run Locally
```bash
git clone https://github.com/<your-username>/netflix-analytics-dashboard.git
cd netflix-analytics-dashboard

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
streamlit run app.py
```
The app opens at http://localhost:8501.

> Run it with `streamlit run app.py`, not `python app.py`.

## Screenshots
Add screenshots here ([Code] (<img width="960" height="540" alt="Screenshot 2026-11-07 010004" src="https://github.com/user-attachments/assets/43c2119d-305d-492b-90bc-d2e447e6af5c" />).
([App Screenshot 1](<img width="960" height="540" alt="Screenshot 2026-11-07 010046" src="https://github.com/user-attachments/assets/2307c389-0ed3-4435-b6ef-0857fa485d97" />)
([App Screenshot 2](<img width="960" height="540" alt="Screenshot 2026-11-07 010114" src="https://github.com/user-attachments/assets/a6cb1ea0-4fcc-47a9-ad16-056823dc8f95" />)
([App Screenshot 3](<img width="960" height="540" alt="Screenshot 2026-11-07 010128" src="https://github.com/user-attachments/assets/93c23a5f-139f-451a-b81c-071a6982fdc2" />)
([App Screenshot 4](<img width="960" height="540" alt="Screenshot 2026-11-07 010150" src="https://github.com/user-attachments/assets/154a84eb-fa01-4a48-8f1f-f36bf321d092" />)


## Author
vineet arya · [GitHub](https://github.com/aryavin)
