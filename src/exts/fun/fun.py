"""
Fun related commands.

(C) 2022-2023 - B1ue-Dev
"""

import logging
import random
import asyncio
import datetime
from requests import Session
import interactions
from interactions.ext.hybrid_commands import (
    hybrid_slash_command,
    HybridContext,
)
from bardapi import Bard
from utils.utils import get_response
from exts.core.error_handler import handle_error
from const import (
    GOOGLE_PSID,
    GOOGLE_PSIDCC,
    GOOGLE_PSIDTS,
)


session = Session()
session.cookies.set("__Secure-1PSID", GOOGLE_PSID)
session.cookies.set( "__Secure-1PSIDCC", GOOGLE_PSIDCC)
session.cookies.set("__Secure-1PSIDTS", GOOGLE_PSIDTS)
session.headers = {
    "Host": "bard.google.com",
    "X-Same-Domain": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.4472.114 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://bard.google.com",
    "Referer": "https://bard.google.com/",
}


class Fun(interactions.Extension):
    def __init__(self, client: interactions.Client) -> None:
        self.client: interactions.Client = client

    bard = Bard(token=GOOGLE_PSID, session=session, timeout=30)

    @hybrid_slash_command(
        name="coffee",
        description="Send an image of coffee.",
    )
    async def coffee(self, ctx: HybridContext) -> None:
        """Sends an image of coffee."""

        url = "https://coffee.alexflipnote.dev/random.json"
        resp = await get_response(url)
        file = resp["file"]

        image = interactions.EmbedAttachment(url=file)
        embed = interactions.Embed(
            title="Coffee ☕", color=0xC4771D, images=[image]
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="roll",
        description="Roll a dice.",
    )
    async def roll(self, ctx: HybridContext) -> None:
        """Rolls a dice."""

        dice = random.randint(1, 6)
        msg = await ctx.send("I am rolling the dice...")
        await asyncio.sleep(1.5)
        await ctx.edit(message=msg.id, content=f"The number is **{dice}**.")

    @hybrid_slash_command(
        name="flip",
        description="Flip a coin.",
    )
    async def flip(self, ctx: HybridContext) -> None:
        """Flips a coin."""

        coin = random.choice(["heads", "tails"])
        msg = await ctx.send("I am flipping the coin...")
        await asyncio.sleep(1.5)
        await ctx.edit(
            message=msg.id, content=f"The coin landed on **{coin}**."
        )

    @hybrid_slash_command(
        name="gay",
        description="Calculate the gay percentage of a user.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="user",
                description="Targeted user",
                required=False,
            ),
        ],
    )
    async def gay(self, ctx: HybridContext, user: str = None) -> None:
        """Calculates the gay percentage of a user."""

        if not user:
            user = ctx.user.username
        perc = int(random.randint(0, 100))

        embed = interactions.Embed(
            title="Gay measure tool",
            description=f"**{user}** is {perc}% gay.",
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="joke",
        description="Send a random joke.",
    )
    async def joke(self, ctx: HybridContext) -> None:
        """Sends a random joke."""

        url = "https://some-random-api.com/joke"
        resp = await get_response(url)

        embed = interactions.Embed(
            description=resp["joke"],
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="quote",
        description="Send a quote.",
    )
    async def quote(self, ctx: HybridContext) -> None:
        """Sends a quote."""

        url = "https://api.quotable.io/random"
        resp = await get_response(url)
        author = resp["author"]
        content = resp["content"]
        dateAdded = resp["dateAdded"]

        footer = interactions.EmbedFooter(text=f"Added on {dateAdded}")
        embed = interactions.Embed(
            title=f"From {author}",
            description=content,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="xkcd",
        description="Send a xkcd comic page.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.INTEGER,
                name="page",
                description="The page you want to read (if any)",
                required=False,
            ),
        ],
    )
    async def xkcd(self, ctx: HybridContext, page: int = None) -> None:
        """Sends a xkcd comic page."""

        url = "https://xkcd.com/info.0.json"
        resp = await get_response(url)
        newest = resp["num"]
        if page is None:
            page = random.randint(1, newest)
        url = "https://xkcd.com/{page}/info.0.json"
        resp = await get_response(url.format(page=page))
        if resp is None:
            return await ctx.send(
                "Invalid page. Please try again.", ephemeral=True
            )

        month = resp["month"]
        year = resp["year"]
        day = resp["day"]
        title = resp["title"]
        alt = resp["alt"]
        img = resp["img"]

        footer = interactions.EmbedFooter(
            text=f"Page {page}/{newest} • Created on {year}-{month}-{day}"
        )
        image = interactions.EmbedAttachment(url=img)
        author = interactions.EmbedAuthor(
            name=f"{title}",
            url=f"https://xkcd.com/{page}/",
            icon_url="https://camo.githubusercontent.com/8bd4217be107c9c190ef649b3d1550841f8b45c32fc0b71aa851b9107d70cdea/68747470733a2f2f6173736574732e7365727661746f6d2e636f6d2f786b63642d626f742f62616e6e6572332e706e67",
        )
        embed = interactions.Embed(
            description=alt,
            color=random.randint(0, 0xFFFFFF),
            footer=footer,
            images=[image],
            author=author,
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="dictionary",
        description="Define a word.",
        options=[
            interactions.SlashCommandOption(
                type=interactions.OptionType.STRING,
                name="word",
                description="The word you want to define",
                required=True,
            ),
        ],
    )
    async def dictionary(self, ctx: HybridContext, word: str) -> None:
        """Defines a word."""

        url = "https://some-random-api.com/dictionary"
        params = {"word": word}
        resp = await get_response(url, params=params)

        if resp is None:
            return await ctx.send(
                "No word found. Please try again.", ephemeral=True
            )

        term = resp["word"]
        definition = resp["definition"]
        if len(definition) > 4096:
            definition = definition[:4000] + "..."
        embed = interactions.Embed(
            title=f"Definition of {term}",
            description=definition,
            color=random.randint(0, 0xFFFFFF),
        )

        await ctx.send(embeds=embed)

    @hybrid_slash_command(
        name="ai",
        description="Chat with an AI.",
        aliases=["gpt"],
    )
    @interactions.slash_option(
        name="message",
        description="The message you want to send",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.cooldown(interactions.Buckets.USER, 1, 20)
    async def ai(
        self, ctx: HybridContext, *, message: interactions.ConsumeRest[str]
    ) -> None:
        """Chat with an AI."""

        await ctx.defer()
        try:
            ans: str = Fun.bard.get_answer(message)["content"]
            await ctx.send(ans)
        except Exception as e:
            await ctx.send("An unknown error occurred.")
            return await handle_error(
                self,
                error=e,
                error_time=datetime.datetime.utcnow().timestamp(),
            )


def setup(client) -> None:
    """Setup the extension."""
    Fun(client)
    logging.info("Loaded Fun extension.")