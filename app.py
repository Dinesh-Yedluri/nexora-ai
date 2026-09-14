import streamlit as st
import json
import pandas as pd
import plotly.express as px
import random

from engine.recommender import recommend_tools
from engine.ranking import rank_tools


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="NEXORA AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# THEME STATE
# -----------------------------

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

st.sidebar.markdown("### 🌗 Appearance")

theme_choice = st.sidebar.radio(
    "Theme",
    options=["Dark", "Light"],
    index=0 if st.session_state.theme == "Dark" else 1,
    horizontal=True,
    label_visibility="collapsed"
)

st.session_state.theme = theme_choice
is_dark = st.session_state.theme == "Dark"


# -----------------------------
# THEME COLORS
# -----------------------------

if is_dark:
    text_color = "#f1f3f6"
    caption_color = "#a8adba"
    card_bg = "#1a1e28"
    card_border = "#2a2e3a"
    sidebar_bg = "#0f1117"
    sidebar_border = "#23262f"
    video_opacity = "0. 15"
    footer_color = "#6b7280"
    anim_colors = "#0b0d13, #151830, #26123d, #0f1117, #0b0d13"
    accent = "#8b7cff"
    accent_hover = "#7566e6"
else:
    text_color = "#1a1d24"
    caption_color = "#6b7280"
    card_bg = "#ffffff"
    card_border = "#e5e7ef"
    sidebar_bg = "#ffffff"
    sidebar_border = "#e5e7ef"
    footer_color = "#9ca3af"
    anim_colors = "#f8f9fc, #eef0ff, #fdeef7, #f0f4ff, #f8f9fc"
    accent = "#6a5cff"
    video_opacity = "0.10"
    accent_hover = "#5646e0"


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Manrope:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Manrope', sans-serif;
    }}

    h1, h2, h3, h4, h5, h6, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
    }}

    .stApp {{
        background: linear-gradient(120deg, {anim_colors});
        background-size: 300% 300%;
        animation: gradientMove 20s ease infinite;
    }}

    @keyframes gradientMove {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    div[data-testid="stTextInput"] input {{
        border-radius: 16px;
        border: 2px solid {card_border};
        padding: 1rem 1.3rem;
        font-size: 1.05rem;
        background: {card_bg};
        color: {text_color} !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }}

    div[data-testid="stTextInput"] input:focus {{
        border-color: {accent} !important;
        box-shadow: 0 0 0 4px {accent}22, 0 4px 14px {accent}33 !important;
    }}

    div[data-testid="stTextInput"] input::placeholder {{
        color: {caption_color};
        font-style: italic;
    }}

    .stButton button, .stLinkButton a {{
        border-radius: 12px;
        font-weight: 600;
        font-family: 'Space Grotesk', sans-serif;
        padding: 0.6rem 1.4rem;
        background-color: {accent} !important;
        color: white !important;
        border: none !important;
        transition: all 0.2s ease;
    }}

    .stButton button {{
    position: relative;
    overflow: hidden;
    }}

    .stButton button::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s ease;
    }}

    .stButton button:hover::before {{
    left: 100%;
    }}

    .stButton button:hover, .stLinkButton a:hover {{
        background-color: {accent_hover} !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px {accent}44;
    }}

    .stButton button p, .stLinkButton a p {{
        color: white !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 16px !important;
    border: 1px solid {card_border} !important;
    background: {card_bg}cc;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    animation: fadeInUp 0.5s ease both;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {{
        border-color: {accent} !important;
        box-shadow: 0 10px 28px {accent}22;
        transform: translateY(-4px);
    }}

    section[data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {sidebar_border};
    }}

    .nexora-footer {{
        text-align: center;
        padding: 2rem 0 0.5rem 0;
        color: {footer_color};
        font-size: 0.85rem;
        font-family: 'Manrope', sans-serif;
    }}

    .stApp, .stApp p, .stApp span, .stApp label,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {{
        color: {text_color} !important;
    }}

    .stApp .stCaption, .stApp small {{
        color: {caption_color} !important;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {caption_color} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {text_color} !important;
        font-family: 'Space Grotesk', sans-serif !important;
    }}

    .nexora-hero-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
    animation: fadeInUp 0.6s ease both;
    background: linear-gradient(90deg, {accent}, #ff6ec4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    }}

    .nexora-hero-sub {{
        animation: fadeInUp 0.6s ease 0.1s both;
    }}


    div[data-testid="stMetricValue"] {{
        color: {text_color} !important;
    }}

    .block-container {{
        position: relative;
        z-index: 1;
    }}

    div[data-testid="stProgress"] > div > div {{
    background: linear-gradient(90deg, {accent}, #ff6ec4) !important;
    }}

    .blob {{
    position: fixed;
    border-radius: 50%;
    filter: blur(90px);
    z-index: -1;
    opacity: 0.35;
    animation: float 18s ease-in-out infinite;
}}

.blob1 {{
    width: 420px;
    height: 420px;
    background: {accent};
    top: -100px;
    left: -100px;
    animation-delay: 0s;
}}

.blob2 {{
    width: 380px;
    height: 380px;
    background: #ff6ec4;
    top: 40%;
    right: -120px;
    animation-delay: 6s;
    }}

    .blob3 {{
    width: 300px;
    height: 300px;
    background: {accent};
    bottom: -100px;
    left: 30%;
    animation-delay: 12s;
    }}

    @keyframes float {{
    0%, 100% {{ transform: translate(0, 0) scale(1); }}
    33% {{ transform: translate(40px, 60px) scale(1.1); }}
    66% {{ transform: translate(-30px, -40px) scale(0.95); }}
    }}

    header[data-testid="stHeader"] {{
    background: {sidebar_bg} !important;
    }}

    header[data-testid="stHeader"] button,
    header[data-testid="stHeader"] span,
    header[data-testid="stHeader"] p,
    header[data-testid="stHeader"] a {{
        color: {text_color} !important;
        opacity: 1 !important;
    }}

    header[data-testid="stHeader"] svg {{
        fill: {text_color} !important;
        opacity: 1 !important;
    }}

    div[data-testid="stToolbar"] button,
    div[data-testid="stToolbar"] span {{
        color: {text_color} !important;
        opacity: 1 !important;
    }}

    div[data-testid="stToolbar"] svg {{
        fill: {text_color} !important;
        opacity: 1 !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    """
    <div class="blob blob1"></div>
    <div class="blob blob2"></div>
    <div class="blob blob3"></div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# CATEGORY ICONS
# -----------------------------

CATEGORY_ICONS = {
    "AI Assistant": "🤖",
    "Writing": "✍️",
    "Presentation": "📊",
    "Video": "🎬",
    "Image Generation": "🖼️",
    "Customer Support": "🎧",
    "Automation": "⚙️",
    "Game Dev": "🎮",
    "Architecture": "🏛️",
    "3D & Animation": "🧊",
    "Audio": "🎧",
    "Career": "💼",
    "Chatbot Builder": "💬",
}

def format_count(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def get_icon(category):
    return CATEGORY_ICONS.get(category, "🔧")

def quiz_to_query(goal, budget, experience):
    query_parts = []

    goal_map = {
        "Create content (video/image/writing)": "create content video image writing",
        "Boost productivity / automate tasks": "automation productivity assistant",
        "Learn something new": "learning research education",
        "Build something (code/app/design)": "coding design development"
    }
    query_parts.append(goal_map.get(goal, ""))

    if budget == "Free only":
        query_parts.append("free")

    if experience == "Beginner":
        query_parts.append("easy simple beginner friendly")

    return " ".join(query_parts)


PERSONA_CATEGORIES = {
    "Everyone": [],
    "Student": ["Writing", "Presentation", "AI Assistant"],
    "Content Creator": ["Video", "Image Generation", "Audio", "Writing"],
    "Developer": ["AI Assistant", "Automation", "Chatbot Builder"],
    "Business / Marketing": ["Writing", "Customer Support", "Automation"],
    "Designer": ["Image Generation", "3D & Animation", "Architecture"],
}

# -----------------------------
# SESSION STATE - FAVORITES
# -----------------------------

if "favorites" not in st.session_state:
    st.session_state.favorites = {}


def toggle_favorite(tool):
    name = tool["name"]
    if name in st.session_state.favorites:
        del st.session_state.favorites[name]
    else:
        st.session_state.favorites[name] = tool

if "compare_list" not in st.session_state:
    st.session_state.compare_list = {}


def toggle_compare(tool):
    name = tool["name"]
    if name in st.session_state.compare_list:
        del st.session_state.compare_list[name]
    else:
        if len(st.session_state.compare_list) >= 3:
            st.warning("You can compare up to 3 tools at a time.")
        else:
            st.session_state.compare_list[name] = tool
if "recently_viewed" not in st.session_state:
    st.session_state.recently_viewed = []


def track_visit(tool):
    name = tool["name"]
    st.session_state.recently_viewed = [
        t for t in st.session_state.recently_viewed if t["name"] != name
    ]
    st.session_state.recently_viewed.insert(0, tool)
    st.session_state.recently_viewed = st.session_state.recently_viewed[:5]
# -----------------------------
# SESSION STATE - REVIEWS
# -----------------------------

if "reviews" not in st.session_state:
    st.session_state.reviews = {}


def add_review(tool_name, reviewer, comment, rating):
    if tool_name not in st.session_state.reviews:
        st.session_state.reviews[tool_name] = []
    st.session_state.reviews[tool_name].append({
        "reviewer": reviewer,
        "comment": comment,
        "rating": rating
    })


# -----------------------------
# LOAD AI TOOLS
# -----------------------------

@st.cache_data
def load_tools():
    with open("data/tools.json", "r", encoding="utf-8") as file:
        return json.load(file)


tools = load_tools()


# -----------------------------
# SIDEBAR - CATEGORY FILTER
# -----------------------------

st.sidebar.markdown("### 🙋 I am a...")

selected_persona = st.sidebar.selectbox(
    "Choose your role:",
    options=list(PERSONA_CATEGORIES.keys()),
    label_visibility="collapsed"
)

st.sidebar.divider()

all_categories = sorted(
    {tool.get("category", "Other") for tool in tools}
)


st.sidebar.markdown("### 🗂️ Filter by Category")

persona_cats = PERSONA_CATEGORIES.get(selected_persona, [])
default_cats = persona_cats if persona_cats else all_categories

selected_categories = st.sidebar.multiselect(
    "Show tools from:",
    options=all_categories,
    default=default_cats,
    label_visibility="collapsed"
)

st.sidebar.markdown("### 💰 Filter by Budget")

all_pricing = sorted(
    {tool.get("pricing", "Other") for tool in tools}
)

selected_pricing = st.sidebar.multiselect(
    "Show tools priced:",
    options=all_pricing,
    default=all_pricing,
    label_visibility="collapsed"
)

filtered_tools = [
    tool for tool in tools
    if tool.get("category", "Other") in selected_categories
    and tool.get("pricing", "Other") in selected_pricing
]


# -----------------------------
# SIDEBAR - FAVORITES
# -----------------------------

st.sidebar.divider()
st.sidebar.markdown(f"### ⭐ Favorites ({len(st.session_state.favorites)})")

if not st.session_state.favorites:
    st.sidebar.caption("No favorites yet. Save a tool to see it here.")
else:
    for fav_name, fav_tool in st.session_state.favorites.items():
        with st.sidebar.container(border=True):
            st.write(f"**{fav_name}**")
            st.caption(fav_tool.get("category", ""))
            if st.button("Remove", key=f"remove_{fav_name}"):
                toggle_favorite(fav_tool)
                st.rerun()

st.sidebar.divider()
st.sidebar.markdown(f"### 🕘 Recently Viewed")

if not st.session_state.recently_viewed:
    st.sidebar.caption("No tools viewed yet.")
else:
    for viewed_tool in st.session_state.recently_viewed:
        with st.sidebar.container(border=True):
            st.write(f"**{viewed_tool['name']}**")
            st.caption(viewed_tool.get("category", ""))


# -----------------------------
# GOOGLE-STYLE CENTERED SEARCH
# -----------------------------

st.write("")
st.write("")

center_col1, center_col2, center_col3 = st.columns([1, 2, 1])

with center_col2:
    st.markdown(
        "<h1 class='nexora-hero-title' style='text-align:center; font-size:3rem; margin-bottom:0;'>"
        "NEXORA AI</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='nexora-hero-sub' style='text-align:center; font-size:1.05rem; "
        f"color:{caption_color}; margin-top:0.4rem;'>"
        "One Task. The Right AI.</p>",
        unsafe_allow_html=True
    )

    st.write("")

    if "quick_fill" not in st.session_state:
        st.session_state.quick_fill = ""

    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)

    with chip_col1:
        if st.button("🎓 Study", width="stretch"):
            st.session_state.quick_fill = "I want to study and learn something new"
    with chip_col2:
        if st.button("💼 Work", width="stretch"):
            st.session_state.quick_fill = "I want to be more productive at work"
    with chip_col3:
        if st.button("🎨 Create", width="stretch"):
            st.session_state.quick_fill = "I want to create content or design something"
    with chip_col4:
        if st.button("🤖 Automate", width="stretch"):
            st.session_state.quick_fill = "I want to automate a repetitive task"

    user_query = st.text_input(
        "🔍 What do you want to do?",
        value=st.session_state.quick_fill,
        placeholder="Example: I want to create a PPT for my college seminar",
        label_visibility="collapsed"
    )

    button_col1, button_col2, button_col3 = st.columns([1, 1.4, 1])
    with button_col1:
        surprise_clicked = st.button("🎲 Surprise Me", width="stretch")
    with button_col2:
        find_clicked = st.button("Find the best AI tools", type="primary", width="stretch")


    st.write("")
    with st.expander("🧭 Not sure what to search? Take a quick quiz"):
        quiz_goal = st.selectbox(
            "What's your main goal?",
            ["Create content (video/image/writing)", "Boost productivity / automate tasks",
             "Learn something new", "Build something (code/app/design)"]
        )
        quiz_budget = st.radio("Budget preference?", ["Free only", "Free + Paid is fine"], horizontal=True)
        quiz_experience = st.radio("Experience level?", ["Beginner", "Experienced"], horizontal=True)

        quiz_submitted = st.button("🎯 Get My Recommendation", width="stretch")

        if quiz_submitted:
            st.session_state.quick_fill = quiz_to_query(quiz_goal, quiz_budget, quiz_experience)
            st.rerun()

st.write("")
st.divider()


# -----------------------------
# COMPARE TOOLS
# -----------------------------

if st.session_state.compare_list:
    st.markdown("### ⚖️ Compare Tools")
    st.caption(f"Comparing {len(st.session_state.compare_list)} tool(s) side by side")
    st.write("")

    compare_cols = st.columns(len(st.session_state.compare_list))

    for i, (name, tool) in enumerate(st.session_state.compare_list.items()):
        with compare_cols[i]:
            with st.container(border=True):
                icon = get_icon(tool.get("category", ""))
                st.markdown(f"**{icon} {tool['name']}**")
                st.caption(tool.get("category", ""))
                st.write(f"⭐ Rating: {tool.get('rating', 0)}/5")
                st.write(f"⚡ Efficiency: {tool.get('efficiency', 0)}/10")
                st.write(f"💰 Pricing: {tool.get('pricing', '')}")
                st.write(tool.get("description", ""))
                if st.button("Remove", key=f"compare_remove_{name}"):
                    toggle_compare(tool)
                    st.rerun()

    if st.button("🗑️ Clear All"):
        st.session_state.compare_list = {}
        st.rerun()

    st.divider()

# -----------------------------
# COMMUNITY FAVORITES
# -----------------------------

if st.session_state.favorites:
    st.markdown("### ❤️ Community Favorites")
    st.caption("Tools you've saved this session")
    st.write("")

    fav_cols = st.columns(min(len(st.session_state.favorites), 4))
    for i, (fav_name, fav_tool) in enumerate(st.session_state.favorites.items()):
        with fav_cols[i % 4]:
            icon = get_icon(fav_tool.get("category", ""))
            st.markdown(f"**{icon} {fav_name}**")
            st.caption(f"⭐ {fav_tool.get('rating', 0)}/5")

    st.divider()

# -----------------------------
# DASHBOARD / STATS
# -----------------------------

st.markdown("### 📊 NEXORA Insights")

total_tools = len(tools)
total_categories = len(all_categories)
avg_rating = round(
    sum(t.get("rating", 0) for t in tools) / total_tools, 2
) if total_tools > 0 else 0

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.metric("🧰 Total AI Tools", total_tools)

with stat_col2:
    st.metric("🗂️ Categories", total_categories)

with stat_col3:
    st.metric("⭐ Avg. Rating", f"{avg_rating}/5")

with st.expander("📈 Tools by Category", expanded=False):
    category_counts = {}
    for tool in tools:
        cat = tool.get("category", "Other")
        category_counts[cat] = category_counts.get(cat, 0) + 1

    chart_df = (
        pd.DataFrame(
            {"Category": list(category_counts.keys()),
             "Tools": list(category_counts.values())}
        )
        .sort_values("Tools", ascending=True)
    )

    fig = px.bar(
        chart_df, x="Tools", y="Category", orientation="h",
        color="Tools", color_continuous_scale=["#6a5cff", "#ff6ec4"], text="Tools"
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font_color=text_color, showlegend=False, coloraxis_showscale=False,
        height=max(400, len(chart_df) * 28), margin=dict(l=10, r=30, t=10, b=10)
    )
    st.plotly_chart(fig, width="stretch")

st.divider()


# -----------------------------
# HELPER - SCORE BADGE
# -----------------------------

def score_badge(score, relevance=1):
    if relevance <= 0.05:
        return (
            "<span style='background:#6b728022; color:#9ca3af; "
            "padding:3px 10px; border-radius:20px; font-size:0.75rem; "
            "font-weight:600;'>💡 You might also like</span>"
        )
    if score >= 70:
        color, label = "#22c55e", "Excellent Match"
    elif score >= 40:
        color, label = "#eab308", "Good Match"
    else:
        color, label = "#ef4444", "Possible Match"

    return (
        f"<span style='background:{color}22; color:{color}; "
        f"padding:3px 10px; border-radius:20px; font-size:0.75rem; "
        f"font-weight:600;'>{label} · {score}</span>"
    )


# -----------------------------
# TOOL CARD RENDERER
# -----------------------------

def render_tool_card(index, tool):
    with st.container(border=True):

        top_col1, top_col2, top_col3 = st.columns([5, 2, 1.3])

    with top_col1:
        icon = get_icon(tool.get("category", ""))
        trending_badge = " 🔥" if tool.get("rating", 0) >= 4.5 else ""
        st.markdown(f"#### {icon} {index}. {tool['name']}{trending_badge}")
        base_reviews = tool.get("reviews", 0)
        live_reviews = len(st.session_state.reviews.get(tool["name"], []))
        total_reviews = base_reviews + live_reviews
        st.caption(
            f"🗂️ {tool['category']}  •  💰 {tool['pricing']}  •  "
            f"⭐ {tool.get('rating', 0)} ({format_count(total_reviews)} ratings)"
    )

       
        with top_col2:
            st.markdown(
                f"<div style='text-align:right; margin-top:0.8rem;'>"
                f"{score_badge(tool.get('overall_score', 0), tool.get('relevance', 1))}</div>",
                unsafe_allow_html=True
            )

        with top_col3:
            is_fav = tool["name"] in st.session_state.favorites
            star_icon = "⭐" if is_fav else "☆"
            if st.button(star_icon, key=f"fav_{tool['name']}_{index}", help="Save to favorites"):
                toggle_favorite(tool)
                st.rerun()

        st.write(tool["description"])

        st.progress(min(tool.get('rating', 0) / 5, 1.0), text=f"⭐ Rating: {tool.get('rating', 0)}/5")
        st.progress(min(tool.get('efficiency', 0) / 10, 1.0), text=f"⚡ Efficiency: {tool.get('efficiency', 0)}/10")

        is_comparing = tool["name"] in st.session_state.compare_list
        compare_checked = st.checkbox(
            "⚖️ Add to Compare",
            value=is_comparing,
            key=f"compare_{tool['name']}_{index}"
        )
        if compare_checked != is_comparing:
            toggle_compare(tool)
            st.rerun()


        tool_reviews = st.session_state.reviews.get(tool["name"], [])

        with st.expander(f"💬 Reviews ({len(tool_reviews)})"):
            if not tool_reviews:
                st.caption("No reviews yet. Be the first to share your experience!")
            else:
                avg_user_rating = round(
                    sum(r["rating"] for r in tool_reviews) / len(tool_reviews), 1
                )
                st.caption(f"⭐ User average: {avg_user_rating}/5 from {len(tool_reviews)} review(s)")
                st.write("")
                for r in tool_reviews:
                    st.markdown(f"**{r['reviewer']}** — {'⭐' * r['rating']}")
                    st.write(r["comment"])
                    st.write("")

            st.divider()

            with st.form(key=f"review_form_{tool['name']}_{index}"):
                reviewer_name = st.text_input("Your name", placeholder="Anonymous")
                review_rating = st.slider("Your rating", 1, 5, 5)
                review_comment = st.text_area("Your review", placeholder="What did you think of this tool?")
                submitted = st.form_submit_button("Post Review")

                if submitted:
                    if review_comment.strip():
                        add_review(
                            tool["name"],
                            reviewer_name.strip() if reviewer_name.strip() else "Anonymous",
                            review_comment.strip(),
                            review_rating
                        )
                        st.success("Review posted!")
                        st.rerun()
                    else:
                        st.warning("Please write a comment before posting.")
        visit_col1, visit_col2 = st.columns([1, 4])
        with visit_col1:
            if st.button("👁️", key=f"track_{tool['name']}_{index}", help="Mark as viewed"):
                track_visit(tool)
        with visit_col2:
            st.link_button("🌐 Visit Tool", tool["website"], width="stretch")


def render_tool_grid(tool_list, per_row=2):
    for i in range(0, len(tool_list), per_row):
        row = tool_list[i:i + per_row]
        cols = st.columns(per_row)
        for col, tool in zip(cols, row):
            with col:
                render_tool_card(i + row.index(tool) + 1, tool)


# -----------------------------
# SURPRISE ME
# -----------------------------

if surprise_clicked:
    if not filtered_tools:
        st.warning("No categories selected. Please select at least one category.")
    else:
        surprise_tool = random.choice(filtered_tools).copy()
        surprise_tool["overall_score"] = round(
            (surprise_tool.get("rating", 0) / 5) * 50
            + (surprise_tool.get("efficiency", 0) / 10) * 50,
            2
        )
        surprise_tool["relevance"] = 1

        st.markdown("### 🎉 Here's a Tool for You!")
        st.write("")
        render_tool_card(1, surprise_tool)


# -----------------------------
# RECOMMENDATION
# -----------------------------

if find_clicked:
    if not user_query.strip():
        st.warning("Please tell me what you want to do.")
    elif not filtered_tools:
        st.warning("No categories selected. Please select at least one category.")
    else:
        recommendations = recommend_tools(user_query, filtered_tools)

        if not recommendations:
            st.info("No matching AI tools found. Try describing your task differently.")
        else:
            relevance_scores = {tool["name"]: relevance for tool, relevance in recommendations}

            ranked_tools = rank_tools(
                [tool for tool, _ in recommendations],
                relevance_scores
            )

            for t in ranked_tools:
                t["relevance"] = relevance_scores.get(t["name"], 0)

            st.success(f"Found {len(ranked_tools)} relevant AI tools!")
            st.markdown("### 🏆 Recommended AI Tools")
            st.write("")

            render_tool_grid(ranked_tools, per_row=2)

            st.write("")
            export_text = f"My NEXORA AI Recommendations for: \"{user_query}\"\n\n"
            for i, t in enumerate(ranked_tools, start=1):
                export_text += f"{i}. {t['name']} ({t['category']}) - {t['pricing']}\n"
                export_text += f"   {t['description']}\n"
                export_text += f"   Rating: {t['rating']}/5 | Website: {t['website']}\n\n"

            st.download_button(
                label="📥 Download Results as Text File",
                data=export_text,
                file_name="nexora_ai_recommendations.txt",
                mime="text/plain",
                width="stretch"
            )

# -----------------------------
# DEFAULT BROWSABLE GRID
# (shown when nothing searched yet)
# -----------------------------

if not find_clicked and not surprise_clicked:
    st.markdown("### ✨ Popular AI Tools")
    st.write("")

    top_tools = sorted(filtered_tools, key=lambda t: t.get("rating", 0), reverse=True)[:6]

    for t in top_tools:
        t["overall_score"] = round(
            (t.get("rating", 0) / 5) * 50 + (t.get("efficiency", 0) / 10) * 50, 2
        )
        t["relevance"] = 1

    render_tool_grid(top_tools, per_row=3)


# -----------------------------
# COMPARE TOOLS TABLE
# -----------------------------

if st.session_state.compare_list:
    st.divider()
    st.markdown("### ⚖️ Compare Selected Tools")

    compare_data = []
    for name, tool in st.session_state.compare_list.items():
        compare_data.append({
            "Tool": tool["name"],
            "Category": tool.get("category", ""),
            "Pricing": tool.get("pricing", ""),
            "Rating": tool.get("rating", 0),
            "Efficiency": tool.get("efficiency", 0),
            "Description": tool.get("description", "")
        })

    compare_df = pd.DataFrame(compare_data)
    st.dataframe(compare_df, width="stretch", hide_index=True)

    if st.button("Clear Comparison"):
        st.session_state.compare_list = {}
        st.rerun()

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    """
    <div class="nexora-footer">
        Built with &#10084;&#65039; by NEXORA AI &middot; One Task. The Right AI.
    </div>
    """,
    unsafe_allow_html=True
)