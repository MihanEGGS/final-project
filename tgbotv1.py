from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests, random,json
# izveido bota pieslēgumu Telegram
app = ApplicationBuilder().token("7112507583:AAGIDFfC-NsKjdeX_T1uj0_nOdvlps1oBas").build()
# offers group members to join a game, after what person, who started the bot, chooses "Enough!"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_joined_list
    people_joined_list = []
    people_joined_list.append(str(update.effective_user.first_name))
    await update.message.reply_text("""YOU STARTED THE GREAT GAME
------------------------------------
THE GAME THEORY
------------------------------------
type /join to join                                 
                                    """)

# function for players to join the game
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pic_girl = open("fuck.png", 'rb')
    pic_waiting_menu = open("gamepic.png", 'rb')
    global people_joined_list
    to_be_printed = ""
  ###  if str(update.effective_user.username) in people_joined_list:
    ###await update.message.reply_photo(pic_girl,"-------------------YOU ALREADY IN-------------------")
   ### else:
    people_joined_list.append(str(update.effective_user.first_name))
    for i in range(len(people_joined_list)):
        to_be_printed = to_be_printed + str(i+1)+"."+ " " + (str(people_joined_list[i])) + '\n'
    await update.message.reply_photo(pic_waiting_menu, to_be_printed) 
    pic_girl.close()
    pic_waiting_menu.close()


# starts the game itself, sending upcoming matches to each player privately and randomly generating them. All
async def enough(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_joined_list
    pic_girl = open("fuck.png", 'rb')
    if str(update.effective_user.first_name) == people_joined_list[0]:# checks, if the user typing enough is correct
        if len(people_joined_list) % 2 != 0:
            await update.message.reply_text("-------------------ONE PLAYER MORE OR LESS, PLEASE-------------------")
        else:
            await update.message.reply_text("""-------------------WE ARE ABOUT TO START-------------------""")
            intervals = ["8-15", "18-25", "28-35", "38-45"]
            global poll
            poll = await context.bot.send_poll(
                update.effective_chat.id,
                "Choose the interval of moves",
                intervals,
                is_anonymous=False,
                allows_multiple_answers=False,
                open_period = -1
            )
    else:
        await update.message.reply_photo(pic_girl,"-------------------ACCESS DENIED-------------------")
    pic_girl.close()
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parameters = []
    completed_poll = await poll.stop_poll()
    print(completed_poll.to_dict())
    for option in completed_poll.options:
        print(option.text, option.voter_count)
    await update.message.reply_text('https://t.me/shrikingkirill_bot'+'\n'+"Type /matches to recieve tournament bracket")
async def matches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people_joined_chat_ids  = []
    people_joined_chat_ids.append
    global people_joined_list
    print(people_joined_list)
    to_be_printed = ""
    people_joined_tossed_list = people_joined_list
    for i in range(3):
        try:
            random_player_1 = random.choice(people_joined_tossed_list)
            people_joined_tossed_list.remove(random_player_1)
            random_player_2 = random.choice(people_joined_tossed_list)
            people_joined_tossed_list.remove(random_player_2)
        except:
            break
        to_be_printed = to_be_printed + '\n'+ str(i+1)+". " + random_player_1 +" vs " +  random_player_2
    await update.message.reply_text("Your tournament bracket: "+'\n'+to_be_printed)
    
async def debil(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I hear: Andrey is gay")
# savieno čata komandu ar funkciju
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("enough", enough))
app.add_handler(CommandHandler("vote", vote))
app.add_handler(CommandHandler("matches", matches))
app.add_handler(CommandHandler("debil", debil))
# sāk bota darbību
app.run_polling()