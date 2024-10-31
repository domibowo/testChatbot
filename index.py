import os
from chatterbot import ChatBot, comparisons, response_selection
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import asyncio
import websockets
import websockets.connection
import websockets.exceptions
from websockets.server import serve
from websockets.sync import client

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

HOST = os.getenv("WEBSOCKET_HOST", "localhost")
PORT = int(os.getenv("WEBSOCKET_PORT", 6605))

corpus_trainer = ChatterBotCorpusTrainer(domThought)
list_trainer = ListTrainer(domThought)

def train_bot(user_question, user_answer):
    corpus_trainer.train(
        'chatterbot.corpus.indonesia'
    )
    conversation = [user_question, user_answer]
    list_trainer.train(
        conversation
    )
    return f"Saya telah berlatih: {user_question} -> {user_answer}"

need_revision = False
question_need_answer = ""
    
def get_response(input_text):
    print("text", input_text)
    global need_revision, question_need_answer
    
    if need_revision is False:
        response = domThought.get_response(input_text)
        if response.confidence > 0.7:
            return response
        else:
            need_revision = True
            question_need_answer = input_text
            return "Saya tidak yakin bagaimana menjawabnya. Tolong bantu saya! \nApa yang seharusnya Bot katakan?"
    else:
        train_bot(question_need_answer, input_text)
        need_revision = False
        question_need_answer = ""
        return 'Terima kasih telah melatih saya kata-kata baru ini!'

async def handler(websocket, path):
    try :
        await websocket.send("Bot: Anda terhubung dengan Tedy Chatbot. Ada yang bisa dibantu?")
        while True:
            data = await websocket.recv()
            bot_response = get_response(str(data))
            await websocket.send(str(bot_response))
    except websockets.exceptions.ConnectionClosedError:
        print("Connection closed")    
    
start_server = serve(handler, HOST, PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()