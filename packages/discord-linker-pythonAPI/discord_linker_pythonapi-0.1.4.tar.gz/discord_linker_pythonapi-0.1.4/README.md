# Description
This package allows python to communicate with a wordpress plugin "discord-linker" that allows you to link discord with wordpress.

This api is used to create discord bots that can communicate with the website and perform actions on behalf of the discord users.

# Requirements
* requests => ```pip install requests```

# Installation
```
pip install discord-linker-pythonAPI
```

# Usage
```
from discord_linker_pythonAPI.wordpress_client import WP_Client

wpclient = WP_Client("<URL>", "<Username>", "<Application Password>")
```


# Links
* **Documentation**: https://vbrawl.github.io/discord-linker-pythonAPI/
* **PyPi**: https://pypi.org/project/discord-linker-pythonAPI/