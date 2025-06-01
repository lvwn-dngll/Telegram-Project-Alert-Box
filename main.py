import os
import command_handlers as telegram_commands
import threading, time, requests
import paho.mqtt.client as mqtt
from flask import Flask
from typing import Final
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

#loads the .env file
load_dotenv()

#load the TOKEN file
TOKEN : Final= os.getenv("TOKEN")

#mqtt broker variables
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic_message = "Telegram_Alertbox_Project/message"
mqtt_topic_background = "Telegram_Alertbox_Project/background"

#mqtt initialization
mqtt_client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
mqtt_client.connect(mqtt_broker, mqtt_port, 60)
mqtt_client.loop_start()

#global variables to be sent to the box:
CURRENT_MESSAGE = "sample_text"
CURRENT_BACKGROUND = "background_1"

#Self ping for the bot to keep itself alive
ONRENDER_URL = 'https://telegram-project-alert-box.onrender.com'

#creates Flask app
app_flask = Flask(__name__)
@app_flask.route('/')
def home():
    return "callback_ping", 200

#Starts flask app and its functions
def keep_alive():
    while True:
        try:
            #keep alive request
            requests.get(ONRENDER_URL)
        except Exception as e:
            print(e)
        #for 5 mins sleep:
        time.sleep(300)

def run_flask():
    app_flask.run(host = "0.0.0.0", port = 10000)

#Starts the app 
if __name__ == "__main__":
    threading.Thread(target = run_flask, daemon = True).start()
    threading.Thread(target = keep_alive, daemon = True).start()

    app = Application.builder().token(TOKEN).build()

    #define conversation handlers
    send_message_handler = ConversationHandler(
        entry_points = [CommandHandler("send_message", telegram_commands.send_message)],
        states = {
            telegram_commands.ASK_VARIABLE : [MessageHandler(filters.TEXT & ~filters.COMMAND, telegram_commands.send_message_phase_2)]
        },
        fallbacks = [CommandHandler("cancel", telegram_commands.cancel)]
    )

    #add app command handlers
    app.add_handler(send_message_handler)
    app.add_handler(CommandHandler("set_background", telegram_commands.set_background))
    app.add_handler(CallbackQueryHandler(telegram_commands.set_background_phase_2))
    app.add_handler(CommandHandler("show_message", telegram_commands.show_message))
    app.add_handler(CommandHandler("show_background", telegram_commands.show_background))
    #update the app by polling
    app.run_polling()