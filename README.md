# 💳 Credit Card Scraper with CrewAI + Gemini Flash 2.0

This project is a smart and scalable **credit card scraping tool** that uses **Selenium** for web automation and **Gemini Flash 2.0** (via Google AI) for intelligent content parsing. It leverages **CrewAI agents** to extract structured credit card data from web pages in a flexible, extensible architecture.

---

## 📁 Project Structure

```
CREDIT_CARD_SCRAPER/
├── Backend/
│   └── app.py                # Flask server to serve frontend
├── Frontend/
│   ├── static/
│   │   ├── script.js
│   │   └── style.css
│   └── templates/
│       └── index.html              # Web UI
├── GeminiCreditCardAgent/
│   ├── agents.py
│   ├── crew.py
│   ├── tasks.py
│   └── tools.py                   # CrewAI logic
├── modules/
│   ├── credit_card_links.py
│   ├── data_pre_process.py
│   └── scrape_format.py          # scraping instruction for agent
├── .env                           # Store your Gemini API key here
├── run.py                         # Main entry point
└── requirements.txt
```

---

## 🚀 Features

- 🔍 Scrapes credit card listings from dynamic sites (e.g., SBI)
- 🤖 Uses **Gemini Flash 2.0** agent for parsing content
- 🧠 Built with **CrewAI** agents and tools
- 🛠️ Preprocesses scraped data with regex
- 🌐 Simple Flask-based web frontend
- 📥 Download extracted data as a CSV file

---

## ⚙️ Setup Instructions

### 1. 🗝️ Get Your Gemini API Key

- Go to [Google AI Studio](https://aistudio.google.com/apikey)
- Create or log into your account
- Generate an **API key**
- Copy the key and add it to your `.env` file in the root directory:

```env
GEMINI_API_KEY=your_key_here
```

---

### 2. 💻 Clone the Repository

```bash
git clone https://github.com/AnurupaK/Credit-Card-Scrape-Agent.git
cd Credit-Card-Scrape-Agent
```

---

### 3. 🐍 Set Up Python Virtual Environment

```bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Or on macOS/Linux:
source venv/bin/activate
```

---

### 4. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have **Google Chrome** and the appropriate **ChromeDriver** installed and accessible in your PATH.

---

### 5. 🔧 Run the Application

```bash
python run.py
```

Then open your browser and navigate to:

```
http://localhost:5000
```

---

## 🌐 Supported Websites

Currently supports scraping from:

- [SBI Credit Cards](https://www.sbicard.com/en/personal/credit-cards.page)

---

## 🧠 How It Works

1. **Selenium** automates visiting each credit card URL and collects the `outerHTML`.
2. This raw HTML is passed to **Gemini Flash 2.0** via CrewAI agent for interpretation.
3. The agent returns a **JSON structure** representing credit card data.
4. The data is cleaned using **regex-based preprocessing**.
5. The frontend allows users to trigger and visualize scraping results.

---

## 🛠️ How to Use the App

The web app provides an interactive interface to control and monitor the scraping process.

### 🔘 UI Components

- **URL Box**: Paste the listing page URL (e.g., SBI credit cards)
- **Batch Size Box**: Set number of links to process at once
- **Buttons**:
  - `Start`: Begins scraping
  - `Next`: Processes the next batch
  - `Download CSV`: Exports current scraped data
- **Output Screen**: Displays parsed credit card info
- **Status Area**: Shows progress (e.g., `Fetching...`)

---

### 🧩 Flow of Operation

```
🔹 STEP 1: Input Details
   └─ 📥 Enter the **URL** of the credit card listing page
   └─ 🔢 Specify the **Batch Size** (number of links to process at a time)

            ⬇️

🔹 STEP 2: Start Scraping
   └─ ▶️ Click the **"Start"** button
   └─ ⏳ Status shows **"Fetching..."**
   └─ 🖥️ Scraped credit card data appears in the **Output Screen**

            ⬇️

🔹 STEP 3: (Optional) Scrape More
   └─ 🔁 Click the **"Next"** button to process the next batch of links
   └─ ⏳ Status shows **"Fetching..."**
   └─ ➕ New batch of scraped data is added to the output

            ⬇️

🔹 STEP 4: Download Data
   └─ 💾 Click **"Download CSV"** to export current data
   └─ 📌 Can be done:
         - After **Start**
         - After any **Next**
         - Or after scraping **all batches**

✅ **Flexible Downloading**: You can export data anytime—no need to wait until the end.
```

---

