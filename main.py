import discord
from discord.ext import commands
import datetime
from Event import Event, Calendar
import os

TOKEN = os.environ['DISCORD_TOKEN']

bot = commands.Bot(command_prefix="!")	# Creates client
calendar = Calendar()

#Fonction appelé lorsque le bot est en ligne
@bot.event
async def on_ready():
    print('Bot connecté en tant que {0.user}'.format(bot))
    print(f"{bot.user.name} prêt à aider les CIRs")
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name="tester comment tuer un humain"))

#Fonction pour la gestion des erreurs
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Désolé, commande non trouvée")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Manque un arguments")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Tu n'as pas la permission de faire cela.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Tu ne peux pas faire ça.")
    if isinstance(error.original, discord.Forbidden):
        await ctx.send("Je n'ai pas la permission de faire cela.-")

#Fonction pour vérifier qui est le créateur du bot pour certaines commandes
def isOwner(ctx):
    return ctx.message.author.id == 604035377497505863

#Fonction pour récupérer le guild du discord
@bot.command()
@commands.check(isOwner)
async def GetId(ctx):
    await ctx.send(ctx.guild.id)

#Fonction pour clear le calendrier
@bot.command()
@commands.check(isOwner)
async def ClearCalendar(ctx):
    calendar.clear()
    await ctx.send("Calendrier clear")

#Fonction pour envoyer un message anonyme
@bot.command()
async def anonyme(ctx,message="test"):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        embed = discord.Embed(title="**Message Anonyme**", description=message, color=0x3498db)
        embed.set_footer(text="Envoyer des messages anonymes en dm avec la commande !anonyme 'message'")
        for guild in bot.guilds:
            if (guild.get_channel(908408431570980896) != None):
                await guild.get_channel(908408431570980896).send(embed=embed)

#Fonction pour afficher les devoirs, du jour, semaine, ou du mois
@bot.command()
async def devoirs(ctx, date="day"):
    today = datetime.date.today()
    embed = discord.Embed(title="**DEVOIRS**", color=0xe74c3c)
    #Si l'intervalle donnée est une semaine
    if (date == "week"):
        nextWeek = (today + datetime.timedelta(days=7))
        events = calendar.get(today,nextWeek)
        for event in events:
            embed.add_field(name=f"Devoir en {event.summary} pour le {event.end}", value=event.description, inline=False)
        embed.set_footer(text="Voici les devoirs de la semaine")
    # Si l'intervalle donnée est un mois
    elif (date == "month"):
        nextMonth = (today + datetime.timedelta(days=31))
        events = calendar.get(today,nextMonth)
        for event in events:
            embed.add_field(name=f"Devoir en {event.summary} pour le {event.end}", value=event.description, inline=False)
        embed.set_footer(text="Voici les devoirs du mois")
    # Sinon l'intervalle est un jour
    else:
        tomorrow = (today + datetime.timedelta(days=1))
        events = calendar.get(today,tomorrow)
        for event in events:
            embed.add_field(name=f"Devoir en {event.summary} pour le {event.end}", value=event.description, inline=False)
        embed.set_footer(text="Voici les devoirs du jour")
    await ctx.message.delete()
    await ctx.channel.send(embed=embed)

#Fonction pour ajouter des devoirs
#Vérification si l'utilisateur est un CIR ou non
@bot.command()
@commands.has_role(884906571497361468)
async def addDevoirs(ctx, matiere="Matière", date=(datetime.date.today().strftime('%d/%m/%y')), description="Description"):
    start = datetime.datetime.strptime(date, '%d/%m/%y')
    end = start
    event = Event(matiere,start,end,description)
    calendar.addEvent(event)
    await ctx.message.delete()
    embed = discord.Embed(title="**AJOUT DE DEVOIRS**", color=0x2ecc71)
    embed.add_field(name=f"Faire {event.description} en {event.summary} ajouté pour le ", value=event.end, inline=False)
    await ctx.channel.send(embed=embed)


bot.remove_command('help')
bot.run(TOKEN)
