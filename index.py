from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

domThought = ChatBot(
    'domThought',
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": comparisons.LevenshteinDistance,
            "response_selection_method": response_selection.get_first_response
        }
    ],
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
)

def train_bot(user_question, user_answer):
    trainer = ListTrainer(domThought)
    conversation = [user_question, user_answer]
    trainer.train(conversation)
    print(f"Trained the bot with new data: {user_question} -> {user_answer}")

trainer = ChatterBotCorpusTrainer(domThought)
trainer.train(
    'chatterbot.corpus.indonesia'
)

response = domThought.get_response(input("Enter text: "))
print(response)