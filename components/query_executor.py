import streamlit as st
import pandas as pd
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta

class QueryExecutor:
    def __init__(self):
        self.sample_data = self._generate_sample_data()
        self.query_templates = {
            "customer_orders": "FIND Customers who ordered more than {threshold} products in the last {days} days",
            "high_value_customers": "FIND Customers with total order value greater than ${amount}",
            "product_popularity": "FIND Products ordered by more than {count} customers",
            "category_analysis": "FIND Categories with average product price above ${price}",
            "recent_activity": "FIND Orders placed in the last {days} days",
            "customer_loyalty": "FIND Customers who have been active for more than {months} months"
        }

    def _generate_sample_data(self) -> Dict[str, List[Dict]]:
        """Generate realistic sample data for demonstration."""
        customers = []
        for i in range(1, 21):
            customers.append({
                'id': f'CUST_{i:03d}',
                'name': f'Customer {i}',
                'email': f'customer{i}@example.com',
                'join_date': datetime.now() - timedelta(days=random.randint(30, 365)),
                'total_orders': random.randint(1, 15),
                'total_spent': round(random.uniform(50, 2000), 2)
            })

        products = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
        for i in range(1, 16):
            products.append({
                'id': f'PROD_{i:03d}',
                'name': f'Product {i}',
                'price': round(random.uniform(10, 500), 2),
                'category': random.choice(categories),
                'orders_count': random.randint(1, 8)
            })

        orders = []
        for i in range(1, 51):
            customer = random.choice(customers)
            order_date = datetime.now() - timedelta(days=random.randint(1, 90))
            orders.append({
                'id': f'ORDER_{i:03d}',
                'customer_id': customer['id'],
                'customer_name': customer['name'],
                'order_date': order_date,
                'total_amount': round(random.uniform(25, 300), 2),
                'product_count': random.randint(1, 5)
            })

        return {
            'customers': customers,
            'products': products,
            'orders': orders
        }

    def parse_query(self, query: str) -> Dict[str, Any]:
        """Parse a natural language query into structured components."""
        query_lower = query.lower()
        
        # Simple keyword-based parsing
        if 'customer' in query_lower and 'order' in query_lower:
            if 'more than' in query_lower:
                # Extract threshold
                import re
                threshold_match = re.search(r'more than (\d+)', query_lower)
                threshold = int(threshold_match.group(1)) if threshold_match else 2
                
                days_match = re.search(r'last (\d+) days', query_lower)
                days = int(days_match.group(1)) if days_match else 30
                
                return {
                    'type': 'customer_orders',
                    'threshold': threshold,
                    'days': days
                }
        
        elif 'total order value' in query_lower or 'total spent' in query_lower:
            import re
            amount_match = re.search(r'\$(\d+)', query)
            amount = int(amount_match.group(1)) if amount_match else 500
            
            return {
                'type': 'high_value_customers',
                'amount': amount
            }
        
        elif 'product' in query_lower and 'ordered by' in query_lower:
            import re
            count_match = re.search(r'more than (\d+)', query_lower)
            count = int(count_match.group(1)) if count_match else 3
            
            return {
                'type': 'product_popularity',
                'count': count
            }
        
        elif 'category' in query_lower and 'average price' in query_lower:
            import re
            price_match = re.search(r'\$(\d+)', query)
            price = int(price_match.group(1)) if price_match else 100
            
            return {
                'type': 'category_analysis',
                'price': price
            }
        
        return {
            'type': 'custom',
            'query': query
        }

    def execute_query(self, parsed_query: Dict[str, Any]) -> pd.DataFrame:
        """Execute the parsed query and return results."""
        query_type = parsed_query.get('type')
        
        if query_type == 'customer_orders':
            threshold = parsed_query.get('threshold', 2)
            days = parsed_query.get('days', 30)
            
            # Filter orders in last N days
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_orders = [
                order for order in self.sample_data['orders']
                if order['order_date'] >= cutoff_date
            ]
            
            # Group by customer and count products
            customer_product_counts = {}
            for order in recent_orders:
                cust_id = order['customer_id']
                if cust_id not in customer_product_counts:
                    customer_product_counts[cust_id] = 0
                customer_product_counts[cust_id] += order['product_count']
            
            # Filter customers above threshold
            results = []
            for cust_id, count in customer_product_counts.items():
                if count > threshold:
                    customer = next(c for c in self.sample_data['customers'] if c['id'] == cust_id)
                    results.append({
                        'Customer ID': cust_id,
                        'Customer Name': customer['name'],
                        'Products Ordered': count,
                        'Total Spent': customer['total_spent'],
                        'Join Date': customer['join_date'].strftime('%Y-%m-%d')
                    })
            
            return pd.DataFrame(results)
        
        elif query_type == 'high_value_customers':
            amount = parsed_query.get('amount', 500)
            
            results = []
            for customer in self.sample_data['customers']:
                if customer['total_spent'] > amount:
                    results.append({
                        'Customer ID': customer['id'],
                        'Customer Name': customer['name'],
                        'Total Spent': customer['total_spent'],
                        'Total Orders': customer['total_orders'],
                        'Join Date': customer['join_date'].strftime('%Y-%m-%d')
                    })
            
            return pd.DataFrame(results)
        
        elif query_type == 'product_popularity':
            count = parsed_query.get('count', 3)
            
            # Count orders per product
            product_orders = {}
            for order in self.sample_data['orders']:
                # Simulate multiple products per order
                for _ in range(order['product_count']):
                    product = random.choice(self.sample_data['products'])
                    if product['id'] not in product_orders:
                        product_orders[product['id']] = 0
                    product_orders[product['id']] += 1
            
            results = []
            for product_id, order_count in product_orders.items():
                if order_count > count:
                    product = next(p for p in self.sample_data['products'] if p['id'] == product_id)
                    results.append({
                        'Product ID': product_id,
                        'Product Name': product['name'],
                        'Orders Count': order_count,
                        'Price': product['price'],
                        'Category': product['category']
                    })
            
            return pd.DataFrame(results)
        
        elif query_type == 'category_analysis':
            price = parsed_query.get('price', 100)
            
            # Group products by category
            category_prices = {}
            for product in self.sample_data['products']:
                cat = product['category']
                if cat not in category_prices:
                    category_prices[cat] = []
                category_prices[cat].append(product['price'])
            
            results = []
            for category, prices in category_prices.items():
                avg_price = sum(prices) / len(prices)
                if avg_price > price:
                    results.append({
                        'Category': category,
                        'Average Price': round(avg_price, 2),
                        'Product Count': len(prices),
                        'Min Price': min(prices),
                        'Max Price': max(prices)
                    })
            
            return pd.DataFrame(results)
        
        else:
            # Default: return all customers
            return pd.DataFrame(self.sample_data['customers'])

    def render(self):
        """Main render method for the Query Executor component."""
        
        st.subheader("🔍 Query Executor")
        st.markdown("Execute declarative queries against your knowledge graph using natural language.")
        
        # Check if schema exists
        if 'current_schema' not in st.session_state:
            st.warning("⚠️ Please define a schema in the Schema Builder tab first.")
            return
        
        # Two-column layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Query Input")
            
            # Query template selector
            st.markdown("**Choose a query template or write your own:**")
            template_name = st.selectbox(
                "Query Template",
                ["Custom Query"] + list(self.query_templates.keys()),
                help="Select a predefined query template or write your own"
            )
            
            if template_name == "Custom Query":
                query = st.text_area(
                    "Enter your query",
                    placeholder="e.g., FIND Customers who ordered more than 2 products in the last 30 days",
                    height=100
                )
            else:
                template = self.query_templates[template_name]
                
                # Add parameters for templates
                if template_name == "customer_orders":
                    threshold = st.slider("Product threshold", 1, 10, 2)
                    days = st.slider("Days", 7, 90, 30)
                    query = template.format(threshold=threshold, days=days)
                elif template_name == "high_value_customers":
                    amount = st.slider("Amount threshold ($)", 100, 1000, 500)
                    query = template.format(amount=amount)
                elif template_name == "product_popularity":
                    count = st.slider("Customer count threshold", 1, 10, 3)
                    query = template.format(count=count)
                elif template_name == "category_analysis":
                    price = st.slider("Price threshold ($)", 50, 200, 100)
                    query = template.format(price=price)
                else:
                    query = template
                
                st.text_area("Generated Query", query, height=100, disabled=True)
            
            # Execute button
            if st.button("🚀 Execute Query", type="primary"):
                if query.strip():
                    # Parse and execute query
                    parsed_query = self.parse_query(query)
                    results = self.execute_query(parsed_query)
                    
                    # Store results in session state
                    st.session_state['query_results'] = results
                    st.session_state['last_query'] = query
                    st.session_state['parsed_query'] = parsed_query
                    
                    st.success(f"✅ Query executed successfully! Found {len(results)} results.")
                else:
                    st.error("Please enter a query to execute.")
        
        with col2:
            st.subheader("📊 Query Results")
            
            if 'query_results' in st.session_state:
                results = st.session_state['query_results']
                
                # Display results
                if not results.empty:
                    st.dataframe(results, use_container_width=True)
                    
                    # Query statistics
                    with st.expander("📈 Query Statistics"):
                        st.write(f"**Total Results:** {len(results)}")
                        st.write(f"**Columns:** {list(results.columns)}")
                        
                        # Show some sample data insights
                        if 'Total Spent' in results.columns:
                            st.write(f"**Average Total Spent:** ${results['Total Spent'].mean():.2f}")
                        if 'Price' in results.columns:
                            st.write(f"**Average Price:** ${results['Price'].mean():.2f}")
                else:
                    st.info("No results found for this query.")
            else:
                st.info("👆 Execute a query to see results here")
        
        # Query examples
        with st.expander("💡 Query Examples"):
            st.markdown("""
            **Customer Analysis:**
            - `FIND Customers who ordered more than 2 products in the last 30 days`
            - `FIND Customers with total order value greater than $500`
            
            **Product Analysis:**
            - `FIND Products ordered by more than 3 customers`
            - `FIND Categories with average product price above $100`
            
            **Order Analysis:**
            - `FIND Orders placed in the last 7 days`
            - `FIND Customers who have been active for more than 6 months`
            """)
        
        # Query history
        if 'last_query' in st.session_state:
            with st.expander("📜 Query History"):
                st.write(f"**Last Query:** {st.session_state['last_query']}")
                if 'parsed_query' in st.session_state:
                    st.write(f"**Parsed Type:** {st.session_state['parsed_query'].get('type', 'unknown')}") 