</head>
<body>

  <!-- Title & Image -->
  <h1 align="center">Data Analysis Project Documentation</h1>
  <p align="center">
    <img src="https://socialify.git.ci/Wakbarr/Proyek-Analisis-Data/image?font=KoHo&language=1&name=1&pattern=Transparent&theme=Auto" alt="Project Image">
  </p>
    This project involves a comprehensive data analysis process using Python. The entire analysis is documented in a Jupyter Notebook (.ipynb) with detailed markdown cells that explain each step—from defining questions to drawing conclusions. The project also includes effective data visualizations, deployment of an interactive dashboard to Streamlit Cloud, and advanced analysis techniques such as RFM Analysis, Geospatial Analysis, and Clustering (without machine learning algorithms).
  </p>

  <!-- Installation Steps -->
  <h2>🛠️ Installation Steps</h2>
  <ol>
    <li>
      <strong>Prerequisites:</strong>
      <ul>
        <li>Python 3.x installed (preferably via Anaconda or Miniconda)</li>
        <li>Jupyter Notebook or JupyterLab</li>
        <li>Git</li>
      </ul>
    </li>
    <li>
      <strong>Clone the Repository:</strong>
      <pre><code>git clone https://github.com/yourusername/data-analysis-project.git</code></pre>
    </li>
    <li>
      <strong>Create and Activate a Virtual Environment:</strong>
      <pre><code>
# Using conda
conda create -n data_analysis_env python=3.8
conda activate data_analysis_env

# or using virtualenv
python -m venv data_analysis_env
source data_analysis_env/bin/activate
      </code></pre>
    </li>
    <li>
      <strong>Install Required Packages:</strong>
      <pre><code>pip install -r requirements.txt</code></pre>
      <p>
        (Ensure your <code>requirements.txt</code> includes packages such as <code>pandas</code>, <code>numpy</code>, <code>matplotlib</code>, <code>seaborn</code>, <code>plotly</code>, <code>geopandas</code>, <code>folium</code>, and <code>streamlit</code>.)
      </p>
    </li>
    <li>
      <strong>Open the Jupyter Notebook:</strong>
      <p>Launch Jupyter Notebook or JupyterLab and open the provided .ipynb file for detailed documentation and code examples.</p>
    </li>
  </ol>

  <!-- Code for Key Steps -->
  <h2>💻 Sample Code for Key Steps</h2>
  
  <h3>1. RFM Analysis</h3>
  <p>
    This sample code calculates the Recency, Frequency, and Monetary values for each customer.
  </p>
  <pre><code class="language-python">
import pandas as pd

# Sample dataset with customer transactions
data = pd.DataFrame({
    'customer_id': [1, 2, 1, 3, 2],
    'purchase_date': pd.to_datetime(['2021-01-01', '2021-02-01', '2021-03-01', '2021-01-15', '2021-03-15']),
    'amount': [100, 200, 150, 120, 300]
})

# Define the analysis date
analysis_date = pd.to_datetime('2021-04-01')

# Calculate RFM metrics
rfm = data.groupby('customer_id').agg({
    'purchase_date': lambda x: (analysis_date - x.max()).days,
    'customer_id': 'count',
    'amount': 'sum'
}).rename(columns={
    'purchase_date': 'Recency', 
    'customer_id': 'Frequency', 
    'amount': 'Monetary'
})

print(rfm)
  </code></pre>

  <h3>2. Geospatial Analysis</h3>
  <p>
    This snippet demonstrates creating a map using <code>folium</code> to visualize data based on geographic locations.
  </p>
  <pre><code class="language-python">
import folium

# Sample list of locations with latitude and longitude
locations = [
    {'name': 'Store A', 'lat': -6.200000, 'lon': 106.816666},
    {'name': 'Store B', 'lat': -6.300000, 'lon': 106.816666}
]

# Create a folium map centered at a given location
m = folium.Map(location=[-6.250000, 106.816666], zoom_start=10)

# Add markers for each location
for loc in locations:
    folium.Marker([loc['lat'], loc['lon']], popup=loc['name']).add_to(m)

# Save the map as an HTML file
m.save("geospatial_map.html")
  </code></pre>

  <h3>3. Clustering Using Manual Grouping &amp; Binning</h3>
  <p>
    This code shows how to perform manual grouping by binning data into intervals.
  </p>
  <pre><code class="language-python">
import pandas as pd

# Sample dataset with customer age and spending
data = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'age': [25, 45, 35, 50, 28],
    'spending': [200, 500, 300, 700, 250]
})

# Binning age into groups (e.g., 20s, 30s, 40-60)
data['age_group'] = pd.cut(data['age'], bins=[20, 30, 40, 60], labels=['20s', '30s', '40-60'])

print(data)
  </code></pre>

  <h3>4. Dashboard Deployment with Streamlit</h3>
  <p>
    A basic example of running a Streamlit dashboard. Deploy your dashboard to Streamlit Cloud for interactive data presentation.
  </p>
  <pre><code class="language-python">
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load sample data
data = pd.DataFrame({
    'x': range(10),
    'y': [x**2 for x in range(10)]
})

st.title("Data Analysis Dashboard")
st.write("This dashboard displays a sample visualization.")

# Plotting
fig, ax = plt.subplots()
ax.plot(data['x'], data['y'])
st.pyplot(fig)
  </code></pre>

  <!-- Contribution Guidelines -->
  <h2>🍰 Contribution Guidelines</h2>
  <p>
    We welcome contributions from developers and data enthusiasts of all levels. Please adhere to the following guidelines:
  </p>
  <ol>
    <li>
      <strong>Fork the Repository:</strong> Click the "Fork" button on GitHub to create a copy under your account.
    </li>
    <li>
      <strong>Clone Your Fork:</strong>
      <pre><code>git clone https://github.com/YOUR_GITHUB_USERNAME/data-analysis-project.git</code></pre>
      Replace <code>YOUR_GITHUB_USERNAME</code> with your GitHub username.
    </li>
    <li>
      <strong>Create a New Branch:</strong>
      <pre><code>git checkout -b feature/your-feature-name</code></pre>
    </li>
    <li>
      <strong>Make Your Changes:</strong>
      <p>
        Ensure your code is well-documented, and add markdown/text cells in your Jupyter Notebook to explain each analysis step.
      </p>
    </li>
    <li>
      <strong>Test Your Changes:</strong>
      <p>Verify that your updates work as expected, and that your dashboard runs correctly on Streamlit Cloud.</p>
    </li>
    <li>
      <strong>Commit Your Changes:</strong>
      <pre><code>git commit -m "Describe your changes here"</code></pre>
    </li>
    <li>
      <strong>Push Your Branch:</strong>
      <pre><code>git push origin feature/your-feature-name</code></pre>
    </li>
    <li>
      <strong>Create a Pull Request (PR):</strong>
      <p>
        Submit a PR on GitHub with a detailed description of your changes, including any relevant screenshots or explanations.
      </p>
    </li>
  </ol>

  <!-- Technologies Used -->
  <h2>💻 Technologies Used</h2>
  <p>This project leverages the following technologies:</p>
  <ul>
    <li><strong>Python 3.x:</strong> Primary programming language for data analysis.</li>
    <li><strong>Jupyter Notebook:</strong> For documenting the analysis process using markdown and code cells.</li>
    <li><strong>pandas &amp; numpy:</strong> For data manipulation and numerical operations.</li>
    <li><strong>matplotlib, seaborn &amp; plotly:</strong> For creating effective and insightful data visualizations.</li>
    <li><strong>GeoPandas &amp; folium:</strong> For geospatial data analysis and mapping.</li>
    <li><strong>Streamlit:</strong> For building and deploying interactive dashboards on Streamlit Cloud.</li>
    <li><strong>Additional Libraries:</strong> Such as scikit-learn (for non-ML clustering support), and other utility packages.</li>
  </ul>

  <p>
    Happy analyzing and coding!
  </p>

</body>
</html>
