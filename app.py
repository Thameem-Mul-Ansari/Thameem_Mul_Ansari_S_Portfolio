import streamlit as st
import json
import os
from PIL import Image
from streamlit_option_menu import option_menu
import datetime
import requests

# Page configuration
st.set_page_config(
    page_title="Thameem Mul Ansari S - Portfolio",
    page_icon="🚀",
    layout="wide", # Keeping wide layout for maximum content area
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with vibrant color scheme (Updated to target image correctly)
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        text-align: center;
        margin-bottom: 0;
    }
    
    .sub-header {
        font-size: 1.4rem;
        color: #6c757d;
        text-align: center;
        margin-top: 10px;
        font-weight: 500;
        background: linear-gradient(135deg, #495057 0%, #6c757d 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .project-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-left: 6px solid;
        border-image: linear-gradient(135deg, #667eea, #764ba2) 1;
        position: relative;
        overflow: hidden;
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
        transition: left 0.6s;
    }
    
    .project-card:hover::before {
        left: 100%;
    }
    
    .project-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.25);
    }
    
    .achievement-card {
        background: linear-gradient(135deg, #fff9c4 0%, #ffecb3 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255, 193, 7, 0.15);
        transition: all 0.4s ease;
        border-left: 6px solid #ffd54f;
        position: relative;
        overflow: hidden;
    }
    
    .achievement-card::after {
        content: '🏆';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 2rem;
        opacity: 0.1;
    }
    
    .achievement-card:hover {
        transform: translateY(-5px) rotate(1deg);
        box-shadow: 0 15px 35px rgba(255, 193, 7, 0.25);
    }
    
    .experience-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(33, 150, 243, 0.15);
        border-left: 6px solid #2196f3;
        transition: all 0.3s ease;
    }
    
    .experience-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(33, 150, 243, 0.2);
    }
    
    .skill-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 18px;
        border-radius: 25px;
        display: inline-block;
        margin: 8px 5px;
        font-size: 0.95rem;
        font-weight: 600;
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .skill-badge:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    .link-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 25px;
        border-radius: 30px;
        text-decoration: none;
        display: inline-block;
        margin: 8px;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
        border: none;
        cursor: pointer;
        text-align: center;
    }
    
    .link-button:hover {
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6);
        color: white;
        text-decoration: none;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stats-card:hover {
        transform: translateY(-8px) rotate(1deg);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .stats-number {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #f5576c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stats-label {
        font-size: 1.1rem;
        color: #495057;
        margin-top: 8px;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #343a40 0%, #495057 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 40px 0 25px 0;
        padding-bottom: 12px;
        border-bottom: 4px solid;
        border-image: linear-gradient(135deg, #667eea, #f5576c) 1;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    @keyframes float {
        0% { transform: translateY(0px) }
        50% { transform: translateY(-10px) }
        100% { transform: translateY(0px) }
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 30px;
        padding: 12px 30px;
        border: none;
        font-weight: 600;
        transition: all 0.4s ease;
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* FIX for profile picture styling using CSS selector */
    /* Targets the first image rendered in the main content area */
    div.stHeadingContainer + div.stImage > img { 
        border-radius: 50%;
        border: 5px solid;
        border-image: linear-gradient(135deg, #667eea, #f5576c) 1;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.4s ease;
        display: block;
        margin: 0 auto;
        animation: float 6s ease-in-out infinite; /* Apply floating animation here */
    }

    div.stHeadingContainer + div.stImage > img:hover {
        transform: scale(1.05) rotate(5deg);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }

    /* Target the sidebar image specifically */
    .st-emotion-cache-1mn048v img { 
        border-radius: 50%;
        border: 3px solid;
        border-image: linear-gradient(135deg, #f5576c, #667eea) 1;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        display: block;
        margin: 0 auto;
    }
    
    .category-tag {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    /* Center the link buttons on the header */
    .link-button-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 15px;
    }
    
    .contact-info-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 20px;
    }
    
    .contact-item {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Data from Resume
def get_resume_data():
    profile = {
        "name": "THAMEEM MUL ANSARI S",
        "title": "APPLIED AI & AUTOMATION ENGINEER | RPA DEVELOPER",
        "email": "thameemmulansaris@gmail.com",
        "phone": "+91 6369318648",
        "location": "Chennai, TN",
        "linkedin": "https://linkedin.com/in/thameem-mul-ansari",
        "github": "https://github.com/thameemmulansari",
        "portfolio": "https://thameem-portfolio.com",
        "about": """Passionate about building intelligent automation systems integrating LLMs, RPA, 
        and data analytics. Skilled in developing AI-driven solutions that optimize business processes, 
        enhance customer experience, and improve operational efficiency across fintech, retail, and enterprise domains."""
    }
    
    experiences = [
        {
            "role": "Applied AI Engineer & RPA Developer",
            "company": "AI Solutions Lab",
            "period": "Jan 2025 – Present",
            "projects": [
                "AI-powered Sales Intelligence Dashboard using Python (Flask), React (TypeScript), Firebase, and Azure GPT-4",
                "Omni-Channel Customer Support Chatbot across WhatsApp, Messenger, and Instagram",
                "Export Bills Regularization Workflow using Microsoft Power Automate and Vision LLM",
                "Store Reconciliation Automation System integrating multiple payment APIs",
                "Hardware Support Assistant using LLaMA-3 Vision and Streamlit",
                "Employee Onboarding Assistant using Gemma-2 9B-IT and Supabase",
                "ATC Crash Analysis Assistant using Whisper + LangChain + CrewAI"
            ]
        }
    ]
    
    projects = [
        {
            "title": "AI-Powered Sales Intelligence Dashboard",
            "description": "Engineered real-time call analytics with automated speech transcription and performance scoring using Azure GPT-4, improving call review coverage from 10% to 100% while reducing manual QA time by 50%.",
            "tech_stack": "Python, Flask, React, TypeScript, Firebase, Azure GPT-4",
            "category": "AI & Automation",
            "impact": "100% call review coverage, 50% reduction in manual QA time",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        },
        {
            "title": "Omni-Channel Customer Support Chatbot",
            "description": "Deployed across WhatsApp, Messenger, and Instagram using N8N, PostgreSQL, and Qdrant Vector DB. Automated 24/7 responses achieving 95% accuracy and reducing agent load by 70%.",
            "tech_stack": "N8N, PostgreSQL, Qdrant Vector DB, Shopify API, GraphQL",
            "category": "AI Chatbot",
            "impact": "95% response accuracy, 70% reduction in agent load",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        },
        {
            "title": "Export Bills Regularization Workflow",
            "description": "Automated workflow using Microsoft Power Automate and Vision LLM to extract invoice metadata from scanned PDFs, reducing multi-day operations to 30 minutes per batch.",
            "tech_stack": "Microsoft Power Automate, Vision LLM, Payment Gateway APIs",
            "category": "RPA & Automation",
            "impact": "Multi-day process reduced to 30 minutes",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        },
        {
            "title": "Store Reconciliation Automation System",
            "description": "Integrated Odoo, ICICI, Paytm, PhonePe, Amex, and Pinelabs APIs with Python data validation logic, cutting financial audit processing time from 8 hours to 15 minutes for 6 stores.",
            "tech_stack": "Python, Odoo, Multiple Payment APIs, Data Validation",
            "category": "Fintech Automation",
            "impact": "8 hours reduced to 15 minutes",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        },
        {
            "title": "Hardware Support Assistant",
            "description": "Leveraged LLaMA-3 Vision and Streamlit to detect hardware defects from uploaded images, automate warranty verification, and schedule service appointments, reducing IT support workload by 40%.",
            "tech_stack": "LLaMA-3 Vision, Streamlit, Computer Vision",
            "category": "AI Assistant",
            "impact": "40% reduction in IT support workload",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        },
        {
            "title": "Employee Onboarding Assistant",
            "description": "Used Gemma-2 9B-IT and Supabase to collect, validate, and store employee data securely through conversational AI interface, accelerating onboarding by 60%.",
            "tech_stack": "Gemma-2 9B-IT, Supabase, Conversational AI",
            "category": "HR Automation",
            "impact": "60% faster onboarding",
            "github_link": "#",
            "hosted_link": "#",
            "video_link": "#",
            "blog_link": "#"
        }
    ]
    
    achievements = [
        {
            "title": "Microsoft Certified: Power Automate RPA Developer",
            "date": "2025",
            "organization": "Microsoft",
            "description": "Professional certification validating expertise in building and deploying RPA solutions using Microsoft Power Automate. Certification ID: PL-500",
            "certificate_link": "#",
            "linkedin_link": "#"
        },
        {
            "title": "Runner-Up - Scale +91 Hackathon FFI 2024",
            "date": "2024",
            "organization": "FFI (Future of Finance Initiative)",
            "description": "Secured second place for developing an AI-Driven Financial Advisor using FinBERT and CrewAI agents with 85% accuracy in S&P 500 predictions.",
            "certificate_link": "#",
            "linkedin_link": "#"
        },
        {
            "title": "Winner - InnoThon'23",
            "date": "2023",
            "organization": "Innovation Hackathon",
            "description": "First place for developing a Financial Guidance Chatbot using fine-tuned LLaMA model with context-aware trading advice capabilities.",
            "certificate_link": "#",
            "linkedin_link": "#"
        },
        {
            "title": "Best Paper Award - Yugam'23",
            "date": "2023",
            "organization": "Yugam Technical Symposium",
            "description": "Recognized for outstanding research paper on Chironomy - Real-Time Sign Language Interpreter achieving 94% accuracy using LSTM-RNNs.",
            "certificate_link": "#",
            "linkedin_link": "#"
        }
    ]
    
    skills = {
        "Programming": ["Python", "TypeScript", "JavaScript", "T-SQL", "Java", "C++"],
        "Frameworks": ["React", "Vite", "Flutter", "Streamlit", "Flask", "FastAPI", "Node.js"],
        "GenAI & LLMs": ["GPT-4", "LLaMA-3", "Whisper", "LangChain", "CrewAI", "RAG", "Fine-tuning"],
        "AI/ML": ["PyTorch", "TensorFlow", "LSTM", "CNN", "RNN", "Computer Vision", "Scikit-learn"],
        "Automation": ["N8N", "Power Automate", "RPA", "ComfyUI", "UiPath"],
        "Databases": ["Supabase", "Firebase", "Qdrant", "FAISS", "Pinecone", "PostgreSQL", "MongoDB"],
        "Cloud & DevOps": ["Docker", "CI/CD", "GCP", "Azure", "RESTful API", "GraphQL", "Kubernetes"]
    }
    
    return profile, experiences, projects, achievements, skills

profile, experiences, projects, achievements, skills = get_resume_data()

# Header with Profile - REVISED FOR NEATNESS & ERROR FIX
def render_header(profile):
    
    # Profile Picture (FIX: Removed unsupported 'class_' argument)
    try:
        profile_img = Image.open("profile.jpg") 
        st.image(profile_img, width=200, output_format="JPEG", caption="", use_container_width=False, 
                 clamp=True, channels="RGB") 
    except FileNotFoundError:
        # Fallback to a colorful placeholder
        st.markdown("""
        <div style='width: 200px; height: 200px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%); 
                     display: flex; align-items: center; justify-content: center; margin: 0 auto 10px auto; border: 5px solid white; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'
                     class='floating'>
            <span style='color: white; font-size: 3rem; font-weight: bold;'>TM</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='main-header'>{profile['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 class='sub-header'>{profile['title']}</h2>", unsafe_allow_html=True)
    
    # Contact info in a clean, centered layout
    st.markdown("<div class='contact-info-container'>", unsafe_allow_html=True)
    
    st.markdown(f"<div class='contact-item'>📧 **{profile['email']}**</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='contact-item'>📱 **{profile['phone']}**</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='contact-item'>📍 **{profile['location']}**</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True) 
    
    # Social links with colorful buttons, centered
    st.markdown("<div class='link-button-container'>", unsafe_allow_html=True)
    st.markdown(f"<a href='{profile['linkedin']}' class='link-button'>🔗 LinkedIn</a>", unsafe_allow_html=True)
    st.markdown(f"<a href='{profile['github']}' class='link-button'>🐱 GitHub</a>", unsafe_allow_html=True)
    st.markdown(f"<a href='{profile['portfolio']}' class='link-button'>🌐 Portfolio</a>", unsafe_allow_html=True)
    st.markdown(f"<a href='mailto:{profile['email']}' class='link-button'>📧 Email Me</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Home Page
def render_home(profile, experiences, projects, achievements, skills):
    render_header(profile)
    
    st.markdown("---")
    
    # Professional Summary
    st.markdown("<h2 class='section-header'>👨‍💻 Professional Summary</h2>", unsafe_allow_html=True)
    st.write(profile['about'])
    
    # Quick Stats
    st.markdown("<h2 class='section-header'>🚀 Quick Highlights</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='stats-card'>
            <div class='stats-number'>12+</div>
            <div class='stats-label'>AI Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='stats-card'>
            <div class='stats-number'>5</div>
            <div class='stats-label'>Awards Won</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='stats-card'>
            <div class='stats-number'>1+</div>
            <div class='stats-label'>Years Experience</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='stats-card'>
            <div class='stats-number'>94%</div>
            <div class='stats-label'>Peak Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Experience
    st.markdown("<h2 class='section-header'>💼 Professional Experience</h2>", unsafe_allow_html=True)
    for exp in experiences:
        st.markdown(f"""
        <div class='experience-card'>
            <h3>🎯 {exp['role']}</h3>
            <p style='color: #666; margin-top: -5px; font-weight: 600;'>{exp['company']} | {exp['period']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        for project_desc in exp['projects']:
            st.markdown(f"<div style='margin: 8px 0; padding-left: 15px; border-left: 3px solid #667eea;'>✨ {project_desc}</div>", unsafe_allow_html=True)
    
    # Featured Projects
    st.markdown("<h2 class='section-header'>🎯 Featured Projects</h2>", unsafe_allow_html=True)
    for i, project in enumerate(projects[:4]):
        st.markdown(f"""
        <div class='project-card'>
            <span class='category-tag'>{project['category']}</span>
            <h3>🚀 {project['title']}</h3>
            <p><strong>Description:</strong> {project['description']}</p>
            <p><strong>Tech Stack:</strong> {project['tech_stack']}</p>
            <p><strong>Impact:</strong> {project['impact']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.success("✨ **Explore more amazing projects in the Projects section!**")
    
    # Skills Overview
    st.markdown("<h2 class='section-header'>🛠️ Technical Skills</h2>", unsafe_allow_html=True)
    for category, skill_list in skills.items():
        st.markdown(f"<h4 style='color: #495057; margin-bottom: 15px;'>🔧 {category}</h4>", unsafe_allow_html=True)
        skill_html = " ".join([f"<span class='skill-badge'>{skill}</span>" for skill in skill_list])
        st.markdown(skill_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Projects Page
def render_projects(projects):
    st.markdown("<h2 class='section-header'>💼 All Projects</h2>", unsafe_allow_html=True)
    
    # Category filter
    categories = list(set([p['category'] for p in projects]))
    selected_category = st.selectbox("🔍 Filter by Category", ["All"] + categories)
    
    filtered_projects = projects if selected_category == "All" else [p for p in projects if p['category'] == selected_category]
    
    for project in filtered_projects:
        st.markdown(f"""
        <div class='project-card'>
            <span class='category-tag'>{project['category']}</span>
            <h3>🚀 {project['title']}</h3>
            <p><strong>Description:</strong> {project['description']}</p>
            <p><strong>Tech Stack:</strong> {project['tech_stack']}</p>
            <p><strong>Impact:</strong> {project['impact']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Links
        link_cols = st.columns(4)
        links = []
        if project['github_link'] and project['github_link'] != "#":
            links.append(('🔗 GitHub', project['github_link']))
        if project['hosted_link'] and project['hosted_link'] != "#":
            links.append(('🌐 Live Demo', project['hosted_link']))
        if project['video_link'] and project['video_link'] != "#":
            links.append(('🎥 Video Demo', project['video_link']))
        if project['blog_link'] and project['blog_link'] != "#":
            links.append(('📝 Blog Post', project['blog_link']))
        
        if links:
            for idx, (label, url) in enumerate(links):
                with link_cols[idx]:
                    st.markdown(f"<a href='{url}' class='link-button' target='_blank' style='display: block; text-align: center;'>{label}</a>", unsafe_allow_html=True)
        
        st.markdown("---")

# Achievements Page
def render_achievements(achievements):
    st.markdown("<h2 class='section-header'>🏆 Achievements & Certifications</h2>", unsafe_allow_html=True)
    
    for achievement in achievements:
        st.markdown(f"""
        <div class='achievement-card'>
            <h3>🏅 {achievement['title']}</h3>
            <p><strong>Organization:</strong> {achievement['organization']}</p>
            <p><strong>Date:</strong> {achievement['date']}</p>
            <p>{achievement['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Links
        link_cols = st.columns(2)
        links = []
        if achievement['certificate_link'] and achievement['certificate_link'] != "#":
            links.append(('📜 View Certificate', achievement['certificate_link']))
        if achievement['linkedin_link'] and achievement['linkedin_link'] != "#":
            links.append(('🔗 LinkedIn Post', achievement['linkedin_link']))
        
        for idx, (label, url) in enumerate(links):
            with link_cols[idx]:
                st.markdown(f"<a href='{url}' class='link-button' target='_blank' style='display: block; text-align: center;'>{label}</a>", unsafe_allow_html=True)
        
        st.markdown("---")

# Skills Page
def render_skills(skills):
    st.markdown("<h2 class='section-header'>🛠️ Technical Skills</h2>", unsafe_allow_html=True)
    
    for category, skill_list in skills.items():
        st.markdown(f"<h3 style='color: #343a40; margin: 25px 0 15px 0;'>🔧 {category}</h3>", unsafe_allow_html=True)
        skill_html = " ".join([f"<span class='skill-badge'>{skill}</span>" for skill in skill_list])
        st.markdown(skill_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

# Contact Page
def render_contact(profile):
    st.markdown("<h2 class='section-header'>📞 Contact Me</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Get In Touch")
        st.write("Feel free to reach out for collaborations, opportunities, or just to say hello!")
        
        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("👤 Your Name")
            email = st.text_input("📧 Your Email")
            subject = st.text_input("📝 Subject")
            message = st.text_area("💭 Your Message", height=150)
            submitted = st.form_submit_button("🚀 Send Message")
            
            if submitted:
                if name and email and message:
                    st.success("✅ Thank you for your message! I'll get back to you soon.")
                    # Here you would typically integrate with an email service
                else:
                    st.error("❌ Please fill in all required fields.")
    
    with col2:
        st.subheader("📱 Contact Info")
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 25px; border-radius: 20px; margin-top: 20px; 
                      box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);'>
            <p>📧 <strong>Email:</strong><br>{profile['email']}</p>
            <p>📱 <strong>Phone:</strong><br>{profile['phone']}</p>
            <p>📍 <strong>Location:</strong><br>{profile['location']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🌐 Connect With Me")
        st.markdown(f"<a href='{profile['linkedin']}' class='link-button' style='display: block; text-align: center; margin: 10px 0;'>🔗 LinkedIn</a>", unsafe_allow_html=True)
        st.markdown(f"<a href='{profile['github']}' class='link-button' style='display: block; text-align: center; margin: 10px 0;'>🐱 GitHub</a>", unsafe_allow_html=True)
        st.markdown(f"<a href='{profile['portfolio']}' class='link-button' style='display: block; text-align: center; margin: 10px 0;'>🌐 Portfolio</a>", unsafe_allow_html=True)

# Main Navigation - REVISED FOR CLEANER SIDEBAR & ERROR FIX
def main():
    with st.sidebar:
        # Load profile image for the sidebar for better branding (FIX: Removed unsupported 'class_' argument)
        try:
            sidebar_img = Image.open("profile.jpg") 
            st.image(sidebar_img, width=100, output_format="JPEG", caption="", use_container_width=False, 
                     clamp=True, channels="RGB")
        except FileNotFoundError:
            # Colorful sidebar header as fallback
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                         padding: 30px 20px; border-radius: 15px; text-align: center; 
                         margin-bottom: 20px; color: white;'>
                <h2 style='color: white; margin: 0;'>Thameem Mul Ansari</h2>
                <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0;'>AI Engineer & RPA Developer</p>
            </div>
            """, unsafe_allow_html=True)
        
        selected = option_menu(
            "🎯 Navigation",
            ["Home", "Projects", "Achievements", "Skills", "Contact"],
            icons=['house-fill', 'code-slash', 'trophy-fill', 'tools', 'envelope-fill'],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "10px", "background-color": "transparent"},
                "icon": {"color": "#667eea", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "8px", "--hover-color": "#e9ecef", "border-radius": "10px"},
                "nav-link-selected": {"background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)", "color": "white"},
            }
        )
        
        st.markdown("---")
        st.markdown("### 🔥 Quick Stats")
        st.markdown("""
- **12+** AI Projects
- **5** Awards Won  
- **94%** Peak Accuracy
- **1+** Years Experience
        """)
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6c757d; font-size: 0.9rem;'>
            <p>Built with ❤️ using Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
    
    if selected == "Home":
        render_home(profile, experiences, projects, achievements, skills)
    elif selected == "Projects":
        render_projects(projects)
    elif selected == "Achievements":
        render_achievements(achievements)
    elif selected == "Skills":
        render_skills(skills)
    elif selected == "Contact":
        render_contact(profile)

if __name__ == "__main__":
    main()
