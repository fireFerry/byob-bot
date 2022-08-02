from discord.ext import commands
import discord
import cogs.utils as utils


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def support(self, ctx):
        await utils.send_embed("Support",
                               "**1.** Ask your question, don't ask to ask.\n**2.** Be patient for support. Don't mention staff, this will result in a warning.\n**3.** Don't repeat your questions, and don't put them in multiple channels.",
                               ctx)

    # port forwarding command

    @commands.command(aliases=['portforward', 'pfw'])
    async def portforwarding(self, ctx):
        await utils.send_embed("Port Forwarding",
                               "Port forwarding is done on your router, and may also be called port mapping or virtual servers. Port triggering is not the same as port forwarding. \nTo use the web-gui version of byob you need to forward ports 1337-1339 to the machine that you're hosting byob on.",
                               ctx)

    # requirements command

    @commands.command(aliases=['req'])
    async def requirements(self, ctx):
        embed = await utils.create_embed("Requirements",
                                         "requirements for byob:")
        embed.add_field(name="OS", value="A Linux distribution, preferably Ubuntu 20.04 LTS", inline=False)
        embed.add_field(name="Software", value="**1.** Python 3 & pip\n**2.** Docker", inline=False)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.message.delete()
        await ctx.send(embed=embed)

    # wsl command

    @commands.command()
    async def wsl(self, ctx):
        await utils.send_embed("Windows Subsystem for Linux",
                               "Using wsl for byob isn't supported. This means that you will receive no support if you run into issues while using byob on wsl. Wsl runs a linux terminal on Windows, and can be found as Ubuntu/Kali on the Microsoft store.",
                               ctx)

    # vps command

    @commands.command()
    async def vps(self, ctx):
        await utils.send_embed("Virtual Private Server",
                               "Byob is not recommended on a vps. Byob may require extra configuration to allow for successful connections. You also need to be able to open ports if you want to use byob, staff will not help with this.",
                               ctx)

    # executable command

    @commands.command(aliases=['exe'])
    async def executable(self, ctx):
        await utils.send_embed("Executable generation",
                               "If your executable doesn't generate correctly, here are some things you should check:\n**1.** Make sure you are using the latest version of byob and have rebooted at least once after installation.\n**2.** Run this command: sudo usermod -aG docker $USER && sudo chmod 666 /var/run/docker.sock, and reboot your system.\n**3.** If this still doesn't work, uninstall docker, run startup.sh again, and reboot your system.\n**4.** If none of the previous steps fixed the issue, a python payload can be manually compiled using pyinstaller.",
                               ctx)

    # wiki command

    @commands.command()
    async def wiki(self, ctx):
        await utils.send_embed("Wiki",
                               "web-gui wiki: https://byob.dev/guide\ncli wiki: https://github.com/malwaredllc/byob/wiki\nGitHub: https://github.com/malwaredllc/byob/",
                               ctx)


async def setup(bot):
    await bot.add_cog(Support(bot))
