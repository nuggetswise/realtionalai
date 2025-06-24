import streamlit as st
import os
import json
from typing import Dict, List, Any
import openai

class PMStrategyHelper:
    def __init__(self):
        # Try to get API key from Streamlit secrets first (production), then environment variable (development)
        self.api_key = None
        try:
            # Production: Get from Streamlit secrets
            self.api_key = st.secrets.get("openai_api_key")
        except:
            # Development: Get from environment variable
            self.api_key = os.getenv("OPENAI_API_KEY")
        
        self.client = None
        if self.api_key:
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                st.error(f"Failed to initialize OpenAI client: {e}")

    def generate_roadmap_suggestions(self, schema: Dict[str, Any], query: str, results: Any, insights: str = "") -> str:
        """Generate product roadmap suggestions using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured. Please add your API key in Streamlit secrets or environment variables."
        
        try:
            # Prepare context
            context = self._prepare_context(schema, query, results, insights)
            
            prompt = f"""
You are a Senior Product Manager at RelationalAI, specializing in platform features for knowledge graph management and AI-augmented analytics.

**Current Graph Schema:**
{json.dumps(schema, indent=2)}

**Recent Query Analysis:**
{query}

**Query Results Summary:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**AI Insights (if available):**
{insights if insights else "No AI insights available"}

**Task:** Generate 3-5 strategic product roadmap suggestions for RelationalAI's platform. Focus on:

1. **Feature Enhancements** - New capabilities that would improve the user experience
2. **Platform Improvements** - Infrastructure and scalability enhancements
3. **AI/ML Integration** - Advanced analytics and automation features
4. **Developer Experience** - Tools and APIs for better developer productivity
5. **Business Intelligence** - Advanced reporting and visualization features

For each suggestion, provide:
- **Feature Name:** Clear, descriptive name
- **Problem Statement:** What user pain point this solves
- **Proposed Solution:** How the feature would work
- **Business Impact:** Expected benefits (user engagement, revenue, etc.)
- **Implementation Priority:** High/Medium/Low
- **Estimated Timeline:** Rough development timeline
- **Success Metrics:** How to measure success

Focus on features that would be valuable for a Product Manager, Platform role at RelationalAI.
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Senior Product Manager at RelationalAI with expertise in platform strategy and feature development."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating roadmap suggestions: {str(e)}"

    def generate_competitive_analysis(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Generate competitive analysis using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured."
        
        try:
            context = self._prepare_context(schema, query, results)
            
            prompt = f"""
You are a Product Manager conducting competitive analysis for RelationalAI's knowledge graph platform.

**Current Graph Schema:**
{json.dumps(schema, indent=2)}

**Query Analysis:**
{query}

**Results Summary:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**Task:** Provide a competitive analysis focusing on:

1. **Market Positioning** - How RelationalAI compares to competitors (Neo4j, Amazon Neptune, etc.)
2. **Feature Gaps** - What capabilities are missing or could be improved
3. **Differentiation Opportunities** - Unique value propositions to pursue
4. **Market Trends** - Emerging technologies and user needs
5. **Strategic Recommendations** - How to maintain competitive advantage

Consider the perspective of a Product Manager, Platform role.
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Product Manager expert in competitive analysis and market strategy."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.6
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating competitive analysis: {str(e)}"

    def generate_user_research_insights(self, schema: Dict[str, Any], query: str, results: Any) -> str:
        """Generate user research insights using OpenAI API."""
        if not self.client:
            return "⚠️ OpenAI API key not configured."
        
        try:
            context = self._prepare_context(schema, query, results)
            
            prompt = f"""
You are a Product Manager analyzing user behavior patterns from knowledge graph usage data.

**Graph Schema:**
{json.dumps(schema, indent=2)}

**User Query:**
{query}

**Query Results:**
{results.to_string() if hasattr(results, 'to_string') else str(results)}

**Task:** Generate user research insights including:

1. **User Personas** - What types of users would use this query pattern
2. **Use Cases** - Common scenarios and workflows
3. **Pain Points** - Potential frustrations or limitations
4. **User Journey** - How users might interact with the platform
5. **Feature Priorities** - What users would value most
6. **Research Questions** - What to investigate further

Focus on insights that would help a Product Manager, Platform make data-driven decisions.
"""

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Product Manager expert in user research and behavioral analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=700,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error generating user research insights: {str(e)}"

    def _prepare_context(self, schema: Dict[str, Any], query: str, results: Any, insights: str = "") -> str:
        """Prepare context information for PM analysis."""
        context_parts = []
        
        # Schema analysis
        if schema:
            node_count = len(schema.get('nodes', []))
            edge_count = len(schema.get('edges', []))
            context_parts.append(f"Schema complexity: {node_count} entities, {edge_count} relationships")
        
        # Query analysis
        if query:
            context_parts.append(f"Query focus: {self._classify_query_focus(query)}")
        
        # Results summary
        if hasattr(results, 'shape'):
            context_parts.append(f"Data volume: {results.shape[0]} records, {results.shape[1]} attributes")
        
        return "\n".join(context_parts)

    def _classify_query_focus(self, query: str) -> str:
        """Classify the focus area of the query for PM context."""
        query_lower = query.lower()
        
        if 'customer' in query_lower:
            return "Customer Analytics"
        elif 'product' in query_lower:
            return "Product Analytics"
        elif 'order' in query_lower:
            return "Transaction Analytics"
        elif 'category' in query_lower:
            return "Categorical Analysis"
        else:
            return "General Analytics"

    def render(self):
        """Main render method for the PM Strategy Helper component."""
        
        st.subheader("📋 PM Strategy Helper")
        st.markdown("Generate product roadmap suggestions and strategic insights for RelationalAI platform.")
        
        # Check prerequisites
        if 'current_schema' not in st.session_state:
            st.warning("⚠️ Please define a schema in the Schema Builder tab first.")
            return
        
        if 'query_results' not in st.session_state:
            st.warning("⚠️ Please execute a query in the Query Executor tab first.")
            return
        
        if not self.api_key:
            st.warning("⚠️ OpenAI API key not configured. Please add your API key in Streamlit secrets or environment variables.")
            st.info("""
            **For Production (Streamlit Cloud):**
            - Add API key in Streamlit Cloud dashboard under "Secrets"
            - Format: `{"openai_api_key": "your-api-key-here"}`
            
            **For Local Development:**
            - Set environment variable: `export OPENAI_API_KEY="your-api-key-here"`
            - Or add to `.streamlit/secrets.toml`: `openai_api_key = "your-api-key-here"`
            """)
            return
        
        # Get current data
        schema = st.session_state['current_schema']
        query = st.session_state.get('last_query', 'No query executed')
        results = st.session_state['query_results']
        insights = st.session_state.get('ai_insights', '')
        
        # Strategy type selector
        st.subheader("🎯 Strategy Analysis Type")
        strategy_type = st.selectbox(
            "Choose strategy analysis type",
            ["Product Roadmap Suggestions", "Competitive Analysis", "User Research Insights"],
            help="Select the type of strategic analysis you want to generate"
        )
        
        # Generate strategy button
        if st.button("🚀 Generate Strategy Analysis", type="primary"):
            with st.spinner("🤖 Generating strategic insights..."):
                if strategy_type == "Product Roadmap Suggestions":
                    strategy = self.generate_roadmap_suggestions(schema, query, results, insights)
                elif strategy_type == "Competitive Analysis":
                    strategy = self.generate_competitive_analysis(schema, query, results)
                else:  # User Research Insights
                    strategy = self.generate_user_research_insights(schema, query, results)
                
                # Store results
                st.session_state['pm_strategy'] = strategy
                st.session_state['strategy_type'] = strategy_type
        
        # Display results
        if 'pm_strategy' in st.session_state:
            st.subheader(f"📋 {st.session_state['strategy_type']}")
            
            # Display strategy with nice formatting
            strategy = st.session_state['pm_strategy']
            
            if strategy.startswith("❌") or strategy.startswith("⚠️"):
                st.error(strategy)
            else:
                # Format the strategy nicely
                st.markdown(strategy)
                
                # Add action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📋 Copy to Clipboard"):
                        st.write("✅ Strategy copied to clipboard!")
                
                with col2:
                    if st.button("💾 Save as Note"):
                        st.session_state['saved_notes'] = st.session_state.get('saved_notes', [])
                        st.session_state['saved_notes'].append({
                            'type': st.session_state['strategy_type'],
                            'content': strategy,
                            'timestamp': st.session_state.get('last_query', 'Unknown')
                        })
                        st.success("✅ Strategy saved to notes!")
                
                with col3:
                    if st.button("🔄 Regenerate"):
                        st.session_state.pop('pm_strategy', None)
                        st.rerun()
        
        # Strategy context
        with st.expander("📊 Strategy Context"):
            st.write("**Current Schema:**")
            st.json(schema)
            
            st.write("**Query Context:**")
            st.code(query)
            
            st.write("**Data Summary:**")
            if not results.empty:
                st.write(f"- **Records:** {len(results)}")
                st.write(f"- **Attributes:** {list(results.columns)}")
                st.write(f"- **Data Types:** {results.dtypes.to_dict()}")
        
        # Saved notes
        if 'saved_notes' in st.session_state and st.session_state['saved_notes']:
            with st.expander("📝 Saved Strategy Notes"):
                for i, note in enumerate(st.session_state['saved_notes']):
                    st.write(f"**{note['type']}** - {note['timestamp']}")
                    st.markdown(note['content'][:200] + "..." if len(note['content']) > 200 else note['content'])
                    if st.button(f"🗑️ Delete Note {i+1}"):
                        st.session_state['saved_notes'].pop(i)
                        st.rerun()
                    st.divider()
        
        # PM best practices
        with st.expander("💡 PM Best Practices"):
            st.markdown("""
            **Product Roadmap Development:**
            - Start with user problems, not solutions
            - Prioritize based on impact and effort
            - Consider technical debt and platform health
            - Align with company strategy and OKRs
            
            **Competitive Analysis:**
            - Focus on differentiation, not feature parity
            - Understand your unique value proposition
            - Monitor market trends and emerging technologies
            - Build sustainable competitive advantages
            
            **User Research:**
            - Combine quantitative and qualitative data
            - Focus on user behavior, not just opinions
            - Validate assumptions with real users
            - Iterate based on feedback and metrics
            """)
        
        # Strategy templates
        with st.expander("📋 Strategy Templates"):
            st.markdown("""
            **Feature Specification Template:**
            ```
            Feature: [Name]
            Problem: [User pain point]
            Solution: [How it works]
            Impact: [Business value]
            Priority: [High/Medium/Low]
            Timeline: [Estimated duration]
            Metrics: [Success indicators]
            ```
            
            **Competitive Analysis Template:**
            ```
            Competitor: [Name]
            Strengths: [What they do well]
            Weaknesses: [Gaps/limitations]
            Opportunities: [Where we can differentiate]
            Threats: [Risks to consider]
            ```
            """) 