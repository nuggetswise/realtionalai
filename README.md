# 🧠 GraphOps Playground

A **RelationalAI-tailored feature demo app** designed to showcase capabilities relevant to the **Product Manager, Platform** role at RelationalAI. This Streamlit application simulates a graph-based query and inference platform with AI-augmented analytics.

## 🎯 Purpose

This demo app showcases:
- **Graph Schema Builder**: Declarative schema definition and visualization
- **Query Executor**: Natural language query processing against graph data
- **Semantic Inference Engine**: AI-powered insights generation
- **PM Strategy Helper**: Product roadmap suggestions and strategic analysis

## 🚀 Features

### 1. 🏗️ Graph Schema Builder
- **YAML-based schema definition** for nodes, edges, and properties
- **Interactive graph visualization** using Plotly
- **Schema validation** and statistics
- **Example schemas** for e-commerce and social networks

### 2. 🔍 Query Executor
- **Natural language query processing** (e.g., "FIND Customers who ordered more than 2 products")
- **Pre-built query templates** with parameterized inputs
- **Realistic sample data generation** for demonstration
- **Query results visualization** and statistics

### 3. 🧠 Semantic Inference Engine
- **AI-powered insights generation** using OpenAI GPT-3.5-turbo
- **Multiple analysis types**: Business Insights, Pattern Analysis, Recommendations
- **Context-aware analysis** based on schema, queries, and results
- **Structured output** with actionable recommendations

### 4. 📋 PM Strategy Helper
- **Product roadmap suggestions** for RelationalAI platform
- **Competitive analysis** and market positioning
- **User research insights** and behavior patterns
- **Strategic templates** and best practices

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (for LLM features)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd relationalai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up OpenAI API key**
   - Get your API key from [OpenAI Platform](https://platform.openai.com/)
   - Add it in the app sidebar when running

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
graphops_playground/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── components/                     # Modular components
    ├── __init__.py
    ├── schema_builder.py          # Graph schema definition & visualization
    ├── query_executor.py          # Query processing & execution
    ├── inference_engine.py        # AI-powered insights generation
    └── pm_strategy_helper.py      # Product strategy & roadmap suggestions
```

## 🎮 Usage Guide

### Getting Started

1. **Configure API Key**: Add your OpenAI API key in the sidebar
2. **Build Schema**: Use the Schema Builder tab to define your graph structure
3. **Execute Queries**: Run natural language queries in the Query Executor
4. **Generate Insights**: Use the Semantic Inference Engine for AI analysis
5. **Plan Strategy**: Get product roadmap suggestions from the PM Strategy Helper

### Example Workflow

1. **Define E-commerce Schema**:
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

2. **Execute Query**:
   ```
   FIND Customers who ordered more than 2 products in the last 30 days
   ```

3. **Generate AI Insights**:
   - Business insights about customer behavior
   - Pattern analysis of purchase trends
   - Actionable recommendations

4. **Get PM Strategy**:
   - Product roadmap suggestions
   - Competitive analysis
   - User research insights

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **OpenAI**: LLM API for AI features
- **NetworkX**: Graph data structures
- **Plotly**: Interactive visualizations
- **Pandas**: Data manipulation
- **PyYAML**: Schema parsing

### Architecture
- **Modular Design**: Each feature is a separate component
- **Session State Management**: Persistent data across tabs
- **Error Handling**: Graceful degradation when API unavailable
- **Responsive UI**: Clean, professional interface

## 🎯 Demo Scenarios

### For RelationalAI PM Interview

1. **Show Graph Modeling Skills**:
   - Define complex schemas with multiple entity types
   - Demonstrate understanding of relationships and properties

2. **Demonstrate Query Understanding**:
   - Use natural language queries effectively
   - Show comfort with declarative query patterns

3. **Showcase AI Integration**:
   - Generate meaningful insights from graph data
   - Demonstrate understanding of AI-augmented analytics

4. **Display Platform Thinking**:
   - Generate relevant product roadmap suggestions
   - Show strategic thinking about platform features

## 🚀 Customization

### Adding New Query Types
1. Extend the `parse_query()` method in `query_executor.py`
2. Add corresponding execution logic
3. Update the query templates dictionary

### Adding New Analysis Types
1. Create new methods in `inference_engine.py`
2. Update the analysis type selector
3. Customize prompts for specific use cases

### Modifying Sample Data
1. Update the `_generate_sample_data()` method in `query_executor.py`
2. Adjust data distributions and relationships
3. Add new entity types as needed

## 🔒 Security & Privacy

- **API Keys**: Stored in session state, not persisted
- **Data**: All sample data is generated locally
- **No External Storage**: No data is sent to external services except OpenAI API

## 🤝 Contributing

This is a demo application for RelationalAI PM interviews. For modifications:
1. Follow the existing code structure
2. Maintain clean separation of concerns
3. Add appropriate error handling
4. Update documentation as needed

## 📄 License

This project is created for demonstration purposes for RelationalAI PM interviews.

---

**Built with ❤️ for RelationalAI Product Manager, Platform role demonstration** 