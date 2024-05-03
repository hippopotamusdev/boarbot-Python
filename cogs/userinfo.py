from discord import slash_command
import discord
import ezcord
from ezcord import View

class Userinfo(ezcord.Cog, emoji="<:info:1147664192325812406>"):

    @slash_command(description="Просматривайте информацию о пользователе на сервере")
    @discord.option("user",discord.Member,description="Выберите пользователя, о котором должна быть информация")
    async def user(self,ctx:discord.ApplicationContext, member:discord.Member=None):
        if member is None:
            member = ctx.author
        if member not in ctx.guild.members:
            await ctx.respond("Этого пользователя нет на сервере",ephemeral=True)
            return
        if isinstance(member, discord.Member):  # Überprüfe, ob member ein Mitglied ist
            activities = []
            for activity in member.activities:
                if isinstance(activity, discord.Spotify):
                    txt = f'Spotify: [{activity.artist} - {activity.title}]({activity.track_url})'
                elif isinstance(activity, discord.Game):
                    txt = f'Играет: {activity.name}'
                elif isinstance(activity, discord.Streaming):
                    txt = f'Транслирует: [{activity.twitch_name} - {activity.game}]({activity.url})'
                elif isinstance(activity, discord.CustomActivity):
                    txt = f'Status: {activity.name}'
                else:
                    txt = f'{activity.name}: {activity.details}'
                activities.append(txt)
        rlist = []
        for role in member.roles:
            rlist.append(str(role.mention))
        rlist.reverse()
        embed = discord.Embed(title=f"Информация о пользователе {member.display_name}", color=0x5965f2)
        embed.add_field(name="Username:", value=f"{member}")
        embed.add_field(name="Псевдоним:", value=f"{member.nick}" if member.nick else "не имеет псевдонима",inline=True)
        embed.add_field(name="Отображаемое имя:", value=f"{member.display_name}")
        embed.add_field(name="hex код баннера:", value=f"{member.colour}")
        embed.add_field(name="Упоминание:", value=f"{member.mention}")
        embed.add_field(name='Статус:', value=member.status, inline=False)
        embed.add_field(name="Бустер:", value=f"Да<t:{int(member.premium_since.timestamp())}:F>" if member.premium_since else "Нет")
        embed.add_field(name="Высшая роль:", value=f"{member.top_role.mention}")
        embed.add_field(name="Бот:", value=f'{("Ja" if member.bot else "Nein")}')
        embed.add_field(name="Присоеденился на сервер:", value=f"<t:{int(member.joined_at.timestamp())}:F>")
        embed.add_field(name="Зарегестрировался в дискорде:", value=f"<t:{int(member.created_at.timestamp())}:F>")
        embed.add_field(name=f"Роли: {len(member.roles) - 1}", value=','.join(rlist),inline=False)
        embed.add_field(name="Замьючен?",value=f"Да" if member.timed_out else "Нет")
        banner_user = await self.bot.fetch_user(member.id)
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            pass
        if activities:
            embed.add_field(name='Деятельностей', inline=False, value='\n'.join(activities))
        embed.set_author(name=f"{member}", icon_url=f"{member.display_avatar}")
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(text=f'Запрошенно от {ctx.user.name} • {ctx.user.id}', icon_url=ctx.user.display_avatar)
        await ctx.respond(embed=embed,view=Userbutton(self,ctx,member,ctx.user))


def setup(bot: discord.Bot):
    bot.add_cog(Userinfo(bot))

class Userbutton(View):
    def __init__(self,bot,ctx,member,user) -> None:
        self.bot = bot
        self.ctx = ctx
        self.member = member
        self.user = user
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🔰 Домой", style=discord.ButtonStyle.green, custom_id="info")
    async def info(self, button,ctx: discord.Interaction):
        if self.member is None:
            self.member = self.ctx.author
        if isinstance(self.member, discord.Member):
            activities = []
            for activity in self.member.activities:
                if isinstance(activity, discord.Spotify):
                    txt = f'Spotify: [{activity.artist} - {activity.title}]({activity.track_url})'
                elif isinstance(activity, discord.Game):
                    txt = f'Играет: {activity.name}'
                elif isinstance(activity, discord.Streaming):
                    txt = f'Транслирует: [{activity.twitch_name} - {activity.game}]({activity.url})'
                elif isinstance(activity, discord.CustomActivity):
                    txt = f'Status: {activity.name}'
                else:
                    txt = f'{activity.name}: {activity.details}'
                activities.append(txt)
        rlist = []
        for role in self.member.roles:
            rlist.append(str(role.mention))
        rlist.reverse()
        embed = discord.Embed(title=f"Информация о пользователе {member.display_name}", color=0x5965f2)
        embed.add_field(name="Username:", value=f"{member}")
        embed.add_field(name="Псевдоним:", value=f"{member.nick}" if member.nick else "не имеет псевдонима",inline=True)
        embed.add_field(name="Отображаемое имя:", value=f"{member.display_name}")
        embed.add_field(name="hex код баннера:", value=f"{member.colour}")
        embed.add_field(name="Упоминание:", value=f"{member.mention}")
        embed.add_field(name='Статус:', value=member.status, inline=False)
        embed.add_field(name="Бустер:", value=f"Да<t:{int(member.premium_since.timestamp())}:F>" if member.premium_since else "Нет")
        embed.add_field(name="Высшая роль:", value=f"{member.top_role.mention}")
        embed.add_field(name="Бот:", value=f'{("Ja" if member.bot else "Nein")}')
        embed.add_field(name="Присоеденился на сервер:", value=f"<t:{int(member.joined_at.timestamp())}:F>")
        embed.add_field(name="Зарегестрировался в дискорде:", value=f"<t:{int(member.created_at.timestamp())}:F>")
        embed.add_field(name=f"Роли: {len(member.roles) - 1}", value=','.join(rlist),inline=False)
        embed.add_field(name="Замьючен?",value=f"Да" if member.timed_out else "Нет")
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            pass
        if activities:
            embed.add_field(name='Деятельность', inline=False, value='\n'.join(activities))
        embed.set_thumbnail(url=self.member.display_avatar)
        await ctx.response.edit_message(embed=embed)

    
    @discord.ui.button(label="Аватарка", style=discord.ButtonStyle.gray, custom_id="avatar")
    async def avatar(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Ты не выполнил команду",ephemeral=True)
        embed = discord.Embed(title="Аватарка {}".format(self.member.display_name))
        embed.set_image(url=self.member.display_avatar)
        await ctx.response.edit_message(embed=embed)
    
    @discord.ui.button(label="Баннер", style=discord.ButtonStyle.blurple, custom_id="banner")
    async def banner(self, button,ctx: discord.Interaction):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Ты не выполнил команду",ephemeral=True)
        
        embed = discord.Embed(title="Баннер {}".format(self.member.display_name))
        if self.member.bot:
            embed.add_field(name=" ",value="У ботов нет баннера")
            return await ctx.response.edit_message(embed=embed)
        banner_user = await ctx.client.fetch_user(self.member.id)
        try:
            embed.set_image(url=banner_user.banner.url)
        except AttributeError:
            embed.add_field(name=" ",value="У этого пользователя нет баннера")
        await ctx.response.edit_message(embed=embed)

    @discord.ui.button(label="Права", style=discord.ButtonStyle.red, custom_id="berechtigungen")
    async def berechtigungen(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Ты не выполнил команду",ephemeral=True)
        
        embed = discord.Embed(title="Права {}".format(self.member.display_name))
        embed.add_field(name="Права",value=",".join([str(perm[0]) for perm in self.member.guild_permissions if perm[1]]))
        await ctx.response.edit_message(embed=embed)


    @discord.ui.button(label="Роли", style=discord.ButtonStyle.blurple, custom_id="Rollen")
    async def rollen(self, button,ctx: discord.ApplicationContext):
        if self.user.id != ctx.user.id:
            return await ctx.respond("Ты не выполнил команду",ephemeral=True)
        rlist = []
        for role in self.member.roles:
            if role.name == "@everyone":
                continue
            rlist.append(str(role.mention))
        embed = discord.Embed(title="Роли {}".format(self.member.display_name))
        if len(rlist) == 0:
            embed.add_field(name="Роли",value="У этого пользователя нет ролей")
            return await ctx.response.edit_message(embed=embed)
        embed.add_field(name=f"Роли: {len(self.member.roles) - 1}", value=','.join(rlist),inline=False)

        await ctx.response.edit_message(embed=embed)