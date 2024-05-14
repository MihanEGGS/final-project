dictt = {'1': 100, '2': 1292, '3': 88}  
  
# Getting the key with maximum value  
Key_max = max(zip(dictt.values(), dictt.keys()))[1]  
print("The key with the maximum value is: ", Key_max)  
async def a(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people_voted_a = []
    global people_voted
    people_voted_a.append(str(update.effective_user.username))
    people_voted ={}
    people_voted["8-15"] = int(len(people_voted_a))
async def b(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_voted
    people_voted ={}
    people_voted_b = []
    people_voted_b.append(str(update.effective_user.username))
    people_voted["18-25"] = int(len(people_voted_b))
async def c(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_voted 
    people_voted ={}
    people_voted_c = []
    people_voted_c.append(str(update.effective_user.username))
    people_voted["28-35"] = int(len(people_voted_c))
async def d(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_voted 
    people_voted ={}
    people_voted_d = []
    people_voted_d.append(str(update.effective_user.username))
    people_voted["38-45"] = int(len(people_voted_d))
async def vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global people_voted 
    Value_max = max(zip(people_voted.values(), people_voted.keys()))[1]
    await update.message.reply_text("The chosen interval is "+ str(Value_max)+'\n'+"Type /begin to play with your first oponent") 