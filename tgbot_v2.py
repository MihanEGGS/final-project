from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, Updater, CallbackContext, BaseHandler
import requests, random, json

# izveido bota pieslēgumu Telegram
bot_points = 0
player_points = 0
bots_choice = '1'
player_previous_choice = None
app = ApplicationBuilder().token("7112507583:AAGIDFfC-NsKjdeX_T1uj0_nOdvlps1oBas").build()

# Tit-for-tat strategy
def tit_for_tat(player_choice, response):
    global bot_points, player_points, bots_choice, player_previous_choice, intervals, repetitions

    bots_choice = '1' if player_previous_choice in [None, '1'] else '2'  # If player's previous choice is '1' or None, bot cooperates, else bot cheats

    if player_choice == bots_choice and player_choice == '1':  # Both cooperate
        bot_points += 3
        player_points += 3
    elif player_choice != bots_choice and bots_choice == '1':  # Player cheats, bot cooperates
        bot_points += 0
        player_points += 5
    elif player_choice == bots_choice and player_choice == '2':  # Both cheat
        bot_points += 1
        player_points += 1
    elif player_choice != bots_choice and bots_choice == '2':  # Player cooperates, bot cheats
        bot_points += 5
        player_points += 0

    response = "Your score is " + str(player_points) + '\n' + "Bot's score is " + str(bot_points)
    player_previous_choice = player_choice
    return response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bot_points, player_points
    bot_points = 0
    player_points = 0
    await update.message.reply_text("""-------------------WE ARE ABOUT TO START-------------------""")
    intervals = ["8-15", "18-25", "28-35", "38-45"]
    global poll
    poll = await context.bot.send_poll(
        update.effective_chat.id,
        "Choose the interval of moves, and type /rules to get familiar with rules!",
        intervals,
        is_anonymous=False,
        allows_multiple_answers=False,
        open_period=-1
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("RULEEEEEEEEEEEEZ" + '\n' + "You are playing with bot, and in your first move you can either cooperate or cheat your bot opponent"
                                    + '\n' + "---If you and your opponent both choose to cooperate, you both gain 3 points"
                                    + '\n' + "---If one of you choose to cheat, that player, who cheats, gains 5 points and second player gains nothing "
                                    + '\n' + "--- If both players choose to cheat both players gain 1 point ")

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        global intervals, repetitions
        repetitions = 0
        completed_poll = await poll.stop_poll()
        print(completed_poll.to_dict())
        for option in completed_poll.options:  # Loop through poll options
            print(option.text, option.voter_count)
            if option.voter_count == 1:  # If option was chosen
                await update.message.reply_text("The chosen interval is " + option.text + " We now start playing ")
                if option.text == "8-15":  # Set intervals based on choice
                    intervals = random.randint(8, 15)
                elif option.text == "18-25":
                    intervals = random.randint(18, 25)
                elif option.text == "28-35":
                    intervals = random.randint(28, 35)
                elif option.text == "38-45":
                    intervals = random.randint(38, 45)
        await game(update.effective_chat.id, context)
    except:
        await update.message.reply_text("Please, to start the game type /start")

async def game(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    global repetitions, intervals
    if repetitions < intervals:  # Check if repetitions are less than intervals
        keyboard = [
            [
                InlineKeyboardButton("Cooperate?", callback_data='1'),
                InlineKeyboardButton("Cheat?", callback_data='2')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text="-------- To cooperate or not to cooperate? --------",
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Game over!"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global repetitions
    query = update.callback_query
    await query.answer()
    response = ""
    player_choice = query.data
    response = tit_for_tat(player_choice, response)
    await query.edit_message_text(text=response)
    repetitions += 1
    await game(query.message.chat_id, context)

async def debil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I hear:  "+update.effective_user.first_name+" sorry, tas sekretfunkcija bija najebalova  :(")

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("game", game))
app.add_handler(CommandHandler("debil", debil))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
