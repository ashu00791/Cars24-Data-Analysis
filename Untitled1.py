#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats


# In[3]:


df = pd.read_csv("Cars24.csv")


# In[5]:


summary = df.describe().round(2)


# In[7]:


df.head()


# In[8]:


df.describe()


# In[9]:


df.describe().round(2)


# In[ ]:


# Defining new metrics


# In[10]:


df['Age'] = 2023 - df['Model Year']
metrics = pd.DataFrame({
    'Metric': ['Total Cars', 'Unique Brands', 'Unique Models', 'Avg Price', 'Avg Age', 'Avg KMs Driven'],
    'Value': [
        len(df),
        df['Car Brand'].nunique(),
        df['Model'].nunique(),
        f"₹{df['Price'].mean():,.0f}",
        f"{df['Age'].mean():.1f} years",
        f"{df['Driven (Kms)'].mean():,.0f} km"
    ]
})

metrics


# In[12]:


import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[13]:


#Creating subplots


# In[14]:


fig = make_subplots(rows=2, cols=1, 
                    subplot_titles=('Price Distribution', 'Average Price by Brand (Top 10)'))


# In[15]:


#Price destribution
fig.add_trace(
    go.Histogram(x=df['Price'], name='Price Distribution', nbinsx=50),
    row=1, col=1
)


# In[16]:


# Average price by brand (top 10)
brand_avg = df.groupby('Car Brand')['Price'].mean().sort_values(ascending=False).head(10)
fig.add_trace(
    go.Bar(x=brand_avg.index, y=brand_avg.values, name='Avg Price by Brand'),
    row=2, col=1
)


# In[17]:


# Update layout
fig.update_layout(height=800, showlegend=False,
                 title_text="Price Analysis",
                 plot_bgcolor='white')

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')


# In[18]:


fig.show()


# In[19]:


# Calculate metrics by location
location_stats = df.groupby('Location').agg({
    'Price': ['mean', 'count'],
    'Model Year': 'mean',
    'Driven (Kms)': 'mean'
}).round(2)

location_stats.columns = ['Avg_Price', 'Inventory_Count', 'Avg_Year', 'Avg_KMs']
location_stats = location_stats.reset_index()


# In[20]:


# Create subplots
fig = make_subplots(rows=2, cols=1,
                    subplot_titles=('Average Price by Location', 
                                  'Inventory Count by Location'),
                    vertical_spacing=0.2)


# In[21]:


# Average price by location
fig.add_trace(
    go.Bar(x=location_stats['Location'],
           y=location_stats['Avg_Price'],
           text=location_stats['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
           textposition='auto',
           name='Average Price'),
    row=1, col=1
)


# In[22]:


# Inventory count by location
fig.add_trace(
    go.Bar(x=location_stats['Location'],
           y=location_stats['Inventory_Count'],
           text=location_stats['Inventory_Count'],
           textposition='auto',
           name='Inventory Count'),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=800,
    showlegend=False,
    title_text="Geographical Market Analysis",
    plot_bgcolor='white'
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

# Show the plot
fig.show()

# Return detailed statistics
location_stats['Avg_Price'] = location_stats['Avg_Price'].apply(lambda x: f'₹{x:,.0f}')
location_stats['Avg_KMs'] = location_stats['Avg_KMs'].apply(lambda x: f'{x:,.0f} km')
location_stats['Avg_Year'] = location_stats['Avg_Year'].round(1)
location_stats


# In[23]:


# Calculate price metrics by location
price_analysis = df.groupby('Location').agg({
    'Price': ['mean', 'std', 'min', 'max', 'count']
}).round(2)

price_analysis.columns = ['Avg_Price', 'Price_Std', 'Min_Price', 'Max_Price', 'Count']
price_analysis = price_analysis.reset_index()

# Calculate price spread and potential margin indicators
price_analysis['Price_Range'] = price_analysis['Max_Price'] - price_analysis['Min_Price']
price_analysis['Price_Volatility'] = (price_analysis['Price_Std'] / price_analysis['Avg_Price']) * 100
price_analysis['Market_Size'] = price_analysis['Count'] * price_analysis['Avg_Price']

# Create visualization
fig = make_subplots(rows=2, cols=1,
                    subplot_titles=('Price Range and Average by Location',
                                  'Price Volatility and Market Size'),
                    vertical_spacing=0.2)

# Price range plot
fig.add_trace(
    go.Bar(name='Price Range',
           x=price_analysis['Location'],
           y=price_analysis['Price_Range'],
           text=price_analysis['Price_Range'].apply(lambda x: f'₹{x:,.0f}'),
           textposition='auto'),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(name='Average Price',
               x=price_analysis['Location'],
               y=price_analysis['Avg_Price'],
               mode='markers+text',
               marker=dict(size=12),
               text=price_analysis['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
               textposition='top center'),
    row=1, col=1
)

# Volatility and market size plot
fig.add_trace(
    go.Bar(name='Price Volatility (%)',
           x=price_analysis['Location'],
           y=price_analysis['Price_Volatility'],
           text=price_analysis['Price_Volatility'].round(1).apply(lambda x: f'{x}%'),
           textposition='auto'),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=800,
    title_text="Price Variation and Market Opportunity Analysis",
    showlegend=True,
    plot_bgcolor='white'
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

fig.show()

# Create summary table
summary = pd.DataFrame({
    'Location': price_analysis['Location'],
    'Avg_Price': price_analysis['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
    'Price_Range': price_analysis['Price_Range'].apply(lambda x: f'₹{x:,.0f}'),
    'Volatility': price_analysis['Price_Volatility'].round(1).apply(lambda x: f'{x}%'),
    'Market_Size': (price_analysis['Market_Size']/10000000).round(2).apply(lambda x: f'₹{x:.2f}Cr')
})

summary


# In[24]:


# Calculate age and add current year for reference
df['Age'] = 2023 - df['Model Year']

# Calculate price metrics by model year and location
yearly_analysis = df.groupby(['Location', 'Model Year']).agg({
    'Price': ['mean', 'std', 'count']
}).reset_index()

yearly_analysis.columns = ['Location', 'Model_Year', 'Avg_Price', 'Price_Std', 'Count']

# Calculate price per year of age
yearly_analysis['Price_per_Year'] = yearly_analysis['Avg_Price'] / (2023 - yearly_analysis['Model_Year'])

# Create visualization
fig = make_subplots(rows=2, cols=1,
                    subplot_titles=('Average Price by Model Year and Location',
                                  'Price Depreciation Rate by Location'),
                    vertical_spacing=0.2)

# Price trends by year
for location in yearly_analysis['Location'].unique():
    location_data = yearly_analysis[yearly_analysis['Location'] == location]
    fig.add_trace(
        go.Scatter(name=location,
                  x=location_data['Model_Year'],
                  y=location_data['Avg_Price'],
                  mode='lines+markers',
                  text=location_data['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
                  hovertemplate='Year: %{x}<br>Price: %{text}'),
        row=1, col=1
    )

# Price per year analysis
location_depreciation = yearly_analysis.groupby('Location')['Price_per_Year'].mean().sort_values(ascending=True)

fig.add_trace(
    go.Bar(x=location_depreciation.index,
           y=location_depreciation.values,
           text=location_depreciation.apply(lambda x: f'₹{x:,.0f}/year'),
           textposition='auto',
           name='Depreciation Rate'),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=800,
    title_text="Price Trends and Depreciation Analysis by Location",
    showlegend=True,
    plot_bgcolor='white'
)

fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

# Show plot
fig.show()

# Create summary table
summary = pd.DataFrame({
    'Location': location_depreciation.index,
    'Avg_Annual_Depreciation': location_depreciation.apply(lambda x: f'₹{x:,.0f}/year'),
    'Newest_Inventory': yearly_analysis.groupby('Location')['Model_Year'].max(),
    'Oldest_Inventory': yearly_analysis.groupby('Location')['Model_Year'].min(),
    'Avg_Model_Year': yearly_analysis.groupby('Location')['Model_Year'].mean().round(1)
})

summary


# In[25]:


# Define luxury brands (based on Indian market context)
luxury_brands = ['BMW', 'Mercedes', 'Audi', 'Volvo', 'Jaguar', 'Land Rover', 'Lexus']
df['Segment'] = df['Car Brand'].apply(lambda x: 'Luxury' if x in luxury_brands else 'Economy')

# Calculate age
df['Age'] = 2023 - df['Model Year']

# Calculate metrics by segment and age
segment_analysis = df.groupby(['Segment', 'Age']).agg({
    'Price': ['mean', 'count'],
    'Model Year': 'mean'
}).reset_index()

segment_analysis.columns = ['Segment', 'Age', 'Avg_Price', 'Count', 'Avg_Model_Year']

# Create visualization
fig = make_subplots(rows=2, cols=1,
                    subplot_titles=('Price Depreciation by Segment',
                                  'Average Price Distribution by Segment'),
                    vertical_spacing=0.2)

# Depreciation curves
for segment in ['Luxury', 'Economy']:
    segment_data = segment_analysis[segment_analysis['Segment'] == segment].sort_values('Age')
    
    fig.add_trace(
        go.Scatter(name=f'{segment} Segment',
                  x=segment_data['Age'],
                  y=segment_data['Avg_Price'],
                  mode='lines+markers',
                  text=segment_data['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
                  hovertemplate='Age: %{x} years<br>Price: %{text}'),
        row=1, col=1
    )

# Price distribution by segment
fig.add_trace(
    go.Box(x=df[df['Segment'] == 'Luxury']['Age'],
           y=df[df['Segment'] == 'Luxury']['Price'],
           name='Luxury',
           boxpoints='outliers'),
    row=2, col=1
)

fig.add_trace(
    go.Box(x=df[df['Segment'] == 'Economy']['Age'],
           y=df[df['Segment'] == 'Economy']['Price'],
           name='Economy',
           boxpoints='outliers'),
    row=2, col=1
)

# Update layout
fig.update_layout(
    height=800,
    title_text="Luxury vs Economy Segment Analysis",
    showlegend=True,
    plot_bgcolor='white'
)

fig.update_xaxes(title_text="Age (Years)", showgrid=False)
fig.update_yaxes(title_text="Price (₹)", showgrid=True, gridwidth=1, gridcolor='LightGray')

fig.show()

# Calculate depreciation rates
def calculate_depreciation_rate(group):
    if len(group) < 2:
        return pd.Series({'Avg_Annual_Depreciation': 0, 'Depreciation_Rate': 0})
    
    max_price = group[group['Age'] == group['Age'].min()]['Avg_Price'].iloc[0]
    min_price = group[group['Age'] == group['Age'].max()]['Avg_Price'].iloc[0]
    years = group['Age'].max() - group['Age'].min()
    
    if years == 0 or max_price == 0:
        return pd.Series({'Avg_Annual_Depreciation': 0, 'Depreciation_Rate': 0})
    
    annual_dep = (max_price - min_price) / years
    dep_rate = (annual_dep / max_price) * 100
    
    return pd.Series({
        'Avg_Annual_Depreciation': annual_dep,
        'Depreciation_Rate': dep_rate
    })

depreciation_stats = segment_analysis.groupby('Segment').apply(calculate_depreciation_rate).round(2)
depreciation_stats['Avg_Price'] = df.groupby('Segment')['Price'].mean().round(2)
depreciation_stats['Inventory_Count'] = df.groupby('Segment')['Price'].count()

# Format the results
summary = pd.DataFrame({
    'Segment': depreciation_stats.index,
    'Avg_Price': depreciation_stats['Avg_Price'].apply(lambda x: f'₹{x:,.0f}'),
    'Annual_Depreciation': depreciation_stats['Avg_Annual_Depreciation'].apply(lambda x: f'₹{x:,.0f}'),
    'Depreciation_Rate': depreciation_stats['Depreciation_Rate'].apply(lambda x: f'{x:.1f}%'),
    'Inventory': depreciation_stats['Inventory_Count']
})

summary


# In[ ]:




