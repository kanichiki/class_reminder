# class_reminder

## Usage

以下の内容で`config.ini`を作ってください
```
[LINE]
channel_access_token = {your_access_token}
channel_secret = {your_secret}
```

以下のコマンドを打つとport5000でflaskが起動します。
```
python main.py
```

ngrokを使って5000番をグローバルに開放し、そのURLをLINE DevelopersのWebhook URLに貼ってあげてください。
```
ngrok http 5000
```
