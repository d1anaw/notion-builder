
from . import api_blueprint
from app.utils.helper_functions import chunk_text, build_prompt
from app.services import openai_service, pinecone_service, scraping_service
from flask import request, jsonify


PINECONE_INDEX_NAME = 'notion-builder-index'

@api_blueprint.route('/embed-and-store', methods=['POST'])
def embed_and_store():
    # call scraping
    url = request.json['url']
    url_text = scraping_service.scrape_website(url)
    chunks = chunk_text(url_text)
    pinecone_service.embed_chunks_and_upload(chunks, PINECONE_INDEX_NAME)
    response_json = {
            "message": "Chunks embedded and uploaded successfully"
            }
    return jsonify(response_json)

    # chunk
    # embed
    # upload to pinecone


@api_blueprint.route('/handle-query', methods=['POST'])
def handle_query():
    question = request.json['question']
    context_chunks = pinecone_service.get_most_similar_chunks(question, PINECONE_INDEX_NAME)
    prompt = build_prompt(question, context_chunks)
    answer = openai_service.get_llm_answer(prompt)
    return jsonify({"question":question, "answer":answer})


