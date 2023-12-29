from easy_pil import Editor, load_image, Font
from pathlib import Path
import db
import unicodedata

backgroundName = ["zIMAGE0.png", "zIMAGE1.jpg", "zIMAGE2.jpg", "zIMAGE3.jpg", "zIMAGE4.jpg", "zIMAGE5.jpg"]

def rank(username, icon, userDb):
    try:
        lvl = userDb['lvl']
        xp = userDb['xp']
        backgroundNumber = userDb['background']
        backgroundNumber = int(backgroundNumber)
        if backgroundNumber+1 > len(backgroundName):
            backgroundNumber = 0
        username = unicodedata.normalize('NFKC', username)

        next_level_xp = (lvl+1) * 100
        xp_need = next_level_xp
        xp_have = xp

        percentage = int(((xp_have * 100)/ xp_need))

        if percentage < 1:
            percentage = 0

        image = icon

        background = Editor(backgroundName[backgroundNumber])
        profile = load_image(image)

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        # Load the ima image
        ima = Editor("zBLACK.png")
        background.blend(image=ima, alpha=0.5, on_top=False)

        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="#fff", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#ff9933",
            radius=20,
        )
        background.text((200, 40), str(username), font=poppins, color="#ff9933")

        background.rectangle((200, 100), width=350, height=2, fill="#ff9933")
        background.text(
            (200, 130),
            f"Level : {lvl}   "
            + f" XP : {xp} / {(lvl+1) * 100}",
            font=poppins_small,
            color="#ff9933",
        )
        output_path = Path("output_image.png")
        background.image.save(output_path)
        return str(output_path)
    except:
        return None

def addXp(ctx, uid, userDb):
    try:
        if userDb is None:
            return
        lvl = userDb['lvl']
        xp = userDb['xp']

        #increase the xp by the number which has 100 as its multiple
        increased_xp = xp+10
        new_level = int(increased_xp/100)

        xp=increased_xp


        if new_level > lvl:
            ctx.send(f'Você upou para o nível {new_level}!')

            lvl=new_level
            xp=0
        
        db.updateUser(uid=uid, xp=xp, lvl=lvl, background=userDb["background"])
    except:
        return None
    
def updateBackground(number, userDb):
    try:
        db.updateUser(uid=userDb['uid'], xp=userDb['xp'], lvl=userDb['lvl'], background=number)
        return "Background atualizado com sucesso!"
    except:
        return "Ocorreu algum erro!"