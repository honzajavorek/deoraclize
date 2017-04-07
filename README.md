# Deoraclize API

[![Build Status](https://travis-ci.org/honzajavorek/deoraclize.svg?branch=master)](https://travis-ci.org/honzajavorek/deoraclize)

API which provides you with explanations of abbreviations and acronyms used in Oracle.

## Usage

```
curl http://deoraclize.herokuapp.com/search?q=OPC
```

See full rendered [API docs](http://docs.deoraclize.apiary.io) for further details. The root URL of the API app redirects to the API docs, by the way.

## Contribute

- 📝 [Contribute your own terms](https://github.com/honzajavorek/deoraclize/wiki/Deoraclize)
- 📐 [Improve API design](https://github.com/honzajavorek/deoraclize/blob/master/deoraclize-apiary.apib)
- 👩‍💻 [Improve the Python Flask app](https://github.com/honzajavorek/deoraclize/blob/master/app.py)

## Why not as a Slack bot?

Because I tried and it was PITA to write it. I wanted to have this done very quickly and for me that means this needs to be a Python app. Benefits: You can integrate this not only with your Slack, but with anything you like!
