{
    "text" : {
        "one" : ":one:",
        "two" : ":two:",
        "three" : ":three:",
        "four" : ":four:",
        "five" : ":five:",
        "six" : ":six:",
        "seven" : ":seven:",
        "eight" : ":eight:",
        "nine" : ":nine:",
        "ten" : ":keycap_ten:",
        "ocean" : ":ocean:",
        "bomb" : ":bomb:",
        "x" : ":x:",
        "fire" : ":fire:",
        "boats" : [":motorboat:", ":rowboat:", ":speedboat:", ":sailboat:"]
    },
    "ascii" : {
        "one" : "1\u20e3",
        "two" : "2\u20e3",
        "three" : "3\u20e3",
        "four" : "4\u20e3",
        "five" : "5\u20e3",
        "six" : "6\u20e3",
        "seven" : "7\u20e3",
        "eight" : "8\u20e3",
        "nine" : "9\u20e3",
        "ten" : "\\U0001f51f",
        "ocean" : "\\U0001f30a",
        "bomb" : "\\U0001f4a3",
        "x" : "\\u274c",
        "fire" : "\\U0001f525",
        "boats" : ["\\U0001f6e5", "\\U0001f6a3", "\\U0001f6a4", "\\u26f5"]
    }
}

!!exec
em = discord.Embed(title=f'{ctx.message.author.name}', description="""Score: 0
:speedboat: :one: :two: :three: :four: :five: :six: :seven: :eight: :nine: :keycap_ten:
:one: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:two: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:three: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:four: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:five: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:six: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:seven: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:eight: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:nine: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
:keycap_ten: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean: :ocean:
GameHash:
27084269535026566901
87914038177605278889
If you are stuck
use !!help battleship""")
await bot.say(embed=em)