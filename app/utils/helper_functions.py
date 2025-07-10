PROMPT_LIMIT = 3750

def chunk_text(text, chunk_size=200):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def build_prompt(query, context_chunks):
    prompt_start = """
                    Please answer the question based on the context below.
                    If you don't know how to answer the question based on
                    the given context, please ask the user follow up questions
                    that are necessary or helpful for you to properly answer
                    the questions.
                    Context: \n"""
    prompt_end = f"\n\nQuestion: {query} \n Answer:"
    prompt = ""
    for i in range(1, len(context_chunks)):
        if len("\n\n---\n\n".join(context_chunks[:i])) >= PROMPT_LIMIT:
            prompt = (
            prompt_start +
            "\n\n---\n\n".join(context_chunks[:i-1]) +
            prompt_end
            )
            break
        elif i == len(context_chunks)-1:
            prompt = (
            prompt_start +
            "\n\n---\n\n".join(context_chunks) +
            prompt_end
            )
    return prompt
