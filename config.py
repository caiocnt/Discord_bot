import discord
from discord.ext import commands
import pymongo
client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.vlndoc0.mongodb.net/?retryWrites=true&w=majority")
db = client.test

class Register_modal(discord.ui.Modal,title="TESTE"):
    disc_user = discord.ui.TextInput(label='Discord user',placeholder='user_exemple#123456')
    board_id = discord.ui.TextInput(label='board ID',placeholder='https://trello.com/b/{BoardID}/{BoardName}')
    key = discord.ui.TextInput(label="API Key")
    tkn = discord.ui.TextInput(label="API Token")
    async def on_submit(self,interaction:discord.Interaction):
        await interaction.response.send_message("finalizado")
        fnd = list(db.server_configuration.find({"user":self.children[0].value}))
        if len(fnd)>0:
            user_id=fnd[0]['_id']
            db.server_configuration.replace_one({'_id':user_id},
            {'user':self.children[0].value,
            'board_id':self.children[1].value,
            'key':self.children[2].value,    
            'token':self.children[3].value
            })
        else:
            db.server_configuration.insert_one(
            {
            'user':self.children[0].value,
            'key':self.children[1].value,    
            'token':self.children[2].value
            }
            )

            
class Buttons(discord.ui.View):
    def __init__(self,*,timeout=20):
        super().__init__(timeout=timeout)

    @discord.ui.button(emoji="⚙",label="Configurações",style=discord.ButtonStyle.green)
    async def click(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(Register_modal())
        await interaction.message.delete()

class Click_me_config(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def config(self,ctx):
        await ctx.send("Click no botão abaixo para abrir as configurações, é necessário a chave e o Token da API Atlassian do trello para poder realizar as consultas",view=Buttons())

async def setup(bot):
    await bot.add_cog(Click_me_config(bot))
