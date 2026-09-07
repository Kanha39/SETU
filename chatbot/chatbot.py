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
 
 
def answer_query(user_message: str, top_n: int = 10) -> str:
    direct_matches = find_direct_match(user_message, top_n=top_n)
 
    if not direct_matches.empty:
        direct_matches = add_risk_columns(direct_matches)
        context_block = build_context_block(direct_matches, len(direct_matches))
        context_block = _with_similar_projects(context_block, direct_matches.iloc[0])
        return call_gemini(user_message, context_block)
 
    entities = extract_entities(user_message)
    matches, total_matches = filter_projects(entities, top_n=top_n)
    context_block = build_context_block(matches, total_matches)
 
    if not matches.empty:
        context_block = _with_similar_projects(context_block, matches.iloc[0])
 
    return call_gemini(user_message, context_block)
 
 
if __name__ == "__main__":
    print("PAIMANA chatbot -- type a question, or 'quit' to exit.\n")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue
        try:
            print("\nBot:", answer_query(user_input), "\n")
        except Exception as e:
            print(f"\nBot: Sorry, something went wrong answering that -- {e}\n")