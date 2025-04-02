import discord
from discord import Guild, Role
from discord.ext import commands
from utils import *
import os

TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>', intents=intents)

# Guild id
GUILD_PORTAL_ID = 1197950576772788424
GUILD_SCENE_ID = 1354956711638728945
GUILD_911_ID = 1355023625597616271

# Role id
ROLE_SCENE_ID = 1355871740340867244
ROLE_911_ID = 1355871584346177652

GUILD_PORTAL = Guild
GUILD_911 = Guild
GUILD_SCENE = Guild

# Getting Role objects
ROLE_911 = Role
ROLE_SCENE = Role

@bot.event
async def on_ready():
    global GUILD_PORTAL
    global GUILD_911
    global GUILD_SCENE

    global ROLE_911
    global ROLE_SCENE

    # Getting Guild objects
    GUILD_PORTAL = bot.get_guild(GUILD_PORTAL_ID)
    GUILD_911 = bot.get_guild(GUILD_911_ID)
    GUILD_SCENE = bot.get_guild(GUILD_SCENE_ID)

    # Getting Role objects
    ROLE_911 = GUILD_PORTAL.get_role(ROLE_911_ID)
    ROLE_SCENE = GUILD_PORTAL.get_role(ROLE_SCENE_ID)
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    if member.guild.id == GUILD_PORTAL_ID:
        if GUILD_911.get_member(member):
            member.add_roles(ROLE_911)
        if GUILD_SCENE.get_member(member):
            member.add_roles(ROLE_SCENE)

    if member.guild.id == GUILD_911_ID:
        member.guild = GUILD_PORTAL
        await member.add_roles(ROLE_911)

    if member.guild.id == GUILD_SCENE_ID:
        member.guild = GUILD_PORTAL
        await member.add_roles(ROLE_SCENE)

@bot.event
async def on_member_remove(member):
    if GUILD_911.get_member(member) is None:
        member.guild = GUILD_PORTAL
        await member.remove_roles(ROLE_911)

    if GUILD_SCENE.get_member(member) is None:
        member.guild = GUILD_PORTAL
        await member.remove_roles(ROLE_SCENE)

@bot.tree.command(name="syncall", description="Синхронізує ролі користувачів")
async def sync(interaction):
    members_portal_list = GUILD_PORTAL.members
    member_911_list = GUILD_911.members
    member_scene_list = GUILD_SCENE.members

    add_911_role_to = [m for m in members_portal_list if m not in ROLE_911.members and m in member_911_list and not m.bot]
    remove_911_role_from = [m for m in members_portal_list if m not in member_911_list and m in ROLE_911.members and not m.bot]

    add_scene_role_to = [m for m in members_portal_list if m not in ROLE_SCENE.members and m in member_scene_list and not m.bot]
    remove_scene_role_from = [m for m in members_portal_list if m not in member_scene_list and m in ROLE_SCENE.members and not m.bot]

    for member in add_911_role_to:
        member.guild = GUILD_PORTAL
        await member.add_roles(ROLE_911)

    for member in add_scene_role_to:
        member.guild = GUILD_PORTAL
        await member.add_roles(ROLE_SCENE)

    for member in remove_911_role_from:
        member.guild = GUILD_PORTAL
        await member.remove_roles(ROLE_911)

    for member in remove_scene_role_from:
        member.guild = GUILD_PORTAL
        await member.remove_roles(ROLE_SCENE)


    await interaction.response.send_message(create_response(added_911_role_list=add_911_role_to,
                                                            removed_911_role_list=remove_911_role_from,
                                                            added_scene_role_list=add_scene_role_to,
                                                            removed_scene_role_list=remove_scene_role_from), ephemeral=True)

bot.run(TOKEN)