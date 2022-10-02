from msilib.schema import TextStyle
import discord
from discord.ext import commands
import pymongo

import requests
import json

client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.vlndoc0.mongodb.net/?retryWrites=true&w=majority")
db = client.test

def lista(key,token,board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    headers = {"Accept": "application/json"}
    query = {'key': key,'token': token}
    response = requests.request("GET",url,headers=headers,params=query)
    return response.json()

def card(list_id,key,token,name,desc):
    url_create = f"https://api.trello.com/1/cards"
    query_create = {'key': key,'token': token,'idList':list_id,'name':name,'desc':desc}
    vlr = requests.post(url_create,query_create)
    return vlr


class Create_modal(discord.ui.Modal,title="TESTE"):
    disc_user = discord.ui.TextInput(label='Discord user',placeholder='user_exemple#123456')
    lis = discord.ui.TextInput(label="Nome da Lista")
    nome = discord.ui.TextInput(label="Nome do Cartão")
    desc = discord.ui.TextInput(label="Descrição do Cartão",style=discord.TextStyle.paragraph)
    async def on_submit(self,interaction:discord.Interaction):
        fnd = list(db.server_configuration.find({"user":self.children[0].value}))
        if len(fnd)>0:
            board_list = lista(fnd[0]['key'],fnd[0]['token'],fnd[0]['board_id'])
            for l in board_list:
                if str(l['name']) == str(self.children[1].value):
                    id_list = l['id']
                    teste = card(id_list,fnd[0]['key'],fnd[0]['token'],self.children[2].value,self.children[3].value)
                    break
            embed = discord.Embed(description='Cartão criado com sucesso!!')
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(description = 'Você não está cadastrado, digite !config')
            await interaction.response.send_message(embed=embed)
            
class Buttons_create(discord.ui.View):
    def __init__(self,*,timeout=20):
        super().__init__(timeout=timeout)

    @discord.ui.button(emoji="🆕",label="Novo Cartão",style=discord.ButtonStyle.green)
    async def click(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.send_modal(Create_modal())
        await interaction.message.delete()

class Click_me_create(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def create(self,ctx):
        await ctx.send("Click no botão abaixo para criar um novo cartão",view=Buttons_create())

async def setup(bot):
    await bot.add_cog(Click_me_create(bot))
