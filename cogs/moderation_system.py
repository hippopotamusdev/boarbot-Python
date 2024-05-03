import discord
from discord import Embed, Color
from discord.commands import slash_command, Option
from discord.ext import commands

import aiosqlite
import datetime

import traceback

class ModerationSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("mod_sys.db") as db:
            await db.executescript(
                """
                CREATE TABLE IF NOT EXISTS WarnList (
                warn_id INTEGER PRIMARY KEY,
                mod_id INTEGER,
                guild_id INTEGER,
                user_id INTEGER,
                warns INTEGER DEFAULT 0,
                warn_reason TEXT,
                warn_time TEXT
                )
                """
            )


    @slash_command(description="Кикает пользователя")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def kick(
        self, 
        ctx, 
        member: Option(discord.Member, "Укажите пользователя", required=True), 
        reason: Option(str, "Укажите причину", required=False, default="Причина не указана")
        ):
        
        kick_embed = discord.Embed(
            title=f"`✅` Кик {member.name}#{member.discriminator}",
            description=f"Пользователь {member.mention} Был кикнут на сервере **{ctx.guild.name}**.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        kick_embed.add_field(name="Администратор:", value=f"{ctx.author}", inline=False)
        kick_embed.add_field(name="Причина:", value=f"{reason}", inline=False)
        kick_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        kick_embed.set_thumbnail(url=member.avatar.url)
        kick_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        try:
            await member.kick(reason=reason)
        except (discord.Forbidden, discord.HTTPException) as e:
            
            error_embed = discord.Embed(
                title="`⚠️` Ошибка",
                description=f"Произошла ошибка.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            error_embed.add_field(name=f"Произошла ошибка при кике пользователя: {member.mention}.", value=f"Пожалуйста, повторите попытку позже.", inline=False)
            error_embed.add_field(name=f"Код ошибки:", value=f"```{e}```", inline=False)
            error_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
            error_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
            
            print(e)
            await ctx.respond(embed=error_embed, ephemeral=True)
            return
        await ctx.respond(embed=kick_embed, ephemeral=False)


    @slash_command(description="Блокирует игрока на сервере")
    @discord.default_permissions(ban_members=True)
    @discord.guild_only()
    async def ban(
        self, 
        ctx, 
        member: Option(discord.Member, "Укажите пользователя", required=True), 
        reason: Option(str, "Укажите причину", required=False, default="Причина не указана")
        ):
        
        ban_embed = discord.Embed(
            title=f"`✅` Блокировка {member.name}#{member.discriminator}",
            description=f"Пользователь {member.mention} был заблокирован на сервере **{ctx.guild.name}**.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        ban_embed.add_field(name="Администратор:", value=f"{ctx.author}", inline=False)
        ban_embed.add_field(name="Причина:", value=f"{reason}", inline=False)
        ban_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        ban_embed.set_thumbnail(url=member.avatar.url)
        ban_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        try:
            await member.ban(reason=reason)
        except (discord.Forbidden, discord.HTTPException) as e:
            
            error_embed = discord.Embed(
                    title="`⚠️` Ошибка",
                    description=f"Произошла ошибка.",
                    color=discord.Color.green(),
                    timestamp=datetime.datetime.utcnow()
                )
            error_embed.add_field(name=f"Произошла ошибка при блокировке пользователя: {member.mention}.", value=f"Пожалуйста, повторите попытку позже.", inline=False)
            error_embed.add_field(name=f"Код ошибки:", value=f"```{e}```", inline=False)
            error_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
            error_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
            print(e)
            await ctx.respond(embed=error_embed, ephemeral=True)
            return
        await ctx.respond(embed=ban_embed, ephemeral=False)


    @slash_command(description="Разблокировывает пользователя")
    @discord.default_permissions(ban_members=True)
    @discord.guild_only()
    async def unban(
        self, 
        ctx, 
        member: Option(discord.Member, "Укажите пользователя", required=True), 
        reason: Option(str, "Укажите причину снятия бана", required=False, default="Причина не указана")
        ):
        
        unban_embed = discord.Embed(
            title=f"`✅` Разблокировка {member.name}#{member.discriminator}",
            description=f"Пользователь {member.mention} был разблокирован на сервере **{ctx.guild.name}**",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        unban_embed.add_field(name="Администратор:", value=f"{ctx.author}", inline=False)
        unban_embed.add_field(name="Причина:", value=f"{reason}", inline=False)
        unban_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        unban_embed.set_thumbnail(url=member.avatar.url)
        unban_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        try:
            ban_entry = await ctx.guild.fetch_ban(member)
            await ctx.guild.unban(ban_entry.user, reason=reason)
        except (discord.Forbidden, discord.HTTPException) as e:
            
            error_embed = discord.Embed(
                title="`⚠️` Ошибка",
                description=f"Произошла ошибка.",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
            error_embed.add_field(name=f"Произошла ошибка при разблокировке пользователя: {member.mention}.", value=f"Пожалуйста, повторите попытку позже.", inline=False)
            error_embed.add_field(name=f"Код ошибки:", value=f"```{e}```", inline=False)
            error_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
            error_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
            
            print(e)
            await ctx.respond(embed=error_embed, ephemeral=True)
            return
        await ctx.respond(embed=unban_embed, ephemeral=False)

          
    @slash_command(description="Выдаёт предупреждение пользователю")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def warn(
        self, 
        ctx, 
        member: Option(discord.Member, "Укажите пользователя", required=True), 
        reason: Option(str, "Укажите причину предупреждения", required=False, default="Причина не указана")
        ):

        warn_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        async with aiosqlite.connect("mod_sys.db") as db:
            await db.execute(
                "INSERT INTO WarnList (user_id, guild_id, warns, warn_reason, mod_id, warn_time) VALUES (?, ?, ?, ?, ?, ?)",
                (member.id, ctx.guild.id, 1, reason, ctx.author.id, warn_time),
            )
            await db.commit()

            async with db.execute(
                "SELECT warn_id FROM WarnList WHERE user_id = ? AND guild_id = ? ORDER BY warn_id DESC LIMIT 1",
                (member.id, ctx.guild.id),
            ) as cursor:
                row = await cursor.fetchone()
                warn_id = row[0]
                
        warnUser_embed = discord.Embed(
            title="`⚠️` Предупреждение",
            description=f"Ты был предупреждён на сервере **{ctx.guild.name}**",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        warnUser_embed.add_field(name="Администратор:", value=f"```{ctx.author}```", inline=False)
        warnUser_embed.add_field(name="ID Предупреждения:", value=f"```{warn_id}```", inline=False)
        warnUser_embed.add_field(name="Причина:", value=f"```{reason}```", inline=False)
        warnUser_embed.set_author(name=f"{ctx.guild.name}", icon_url=member.avatar.url)
        warnUser_embed.set_thumbnail(url=member.avatar.url)
        warnUser_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        warn_embed = discord.Embed(
            title="`✅` Предупреждение",
            description=f"Пользователь {member.mention} Получил варн на сервере **{ctx.guild.name}**.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        warn_embed.add_field(name="Администратор:", value=f"```{ctx.author}```", inline=False)
        warn_embed.add_field(name="ID Предупреждения:", value=f"```{warn_id}```", inline=False)
        warn_embed.add_field(name="Причина:", value=f"```{reason}```", inline=False)
        warn_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.user.avatar.url)
        warn_embed.set_thumbnail(url=member.avatar.url)
        warn_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        await member.send(embed=warnUser_embed)
        await ctx.respond(embed=warn_embed, ephemeral=False)


    @slash_command(description="Снимает предупреждение")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def unwarn(
        self, 
        ctx, 
        member: Option(discord.Member, "Укажите пользователя, у которого хотите снять предупреждение", required=True),
        warn_id: Option(int, "Укажите ID предупреждения пользователя", required=True),
        reason: Option(str, "Укажите причину снятия предупреждения", required=False, default="Причина не указана")
        ):
        
        unwarnUser_embed = discord.Embed(
            title="`🍀` Снятие предупреждения",
            description=f"Предупреждение от тебя с сервера **{ctx.guild.name}** было отозвано.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        unwarnUser_embed.add_field(name="Администратор:", value=f"```{ctx.author}```", inline=False)
        unwarnUser_embed.add_field(name="ID Предупреждения:", value=f"```{warn_id}```", inline=False)
        unwarnUser_embed.add_field(name="Причина:", value=f"```{reason}```", inline=False)
        unwarnUser_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
        unwarnUser_embed.set_thumbnail(url=ctx.guild.icon.url)
        unwarnUser_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        unwarn_embed = discord.Embed(
            title=f"`✅` Снятие предупреждения",
            description=f"Предупреждение с {member.mention} было снято на сервере **{ctx.guild.name}**.",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        )
        unwarn_embed.add_field(name="Администратор:", value=f"```{ctx.author}```", inline=False)
        unwarn_embed.add_field(name="ID Предупреждения:", value=f"```{warn_id}```", inline=False)
        unwarn_embed.add_field(name="Администратор:", value=f"```{reason}```", inline=False)
        unwarn_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.bot.user.avatar.url)
        unwarn_embed.set_thumbnail(url=member.avatar.url)
        unwarn_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
        
        
        async with aiosqlite.connect("mod_sys.db") as db:
            await db.execute(
                "DELETE FROM WarnList WHERE user_id = ? AND guild_id = ? AND warn_id = ?",
                (member.id, ctx.guild.id, warn_id)
            )
            await db.commit()
 
        await member.send(embed=unwarnUser_embed)
        await ctx.respond(embed=unwarn_embed, ephemeral=False)


    @slash_command(description="Отображение всех предупреждений пользователя с сервера")
    @discord.default_permissions(kick_members=True)
    @discord.guild_only()
    async def warnings(self, ctx, member: discord.Member):

        warns_info = []
        async with aiosqlite.connect("mod_sys.db") as db:
            async with db.execute("SELECT warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time FROM WarnList WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id)) as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    warn_id, mod_id, guild_id, user_id, warns, warn_reason, warn_time = row
                    warn_time = datetime.datetime.strptime(warn_time, '%Y-%m-%d %H:%M:%S')
                    warns_info.append(f"**ID Предупреждения:** __{warn_id}__ | **Время предупреждения AM:** {warn_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    warns_info.append(f"**Администратор:** <@{mod_id}> | **ID - Адм**: __{mod_id}__\n")
                    warns_info.append(f"**> Причина:**\n```{warn_reason}```")
                    warns_info.append("\n")

        if not warns_info:
            warnings_embed = discord.Embed(
                title="`⚠️` Пользователь не имеет предупреждений!",
                description=f"Пользователь: {member.mention}",
                color=discord.Color.red(),
            )
        else:
            warnings_embed = discord.Embed(
                title=f"`⚠️` Список предупреждений пользователя {member.name}#{member.discriminator}",
                description=f"__**Список предупреждений**__",
                color=discord.Color.green(),
                timestamp=datetime.datetime.utcnow()
            )
        warnings_embed.add_field(name="", value="".join(warns_info), inline=False)
        warnings_embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        warnings_embed.set_thumbnail(url=member.avatar.url)
        warnings_embed.set_footer(text=f"{ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)

        await ctx.respond(embed=warnings_embed, ephemeral=False)
        
        
    @slash_command(description="Удаляйте сообщения с канала")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount: Option(int, "Кол-во сообщений (Min 1 | Max 100)", required=True)):
        amount = amount+1
        
        if amount > 101:
            
            error_embed = discord.Embed(
            title="`❌` Ошибка!",
            description="`Вы указали >100 сообщений!`",
            color=discord.Color.red(),
            timestamp=datetime.datetime.utcnow()
            )
            error_embed.set_thumbnail(url=ctx.guild.icon.url)
            error_embed.set_footer(text=f"| {ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
            error_embed.set_author(name=f"Очистка", icon_url=ctx.bot.user.avatar.url)
    
            await ctx.respond(embed=error_embed, delete_after=6, ephemeral=True)
            
        else:
            deleted = await ctx.channel.purge(limit=amount)
            
            success_embed = discord.Embed(
            title="`✅` Успешно!",
            description="**{}** `Удалено сообщений!`".format(len(deleted)),
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
            )
            success_embed.set_thumbnail(url=ctx.guild.icon.url)
            success_embed.set_footer(text=f"| {ctx.bot.user.name}#{ctx.bot.user.discriminator}", icon_url=ctx.bot.user.avatar.url)
            success_embed.set_author(name=f"Очистка", icon_url=ctx.bot.user.avatar.url)
                    
            await ctx.respond(embed=success_embed, delete_after=3, ephemeral=True)
        
def setup(bot):
    bot.add_cog(ModerationSystem(bot))
