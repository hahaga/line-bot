# Linebot

![web front end](./imgs/webapp.png)

# How to Run Locally

Run flask in one terminal run:

```
$ python src/app.py
```

And in another terminal run the client:

```
$ npm run dev
```

Now visit the page `http://localhost:8080/`

# pip Requirements

- `bothub-cli`

# Bothub tips

To use, make sure to configure:

```
bothub configure

# configure linebot channel
bothub channel add line --channel-id=<channel id> \
                        --channel-secret=<channel secret> \
                        --channel-access-token=<channel access token>
```

after changing things on the bot, update with:

```
bothub deploy
```