import streamlit as st
import pandas as pd
from main_processor import process_records

def main():
    st.title("URL Data Programmatic Data Extraction Application")

    instructions_placeholder = st.empty()
    instructions_placeholder.info(
        "Instructions for using the application:"
        "\n\n"
        "1. Upload the 'records' file (fill in template do not change headers or file structure)"
        "\n\n"
        "2. Upload the 'queries' file (fill in template do not change headers or file structure)"
        "\n\n"
        "3. Click the 'Process' button to start data processing."
        "\n\n"
        "4. The processed data will be displayed below."
        "\n\n"
        "5. Enter Your API Key (will not be stored)"
        "\n\n"
        "6. You can download the processed data as a CSV file."
        "\n\n"
        "***Please note this application may take time to run, do not close the window while it is running.***"
    )

    upload_files_placeholder = st.empty()
    with upload_files_placeholder.container():
        st.subheader("Upload CSV Files")
        download_template_records = st.markdown(
            """
            <div style="display: flex; justify-content: flex-end;">
                <a href="https://drive.google.com/uc?export=download&id=1S9Cy-njxZk5Fkg_IhRgXpGYHWXGiLcuA" download="records_template.csv" style="margin-left: 10px;">Download records template.csv</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        records_file = st.file_uploader("Upload RECORDS FILE", type=['csv'])
        download_template_queries = st.markdown(
            """
            <div style="display: flex; justify-content: flex-end;">
                <a href="https://drive.google.com/uc?export=download&id=1Wn0WqJzAZBxWvbF1W74BOHeJCL8sCdcR" download="queries_template.csv" style="margin-left: 10px;">Download queries template.csv</a>
            </div>
            """,
            unsafe_allow_html=True
        )
        queries_file = st.file_uploader("Upload QUERIES FILE", type=['csv'])
    
    api_key_placeholder = st.empty()
    with api_key_placeholder.container():
        st.subheader("OpenAI API Key")
        api_key = st.text_input("Enter your OpenAI API key (it will not be stored)", type="password")

    process_button_placeholder = st.empty()
    process_button = process_button_placeholder.button("Process Files")

    if process_button:
        if records_file is not None and queries_file is not None and api_key:
            try:
                records_df = pd.read_csv(records_file)
                queries_df = pd.read_csv(queries_file)
                progress_bar = st.progress(0)
                output_df = process_records(records_df, queries_df, progress_bar, api_key)  # Pass the API key here
                # Once processing is complete, clear all unnecessary elements
                api_key_placeholder.empty()
                instructions_placeholder.empty()
                upload_files_placeholder.empty()
                process_button_placeholder.empty()
                progress_bar.empty()
                
                # Display the results and download button
                st.write(output_df)
                st.download_button("Download Results", output_df.to_csv().encode('utf-8'), "output.csv", "text/csv", key='download-csv')
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please upload both files and enter your OpenAI API key to proceed.")

if __name__ == "__main__":
    main()