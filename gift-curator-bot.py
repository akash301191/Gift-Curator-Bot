import streamlit as st
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.models.openai import OpenAIChat

from textwrap import dedent

def render_sidebar():
    st.sidebar.title("🔐 API Configuration")
    st.sidebar.markdown("---")

    # OpenAI API Key input
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://platform.openai.com/account/api-keys)."
    )
    if openai_api_key:
        st.session_state.openai_api_key = openai_api_key
        st.sidebar.success("✅ OpenAI API key updated!")

    # SerpAPI Key input
    serp_api_key = st.sidebar.text_input(
        "Serp API Key",
        type="password",
        help="Don't have an API key? Get one [here](https://serpapi.com/manage-api-key)."
    )
    if serp_api_key:
        st.session_state.serp_api_key = serp_api_key
        st.sidebar.success("✅ Serp API key updated!")

    st.sidebar.markdown("---")

def render_gift_preferences():
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    # Column 1: Recipient Info
    with col1:
        st.subheader("👤 Recipient Info")
        age = st.number_input("Recipient’s Age*", min_value=1, step=1)
        relationship = st.selectbox(
            "Relationship to You*",
            ["Parent", "Sibling", "Partner", "Friend", "Child", "Colleague", "Teacher", "Other"]
        )
        gender = st.selectbox(
            "Gender (Optional)",
            ["Prefer not to say", "Male", "Female", "Other"]
        )

    # Column 2: Occasion & Interests
    with col2:
        st.subheader("🎉 Occasion & Interests")
        occasion = st.selectbox(
            "Occasion*",
            ["Birthday", "Anniversary", "Graduation", "Wedding", "Retirement", "Thank You", "Housewarming", "Baby Shower", "Just Because"]
        )
        interests = st.multiselect(
            "Recipient’s Interests*",
            ["Books", "Tech/Gadgets", "Fashion", "Fitness", "Food & Cooking", "Art & Craft", "Home Decor", "Travel", "Gaming", "Pets", "Wellness", "Music", "Hobbies"]
        )
        personality = st.selectbox(
            "Personality Type (Optional)",
            ["Not sure", "Sentimental", "Practical", "Trendy", "Humorous", "Creative", "Adventurous"]
        )

    # Column 3: Budget & Style
    with col3:
        st.subheader("💰 Budget & Style")
        budget = st.selectbox(
            "Budget Range*",
            ["Under $25", "$25–50", "$50–100", "$100–200", "$200+"]
        )
        gift_style = st.selectbox(
            "Preferred Gift Style (Optional)",
            ["No preference", "Thoughtful", "Fun", "Luxury", "Personalized", "DIY-friendly", "Techy", "Surprise me"]
        )
        notes = st.text_area("Special Notes (Optional)", placeholder="e.g., Avoid perfumes, they already have a Kindle")

    # Assemble user gift profile
    user_gift_preferences = f"""
**Recipient Info:**
- Age: {age}
- Relationship: {relationship}
- Gender: {gender}

**Occasion & Interests:**
- Occasion: {occasion}
- Interests: {', '.join(interests) if interests else 'Not specified'}
- Personality: {personality}

**Budget & Style:**
- Budget: {budget}
- Gift Style: {gift_style}
- Notes: {notes if notes.strip() else 'None'}
"""

    return user_gift_preferences

def generate_gift_recommendations(user_gift_preferences: str) -> str:
    # Step 1: Run Gift Researcher Agent
    research_agent = Agent(
        name="Gift Researcher",
        role="Finds trending and highly rated gift recommendations based on the user's recipient profile, occasion, and budget.",
        model=OpenAIChat(id='gpt-4o', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a gift discovery expert. Your task is to help users find thoughtful, trending, and well-reviewed gift ideas.
            Based on the user's detailed inputs—such as recipient age, relationship, occasion, interests, and budget—you'll generate a focused search term.
            Use this query to perform a web search and extract curated gift ideas from trustworthy sources.
        """),
        instructions=[
            "Carefully read the user's gift preferences to understand the recipient profile, occasion, interests, and budget.",
            "Generate ONE concise, focused gift search query. Example: 'best anniversary gifts for wife who loves cooking under $100'.",
            "Avoid vague queries like 'gift ideas' or 'top products'. Be specific and situational.",
            "Use `search_google` with the query.",
            "Extract 8–10 highly relevant links with curated gift lists, including sources like Good Housekeeping, Wirecutter, BuzzFeed, The Strategist, Etsy, UncommonGoods, etc.",
            "Do NOT generate or fabricate links. Only use what is found in the search results.",
        ],
        tools=[SerpApiTools(api_key=st.session_state.serp_api_key)],
        add_datetime_to_instructions=True,
    )

    research_response = research_agent.run(user_gift_preferences)
    research_results = research_response.content

    # Step 2: Run Gift Curator Agent
    curator_agent = Agent(
        name="Gift Curator",
        role="Creates a personalized gift shortlist using the user's profile and curated web results.",
        model=OpenAIChat(id='o3-mini', api_key=st.session_state.openai_api_key),
        description=dedent("""
            You are a thoughtful gift recommendation assistant.
            Your role is to use the user's recipient profile and a set of trusted links to create a personalized, curated shortlist of gift suggestions.

            Use:
            1. A structured summary of the user's gift preferences (recipient, occasion, interests, budget, style).
            2. A list of URLs pointing to curated gift recommendation sources.

            All gift suggestions must be based on real products mentioned in the links.
        """),
        instructions=[
            "Review the user's gift preferences carefully.",
            "Then analyze the provided research links.",
            "Extract real gift suggestions that match the recipient's profile, occasion, and budget.",
            "For each gift, provide: product name, 1-line description, why it's a good match, and a markdown link to the product or source.",
            "Use this format exactly:\n"
            "### [Gift Name]\n"
            "**Description**: \n"
            "**Why it's a great fit**: \n"
            "**Source**: [Site Name](link)\n",
            "Do NOT invent or fabricate gift ideas. Only include products found in the sources.",
            "Do NOT add intros or summaries — start directly with '## 🧾 Gift Recommendations'.",
            "Include 8–12 recommendations only. Focus on quality, variety, and relevance.",
        ],
        add_datetime_to_instructions=True,
    )

    curator_input = f"""
    User's Gift Preferences:
    {user_gift_preferences}

    Research Results:
    {research_results}

    Use these details to generate a gift recommendation report.
    """

    curator_response = curator_agent.run(curator_input)
    gift_report = curator_response.content

    return gift_report

def main() -> None:
    # Page config
    st.set_page_config(page_title="Gift Curator Bot", page_icon="🎁", layout="wide")

    # Custom styling
    st.markdown(
        """
        <style>
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        div[data-testid="stTextInput"] {
            max-width: 1200px;
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Header and intro
    st.markdown("<h1 style='font-size: 2.5rem;'>🎁 Gift Curator Bot</h1>", unsafe_allow_html=True)
    st.markdown(
        "Welcome to Gift Curator Bot — a personalized gift-finding tool that searches the web for the best gifts based on your inputs and filters them into a smart shortlist with description, links, and reasons to choose.",
        unsafe_allow_html=True
    )

    render_sidebar()
    user_gift_preferences = render_gift_preferences()

    st.markdown("---")

    if st.button("🎁 Get Gift Recommendations"):
        if not hasattr(st.session_state, "openai_api_key"):
            st.error("Please provide your OpenAI API key in the sidebar.")
        elif not hasattr(st.session_state, "serp_api_key"):
            st.error("Please provide your SerpAPI key in the sidebar.")
        else:
            with st.spinner("Finding the perfect gifts for you..."):
                gift_report = generate_gift_recommendations(user_gift_preferences=user_gift_preferences)
                st.session_state.gift_report = gift_report

    if "gift_report" in st.session_state:
        st.markdown(st.session_state.gift_report, unsafe_allow_html=True)
        st.markdown("---")

        st.download_button(
            label="📥 Download Gift List",
            data=st.session_state.gift_report,
            file_name="gift_recommendations.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()