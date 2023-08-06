<h1>Pyrubi 1.4.1<h1/>

> Pyrubi is a powerful library for building self robots in Rubika

<p align='center'>
    <img src='https://iili.io/HIjPRS9.jpg' alt='Pyrubi Library 1.4.1' width='356'>
    <a href='https://github.com/AliGanji1/pyrubi'>GitHub</a>
</p>

<hr>

**Example:**
``` python
from pyrubi import Bot, Message

bot = Bot('TOKEN')

for msg in bot.on_message():
    m = Message(msg)
    if m.text() == 'Hello':
        bot.reply(msg, 'Hello from Pyrubi Library')
```

<hr>

### Features

**Fast**, **Easy**, **Async**, **Powerful**

<hr>

### Installing

``` bash
python -m pip install -U pyrubi
```