# Data-Science-Project

# Setup Environment - Anaconda
conda create --name base python=3.11.0  
conda activate base  
pip install -r requirements.txt  

# Setup Environment - Shell/Terminal
mkdir proyek_analisis_data  
cd proyek_analisis_data  
pipenv install  
pipenv shell  
pip install -r requirements.txt  

# Run steamlit app
streamlit run Dashboard.py  

