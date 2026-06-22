from dotenv import load_dotenv

load_dotenv()

# Claude model selection and recommended task roles.
#
# Haiku 4.5:
# - Best for fast, low-cost, high-volume work
# - Good for classification, tagging, lightweight extraction, first-pass summarization,
#   fast chat UX, cheap sub-agent work, and parallel worker patterns.
#
# Sonnet 4.5 / 4.6:
# - Best as the default production workhorse for most product features
# - Good for user-facing answers, moderate reasoning, coding, RAG synthesis,
#   and polished final outputs where quality still matters.
#
# Opus 4.8:
# - Best for hard reasoning, long multi-step agent tasks, and high-stakes outputs
# - Use only for final review, deep critique, or premium decision-making.
#
# Recommended stack for this project:
# - Haiku = cheap structured subtasks and worker-level extraction
# - Sonnet = main reasoning / final user-facing content
# - Opus = optional premium reviewer / judge

CLAUDE_MODEL_HAIKU = "claude-haiku-4-5"
CLAUDE_MODEL_SONNET = "claude-sonnet-4-6"
CLAUDE_MODEL_OPUS = "claude-opus-4.8"
CLAUDE_DEFAULT_MODEL = CLAUDE_MODEL_SONNET

CLAUDE_DEFAULT_MAX_TOKENS = 1000
CLAUDE_DEFAULT_TEMPERATURE = 1.0
