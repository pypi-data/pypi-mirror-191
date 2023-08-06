<p align="center">
    <a href="https://github.com/agram/agram">
        <img src="https://docs.agram.org/_static/agram.png" alt="agram" width="128">
    </a>
    <br>
    <b>Telegram MTProto API Framework for Python</b>
    <br>
    <a href="https://selamarket.shop">
        Homepage
    </a>
    •
    <a href="https://selamarket.shop">
        Documentation
    </a>
    •
    <a href="https://selamarket.shop">
        Releases
    </a>
    •
    <a href="https://t.me/XTIORY">
        News
    </a>
</p>

## agram

> Elegant, modern and asynchronous Telegram MTProto API framework in Python for users and bots

``` python
from agram import Client, filters

app = Client("my_account")


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from agram!")


app.run()
```

**agram** is a modern, elegant and asynchronous [MTProto API](https://docs.agram.org/topics/mtproto-vs-botapi)
framework. It enables you to easily interact with the main Telegram API through a user account (custom client) or a bot
identity (bot API alternative) using Python.


### Key Features

- **Ready**: Install agram with pip and start building your applications right away.
- **Easy**: Makes the Telegram API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by [TgCrypto](https://github.com/agram/tgcrypto), a high-performance cryptography library written in C.  
- **Type-hinted**: Types and methods are all type-hinted, enabling excellent editor support.
- **Async**: Fully asynchronous (also usable synchronously if wanted, for convenience).
- **Powerful**: Full access to Telegram's API to execute any official client action and more.

### Installing

``` bash
pip3 install agram
```

### Resources

- Check out the docs at https://selamarket.shop to learn more about agram, get started right
away and discover more in-depth material for building your client applications.
- Join the official channel at https://t.me/XTIORY and stay tuned for news, updates and announcements.
