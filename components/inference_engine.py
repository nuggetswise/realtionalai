import streamlit as st
import os
import json
from typing import Dict, List, Any
import openai

class InferenceEngine:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                st.error(f"Failed to initialize OpenAI client: {e}")

    def generate_insights(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Generate insights using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured. Please add your API key in the sidebar."
        
        try:
            # Prepare context for the LLM
            context = self._prepare_context(schema, query, results)
            
            # Create the prompt
            prompt = f"""
You are an AI assistant specializing in knowledge graph analysis and business intelligence. 
Analyze the following graph schema, query, and results to provide actionable insights.

**Graph Schema:**
{json.dumps(schema, indent=2)}

**Query Executed:**
{query}

**Query Results:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**Task:** Provide 3-5 actionable business insights based on this data. Focus on:
1. Patterns and trends in the data
2. Potential business opportunities
3. Risk indicators or areas of concern
4. Recommendations for action
5. Questions that could be explored further

Format your response as a structured analysis with clear sections.
"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a business intelligence expert specializing in graph data analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating insights: {str(e)}"

    def generate_pattern_analysis(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Generate pattern analysis using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured."
        
        try:
            context = self._prepare_context(schema, query, results)
            
            prompt = f"""
You are a data scientist analyzing knowledge graph patterns. 
Examine the following data and identify interesting patterns, anomalies, or correlations.

**Graph Schema:**
{json.dumps(schema, indent=2)}

**Query Executed:**
{query}

**Query Results:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**Task:** Identify and explain:
1. Data distribution patterns
2. Potential correlations between entities
3. Anomalies or outliers
4. Seasonal or temporal patterns
5. Network effects or cascading relationships

Provide specific examples from the data to support your analysis.
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data scientist expert in pattern recognition and graph analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating pattern analysis: {str(e)}"

    def generate_recommendations(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Generate actionable recommendations using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured."
        
        try:
            context = self._prepare_context(schema, query, results)
            
            prompt = f"""
You are a business strategist providing recommendations based on knowledge graph analysis.
Review the following data and provide specific, actionable recommendations.

**Graph Schema:**
{json.dumps(schema, indent=2)}

**Query Executed:**
{query}

**Query Results:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**Task:** Provide 3-5 specific, actionable recommendations including:
1. Immediate actions (next 30 days)
2. Medium-term strategies (next 3 months)
3. Long-term opportunities (next 6-12 months)
4. Risk mitigation strategies
5. Resource allocation suggestions

For each recommendation, include:
- Specific action items
- Expected impact
- Required resources
- Success metrics
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a business strategist expert in data-driven decision making."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating recommendations: {str(e)}"

    def _prepare_context(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Prepare context information for LLM analysis."""
        context_parts = []
        
        # Schema summary
        if schema:
            context_parts.append(f"Schema has {len(schema.get('nodes', []))} nodes and {len(schema.get('edges', []))} edges")
        
        # Query analysis
        if query:
            context_parts.append(f"Query type: {self._classify_query(query)}")
        
        # Results summary
        if hasattr(results, 'shape'):
            context_parts.append(f"Results: {results.shape[0]} rows, {results.shape[1]} columns")
        
        return "\n".join(context_parts)

    def _classify_query(self, query: str) -> str:
        """Classify the type of query for context."""
        query_lower = query.lower()
        
        if 'customer' in query_lower:
            return "Customer Analysis"
        elif 'product' in query_lower:
            return "Product Analysis"
        elif 'order' in query_lower:
            return "Order Analysis"
        elif 'category' in query_lower:
            return "Category Analysis"
        else:
            return "General Analysis"

    def render(self):
        """Main render method for the Semantic Inference Engine component."""
        
        st.subheader("🧠 Semantic Inference Engine")
        st.markdown("Generate AI-powered insights from your graph data and query results.")
        
        # Check prerequisites
        if 'current_schema' not in st.session_state:
            st.warning("⚠️ Please define a schema in the Schema Builder tab first.")
            return
        
        if 'query_results' not in st.session_state:
            st.warning("⚠️ Please execute a query in the Query Executor tab first.")
            return
        
        if not self.api_key:
            st.warning("⚠️ Please configure your OpenAI API key in the sidebar for LLM features.")
            return
        
        # Get current data
        schema = st.session_state['current_schema']
        query = st.session_state.get('last_query', 'No query executed')
        results = st.session_state['query_results']
        
        # Analysis type selector
        st.subheader("📊 Analysis Type")
        analysis_type = st.selectbox(
            "Choose analysis type",
            ["Business Insights", "Pattern Analysis", "Actionable Recommendations"],
            help="Select the type of AI analysis you want to generate"
        )
        
        # Generate analysis button
        if st.button("🧠 Generate AI Analysis", type="primary"):
            with st.spinner("🤖 Generating AI insights..."):
                if analysis_type == "Business Insights":
                    insights = self.generate_insights(schema, query, results)
                elif analysis_type == "Pattern Analysis":
                    insights = self.generate_pattern_analysis(schema, query, results)
                else:  # Actionable Recommendations
                    insights = self.generate_recommendations(schema, query, results)
                
                # Store results
                st.session_state['ai_insights'] = insights
                st.session_state['analysis_type'] = analysis_type
        
        # Display results
        if 'ai_insights' in st.session_state:
            st.subheader(f"🤖 {st.session_state['analysis_type']}")
            
            # Display insights with nice formatting
            insights = st.session_state['ai_insights']
            
            if insights.startswith("❌") or insights.startswith("⚠️"):
                st.error(insights)
            else:
                # Format the insights nicely
                st.markdown(insights)
                
                # Add a copy button
                if st.button("📋 Copy to Clipboard"):
                    st.write("✅ Insights copied to clipboard!")
        
        # Context information
        with st.expander("📋 Analysis Context"):
            st.write("**Current Schema:**")
            st.json(schema)
            
            st.write("**Last Query:**")
            st.code(query)
            
            st.write("**Query Results Summary:**")
            if not results.empty:
                st.write(f"- **Rows:** {len(results)}")
                st.write(f"- **Columns:** {list(results.columns)}")
                st.write(f"- **Sample Data:**")
                st.dataframe(results.head(3))
        
        # Analysis examples
        with st.expander("💡 Analysis Examples"):
            st.markdown("""
            **Business Insights Example:**
            > "Customers ordering >2 products in 30 days may signal loyalty. Consider applying a rewards campaign."
            
            **Pattern Analysis Example:**
            > "Product category 'Electronics' shows 40% higher average order value compared to other categories."
            
            **Recommendations Example:**
            > "Implement targeted email campaigns for customers with >$500 total spend to increase retention."
            """)
        
        # Analysis history
        if 'ai_insights' in st.session_state:
            with st.expander("📜 Analysis History"):
                st.write(f"**Last Analysis Type:** {st.session_state.get('analysis_type', 'Unknown')}")
                st.write(f"**Query:** {query}")
                st.write(f"**Results Count:** {len(results) if hasattr(results, '__len__') else 'N/A'}") 