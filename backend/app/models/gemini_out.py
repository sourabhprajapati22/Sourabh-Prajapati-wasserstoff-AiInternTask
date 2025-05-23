from google import genai
from google.genai import types
import pandas as pd


def formatted_prompt(docs):
    df = pd.DataFrame(docs, columns=["doc_id", "page_idx", "para_idx","text","score"])

    # Create citation column
    df["citation"] = df.apply(lambda row: f"Page {row['page_idx']}, \nPara {row['para_idx']}", axis=1)

    # Reorder and select required columns
    formatted_df = df[["doc_id", "text", "citation"]]
    formatted_df.columns = ["Document ID", "Extracted Answer", "Citation"]

    # print(formatted_df)
    return formatted_df

def dataframe_to_prompt(df):
    prompt = "Document \nID \n"
    prompt += "\n".join(df["Document ID"]) + "\n"
    prompt += "●  \nExtracted Answer \n"
    prompt += "\n".join(df["Extracted Answer"]) + "\n"
    prompt += "Citation \n"
    prompt += "\n".join(df["Citation"]) + "\n"
    prompt += """
    Final synthesized response in chat format with clear citations marked by 
    document IDs. Example: 
    Theme 1 - Regulatory Non-Compliance: 
    Documents (DOC001, DOC002) highlight regulatory non-compliance with 
    SEBI Act and LODR. 
    Theme 2 - Penalty Justification: 
    DOC001 explicitly justifies penalties under statutory frameworks.
    """
    return prompt

def model_output(docs,query):
    client=genai.Client(api_key='AIzaSyCE5x3HfAIFyl_ptspFZ23Y1iCkM1pYl_Y')

    temp_df=formatted_prompt(docs)
    # Generate the prompt
    prompt = dataframe_to_prompt(temp_df)

    # prompt = build_prompt_with_query(docs, query)

    response = client.models.generate_content(
        model="models/gemini-1.5-flash",  # use full model ID
        contents=prompt
    )

    # Convert DataFrame to markdown table
    df_markdown = temp_df.to_markdown(index=False)

    # Combine
    combined_output = f"### Extracted Table:\n\n{df_markdown}\n\n---\n\n### Synthesized Response:\n\n{response.text}"

    return combined_output

