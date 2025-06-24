import streamlit as st
import yaml
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List, Any

class SchemaBuilder:
    def __init__(self):
        self.default_schema = """nodes:
  - Customer
  - Order
  - Product
  - Category
edges:
  - Customer -> Order
  - Order -> Product
  - Product -> Category
  - Customer -> Product
properties:
  Customer:
    - id: string
    - name: string
    - email: string
    - join_date: date
  Order:
    - id: string
    - customer_id: string
    - order_date: date
    - total_amount: float
  Product:
    - id: string
    - name: string
    - price: float
    - category_id: string
  Category:
    - id: string
    - name: string
    - description: string"""

    def parse_schema(self, schema_text: str) -> Dict[str, Any]:
        """Parse YAML schema text into a structured format."""
        try:
            schema = yaml.safe_load(schema_text)
            return schema
        except yaml.YAMLError as e:
            st.error(f"Invalid YAML format: {e}")
            return None

    def create_graph(self, schema: Dict[str, Any]) -> nx.DiGraph:
        """Create a NetworkX graph from the schema."""
        G = nx.DiGraph()
        
        # Add nodes
        if 'nodes' in schema:
            for node in schema['nodes']:
                G.add_node(node, label=node)
        
        # Add edges
        if 'edges' in schema:
            for edge in schema['edges']:
                if ' -> ' in edge:
                    source, target = edge.split(' -> ')
                    G.add_edge(source.strip(), target.strip())
        
        return G

    def visualize_graph(self, G: nx.DiGraph) -> go.Figure:
        """Create a Plotly visualization of the graph."""
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Create edge trace
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="middle center",
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=30,
                color=[],
                line_width=2,
                line_color='white'
            ))

        # Color nodes by degree
        node_adjacencies = []
        for node in G.nodes():
            node_adjacencies.append(len(list(G.neighbors(node))))
        node_trace.marker.color = node_adjacencies

        # Create the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                       layout=go.Layout(
                           title='Knowledge Graph Schema',
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                       )
        
        return fig

    def render_properties_table(self, schema: Dict[str, Any]):
        """Render properties as a table."""
        if 'properties' not in schema:
            return
        
        properties_data = []
        for entity, props in schema['properties'].items():
            for prop in props:
                if ':' in prop:
                    prop_name, prop_type = prop.split(':', 1)
                    properties_data.append({
                        'Entity': entity,
                        'Property': prop_name.strip(),
                        'Type': prop_type.strip()
                    })
        
        if properties_data:
            df = pd.DataFrame(properties_data)
            st.subheader("📋 Entity Properties")
            st.dataframe(df, use_container_width=True)

    def render(self):
        """Main render method for the Schema Builder component."""
        
        # Two-column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Schema Definition")
            st.markdown("Define your knowledge graph schema using YAML format:")
            
            # Schema input
            schema_text = st.text_area(
                "Graph Schema (YAML)",
                value=self.default_schema,
                height=400,
                help="Define nodes, edges, and properties for your knowledge graph"
            )
            
            # Parse and validate button
            if st.button("🔍 Parse & Validate Schema", type="primary"):
                schema = self.parse_schema(schema_text)
                if schema:
                    st.session_state['current_schema'] = schema
                    st.success("✅ Schema parsed successfully!")
                    
                    # Show schema summary
                    with st.expander("📊 Schema Summary"):
                        if 'nodes' in schema:
                            st.write(f"**Nodes:** {len(schema['nodes'])}")
                        if 'edges' in schema:
                            st.write(f"**Edges:** {len(schema['edges'])}")
                        if 'properties' in schema:
                            st.write(f"**Entities with Properties:** {len(schema['properties'])}")
        
        with col2:
            st.subheader("🎨 Graph Visualization")
            
            # Check if we have a valid schema
            if 'current_schema' in st.session_state:
                schema = st.session_state['current_schema']
                G = self.create_graph(schema)
                
                # Visualize graph
                fig = self.visualize_graph(G)
                st.plotly_chart(fig, use_container_width=True)
                
                # Show properties table
                self.render_properties_table(schema)
                
                # Graph statistics
                with st.expander("📈 Graph Statistics"):
                    st.write(f"**Total Nodes:** {G.number_of_nodes()}")
                    st.write(f"**Total Edges:** {G.number_of_edges()}")
                    st.write(f"**Is Connected:** {nx.is_weakly_connected(G)}")
                    
                    # Centrality metrics
                    if G.number_of_nodes() > 1:
                        degree_centrality = nx.degree_centrality(G)
                        most_central = max(degree_centrality, key=degree_centrality.get)
                        st.write(f"**Most Central Node:** {most_central}")
            else:
                st.info("👆 Parse a schema to see the visualization")
        
        # Example schemas
        with st.expander("💡 Example Schemas"):
            st.markdown("""
            **E-commerce Schema:**
            ```yaml
            nodes:
              - Customer
              - Order
              - Product
              - Category
            edges:
              - Customer -> Order
              - Order -> Product
              - Product -> Category
            ```
            
            **Social Network Schema:**
            ```yaml
            nodes:
              - User
              - Post
              - Comment
              - Tag
            edges:
              - User -> Post
              - Post -> Comment
              - User -> Comment
              - Post -> Tag
            ```
            """) 