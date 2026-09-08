from chatbot.entity_extractor import extract_entities
from chatbot.retrieval import find_direct_match, filter_projects, add_risk_columns
from chatbot.similar_projects import find_similar_past_projects
from chatbot.context_builder import build_context_block, build_similar_projects_block
from chatbot.gemini_client import call_gemini
 
 
def _with_similar_projects(context_block: str, top_row) -> str:
    """Appends real past comparable projects so root-cause explanations
    can cite precedent instead of reasoning in the abstract."""
    similar = find_similar_past_projects(top_row, top_n=3)
    similar_block = build_similar_projects_block(similar)
    return context_block + "\n\n" + similar_block
 
 
def answer_query(user_message: str, user_project_row: dict = None, history: list = None, top_n: int = 10) -> str:
    # 1. If user submitted a new project via the form, inject it directly!
    if user_project_row is not None:
        import pandas as pd
        df_proj = pd.DataFrame([user_project_row])
        df_proj = add_risk_columns(df_proj)
        context_block = build_context_block(df_proj, 1)
        context_block = _with_similar_projects(context_block, df_proj.iloc[0])
        return call_gemini(user_message, context_block, history=history)

    # 2. Try to find an exact project code or name
    direct_matches = find_direct_match(user_message, top_n=top_n)
    if not direct_matches.empty:
        direct_matches = add_risk_columns(direct_matches)
        context_block = build_context_block(direct_matches, len(direct_matches))
        context_block = _with_similar_projects(context_block, direct_matches.iloc[0])
        return call_gemini(user_message, context_block, history=history)
 
    # 3. Extract keywords (sector, state, etc.)
    entities = extract_entities(user_message)
    
    # Check if any specific filters/keywords were actually found
    has_filters = any(v for k, v in entities.items() if v)

    # 4. FOLLOW-UP DETECTION FIX
    # If no exact match and no keywords are found, it's a follow-up question (like "tell me more").
    # If we have chat history, we skip the search so we don't overwrite the memory with random projects.
    if not has_filters and history and len(history) > 0:
        context_block = "[NO NEW SEARCH PERFORMED. PLEASE REFER TO THE PROJECT DATA IN OUR PREVIOUS MESSAGES TO ANSWER THIS FOLLOW-UP QUESTION.]"
        return call_gemini(user_message, context_block, history=history)

    # 5. Standard fallback search
    matches, total_matches = filter_projects(entities, top_n=top_n)
    context_block = build_context_block(matches, total_matches)
 
    if not matches.empty:
        context_block = _with_similar_projects(context_block, matches.iloc[0])
 
    return call_gemini(user_message, context_block, history=history)
 
 
if __name__ == "__main__":
    print("PAIMANA chatbot -- type a question, or 'quit' to exit.\n")
    
    # 1. Create a memory list for this terminal session
    session_history = []
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        try:
            # 2. Pass the memory into answer_query
            answer = answer_query(user_input, history=session_history)
            
            print("\nBot:", answer, "\n")
            
            # 3. AFTER Gemini answers, save both messages to memory for the next turn
            session_history.append({"role": "user", "text": user_input})
            session_history.append({"role": "model", "text": answer})
            
        except Exception as e:
            print(f"\nBot: Sorry, something went wrong answering that -- {e}\n")