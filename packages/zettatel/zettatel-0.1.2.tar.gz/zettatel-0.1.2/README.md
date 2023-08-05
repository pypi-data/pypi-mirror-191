# zettatel

a python package to help send messages using the Zettatel API

## Usage

to use this package, you can either git clone or install using pip:

```
pip install zettatel
```

This will install all the required packages. Next we need to initialize the packacge as shown below:

```
from zettatel.app import Client

zettatel = Client(
    "username",
    "password",
    "senderId"
)
```

To send a quick message use the following sample:

```
zettatel.send_quick_SMS('254712345678', "this is test from python package")
```

To send a scheduled quick sms :

```
zettatel.send_quick_smartlink_sms(
    '254712345678', "this is test from python package",scheduleTime = '2023-09-16 13:24')
```
