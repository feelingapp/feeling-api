# Feeling API

> Internal REST API for Feeling

📚 [Documentation](docs/main.md)

## How To Use

1. Install Python libraries:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Install JavaScript libraries:

```bash
npm install -g serverless
npm install
```

3. Generate the tables (make sure PostgreSQL is running):

```bash
python -m src.setup
```

4. To run the functions locally:

```bash
npm run develop
```
