# BEM2Deployment - API Deployment and CI/CD Pipeline

This project deploys the Mechanic Shop API to Render and uses GitHub Actions for continuous integration and deployment.

## Local Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file (never commit this file) and set:

```bash
SECRET_KEY=your-local-secret-key
DATABASE_URL=sqlite:///mechanic_shop.db
SWAGGER_HOST=127.0.0.1:5000
```

Run with Flask CLI:

```bash
flask --app flask_app run
```

## Production Deployment (Render)

1. Create a managed PostgreSQL database in Render.
2. Create a Web Service from this GitHub repo.
3. Set environment variables in Render:
	- `SECRET_KEY`
	- `DATABASE_URL`
	- `SWAGGER_HOST` (example: `your-service-name.onrender.com` without `https://`)
4. Set the Render start command:

```bash
gunicorn flask_app:app
```

## Swagger Requirements

- `host` should be your live Render base URL without `https://`.
- `schemes` should be `https` in production.

This app uses config values to support both local and production Swagger behavior.

## Run Tests

```bash
python -m unittest discover tests
```

## CI/CD Pipeline

GitHub Actions workflow file:

- `.github/workflows/main.yaml`

Pipeline jobs:

- `build`: install dependencies and validate code compiles.
- `test`: run unit tests.
- `deploy`: trigger Render deploy only after tests pass.

Required GitHub repository secrets:

- `SERVICE_ID` (Render service ID)
- `RENDER_API_KEY` (Render API key)

## Presentation Submission Reminder

- Record a video under 5 minutes.
- Be visible on camera while presenting.
- Explain what the project does, how it works (high level), and demo it running.
- Upload the video directly to Disco.
- Submit the GitHub repository URL in the submission field.
