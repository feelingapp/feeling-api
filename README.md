# Feeling API

> Internal REST API for Feeling

📚 [Documentation](docs/main.md)

## How To Use

1. Make sure you have Docker running. To start the database:

```bash
npm run start-database
```

2. Install JavaScript libraries:

```bash
npm install -g serverless
npm install
```

3. Install Python libraries:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Generate the database tables:

```bash
python -m src.setup
```

5. To run the functions locally:

```bash
npm run develop
```

6. To stop the database when you're finished:

```bash
npm run stop-database
```
