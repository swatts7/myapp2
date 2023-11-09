import pandas as pd
import requests
from modular_scraper import scrape_page_to_text
import logging
import streamlit as st


# Configure logging
logging.basicConfig(level=logging.INFO)

# Usage: logging.info("Your log message")


def process_records(records_df, queries_df, progress_bar, api_key):
    results = []
    total_records = len(records_df)

    record_info_placeholder = st.empty()

    for index, record in records_df.iterrows():
        try:
            # Update progress in Streamlit
            progress_percentage = int((index + 1) / total_records * 100)
            progress_bar.progress(progress_percentage)

            # Display record processing
            record_info_placeholder.text(f"Processing record: {record['record_name']} – please be patient 🙂")

            # Retrieve URL content
            record_info_placeholder.text(f"Retrieving URL content for record: {record['record_name']}")
            scraped_content = scrape_page_to_text(record['target_urls_scraping'])

            for _, query_row in queries_df.iterrows():
                try:
                    modified_query = query_row['query'].replace('{variable}', record['variable_1'])

                    # Constructing the full query with additional elements
                    full_query = (
                        f"{query_row['general_instruction']}\n"
                        f"Query: {modified_query}\n"
                        f"{query_row['format_instruction']}\n"
                        f"Example 1: {query_row['example_1']}\n"
                        f"Example 2: {query_row['example_2']}\n"
                        f"Source Context: {scraped_content}"
                    )

                    # Print the query for debugging
                    print("Full Query being sent to OpenAI:", full_query)

                    # Display sending query
                    record_info_placeholder.text(f"Sending query for record {record['record_name']}, variable: {query_row['variable_name']}")

                    # Create the conversation variable
                    conversation = [
                        {'role': 'system', 'content': 'You are a helpful assistant.'},
                        {'role': 'user', 'content': full_query}
                    ]

                    # Call the send_openai_request function
                    response = send_openai_request(conversation, api_key)

                    results.append({
                        'record_name': record['record_name'],
                        'variable_name': query_row['variable_name'],
                        'output': response
                    })

                except KeyError as ke:
                    logging.error(f"Key Error in query processing for record {record['record_name']}: {ke}")
                except Exception as e:
                    logging.error(f"Error processing query for record {record['record_name']}: {e}")

        except Exception as e:
            logging.error(f"Error processing record {record['record_name']}: {e}")

    record_info_placeholder.empty()
    return pd.DataFrame(results)

def send_openai_request(conversation, api_key):
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'messages': conversation,
        'model': 'gpt-3.5-turbo-0613',
        'temperature': 0,  # Adjust as needed
        'max_tokens': 200  # Adjust as needed
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            api_response = response.json()
            # Extract the assistant's reply
            assistant_reply = api_response['choices'][0]['message']['content']
            return assistant_reply
        else:
            return {"error": f"API Error: Status Code {response.status_code}, Response {response.text}"}
    except Exception as e:
        return {"error": f"Request Failed: {e}"}
