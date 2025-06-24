import streamlit as st
import os
from components.schema_builder import SchemaBuilder
from components.query_executor import QueryExecutor
from components.inference_engine import InferenceEngine
from components.pm_strategy_helper import PMStrategyHelper

# Page configuration
st.set_page_config(
    page_title="GraphOps Playground",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🧠 GraphOps Playground</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">RelationalAI Platform Feature Demo - Graph-based Query & Inference Simulator</p>', unsafe_allow_html=True)
    
    # Sidebar for app info
    with st.sidebar:
        st.header("ℹ️ About This Demo")
        st.markdown("""
        This app simulates a **Product Manager, Platform** feature at RelationalAI:
        
        - **Graph Schema Builder**: Define relational schemas
        - **Query Executor**: Run declarative queries
        - **Semantic Inference**: AI-powered insights
        - **PM Strategy Helper**: Product roadmap suggestions
        
        Built to showcase graph modeling, semantic AI, and platform thinking.
        """)
        
        st.divider()
        
        # API Key configuration info
        st.subheader("🔑 API Configuration")
        st.markdown("""
        **For Production (Streamlit Cloud):**
        - Add API key in Streamlit Cloud dashboard under "Secrets"
        - Format: `{"openai_api_key": "your-api-key-here"}`
        
        **For Local Development:**
        - Set environment variable: `export OPENAI_API_KEY="your-api-key-here"`
        - Or add to `.streamlit/secrets.toml`: `openai_api_key = "your-api-key-here"`
        """)
        
        # Check if API key is available
        try:
            api_key = st.secrets.get("openai_api_key")
            if api_key:
                st.success("✅ API key configured (Streamlit secrets)")
            else:
                api_key = os.getenv("OPENAI_API_KEY")
                if api_key:
                    st.success("✅ API key configured (environment variable)")
                else:
                    st.warning("⚠️ API key not found")
        except:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                st.success("✅ API key configured (environment variable)")
            else:
                st.warning("⚠️ API key not found")
    
    # Main content area with tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏗️ Schema Builder",
        "🔍 Query Executor", 
        "🧠 Semantic Inference",
        "📋 PM Strategy Helper"
    ])
    
    # Initialize components
    schema_builder = SchemaBuilder()
    query_executor = QueryExecutor()
    inference_engine = InferenceEngine()
    pm_helper = PMStrategyHelper()
    
    # Tab 1: Schema Builder
    with tab1:
        st.markdown('<h2 class="sub-header">🏗️ Graph Schema Builder</h2>', unsafe_allow_html=True)
        st.markdown("Define your knowledge graph schema using a declarative format.")
        schema_builder.render()
    
    # Tab 2: Query Executor
    with tab2:
        st.markdown('<h2 class="sub-header">🔍 Query Executor</h2>', unsafe_allow_html=True)
        st.markdown("Execute declarative queries against your graph schema.")
        query_executor.render()
    
    # Tab 3: Semantic Inference
    with tab3:
        st.markdown('<h2 class="sub-header">🧠 Semantic Inference Engine</h2>', unsafe_allow_html=True)
        st.markdown("Generate AI-powered insights from your graph data and queries.")
        inference_engine.render()
    
    # Tab 4: PM Strategy Helper
    with tab4:
        st.markdown('<h2 class="sub-header">📋 PM Strategy Helper</h2>', unsafe_allow_html=True)
        st.markdown("Get product roadmap suggestions based on your graph analysis.")
        pm_helper.render()

if __name__ == "__main__":
    main() 