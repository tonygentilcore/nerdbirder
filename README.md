# nerdbirder

Scrapes [@nerdbirder](https://www.instagram.com/nerdbirder/) instagram posts, visualizes them by taxonomy and publishes to [thenerdbirder.com](http://thenerdbirder.com/).

If there's any interest in using this project, please let me know and I'd be happy to generalize it for others. It's currently ad hoc for my account just for expedience.

## Development

### First run setup
```sh
pip install -t lib -r requirements.txt
```

### Update graph json
```sh
./scripts/regenerate_json_cli.py
```

### View locally
```sh
dev_appserver.py app.yaml
```
http://localhost:8080/

### Deploy
```sh
gcloud app deploy
gcloud app deploy cron.yaml
```
