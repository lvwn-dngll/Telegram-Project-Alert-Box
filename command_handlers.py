import main as m

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

ASK_VARIABLE = 1

#send message command handlers
async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #conversation:
    await update.message.reply_text("Please enter the message to be sent (type /cancel to cancel):")
    return ASK_VARIABLE

async def send_message_phase_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #updating the text:
    response = update.message.text
    m.CURRENT_MESSAGE = response

    #send to third party integrated application here
    m.mqtt_client.publish(m.mqtt_topic_message, m.CURRENT_MESSAGE, retain = True)

    #respond to the user succesfull (add error here later).
    await update.message.reply_text("The message was set to: \"" + m.CURRENT_MESSAGE + "\".")

    #end the conversation
    return ConversationHandler.END

#Sent background command handlers

#create dictionary:
background = {
    "Eating" : "background_1",
    "Sleeping" : "background_2",
    "Studying" : "background_3",
    "Playing" : "background_4",
    "Travelling" : "background_5",
    "Watching" : "background_6",
    "Love" : "background_7",
    "Sad" : "background_8",
    "Hungry" : "background_9",
    "Happy" : "background_10",
}
async def set_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
   #create custom keyboard:
   keyboard = [
        [InlineKeyboardButton("Eating", callback_data = "Eating")],
        [InlineKeyboardButton("Sleeping", callback_data = "Sleeping")],
        [InlineKeyboardButton("Studying", callback_data = "Studying")],
        [InlineKeyboardButton("Playing", callback_data = "Playing")],
        [InlineKeyboardButton("Travelling", callback_data = "Travelling")],
        [InlineKeyboardButton("Watching", callback_data = "Watching")],
        [InlineKeyboardButton("Love", callback_data = "Love")],
        [InlineKeyboardButton("Sad", callback_data = "Sad")],
        [InlineKeyboardButton("Hungry", callback_data = "Hungry")],
        [InlineKeyboardButton("Happy", callback_data = "Happy")],
        [InlineKeyboardButton("Cancel", callback_data = "cancel")]
   ]

   reply_markup = InlineKeyboardMarkup(keyboard)
   await update.message.reply_text("Please Select the Background: ", reply_markup = reply_markup)

async def set_background_phase_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.callback_query
    await response.answer() 

    if response.data == "cancel":
        await response.edit_message_text(text = "Operation canceled.")

    else:
        m.CURRENT_BACKGROUND = response.data

        #add third party background change here
        m.mqtt_client.publish(m.mqtt_topic_background, background[m.CURRENT_BACKGROUND], retain = True)

        #respond if done successfuly
        currentBackground = m.CURRENT_BACKGROUND
        
        await response.edit_message_text(text = "The background changed to \"" + currentBackground + "\".")

#Cancel Operation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation canceled.")
    return ConversationHandler.END

#Show current data handlers:
async def show_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Current message set: \"" + m.CURRENT_MESSAGE + "\".")

async def show_background(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentBackground = m.CURRENT_BACKGROUND
    await update.message.reply_text("Current background set: \"" + currentBackground + "\".")