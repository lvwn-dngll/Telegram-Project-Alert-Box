import os
import command_handlers as telegram_commands
import paho.mqtt.client as mqtt
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

#Starts the app 

if __name__ == "__main__":
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