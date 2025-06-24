#!/usr/bin/env python3
"""
Demo script for GraphOps Playground
This script demonstrates the app functionality without requiring OpenAI API.
"""

import streamlit as st
import pandas as pd
import yaml
from datetime import datetime, timedelta
import random

def demo_schema():
    """Demo schema for testing"""
    return {
        'nodes': ['Customer', 'Order', 'Product', 'Category'],
        'edges': ['Customer -> Order', 'Order -> Product', 'Product -> Category'],
        'properties': {
            'Customer': ['id: string', 'name: string', 'email: string'],
            'Order': ['id: string', 'customer_id: string', 'total_amount: float'],
            'Product': ['id: string', 'name: string', 'price: float'],
            'Category': ['id: string', 'name: string']
        }
    }

def demo_query_results():
    """Demo query results for testing"""
    return pd.DataFrame({
        'Customer ID': ['CUST_001', 'CUST_002', 'CUST_003'],
        'Customer Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Total Spent': [1250.50, 890.25, 2100.75],
        'Orders Count': [5, 3, 8]
    })

def demo_ai_insights():
    """Demo AI insights for testing"""
    return """
## Business Insights Analysis

### Key Patterns Identified
1. **High-Value Customer Segment**: 3 customers with average spend of $1,413.83
2. **Order Frequency**: Average of 5.3 orders per customer
3. **Revenue Distribution**: Top customer contributes 50% of total revenue

### Business Opportunities
- **Loyalty Program**: Customers with >$1000 spend show high engagement
- **Cross-selling**: High-order customers likely to purchase additional products
- **Retention Strategy**: Focus on customers with 5+ orders

### Risk Indicators
- **Customer Concentration**: Heavy reliance on top customer
- **Order Volume**: Some customers have low order frequency

### Recommendations
1. **Immediate (30 days)**: Implement targeted email campaigns for high-value customers
2. **Medium-term (3 months)**: Develop loyalty rewards program
3. **Long-term (6 months)**: Expand customer base to reduce concentration risk

### Success Metrics
- Customer retention rate
- Average order value
- Customer lifetime value
- Revenue diversification
"""

def main():
    """Main demo function"""
    st.title("🧠 GraphOps Playground - Demo Mode")
    st.markdown("This is a demo showing the app functionality without OpenAI API.")
    
    # Demo data setup
    if 'current_schema' not in st.session_state:
        st.session_state['current_schema'] = demo_schema()
    
    if 'query_results' not in st.session_state:
        st.session_state['query_results'] = demo_query_results()
    
    if 'last_query' not in st.session_state:
        st.session_state['last_query'] = "FIND Customers with total spend greater than $500"
    
    if 'ai_insights' not in st.session_state:
        st.session_state['ai_insights'] = demo_ai_insights()
    
    # Display demo info
    st.info("""
    **Demo Mode Active** - This shows how the app would work with real data and API.
    
    To use the full app with AI features:
    1. Run `streamlit run app.py`
    2. Add your OpenAI API key in the sidebar
    3. Start building schemas and running queries!
    """)
    
    # Show current state
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Current Schema")
        st.json(st.session_state['current_schema'])
    
    with col2:
        st.subheader("🔍 Query Results")
        st.dataframe(st.session_state['query_results'])
    
    # Show AI insights
    st.subheader("🧠 AI Insights (Demo)")
    st.markdown(st.session_state['ai_insights'])
    
    # Demo actions
    st.subheader("🎮 Demo Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Demo Data"):
            st.session_state['query_results'] = demo_query_results()
            st.rerun()
    
    with col2:
        if st.button("📋 Copy Demo Schema"):
            st.code(yaml.dump(st.session_state['current_schema'], default_flow_style=False))
    
    with col3:
        if st.button("🚀 Launch Full App"):
            st.info("Run 'streamlit run app.py' in your terminal to launch the full application!")

if __name__ == "__main__":
    main() 