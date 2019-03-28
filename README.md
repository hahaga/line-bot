# Linebot

![web front end](./imgs/webapp.png)

## Instructions to get started:

To get the project running, you will need to install these dependencies:

# Requirements

Python: 
* [Python 3.6+](https://www.python.org/downloads/)
* pipenv

If you don't have pipenv then run this command:
```
pip install pipenv
```
Run this command in the root of the project folder:
```
pipenv shell
```

Node:
* [Node](https://nodejs.org/en/download/)

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

# How to run deploy through bothub

First install bothub-cli
```
$ pip install bothub-cli
```
Be sure to get the needed credentials and  put it in the .bothub folder
```
mkdir ~/.bothub
```
Navigate to the MyBot directory
```
cd MyBot
```

```
$ bothub deploy
```
Successfully deploying will allow you to add the bot by scanning this QR code

Message your new friend, "@Fortune Bot fortune!" to test it out
![QR Code](./imgs/linebot-QR.png)