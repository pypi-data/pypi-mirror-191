## Fyers Token Generator

```
from fyers_token_manager import FyersApiBuilder
```

```
config = {
  "username": "<USERNAME>",
  "password": "<PASSWORD>",
  "pin": "<PIN>",
  "client_id": "<CLIENT_ID>",
  "secret_key": "<SECRET_KEY>",
  "redirect_uri": <REDIRECT_URL>
}
```

#### Initialization

```
from fyers_api import accessToken, fyersModel
from fyers_api.Websocket import ws

fyersApiBuilder = FyersApiBuilder(config=config, accessToken=accessToken, fyersModel=fyersModel, ws=ws)
```

#### HTTP Client

- fyersApiBuilder.client.get_profile()
- fyersApiBuilder.client.history(payload)

#### WebSocket Client

- fyersApiBuilder.ws_client.subscribe(payload)
