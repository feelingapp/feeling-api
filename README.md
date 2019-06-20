# Feeling API

> Internal REST API for Feeling

📚 [Documentation](docs/main.md)

## How To Use

1. Make sure Postgres is running with the uuid-ossp extension. Run the following on your Postgres server to install the extension:

```sql
CREATE EXTENSION "uuid-ossp";
```

2. Install Python libraries:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Install JavaScript libraries:

```bash
npm install -g serverless
npm install
```

4. Generate the tables:

```bash
python -m src.setup
```

5. To run the functions locally:

```bash
npm run develop
```
