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
npm install -g serverless@1.52.0
npm install
```

3. Install Python libraries:

On Unix:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python3 -m venv venv
.\venv\scripts\activate.bat
pip install -r requirements.txt
```

4. Generate the database tables:

```bash
python -m src.setup --generate-data
```

Note: `--generate-data` prepopulates the database with mock data.

5. To run the functions locally:

```bash
npm run develop
```

6. To stop the database when you're finished:

```bash
npm run stop-database
```
