from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import random

# Initialize the bot connection to Telegram
app = ApplicationBuilder().token("7112507583:AAGIDFfC-NsKjdeX_T1uj0_nOdvlps1oBas").build()

# Global variables to store the poll and repetition counters
poll = None
repetitions = 0
current_repetition = 0
bot_points = 0
player_points = 0
player_previous_move = None

def tit_for_tat(player_choice):
    global bot_points, player_points, player_previous_move
    bots_choice = '1' if player_previous_move in [None, '1'] else '2'

    if player_choice == bots_choice and player_choice == '1':
        bot_points += 3
        player_points += 3
    elif player_choice != bots_choice and player_choice == '2':
        bot_points += 0
        player_points += 5
    elif player_choice == bots_choice and player_choice == '2':
        bot_points += 1
        player_points += 1
    elif player_choice != bots_choice and bots_choice == '2':
        bot_points += 5
        player_points += 0

    response = f"Your score is {player_points}\nBot's score is {bot_points}"
    player_previous_move = player_choice
    return response

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""-------------------WE ARE ABOUT TO START-------------------""")
    intervals = ["8-15", "18-25", "28-35", "38-45"]
    global poll
    poll = await context.bot.send_poll(
        update.effective_chat.id,
        "Choose the interval of moves, and type /rules to get familiar with rules!",
        intervals,
        is_anonymous=False,
        allows_multiple_answers=False,
        open_period=60  # The poll will be open for 60 seconds
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "RULEEEEEEEEEEEEZ\n"
        "You are playing with bot, and in your first move you can either cooperate or cheat your bot opponent\n"
        "---If you and your opponent both choose to cooperate, you both gain 3 points\n"
        "---If one of you choose to cheat, that player, who cheats, gains 5 points and second player gains nothing\n"
        "--- If both players choose to cheat both players gain 1 point"
    )

async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global repetitions, current_repetition

    completed_poll = await context.bot.stop_poll(poll.chat_id, poll.message_id)
    chosen_interval = None

    for option in completed_poll.options:
        if option.voter_count > 0:
            chosen_interval = option.text
            break

    if chosen_interval:
        await update.message.reply_text(f"The chosen interval is {chosen_interval}. We now start playing.")
        lower_bound, upper_bound = map(int, chosen_interval.split('-'))
        repetitions = random.randint(lower_bound, upper_bound)
        current_repetition = 0

        await send_inline_keyboard(update.effective_chat.id, context)  # Start the repeated interaction

    else:
        await update.message.reply_text("No interval was chosen.")

async def send_inline_keyboard(chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    global current_repetition

    if current_repetition < repetitions:
        keyboard = [
            [
                InlineKeyboardButton("Cooperate?", callback_data='1'),
                InlineKeyboardButton("Cheat?", callback_data='2')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"-------- To cooperate or not to cooperate? ({current_repetition+1}/{repetitions}) --------",
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Game over!"
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_repetition

    query = update.callback_query
    await query.answer()

    player_choice = query.data
    response = tit_for_tat(player_choice)
    
    await query.edit_message_text(text=response)

    # Increment the repetition counter and send the next inline keyboard
    current_repetition += 1
    await send_inline_keyboard(query.message.chat_id, context)

async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type /matches to receive tournament bracket")

async def debil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I hear: Andrey is gay")

# Connect chat commands with their functions
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CommandHandler("rules", rules))
app.add_handler(CommandHandler("debil", debil))
app.add_handler(CallbackQueryHandler(button))

# Start the bot
app.run_polling()
