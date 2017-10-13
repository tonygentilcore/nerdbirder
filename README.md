# nerdbirder

## Development

### First run setup
```sh
pip install -r requirements.txt
```

### Update graph json
```sh
./scripts/taxonomy.py
```

### View locally
```sh
dev_appserver.py app.yaml
```
http://localhost:8080/

### Deploy
```sh
gcloud app deploy
```
