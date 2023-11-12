import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import streamlit_authenticator as stauth
import matplotlib.pyplot as plt

# Authentication
names = ['Prashant', 'C H Raju']
usernames = ['prashant', 'raju']
passwords = ['9216', 'pdqc123']
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, 'some_cookie_name', 'some_signature_key',
                                    cookie_expiry_days=0)
name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    test = authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')

    # Function for Data Visualization
    def visualize_data(df):
        # Scatter Plot
        if selected_graph == "Scatter Plot":
            fig_scatter = px.scatter(df, x=st.session_state["parameter1"], y=st.session_state["parameter2"])
            st.write("Scatter Plot:")
            st.plotly_chart(fig_scatter)

        # Box Plot
        if selected_graph == "Box Plot":
            fig_box = px.box(df, y=st.session_state["parameter1"])
            st.write("Box Plot:")
            st.plotly_chart(fig_box)

        # Bar Plot
        if selected_graph == "Bar Plot":
            fig_bar = px.bar(df, x=st.session_state["parameter1"], y=st.session_state["parameter2"])
            st.write("Bar Plot:")
            st.plotly_chart(fig_bar)

        # Pie Chart
        if selected_graph == "Pie Chart":
            fig_pie = px.pie(df, values=st.session_state["parameter1"], names=df.index)
            st.write("Pie Chart:")
            st.plotly_chart(fig_pie)

        # Histogram
        if selected_graph == "Histogram":
            fig_hist = px.histogram(df, x=st.session_state["parameter1"])
            st.write("Histogram:")
            st.plotly_chart(fig_hist)

        # Line Chart
        if selected_graph == "Line Chart":
            fig_line = px.line(df, x=df.index, y=st.session_state["parameter1"])
            st.write("Line Chart:")
            st.plotly_chart(fig_line)

        # Area Chart
        if selected_graph == "Area Chart":
            fig_area = px.area(df, x=df.index, y=st.session_state["parameter1"])
            st.write("Area Chart:")
            st.plotly_chart(fig_area)

        # Violin Plot
        if selected_graph == "Violin Plot":
            fig_violin = px.violin(df, y=st.session_state["parameter1"])
            st.write("Violin Plot:")
            st.plotly_chart(fig_violin)

        # Heatmap
        if selected_graph == "Heatmap":
            fig_heatmap = px.imshow(df.corr())
            st.write("Heatmap:")
            st.plotly_chart(fig_heatmap)

        # Boxen Plot (Seaborn)
        if selected_graph == "Boxen Plot":
            st.write("Boxen Plot:")
            plt.figure(figsize=(8, 6))
            sns.boxenplot(data=df, y=st.session_state["parameter1"], x=df.index)
            st.pyplot()

        # Pair Plot (Seaborn)
        if selected_graph == "Pair Plot":
            st.write("Pair Plot:")
            sns.pairplot(df)
            st.pyplot()
            st.set_option('deprecation.showPyplotGlobalUse', False)

        # Joint Plot (Seaborn)
        if selected_graph == "Joint Plot":
            st.write("Joint Plot:")
            sns.jointplot(data=df, x=st.session_state["parameter1"], y=st.session_state["parameter2"])
            st.pyplot()

    st.title("Data Visualization App")
    files = st.file_uploader("Upload Multiple Files", type=["xlsx"], accept_multiple_files=True)
    files_name = [file.name for file in files] if files else []
    selected_files = st.multiselect("Select Multiple Files", options=files_name)
    if selected_files:
        for file in files:
            if file.name in selected_files:
                # Read all sheets from the Excel file
                xls = pd.ExcelFile(file)
                sheet_names = xls.sheet_names

                # Allow the user to choose a sheet
                selected_sheet = st.selectbox("Select a sheet", options=sheet_names)
                df = pd.read_excel(file, sheet_name=selected_sheet)

                st.write(df)
                st.session_state["parameter1"] = st.selectbox("Choose your parameter for x-axis", options=list(df.columns), key=f"{file.name}_{selected_sheet}_param1")
                st.session_state["parameter2"] = st.selectbox("Choose your parameter for y-axis", options=list(df.columns), key=f"{file.name}_{selected_sheet}_param2")
                selected_graph = st.selectbox("Select the type of plot", options=["Scatter Plot", "Bar Plot", "Box Plot", "Pie Chart", "Histogram", "Line Chart", "Area Chart", "Violin Plot", "Heatmap", "Boxen Plot", "Pair Plot", "Joint Plot"], key=f"{file.name}_{selected_sheet}_graph")
                visualize_data(df)

elif not st.session_state["authentication_status"]:
    st.error('Username/password is incorrect')

elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
