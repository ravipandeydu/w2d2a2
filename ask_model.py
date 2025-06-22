import json
import os
import random
import time

# Function to load the knowledge base
def load_knowledge_base(kb_path):
    with open(kb_path, 'r') as f:
        kb = json.load(f)
    return kb

# Function to simulate asking a model a question
def ask_model(question, retry=False):
    """
    Simulates asking a language model a question.
    In a real implementation, this would call an actual LLM API.
    
    For this simulation:
    - If the question is in our KB, we'll randomly decide to give correct or incorrect answer
    - If it's not in KB or on retry, we'll generate a plausible but potentially incorrect answer
    """
    # Load knowledge base
    kb = load_knowledge_base('kb.json')
    kb_questions = {q['question']: q['answer'] for q in kb['questions']}
    
    # Check if question is in knowledge base
    if question in kb_questions:
        # On first try, 70% chance of correct answer, 30% chance of hallucination
        if not retry and random.random() < 0.7:
            return kb_questions[question]
        else:
            # Simulate a hallucinated answer that's different from the correct one
            return f"Simulated incorrect answer for: {question}"
    else:
        # For questions not in KB, always generate a simulated answer
        return f"Simulated answer for out-of-domain question: {question}"

# Function to run the Q&A process
def run_qa_process():
    # Load knowledge base
    kb = load_knowledge_base('kb.json')
    kb_questions = [q['question'] for q in kb['questions']]
    
    # Create 5 additional unseen questions
    unseen_questions = [
        "What is the speed of light?",
        "Who is the current president of Brazil?",
        "What is the capital of Australia?",
        "How many chromosomes do humans have?",
        "What year was the internet invented?"
    ]
    
    # Combine all questions
    all_questions = kb_questions + unseen_questions
    random.shuffle(all_questions)
    
    # Create results directory if it doesn't exist
    if not os.path.exists('results'):
        os.makedirs('results')
    
    # Open log file
    with open('run.log', 'w') as log_file:
        log_file.write("=== Q&A Session Log ===\n\n")
        
        # Process each question
        for i, question in enumerate(all_questions):
            log_file.write(f"Question {i+1}: {question}\n")
            
            # First attempt
            first_answer = ask_model(question)
            log_file.write(f"First answer: {first_answer}\n")
            
            # Validate the answer
            from validator import validate_answer
            validation_result = validate_answer(question, first_answer)
            log_file.write(f"Validation: {validation_result}\n")
            
            # If validation suggests retry, make a second attempt
            if validation_result.startswith("RETRY"):
                log_file.write("Making second attempt...\n")
                second_answer = ask_model(question, retry=True)
                log_file.write(f"Second answer: {second_answer}\n")
                
                # Validate the second answer
                second_validation = validate_answer(question, second_answer)
                log_file.write(f"Second validation: {second_validation}\n")
            
            log_file.write("\n---\n\n")

# Run the Q&A process if this script is executed directly
if __name__ == "__main__":
    run_qa_process()
    print("Q&A process completed. Check run.log for results.")