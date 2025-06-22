# Hallucination Detection & Guardrails System

## Overview

This project implements a simple system to detect hallucinations in language model responses by verifying answers against a knowledge base (KB). The system consists of three main components:

1. **Knowledge Base (`kb.json`)**: Contains 10 factual question-answer pairs.
2. **Question Asker (`ask_model.py`)**: Simulates asking a language model questions and getting responses.
3. **Validator (`validator.py`)**: Checks if the model's answers match what's in the knowledge base.

## How It Works

### Knowledge Base

The knowledge base is a JSON file containing 10 factual Q-A pairs. Each pair consists of a question and its correct answer.

### Question Asking Process

The system asks the model:
- All 10 questions from the knowledge base
- 5 additional unseen/edge-case questions

For simulation purposes, the model has:
- 70% chance of answering correctly for in-KB questions on first try
- Will always give a simulated answer for out-of-KB questions

### Validation Process

The validator uses basic string matching to check answers:

- If the question is in the KB and the answer matches → "VALID"
- If the question is in the KB but the answer doesn't match → "RETRY: answer differs from KB"
- If the question is not in the KB → "RETRY: out-of-domain"

When a "RETRY" result is received, the system asks the model again.

### Logging

All interactions are logged in `run.log`, including:
- Questions asked
- Model's first answers
- Validation results
- Second attempts (if needed)
- Final validation results

## Running the System

To run the system:

```bash
python ask_model.py
```

This will generate a `run.log` file with the results of the Q&A session.

## Limitations

1. The validator uses simple string matching, which might not catch semantically equivalent answers.
2. The model simulation is simplified and doesn't represent the nuanced behavior of real language models.
3. There's no handling of partially correct answers.

## Future Improvements

1. Implement semantic similarity for answer validation instead of exact string matching.
2. Add support for multiple correct answers per question.
3. Implement a more sophisticated retry strategy based on the type of error.
4. Connect to a real language model API instead of simulation.