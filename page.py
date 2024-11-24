import streamlit as st
import os
import pandas as pd
from PIL import Image
import streamlit.components.v1 as components
import time
from datetime import datetime as dt
import random as rd
from wordcloud import WordCloud , STOPWORDS
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot

data = pd.read_csv(r"C:\\Users\\utkun\\Desktop\\Minor-1\\clean.csv")
#print(data.head())

title_html = """
    <h1 style="color: white;">Interactive Job Market Analysis Dashboard</h1>
"""

# Use st.markdown to display the title with custom styling
st.markdown(title_html, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        background-color: black; /* Set the background color to black */
        color: white; /* Set the text color to white */
    }
    .stMarkdown h1, h2, h3, h4, h5, h6, p {
        color: white; /* Apply white color to all headers and paragraphs */
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.subheader("Dataset")
st.dataframe(data.head())

def save_img(fig,file_path,library='plotly'):
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # Save the new plot
    if library == 'plotly':
        fig.write_image(file_path)
    elif library == 'matplotlib':
        plt.savefig(file_path)
        
    print(f"Plot saved as {file_path}")


st.subheader("Job Post Frequency")
job_counts = data["Tag"].value_counts()
fig, ax = plt.subplots()
job_counts.plot(kind="bar", color="blue", ax=ax)
plt.title("Job Post Frequency")
plt.xlabel("Job Cluster")
plt.ylabel("Count")
st.pyplot(fig)


IMAGE_DIR = 'E:\minor_flask\images'
# Function to load images from the directory
def load_images(image_dir):
    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    images = []
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        image = Image.open(image_path)
        images.append((image_file, image))
    return images

images = load_images(IMAGE_DIR)
i=0
while(i<len(images)):
    st.image(images[i][1], caption=images[i][0], use_column_width=True)
    i=i+1


st.subheader("Wordcloud")
jb_options = data['Title'].unique()
jb_options = ["None"] + jb_options.tolist()
jb = st.selectbox("Choose an option", jb_options)
if jb != 'None':
    j = pd.DataFrame(data[data['Title']==jb]).reset_index()
    st.dataframe(j)

lc_options = data['Location'].unique()
lc_options = ["None"] + lc_options.tolist()
lc = st.selectbox("Choose an option", lc_options)
if lc != 'None':
    l = pd.DataFrame(data[data['Location']==lc]).reset_index()
    st.dataframe(l)


tg_options = data['Tag'].unique()
tg_options = ["None"] + tg_options.tolist()
tg = st.selectbox("Choose an option", tg_options)
if tg != 'None':
    t = pd.DataFrame(data[data['Tag']==tg]).reset_index()
    st.dataframe(t)

temp = pd.DataFrame(data['Cluster'].value_counts()).reset_index()
temp.columns = ['Cluster','Count']

f = px.pie(temp, names=temp['Cluster'], values=temp['Count'], title='Pie Chart')
# Display pie chart in Streamlit
st.plotly_chart(f)