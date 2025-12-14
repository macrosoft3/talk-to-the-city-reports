import concurrent.futures
import json
import os

import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from tqdm import tqdm
from utils import messages, update_progress


class Comment(BaseModel):
    # comment_id: str = Field(..., description="unique identifier for the comment")
    comment_body: str = Field(..., description="main content of the comment")
    # agree: int = Field(..., description="number of upvotes")
    # disagree: int = Field(..., description="number of downvotes")
    # video: str = Field(..., description="link to a video")
    # interview: str = Field(..., description="name of interviewee")
    # timestamp: str = Field(..., description="timestamp in the video")


class Comments(BaseModel):
    comments: list[Comment] = Field(..., description="list of comments")


def conversion(config):
    dataset = config["output_dir"]
    path = f"inputs/{config['input']}.csv"
    docs = read_pdf(f"inputs/{config['input']}.pdf")

    if os.path.splitext(f"inputs/{config['input']}.pdf")[1] == ".csv":
        return

    model = config["conversion"]["model"]
    prompt = config["conversion"]["prompt"]
    workers = config["conversion"]["workers"]
    limit = config["conversion"]["limit"]

    comment_id = 0
    docs = docs[:limit]
    results = pd.DataFrame()
    update_progress(config, total=len(docs))
    for i in tqdm(range(0, len(docs), workers)):
        batch = docs[i : i + workers]
        batch_results = extract_batch(batch, prompt, model, workers)
        for extracted_comments in batch_results:
            for comment in extracted_comments:
                new_row = {
                    "comment-id": int(comment_id),
                    "comment-body": comment,
                }
                results = pd.concat(
                    [results, pd.DataFrame([new_row])], ignore_index=True
                )
                comment_id += 1
        update_progress(config, incr=len(batch))
    results.to_csv(path, index=False)


def read_pdf(path):
    loader = PyPDFLoader(path)
    return loader.load()


def extract_batch(batch, prompt, model, workers):
    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        for input in batch:
            futures.append(
                executor.submit(extract_comments, input.page_content, prompt, model)
            )
        concurrent.futures.wait(futures)
        return [future.result() for future in futures]


def extract_comments(input, prompt, model, retries=3):
    llm = ChatOpenAI(model_name=model, temperature=0.0)
    llm_with_structure = llm.with_structured_output(Comments)
    response = llm_with_structure.invoke(messages(prompt, input))
    try:
        obj = response.comments
        # LLM sometimes returns valid JSON string
        if isinstance(obj, str):
            obj = [obj]
        items = [a.comment_body.strip() for a in obj]
        items = filter(None, items)  # omit empty strings
        return list(items)
    except Exception as e:
        print("error:", e)
        print("Input was:", input)
        print("Response was:", response)
        if retries > 0:
            print("Retrying...")
            return extract_comments(input, prompt, model, retries - 1)
        else:
            print("Silently giving up on trying to generate valid list.")
            return []
