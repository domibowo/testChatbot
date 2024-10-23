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
    corpus_trainer = ChatterBotCorpusTrainer(domThought)
    corpus_trainer.train(
        'chatterbot.corpus.indonesia'
    )
    list_trainer = ListTrainer(domThought)
    conversation = [user_question, user_answer]
    list_trainer.train(
        conversation
    )
    return f"Saya telah berlatih: {user_question} -> {user_answer}"
    
def get_response(input_text):
    
    response = domThought.get_response(input_text)
    if response.confidence > 0.7:
        return response
        
    print("Bot: Saya tidak yakin bagaimana menjawabnya. Tolong bantu saya!")
    user_answer = input('Apa yang seharusnya Bot katakan? ')
    train_bot(input_text, user_answer)
    return 'Terima kasih telah melatih saya kata-kata baru ini!'
        
    
        
while True:
    user_input = input("Anda: ")
    if user_input.lower() == 'exit':
        break
    
    bot_response = get_response(user_input)
    print(f"Bot: {bot_response}")
    