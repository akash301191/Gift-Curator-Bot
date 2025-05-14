# Gift Curator Bot

**Gift Curator Bot** is a smart Streamlit application that helps you discover thoughtful, personalized gift ideas based on your recipient's profile, occasion, and budget. Powered by [Agno](https://github.com/agno-agi/agno), OpenAI's GPT-4o, and SerpAPI, the bot searches the web for curated gift suggestions and generates a well-formatted shortlist with descriptions, links, and reasons to choose.

## Folder Structure

```
Gift-Curator-Bot/
├── gift-curator-bot.py
├── README.md
└── requirements.txt
```

* **gift-curator-bot.py**: The main Streamlit application.
* **requirements.txt**: Required Python packages.
* **README.md**: This documentation file.

## Features

* **Gift Preferences Input**
  Provide details about the recipient's age, relationship, occasion, interests, and budget for personalized results.

* **AI-Powered Gift Research**
  The Gift Researcher agent builds a targeted search query and uses SerpAPI to pull real-time curated gift lists from trusted sources.

* **Personalized Gift Report**
  The Gift Curator agent extracts high-quality product ideas and presents a short, tailored list with links, descriptions, and justifications.

* **Structured Markdown Output**
  Recommendations are presented in a clean, readable format using headings, bullets, and markdown links.

* **Download Option**
  Easily download the gift list as a `.txt` file for sharing or future reference.

* **Clean Streamlit UI**
  Designed with a wide layout, custom styling, and an intuitive interface for seamless exploration and gifting.

## Prerequisites

* Python 3.11 or higher
* An OpenAI API key ([Get one here](https://platform.openai.com/account/api-keys))
* A SerpAPI key ([Get one here](https://serpapi.com/manage-api-key))

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/akash301191/Gift-Curator-Bot.git
   cd Gift-Curator-Bot
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate        # On macOS/Linux
   # or
   venv\Scripts\activate           # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the app**:

   ```bash
   streamlit run gift-curator-bot.py
   ```

2. **In your browser**:

   * Add your OpenAI and SerpAPI keys in the sidebar.
   * Fill in recipient details, interests, and budget.
   * Click **🎁 Get Gift Recommendations**.
   * View your personalized AI-generated gift list.

3. **Download Option**
   Use the **📥 Download Gift List** button to save your recommendations as a `.txt` file.

## Code Overview

* **`render_gift_preferences()`**: Captures user input like relationship, occasion, interests, and budget.
* **`render_sidebar()`**: Stores and manages OpenAI and SerpAPI keys using Streamlit session state.
* **`generate_gift_recommendations()`**:

  * Uses the `Gift Researcher` agent to search curated gift suggestions.
  * Passes those results to the `Gift Curator` agent to generate a markdown report with links and summaries.
* **`main()`**: Manages the UI layout, input collection, gift generation flow, and output rendering.



## Contributions

Contributions are welcome! Feel free to fork the repo, suggest features, report bugs, or open a pull request. Please ensure your changes are well-tested and aligned with the app’s focus on curated, thoughtful user experiences.
