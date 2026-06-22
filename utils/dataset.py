"""Data schema and synthetic dataset helpers for CircleMatch."""

from .claude import add_user_message, chat


def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing a task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task"
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code.

Please generate 3 objects.
"""

    messages = []
    add_user_message(messages, prompt)
    response = chat(messages, system="You are a helpful assistant. Answer with valid JSON only.")
    return response
