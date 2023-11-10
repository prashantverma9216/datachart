import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff

import streamlit_authenticator as stauth
figure= plt.figure()
import streamlit as st

# function
def main():
    
        st.title("Data Visualization App")
    
        files =st.file_uploader("upload Multiple File",type=["xlsx"],accept_multiple_files=True)
        files_name =[]
        if files:
            for file in files:
                files_name.append(file)
        selected_files = st.multiselect("You can select multiple files",options=files_name)
        if selected_files:
            for file in files_name:
                if file in selected_files:
                    df = pd.read_excel(file)
                    st.write(df)
                    parameter1=st.selectbox("chose your parameter to plot", options = list(df.columns),key=5)
                    parameter2=st.selectbox("chose your parameter to plot", options = list(df.columns),key=6)
                    st.write(parameter1)
                    selected_graph=st.selectbox("Select the type of plot you want to plot",options=["Scatter","Bar Plot","BoxPlot","Pie Chart","Histogram","Distplot","2D Density Heatmap"],key=1)
                   
                         
                        
                    if selected_graph=="Scatter":
                            
                        fig1 = px.scatter(df,y=df[parameter1],x=df[parameter2])
                        st.write(fig1)
                    elif selected_graph == "BoxPlot" :
                             fig = px.box(df,y=df[parameter1])
                             st.write(fig)
                            
                    elif selected_graph == "Bar Plot" :
                             fig2 = px.bar(df,x=df[parameter1],y=df[parameter2])
                             st.write(fig2)
                    elif selected_graph == "Pie Chart" :        
                        fig = px.pie(df, values=df[parameter1],names=df[parameter2])
                        st.write(fig)         
                    
                    elif selected_graph == "Distplot": 
                        fig = ff.create_distplot([df[parameter1]], group_labels=[parameter1])
                        st.write(fig)
                    elif selected_graph == "2D Density Heatmap":
                        fig = px.density_heatmap(df, x=parameter1, y=parameter2)
                        st.write(fig)

# ...

                          
# Authentication                
names = ['Prashant','C H Raju']
usernames = ['prashant','raju']
passwords = ['9216','pdqc123']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names,usernames,hashed_passwords,'some_cookie_name','some_signature_key',cookie_expiry_days=30)
name, authentication_status, username = authenticator.login('Login', 'main')
        
if st.session_state["authentication_status"]:
        test=authenticator.logout('Logout', 'main')
        st.write(f'Welcome *{st.session_state["name"]}*')
        main()
elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')
        
