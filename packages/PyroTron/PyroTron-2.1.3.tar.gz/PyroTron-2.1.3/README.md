## PyroTron

> Smart Fork of [Pyrogram](https://github.com/pyrogram/pyrogram)

``` python
from pyrogram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from PyroTron!")


app.run()
```

**PyroTron** is a fork of pyrogram, this fork consists of extra high level api methods
which weren't added by Dan (Owner of pyrogram) in pyrogram, all credits of this library goes to him.

### Installing

``` bash
pip3 install PyroTron
```

### Difference in Pyrogram & PyroTron

- There is no difference in Pyrogram & PyroTron, all the methods in Pyrogram
are added in PyroTron, including some new extra methods which are not available
in Pyrogram, both libraries are same.

### Contact

- Join the official channel of PyroTron https://t.me/PyroTronOfficial and stay tuned for news, updates and announcements.
