RAG_PROMPT = (
    'Context information is below.'
    '---------------------\n'
    '{context_str}\n'
    '---------------------\n'
    'This is a portion of an audio transcript query from a client asking about Tiktok Ads.\n'
    'Given the context information and not prior knowledge, reply the transcript.\n'
    'Keep the response SIMPLE and below 40 words.\n'
    'Transcript: {query_str}\n'
    'Answer: '
)

QUESTION_PROMPT = (
    'TRANSCRIPT: {transcript}\n'
    'This is a portion of an audio transcript query from a client asking about Tiktok Business, and how to use their advertise on their platform:\n'
    'Generate a question in a short sentence using the context in TRANSCRIPT and keep the main key words in this question.\n'
    'Make the query SIMPLE.'
)
