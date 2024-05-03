import discord
from discord.ext import commands, tasks
from discord.commands import slash_command, message_command, user_command, Option
import ezcord

class Ticket(ezcord.Cog, emoji="🎫"):

# Ticket System

    @slash_command()
    @discord.default_permissions(administrator=True)
    async def ticket(self, ctx):
        embed3 = discord.Embed(
            title="Заявка в стафф",
            description=f"Перед подачей заявки, [__ознакомьтесь__ с её __правилами__ и __условиями__ подачи.](https://telegra.ph/Pravila-podachi-zayavki-v-staff-05-01)",
            color=discord.Color.dark_blue(),
        )

        await ctx.send(embed=embed3, view=ANView())
        await ctx.respond("Заявка была создана", ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ANView())
        self.bot.add_view(ANClose())


class ANView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Подать заявку", style=discord.ButtonStyle.primary, emoji="🎟️", custom_id="ticket")
    async def button_callback1(self, button, interaction: discord.Interaction):

        ### Authorizations for the new ticket channel

        staff_role = interaction.guild.get_role(1218533357470613504)
        username = interaction.user.name

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        ### Ticket message in the new ticket channel

        embed = discord.Embed(
            title="Заявка стафф",
            description=f"{username} создал заявку.\n {staff_role.mention}",
            color=discord.Color.dark_blue(),
        )

        embed.set_footer(text="Evatable.ru - Сервер где тебя ценят!.")

        ### Create ticket channel

        ticket_channel = await interaction.guild.create_text_channel(f"Стафф-{username}", category=interaction.channel.category, overwrites=overwrites)
        await ticket_channel.send(embed=embed, view=ANClose())

        ### Confirmation message

        embed2 = discord.Embed(
            title="Заявка в стафф",
            description=f"Был создан канал: {ticket_channel.mention}",
            color=discord.Color.purple(),
        )

        await interaction.response.send_message(embed=embed2, ephemeral=True)

class ANClose(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Закрыть тикет", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close")
    async def button_callback1(self, button, interaction: discord.Interaction):

        staff_role = interaction.guild.get_role(1218533357470613504)
        if staff_role not in interaction.user.roles:
            await interaction.response.send_message("У вас нет разрешения на закрытие этого тикета.", ephemeral=True)
            return

        ### Close ticket

        await interaction.channel.delete()

        ### Confirmation message

        embed = discord.Embed(
            title="Evatable.ru",
            description=f"Ваш тикет был закрыт.",
            color=discord.Color.blue(),
        )

        await interaction.user.send(embed=embed)

def setup(bot: discord.Bot):
    bot.add_cog(Ticket(bot))