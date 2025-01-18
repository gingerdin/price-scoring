import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set custom CSS to match slider width with plot
st.markdown("""
    <style>
    /* Adjust slider container */
    .stSlider {
        width: auto;
        margin: 0 40px;  /* Match plot margins */
    }
    
    /* Adjust slider track */
    .stSlider > div[data-baseweb="slider"] {
        width: 100% !important;
    }
    
    /* Adjust slider label */
    .stSlider [data-testid="stWidgetLabel"] {
        margin-left: 0;
    }
    
    /* Hide default padding */
    .element-container {
        padding: 0;
    }
    </style>
""", unsafe_allow_html=True)

# Set page title
st.title('Product Metrics vs Price Demo')

# Create realistic data with common pricing psychology patterns
prices = np.array([4.99, 9.99, 14.99, 19.99, 24.99, 29.99, 34.99, 39.99, 44.99, 49.99,
                  54.99, 59.99, 64.99, 69.99, 74.99, 79.99, 84.99, 89.99, 94.99, 99.99])

# Engagement typically starts high at low prices, drops sharply at first, then gradually
engagement = np.array([92, 88, 85, 80, 75, 71, 68, 65, 63, 60,
                      58, 56, 54, 52, 50, 48, 46, 44, 42, 40])

# Satisfaction often follows a bell curve - too cheap might mean low quality, too expensive creates high expectations
satisfaction = np.array([75, 82, 88, 92, 94, 93, 91, 88, 85, 81,
                        77, 74, 70, 67, 64, 61, 58, 55, 52, 50])

# Retention typically follows a similar pattern to satisfaction
retention = np.array([70, 78, 85, 89, 91, 90, 88, 85, 82, 78,
                     74, 71, 68, 65, 62, 59, 56, 53, 50, 48])

# Create dataframe
df = pd.DataFrame({
    'Price (USD)': prices,
    'Engagement Score': engagement,
    'Satisfaction Score': satisfaction,
    'Retention Rate': retention
})

# Add price slider
selected_price = st.slider(
    'Select Price Point (USD)',
    min_value=float(df['Price (USD)'].min()),
    max_value=float(df['Price (USD)'].max()),
    value=float(df['Price (USD)'].min()),
    step=0.01
)

# Create plot
fig = go.Figure()

# Add traces for each metric
fig.add_trace(go.Scatter(
    x=df['Price (USD)'],
    y=df['Engagement Score'],
    mode='lines+markers',
    name='Engagement Score'
))

fig.add_trace(go.Scatter(
    x=df['Price (USD)'],
    y=df['Satisfaction Score'],
    mode='lines+markers',
    name='Satisfaction Score'
))

fig.add_trace(go.Scatter(
    x=df['Price (USD)'],
    y=df['Retention Rate'],
    mode='lines+markers',
    name='Retention Rate'
))

# Add vertical line for selected price
fig.add_shape(dict(
    type='line',
    x0=selected_price,
    x1=selected_price,
    yref='paper',
    y0=0,
    y1=1,
    line=dict(color='red', dash='dash')
))

# Update layout with specific width
fig.update_layout(
    title='Product Metrics vs Price',
    xaxis_title='Price (USD)',
    yaxis_title='Score/Rate',
    template='plotly_white',
    xaxis=dict(
        range=[df['Price (USD)'].min(), df['Price (USD)'].max()]
    ),
    width=None,
    height=600,
    margin=dict(l=40, r=40, t=40, b=40)
)

# Display plot
st.plotly_chart(fig, use_container_width=True)

# Add explanation outside the column
st.markdown("""
This demo shows realistic relationships between product price and key metrics:
- **Engagement Score**: Highest at lower price points, showing a steady decline as price increases
- **Satisfaction Score**: Follows a bell curve - peaks around $25-30, as very low prices might indicate low quality while high prices create expectations that are harder to meet
- **Retention Rate**: Similar to satisfaction, optimal in the mid-price range where perceived value matches cost
- The red dashed line shows your selected price point to compare metrics

Common patterns shown:
1. Price sensitivity affects engagement most directly
2. Mid-range prices often achieve optimal satisfaction
3. There's a "sweet spot" where metrics converge for optimal pricing
""")