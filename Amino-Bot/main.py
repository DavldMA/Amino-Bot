from pymino import Bot
from pymino.ext import *
from datetime import datetime
from commands import *
from typing import List
from gtts import gTTS
from unidecode import unidecode
import random
import time
import re





################################## Bot Setup ##################################

medieval = "XXXXXXXX" #com id


chatOffId = "id"
logsChatId = "id"
reportsChatId = "id"
suggestionChatId = "id"
deletedMessagesChatId = "id"


chatModerators = {}
commands = ["help", "ping", "horoscope", "coinflip", "fortune", "rps", "speak", "say", "8ball", "love", "gay", "roll", "createrank", "rank", "leaderboard", "background", "download", "suggest", "report", "slap", "punch", "kiss", "hug", "patpat", "lick"]
coHostCommands = ["kick", "purge"]
admCommands = ["joinchat", "getuser", "viewonly", "fetchstaff", "chatid", "inviteall", "info", "raffle", "sendmessage", "here", "joinall", "getbg","resetallranks"]
limitedTimeCommands = []


bot = Bot(command_prefix="!", community_id=medieval, online_status=True, intents=True)
bot.run("gmail", "password", device_id="deviceid")

@bot.on_ready()
def ready():
    print(f"{bot.profile.username} has logged in!")


def moderator_only(func):
    try:
        def wrapper(ctx: Context, message: str) -> None:
            if ctx.author.userId not in staff:
                return ctx.reply("[ci]Não tem permissão para executar este comando.")
            func(ctx, message)
        return wrapper
    except:
        return None



def getChatMods(chat_id: str):
    try:
        global chatModerators
        if chat_id not in chatModerators:
            chatModerators[chat_id] = bot.community.fetch_chat_mods(chatId=chat_id)
        return list(chatModerators[chat_id]) + list(staff)
    except:
        return None



def getStaff(leader_locked: bool=False) -> None:
    try:
        global staff
        leaders = bot.community.fetch_users(userType="leaders").userId
        if leader_locked:
            staff = set(leaders)
        else:
            curators = bot.community.fetch_users(userType="curators").userId
            staff = set(leaders + curators)
    except Exception as e:
        print(f"Error while fetching staff. {e}")
        getStaff(leader_locked)





################################## Basic Commands ##################################

@bot.command(name="help", description="Mostra os comandos do bot.", aliases=["Help", "HELP", "comandos", "h"], usage="!help")
def helpCommand(ctx: Context, message: str):
    try:
        try:
            if bot.command_exists(message):
                commandNow = bot.fetch_command(message)
                text = f"[bc]─ㅤ{commandNow.name}ㅤ──\n[cb]Detalhes do Comando\n[cb]___________________________\n[cb]꒷ ꒦ ꒷ 𓏸⠀⠀.𖣔.⠀⠀𓏸 ꒷ ꒦ ꒷"
                text += f"\n╰► Nome: {commandNow.name}"
                text += f"\n╰► Descrição: {commandNow.description}"
                text += f"\n╰► Uso: {commandNow.usage}"
                text += f"\n╰► Alternativas: !{' !'.join(commandNow.aliases)}"
                return ctx.send(text)
            
            pageNumber = int(message)
        except ValueError:
            pageNumber = 1
            message = 1

        adminCommandsList = [bot.fetch_command(c).name for c in admCommands]
        coHostCommandsList = [bot.fetch_command(c).name for c in coHostCommands]
        memberCommandsList = [bot.fetch_command(c).name for c in commands] 
        numAdminCommands = len(adminCommandsList)
        numCoHostCommands = len(coHostCommandsList)
        numMemberCommands = len(memberCommandsList)
        perPage = 8

        if numAdminCommands == 0 and numCoHostCommands == 0 and numMemberCommands == 0:
            ctx.send("Não há comandos disponíveis.")
            return

        numAdminPages = (numAdminCommands - 1) // perPage + 1
        numCoHostPages = (numCoHostCommands - 1) // perPage + 1
        numMemberPages = (numMemberCommands - 1) // perPage + 1

        if pageNumber < 1 or pageNumber > numMemberPages + numCoHostPages + numAdminPages:
            ctx.send("Página inválida.")
            return
        numPages = numMemberPages + numCoHostPages + numAdminPages
        if pageNumber <= numMemberPages:
            commandName = "Membro"  
            commandsToShow = memberCommandsList
        elif pageNumber <= numMemberPages + numCoHostPages:
            commandName = "Co-Host" 
            commandsToShow = coHostCommandsList
            pageNumber -= numMemberPages         
        else:
            commandName = "Admin" 
            commandsToShow = adminCommandsList
            pageNumber = pageNumber - numMemberPages - numCoHostPages

        startIdx = (pageNumber - 1) * perPage
        endIdx = pageNumber * perPage
        pageCommands = commandsToShow[startIdx:endIdx]
        text = f"[bc]─ㅤ{message}/{numPages}ㅤ──\n[cb]Comandos de {commandName}\n[cb]___________________________\n[cb]꒷ ꒦ ꒷ 𓏸⠀⠀.𖣔.⠀⠀𓏸 ꒷ ꒦ ꒷"
        for c in pageCommands:
            text += f"\n╰► !{c}"

        return ctx.send(text)

    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="ping", description="Pong.", aliases=["Ping", "PING"], usage="!ping")
def pingCommand(ctx: Context):
    try:
        return ctx.reply(f"[ci]Pong! ({bot.ping()}ms)")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="horoscope", description="Responde com o horoscopo do dia.", aliases=["Horoscope", "HOROSCOPE"], usage="!horoscope signo")
def horoscopeCommand(ctx: Context, message: str):
    try:
        cleanedString = unidecode(''.join(char for char in message if char.isalpha() or char.isspace())).lower()
        horoscope = getHoroscope(cleanedString)
        return ctx.reply(horoscope)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")  

@bot.command("mention")
def mention(ctx: Context):
    mentioned_users = []
    mentioned_users.append(ctx.author.username)
    mentioned_userss = []
    mentioned_userss.append(ctx.author.userId)
    mentioned = ctx.prepare_mentions(mentioned_users)
    return ctx.reply(
        "b: " + ", ".join(mentioned), mentioned=list(mentioned_userss)
    )

@bot.command(name="coinflip", description="Cara ou coroa?", aliases=["Coinflip", "COINFLIP", "coinFlip", "cf"], usage="!coinflip")
def horoscopeCommand(ctx: Context):
    try:
        return ctx.send_image(f"{random.randint(0, 1)}.PNG")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")  

@bot.command(name="fortune", description="Diz sua sorte do dia.", aliases=["Fortune", "FORTUNE"], usage="!fortune")
def fortuneCommand(ctx: Context):
    try:
        with open("fortunes.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return ctx.reply(f"[ci]{random.choice(lines)}")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")  

@bot.command(name="rps", description="Responde com o horoscopo do dia.", aliases=["Rps", "RPS"], usage="!rps pedra")
def rpsCommand(ctx: Context, message: str):
    try:
        userC = getUserChoice(message)
        botC = getComputerChoice()
        return ctx.reply(determineWinner(userC, botC))
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")  

@bot.command(name="speak", description="Responde com uma mensagem de áudio.", aliases=["Speak", "SPEAK"], usage="!speak mensagem")
def audioCommand(ctx: Context, message: str):
    try:
        tts = gTTS(text=message, lang='pt-PT')

        tts.save("temp_audio.mp3")

        ctx.send_audio("temp_audio.mp3")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="say", description="Escreve uma mensagem dada pelo utilizador.", aliases=["Say", "SAY"], usage="!say mensagem")
def sayCommand(ctx: Context, message: str):
    try:
        bot.community.delete_message(ctx.chatId, ctx.message.messageId, comId=ctx.comId)
        ctx.send(f"[ci]{message}")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="8ball", description="Responde a uma pergunta sua.", aliases=["8b", "8BALL"], usage="!ball pergunta")
def ball8Command(ctx: Context):
    try:
        answers = ['É certo.', 'Sem dúvida.', 'Sim - definitivamente.', 'Pode contar com isso.', 'Parece-me que sim.', 'Muito provável.', 'Perspectivas boas.', 'Sim.', 'Sinais apontam para sim.', 'Resposta nebulosa, tente novamente.', 'Pergunte novamente mais tarde.', 'Melhor não dizer agora.', 'Não é possível prever agora.', 'Concentre-se e pergunte novamente.', 'Não conte com isso.', 'Minha resposta é não.', 'Minhas fontes dizem não.', 'Perspectivas não são boas.', 'Muito duvidoso.', 'Certamente não.', 'Deuses dizem sim.', 'Deuses dizem não.', 'Ninguém sabe.', 'Eu não acho que sim.']
        ctx.reply(random.choice(answers))
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")


@bot.command(name="love", description="Avalia o amor entre duas pessoas.", aliases=["Love", "LOVE"], usage="!love @utilizador")
def loveCommand(ctx: Context, message: str):
    try:
        
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        if targetId is None:
            return ctx.reply("[ci]Voce não mencionou ninguem.")
        
        user = bot.community.fetch_user(targetId)
        loveValue = random.randint(1, 100)
        text = (f'{ctx.author.username} ❤️ {user.username} = {loveValue}%')
        
        ctx.reply(content=text)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="gay", description="Responde com o utilizador identificado mas gay.", aliases=["Gay", "GAY"], usage="!gay @utilizador")
def infoCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser)
        if targetId is None:
            return ctx.reply("[ci]Voce não mencionou ninguem.")
        user = bot.community.fetch_user(targetId)
        img = sendUrlToGay(user.icon)
        gayValue = random.randint(1, 100)
        
        ctx.send_link_snippet(image=img, message=f"[ci]{user.nickname} é {gayValue}% gay, parabéns!")
    except:
        
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")


@bot.command(name="roll", description="Roda dados personalizados.", aliases=["Roll", "ROLL"], usage="!roll d20")
def diceCommand(ctx: Context, message: str):
    try:
        r = rollDice(ctx, message)
        ctx.reply(f"[ci]{r}")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="createrank", description="Cria o seu rank e o seu cartão de rank.", aliases=["Createrank", "createRank", "CREATERANK", "cr"], usage="!createrank")
def rankCreateCommand(ctx: Context):
    try:
        return ctx.send(f"[ci] {createCard(ctx)}")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="rank", description="Responde com o cartão do rank da pessoa.", aliases=["Rank", "RANK", "r"], usage="!rank")
def rankViewerCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser)
        image = getRankCard(targetId, bot)
        if image is None: 
            user = bot.community.fetch_user(targetId)
            return ctx.send(f"[ci]{user.nickname} ainda nao tem um rank! Use !createrank para criar um!")
        return ctx.send_image(image)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="leaderboard", description="Responde com as pessoas no top 5.", aliases=["Leaderboard", "LEADERBOARD", "lb"], usage="!leaderboard")
def leaderboardCommand(ctx: Context):
    try:
        userList = getLeaderBoard()
        texto = ''
        i = 0

        for user in userList:
            i += 1
            uid = user['uid']
            xp = user['xp']
            lvl = user['lvl']

            usuario = bot.community.fetch_user(uid)

            user_data = f"{i}- XP: {xp}, LVL: {lvl}, {usuario.username}\n"
            texto += user_data

        ctx.send(texto)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="background", description="Permite mudar o background do cartão de rank.", aliases=["Background", "BACKGROUND", "bg"], usage="!background 1")
def backgroundCommand(ctx: Context, message: str):
    try:
        if message is None:
            return ctx.send("[ci]Use !background 1")
        text = updateBackground(ctx, message)
        return ctx.send(text)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="download", description="Envia um link para baixar uma imagem identificada.", aliases=["Download", "DOWNLOAD", "dl"], usage="!download")
def downloadCommand(ctx: Context):
    try:
        info = bot.community.fetch_messages(chatId=ctx.chatId, size=1).data
        url = sendImageLink(info[0]['extensions']['replyMessage']['mediaValue'])
        ctx.send(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="suggest", description="Envia uma sugestão. O seu user será enviado também.", aliases=["Suggest", "SUGGEST", "sugerir"], usage="!suggest mensagem")
def suggestCommand(ctx: Context, message: str):
    try:
        text = f"[cb]{ctx.author.username} ({ctx.author.uid}) disse:\n[ci]{message}"
        bot.community.send_message(chatId=suggestionChatId, content=text)
        return ctx.reply("Sugestão enviada com sucesso.")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="report", description="Envia algo a reportar. O seu user será enviado também.", aliases=["Report", "REPORT", "reportar"], usage="!report mensagem")
def reportCommand(ctx: Context, message: str):
    try:
        text = f"[cb]{ctx.author.username} ({ctx.author.uid}) disse:\n[ci]{message}"
        bot.community.send_message(chatId=reportsChatId, content=text)
        return ctx.reply("Report enviado com sucesso.")
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")





################################## Comandos de Interações

@bot.command(name="slap", description="Dá um tapa em alguém.", aliases=["Slap", "SLAP", "tapa"], usage="!slap @utilizador")
def slapCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=slap").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} deu um tapa em {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="punch", description="Dá um soco em alguém.", aliases=["Punch", "PUNCH", "soco"], usage="!punch @utilizador")
def punchCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=punch").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} deu um socao em {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="kiss", description="Dá um beijo em alguém.", aliases=["Kiss", "KISS", "beijo"], usage="!kiss @utilizador")
def kissCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=kiss").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} beijou {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="hug", description="Dá um abraço em alguém.", aliases=["Hug", "HUG", "abraco"], usage="!hug @utilizador")
def hugCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=hug").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} abraçou {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="patpat", description="Dá um pat pat em alguém.", aliases=["pat", "Pat", "PAT", "Patpat", "PATPAT"], usage="!patpat @utilizador")
def patpatCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=pat").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} pat pat em {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="lick", description="Dá uma lambida em alguém.", aliases=["Lick", "LICK", "lamber"], usage="!lick @utilizador")
def lickCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        url = get(f"https://api.otakugifs.xyz/gif?reaction=lick").json()["url"] 
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário mencionado")
        
        user = bot.community.fetch_user(targetId)
        text = (f'{ctx.author.username} lambeu {user.nickname}')
        
        ctx.send(content=text)
        ctx.send_gif(url)
    except:
        try:
            return bot.community.start_chat(userIds=ctx.author.uid, message="[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")





################################## Co-Host Commands ##################################

@bot.command(name="kick", description="Remove um utilizador do chat.", aliases=["Kick", "KICK", "ban+"], usage="!kick @utilizador")
def kickCommand(ctx: Context, message: str = None):
    try:
        user = ctx.message.author
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser, userCant=True)
        
        if targetId is None:
            return ctx.reply("[ci]Nenhum usuário selecionado. !kick @utilizador")

        chat_mods = list(getChatMods(ctx.message.chatId))
        moderators = list()
        banned_list = list()

        for user_name in targetId:
            if targetId in chat_mods:
                moderators.append(user_name)
            else:
                banned_list.append(user_name)

        if not user.userId in chat_mods: 
            return ctx.reply("[ci]Apenas moderadores podem usar o comando de kick.")

        if moderators:
            return ctx.reply(f"[ci]Não podes kickar outros moderadores.")

        if banned_list:
            for user_name in targetId:
                try:
                    bot.community.kick(userId=targetId, chatId=ctx.message.chatId, comId=ctx.message.comId, allowRejoin=True)
                    bot.community.send_message(chatId=logsChatId, content=f"[ci]{user.nickname} ({user.userId}) usou o comando de kick no {targetId}.")
                except AccessDenied:
                    return ctx.reply("[ci]Sem permissão para kickar.")

            return ctx.reply("[ci]User kickado com sucesso.")

        return ctx.reply("[ci]Nenhum usuário kickado.")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="purge", description="Deleta mensagens.", aliases=["Purge", "PURGE", "del"], usage="!purge 5")
def purgeCommand(ctx: Context, message: int):
    try:
        user = ctx.message.author


        chat_mods = list(getChatMods(ctx.message.chatId))

        if not user.userId in chat_mods: 
            return ctx.reply("[ci]Apenas moderadores podem usar o comando de purge.")


        try:
            try:
                amount = int(message)
            except ValueError:
                return ctx.reply("[ci]Coloque uma quantidade válida.\n[ci]Exemplo: !purge 5")

            if amount > 100:
                return ctx.reply("[ci]Máximo de 100 mensagens que podem ser deletadas.")

            messages = bot.community.fetch_messages(chatId=ctx.message.chatId, size=100).messageId
            for i in range(amount+1):
                bot.community.delete_message(chatId=ctx.message.chatId, messageId=messages[i], asStaff=True, reason=f'Comando do bot executado por {ctx.author.username} ({ctx.author.uid})')
            bot.community.send_message(chatId=logsChatId, content=f"[ci]{ctx.author.nickname} ({ctx.author.uid}) usou o comando de purge.")
            return ctx.send(f"[ci]Deletei {amount} mensagens com sucesso.")
        except AccessDenied:
            return ctx.reply("[ci]Sem permissão para deletar.")

    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



################################## Admin Commands ##################################

@bot.command(name="joinchat", description="Entra em um chat de uma comunidade.", aliases=["Joinchat", "joinChat", "JOINCHAT", "joinc"], usage="!joinchat LinkDoChat")
@moderator_only
def comIdCommand(ctx: Context, message: str):
    try:
        id = bot.community.fetch_object_id(message)
        bot.community.join_chat(id)
        ctx.reply("[ci]Entrei no chat com sucesso!")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="getuser", description="Responde com um link do perfil do utilizador.", aliases=["Getuser", "getUser", "GETUSER", "getu"], usage="!getuser IdDoUser")
@moderator_only
def getUserCommand(ctx: Context, message: str):
    try:
        user = bot.community.fetch_user(message)
        ctx.reply(bot.community.fetch_object(user.uid).shareURLShortCode)
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="viewonly", description="Muda o modo de visualização do chat.", aliases=["Viewonly", "viewOnly", "VIEWONLY", "viewo"], usage="!viewonly on/off")
@moderator_only
def viewonlyCommand(ctx: Context, message: str):
    try:
        if message == "on":
            bot.community.set_view_only(viewOnly=True, chatId=ctx.message.chatId, comId=ctx.message.comId)
            return ctx.reply("[ci]Chat está em modo de visualização!")
        elif message == "off":
            bot.community.set_view_only(viewOnly=False, chatId=ctx.message.chatId, comId=ctx.message.comId)
            return ctx.reply("[ci]Chat já não está em modo de visualização!")
        else:
            return ctx.reply("[ci]Coloque uma opção válida.\n[cu]Exemplo: !viewonly on")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="fetchstaff", description="Atualiza a lista da staff.", aliases=["Fetchstaff", "fetchStaff", "FETCHSTAFF", "fetchs", "fs"], usage="!fetchstaff")
@moderator_only
def getStaffCommand(ctx: Context, message: str):
    try:
        getStaff()
        return ctx.reply('[ci]Lista da staff Atualizada')
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")


 
@bot.command(name="chatid", description="Responde com o id de um chat.", aliases=["Chatid", "chatId", "CHATID"], usage="!chatid LinkDoChat")
@moderator_only
def chatIdCommand(ctx: Context, message: str):
    try:
        chatId = bot.community.fetch_object_id(message)
        ctx.reply(chatId)   
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")


@bot.command(name="inviteall", description="Convida até 100 utilizadores online para o chat.", aliases=["Inviteall", "inviteAll", "INVITEALL", "invitea"], usage="!inviteall")
@moderator_only
def inviteAllCommand(ctx: Context, message: str):
    try:
        users = bot.community.fetch_online_users(start=0, size=100)
        i = 0
        for user in users.userId:
            bot.community.invite_chat(chatId=ctx.chatId, userIds=user)
            i+=1
        return ctx.reply(f'Convidado {i} pessoas')
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")



@bot.command(name="info", description="Responde com informacao de um utilizador.", aliases=["Info", "INFO"], usage="!info @utilizador")
@moderator_only
def infoCommand(ctx: Context, message: str):
    try:
        mentionedUser = ctx.message.mentioned_dictionary
        targetId = getUserId(ctx=ctx, message=message, bot=bot, mentionedUser=mentionedUser)
        target = bot.community.fetch_object(targetId)
        profile = bot.community.fetch_user(targetId)
        isoDatetime = datetime.fromisoformat(profile.created_time[:-1])
        humanReadableDate = isoDatetime.strftime("%A, %B %d, %Y %I:%M %p")
        chatId = ctx.chatId
        comunityId = ctx.communityId
        text = (f"[ci]𝗚𝗹𝗼𝗯𝗮𝗹 𝗱𝗼 𝗨𝘁𝗶𝗹𝗶𝘇𝗮𝗱𝗼𝗿: ndc://g/user-profile/{profile.userId}\n\n[ci]𝗜𝗗 𝗱𝗼 𝗖𝗵𝗮𝘁: {chatId}\n\n[ci]𝗜𝗗 𝗱𝗮 𝗖𝗼𝗺𝘂𝗻𝗶𝗱𝗮𝗱𝗲: {comunityId}\n\n[ci]𝗜𝗗 𝗱𝗼 𝗨𝘁𝗶𝗹𝗶𝘇𝗮𝗱𝗼𝗿: {profile.userId}\n")
        return embedOnApp(ctx, text, profile.nickname, humanReadableDate, profile.icon, target.shareURLShortCode)
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="getbg", description="Retorna o background do chat.", aliases=["getbg", "GETBG", "getBg"], usage="!getbg")
@moderator_only
def joinChatsCommand(ctx: Context, message: str):
    try:
        chat = bot.community.fetch_chat(chatId=ctx.chatId).extensions.background
        chats = bot.community.fetch_chat(chatId=ctx.chatId).data
        ctx.send_image(chats['icon'])
        return ctx.send_image(chat)
        
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="joinall", description="Entra em todos os chats.", aliases=["Joinall", "JOINALL", "joinAll"], usage="!joinall")
@moderator_only
def joinChatsCommand(ctx: Context, message: str):
    try:
        chats = bot.community.fetch_public_chats(chatType= ChatTypes.RECOMMENDED,start=0, size=50).chatId
        for c in chats:
            try:
                bot.community.join_chat(chatId=c)
            except:
                print("")
        return ctx.reply('Entrei em todos os chats que encontrei!')
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")

@bot.command(name="raffle", description="Realiza um sorteio em um blog.", aliases=["Raffle", "RAFFLE"], usage="!raffle LinkDoBlog \"Mensagem para o vencedor\"")
@moderator_only
def sorteioCommand(ctx: Context, message: str):
    try:
        parts = message.split(" ", 1)
        text = parts[1].split('"')
        id = bot.community.fetch_object_id(link=parts[0])
        count = bot.community.fetch_blog(blogId=id)
        comments = bot.community.fetch_comments(blogId=id, size=count.commentsCount)
        printedUsers = set()
        
        for comment in comments.author.uid:
            if comment not in printedUsers:
                printedUsers.add(comment)
                
        if printedUsers:
            random_user = random.choice(list(printedUsers))
            bot.community.start_chat(userIds=random_user, message=text)
            user = bot.community.fetch_user(random_user)
            ctx.reply(f"[ci]O vencedor é {user.nickname} ({user.uid})")
        else:
            ctx.reply("[ci]Nenhum utilizador encontrado!")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")    

@bot.command(name="here", description="Identifica todos os users do chat", aliases=["here", "everyone", "HERE", "EVERYONE"], usage=["!here"])
@moderator_only
def identifyAllCommand(ctx: Context, message: str):
    try:
        chatId = ctx.chatId
        mentioned_users = []
        mentioned_userss = []

        chatUsers = bot.community.fetch_chat_members(chatId=chatId, start=0, size=100).members

        chatUsersCount = bot.community.fetch_chat(chatId=chatId).members_count

        start_index = 0
        while start_index < chatUsersCount:
            mentioned_users = []
            mentioned_userss = []
            chatUsers = bot.community.fetch_chat_members(chatId=chatId, start=start_index, size=100).members

            mentioned_users.extend(chatUsers.username)
            mentioned_userss.extend(chatUsers.userId)
            start_index += 100
            mentioned = ctx.prepare_mentions(mentioned_users)
            result_string = " ".join(mentioned)
            ctx.reply(result_string, mentioned=list(set(mentioned_userss)))

        

    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")


@bot.command(name="sendmessage", description="Envia mensagem para N utilizadores.", aliases=["Sendmessage", "sendMessage", "SENDMESSAGE", "sendm"], usage=["!sendmessage Link1 Link2 \"texto\""])
@moderator_only
def dmSomeoneCommand(ctx: Context, message: str):
    try:
        users, text = extractUsersAndText(message)
        for u in users:
            targetId = bot.fetch_object_id(u)
            bot.community.start_chat(userIds=targetId, message=text)
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")   



@bot.command(name="resetallranks", description="Reseta todos os ranks.", aliases=["Resetallranks", "resetAllRanks", "RESETALLRANKS", "ral"], usage="!resetallranks password")
@moderator_only
def deleteAllRanksCommand(ctx: Context, message: str):
    try:
        if message != '123456':
            bot.community.delete_message(ctx.chatId, ctx.message.messageId, comId=ctx.comId, asStaff=True)
            return ctx.send('[ci]Palavra passe errada!')
        text = deleteAllRanks()
        bot.community.delete_message(ctx.chatId, ctx.message.messageId, comId=ctx.comId, asStaff=True)
        return ctx.send(f"[ci]{text}")
    except:
        try:
            return ctx.reply("[ci]Algo inesperado aconteceu, por favor tente mais tarde ou verifique se o comando foi feito corretamente!")
        except:
            return print("Erro no servidor do amino!")





################################## Events ##################################

@bot.task(interval=1000)
def wellcome(community: Community):
    try:
        if community.community_id != medieval:
            return
        welcomeMessage = "[c]︵ ❀ ︿ ❁ ︵ ❀ ︿ ❁ ︵\n[c]𝘖𝘐, 𝘉𝘌𝘔-𝘝𝘐𝘕𝘋𝘖\n[c]🌺\n[c]୨:୧┈┈┈┈┈ · · ┈┈┈┈┈୨:୧\n[c]Olá, seja muito bem-vindo a este\n[c]Amino! Eu estou aqui como um bot\n[c]para te ajudar a dar os primeiros\n[c]passos nesta comunidade, talvez\n[c]você deva começar por olhar aqui\n[c]nos links que vou deixar aqui\n[c]em baixo, se precisar de mim,\n[c]não exite em me chamar, abraços!\n[c]Tenho de ir dar bem-vindo ao\n[c]resto da comunidade, se divirta!\n[c]୨:୧┈┈┈┈┈ · · ┈┈┈┈┈୨:୧\n[c]𝘓𝘐𝘕𝘒𝘚 𝘐𝘔𝘗𝘖𝘙𝘛𝘈𝘕𝘛𝘌𝘚\n[c]❁⌇ http://aminoapps.com/p/2i2awm\n[c]✧⌇ http://aminoapps.com/p/51n4p9\n[c]୨:୧┈┈┈┈┈ · · ┈┈┈┈┈୨:୧\n[c]𝘈𝘋𝘌𝘜𝘡𝘐𝘕𝘏𝘖\n[c]︵ ❀ ︿ ❁ ︵ ❀ ︿ ❁ ︵"
        users = community.fetch_users(userType=UserTypes.RECENT, start=0, size=10)
        for user in users.userId:
            welcomeComment = (community.fetch_comments(userId=user, start=0, size=0).commentId)
            if(not welcomeComment):
                community.comment(content=welcomeMessage, userId=user)
                time.sleep(3) 
        try:
            
            bot.community.check_in()
        except:
            try:
                bot.community.play_lottery()
            except:
                return bot.community.edit_profile(content=f"[ci]Bot construído por [Mim|https://github.com/DavldMA/Amino-Bot]\n[ci]Quantidade de Moedas: {bot.fetch_wallet().totalCoins}")
                  
        
    except:
        try:
            return bot.community.send_message(chatId=reportsChatId, content=f"[ci]Aconteceu um erro ao tentar fazer check-in, jogar na loteria ou dar bem vindo a um membro.")
        except:
            return print("Erro no servidor do amino!")



@bot.on_member_join()
def join(ctx: Context, member: Member):
    try:

        text = (f"[c]━━━━━━━━━━━━━━━\n[c]Bem vindo, {member.nickname}!\n[c]━━━━━━━━━━━━━━━\n-> Sem spam.\n-> Não seja tóxico.\n-> Respeite todos os membros.\n-> Não espalhe ódio gratuito.\n-> Não divulgue nada sem autorização.\n[c]━━━━━━━━━━━━━━━")
        embedOnApp(ctx, text, member.nickname, "", member.icon, bot.community.fetch_object(member.userId).shareURLShortCode)
    except:
        try:
            return bot.community.send_message(chatId=reportsChatId, content=f"[ci]Algo inesperado aconteceu, quando um membro entrou!")
        except:
            return print("Erro no servidor do amino!")



@bot.on_text_message()
def text_message(ctx: Context, message: str):
    try:
        addXp(ctx=ctx)
        message = message.lower()
        if message == 'bot' or message == 'botzinho':
            return ctx.reply("Fala ai!")
        reactions = ["airkiss","angrystare","bite","bleh","blush","brofist","celebrate","cheers","clap","confused","cool","cry","cuddle","dance","drool","evillaugh","facepalm","handhold","happy","headbang","hug","kiss","laugh","lick","love","mad","nervous","no","nom","nosebleed","nuzzle","nyah","pat","peek","pinch","poke","pout","punch","roll","run","sad","scared","shrug","shy","sigh","sip","slap","sleep","slowclap","smack","smile","smug","sneeze","sorry","stare","stop","surprised","sweat","thumbsup","tickle","tired","wave","wink","woah","yawn","yay","yes"] # basically a list of commands.
        if message in reactions: 
            url = get(f"https://api.otakugifs.xyz/gif?reaction={message}").json()["url"] 
            return ctx.send_gif(url) 
        if re.match(r'\d+d\d+|d\d+', message) or re.match(r'\d+#\d*d\d+', message):
            r = rollDice(ctx, message)
            return ctx.reply(r)
    except:
        try:
            return bot.community.send_message(chatId=reportsChatId, content=f"[ci]Algo inesperado aconteceu com a mensagem de um utilizador!")
        except:
            return print("Erro no servidor do amino!")



@bot.on_error()
def on_error(error: Exception):
    print(f"Error: {error}")


getStaff()