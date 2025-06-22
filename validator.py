import json

def load_knowledge_base(kb_path='kb.json'):
    """
    Load the knowledge base from a JSON file.
    
    Args:
        kb_path (str): Path to the knowledge base JSON file
        
    Returns:
        dict: Dictionary containing questions and answers
    """
    with open(kb_path, 'r') as f:
        kb = json.load(f)
    return kb

def validate_answer(question, answer):
    """
    Validate if the answer matches what's in the knowledge base.
    
    Args:
        question (str): The question being asked
        answer (str): The answer provided by the model
        
    Returns:
        str: Validation result
            - "VALID" if the answer matches the KB
            - "RETRY: answer differs from KB" if in KB but answer doesn't match
            - "RETRY: out-of-domain" if question not in KB
    """
    # Load knowledge base
    kb = load_knowledge_base()
    
    # Create a dictionary mapping questions to answers for easy lookup
    kb_qa_pairs = {q['question']: q['answer'] for q in kb['questions']}
    
    # Check if the question is in our knowledge base
    if question in kb_qa_pairs:
        # Question is in KB, check if answer matches
        correct_answer = kb_qa_pairs[question]
        
        # Simple string matching (case-insensitive)
        if answer.lower().strip() == correct_answer.lower().strip():
            return "VALID"
        else:
            return f"RETRY: answer differs from KB (expected: {correct_answer})"
    else:
        # Question is not in our knowledge base
        return "RETRY: out-of-domain"

# Example usage if run directly
if __name__ == "__main__":
    # Test with a question from KB
    test_question = "What is the capital of France?"
    test_answer_correct = "Paris"
    test_answer_wrong = "London"
    
    print(f"Question: {test_question}")
    print(f"Correct answer validation: {validate_answer(test_question, test_answer_correct)}")
    print(f"Wrong answer validation: {validate_answer(test_question, test_answer_wrong)}")
    
    # Test with a question not in KB
    test_question_unknown = "What is the population of Tokyo?"
    test_answer_unknown = "Approximately 14 million"
    
    print(f"\nQuestion: {test_question_unknown}")
    print(f"Unknown question validation: {validate_answer(test_question_unknown, test_answer_unknown)}")