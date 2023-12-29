import dice
import re
import levels
import db
import image
import requests
import random
from bs4 import BeautifulSoup
from google_translate_py import Translator

def embedOnApp(ctx, m, t, c, i, l):
    try:
        return ctx.send_embed(
            message = m,
            title = t,
            content = c,
            image = i,
            link = l
        )
    except:
        try:
            i = "default.jpg"
            return ctx.send_embed(
                message = m,
                title = t,
                content = c,
                image = i,
                link = l
            )
        except:
            return None

def rollDice(ctx, message):
    try:
        result = dice.parseInput(message)
        result = f"[c]━━━━━ • 🎲 • ━━━━━{result}\n[c]━━━━━━━━━━━━━━"
        return result
    except:
        return None

def getUserId(ctx = None, message = None, bot = None, mentionedUser = None, userCant = False):
    try:
        if mentionedUser is not None: # Mention
            for userId in mentionedUser:
                return userId
        if message is not None and isAminoLink(message): # Link
            return bot.community.fetch_object_id(message) 
        if bot is not None:
            info = bot.community.fetch_messages(chatId=ctx.chatId, size=1).data
            if bool(info[0]['extensions']):
            
                return info[0]['extensions']['replyMessage']['author']['uid']
        if ctx is not None and userCant is False:  
            return ctx.author.userId
        return None
    except:
        return None

def sendImageLink(url):
    try:
        link = image.convertImageToLink(url)
        return link
    except:
        return None

def sendUrlToGay(url):
    try:
        img = image.processGayImage(url)
        return img
    except:
        return None

def isAminoLink(message):
    try:
        pattern = r'https?://aminoapps\.com/.*'

        if re.match(pattern, message):
            return True
        else:
            return False
    except:
        return None

def getUsernameImage(bot, uid):
    try:
        person = bot.community.fetch_user(uid)
        return (person.username, person.icon)
    except:
        return None

def createCard(ctx):
    try:
        id = getUserId(ctx=ctx, message=None, bot=None, mentionedUser=None)
        return db.addNewUser(id)
    except:
        return None

def getRankCard(id, bot):
    try:
        userDb = db.getUser(id)
        if userDb is None:
            return None
        result = getUsernameImage(bot, id)
        username = result[0]
        icon = result[1]
        image = levels.rank(username=username, icon=icon, userDb=userDb)
        return image
    except:
        return None

def addXp(ctx):
    try:
        id = getUserId(ctx=ctx, message=None, bot=None, mentionedUser=None)
        levels.addXp(ctx=ctx, uid=id, userDb=db.getUser(id))
        return
    except:
        return None

def getLeaderBoard():
    try:
        return db.sortLeaderboard()
    except:
        return None

def resetRank(ctx):
    try:
        id = getUserId(ctx=ctx, message=None, bot=None, mentionedUser=None)
        message = db.deleteUser(id)
        return message
    except:
        return None

def deleteAllRanks():
    try:
        message = db.deleteAllUsers()
        return message
    except:
        return None

def updateBackground(ctx, number):
    try:
        id = getUserId(ctx=ctx, message=None, bot=None, mentionedUser=None)
        userDb = db.getUser(id)
        if userDb is None:
            return "Use !createrank para criar o seu rank!"
        message = levels.updateBackground(number=number, userDb=userDb)
        return message
    except:
        return None

def extractUsersAndText(input_str):
    try:
        pattern = r'((?:\w+\s+)+)"([^"]+)"'

        match = re.search(pattern, input_str)

        if match:
            users = match.group(1).split()
            text = match.group(2)
            return users, text
        else:
            return None
    except:
        return None
    
def getHoroscope(horoscope):
    try:
        url = f"https://www.personare.com.br/horoscopo-do-dia/{horoscope}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div_element = soup.find("div", class_="styles__Text-sc-1ryixz1-3 bGfRVK")

            if div_element:
                extracted_data = div_element.text
                string_to_remove = "Que tal conferir seu horóscopo personalizado para o dia?"
                cleaned_data = extracted_data.replace(string_to_remove, "")
                words = cleaned_data.split()
                try:
                    index_of_target = words.index("PERFUME")
                    result_string = ' '.join(words[:index_of_target])
                except ValueError:
                    result_string = cleaned_data  # Word not found, return the original string
                return(result_string.strip())
            else:
                return("Elemento não encontrado.")
        else:
            return("Falha para encontrar a página.")
    except:
        return "Ocorreu um erro inesperado."

def getUserChoice(choice):
    try:
        choice = choice.strip().lower()
        
        if choice in ['r', 'pedra', 'rock']:
            return 'pedra'
        elif choice in ['p', 'papel', 'paper']:
            return 'papel'
        elif choice in ['s', 'tesoura', 'scissors']:
            return 'tesoura'
        else:
            return None
    except:
        return None
  
def getComputerChoice():
    try:
        choices = ["pedra", "papel", "tesoura"]
        return random.choice(choices)
    except:
        return "pedra"

def determineWinner(userChoice, computerChoice):
    try:
        if userChoice is None:
            return ("[ci]Escolha inválida. Por favor, escolha Pedra, Papel ou Tesoura.")
        text = f"[c]━━━━━━━━━━━━━━\n[cu]↳{userChoice} x {computerChoice}↲\n[ci]"
        if userChoice == computerChoice:
            text += "É um empate!"
        elif (userChoice == "pedra" and computerChoice == "tesoura") or (userChoice == "papel" and computerChoice == "pedra") or (userChoice == "tesoura" and computerChoice == "papel"):
            text += "Você venceu!"
        else:
            text += "Bot vence!"
        text += "\n[c]━━━━━━━━━━━━━━"
        return text
    except:
        return ("[ci]Algo deu errado. Por favor tente mais tarde.")