# Imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set the app
st.set_page_config(page_title='Data Sweeper', layout='wide')
st.title('Data Sweeper')
st.write('Transform your files between formats CSV and Excel with buld-in Data cleaning and visualization!')

# Uploaded files
uploaed_files = st.file_uploader('Upload your files (CSV or Excel)', type=['csv', 'xlsx'],
                                  accept_multiple_files=True)

# Check if files are in which format

if uploaed_files:
    for file in uploaed_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df = pd.read_excel(file)
        else:
            st.error('File type not supported:{file_ext}')
            continue

    # Display info about the file
    st.write(f'**File name:** {file.name}')
    st.write(f'**File type:** {file_ext}')
    st.write(f'**File size:** {file.size/1024}')

    # Show the 5 rows dataframe
    st.write('**Preview First 5 rows of the Dataframe**')
    st.dataframe(df.head())

    # Options for Data cleaning
    st.subheader('Data Cleaning Options')
    if st.checkbox(f'Clean Data for {file.name}'):
        col1, col2 = st.columns(2)

        with col1:
            if st.button(f'Remove Duplicates from {file.name}'):
                df.drop_duplicates(inplace=True)  # <-- Fixed: Removed assignment to avoid None
                st.write('Duplicates Removed')

        with col2:
            if st.button(f'Fill Missing Values for {file.name}'):
                num_col = df.select_dtypes(include=['number']).columns
                df[num_col] = df[num_col].fillna(df[num_col].mean())
                st.write('Missing Values Filled')

    # Choose the specified columns to Keep or to Convert
    st.subheader(f'Choose Columns to Keep or Convert from {file.name}')
    columns = st.multiselect("Select columns to keep", options=df.columns, default=list(df.columns))
    df = df[columns]

    # Create some Visualization
    st.subheader('Data Visualization')
    if st.checkbox(f'Show Visualization for {file.name}'):
        st.bar_chart(df.select_dtypes(include=['number']).iloc[:, :2])

    # Convert the file to CSV or Excel
    st.subheader(f'Convert {file.name} to CSV or Excel')
    convert_option = st.radio(f'Convert {file.name} to:', ['CSV', 'Excel'], key=file.name)
    if st.button(f'Convert {file.name}'):
        buffer = BytesIO()
        if convert_option == 'CSV':
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, '.csv')
            mime_type = 'text/csv'

        elif convert_option == 'Excel':
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, '.xlsx')
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        buffer.seek(0)

        # Download Button
        st.download_button(
            label=f'Download {file.name} as {convert_option}',
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
    st.success('Thank you for using Data Sweeper!')
