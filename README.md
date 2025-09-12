## Development setup with Docker
This project ships with a `docker-compose.yml` that runs both the backend (FastAPI) and the frontend (React).

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine
- An OpenAI API key (you can run w/o it, but AI won't work)

### Environment variables
Create a `.env` file in the repo root:

```bash
OPENAI_API_KEY=sk-yourkeyhere
HOST_BACKEND_ABSOLUTE_DIR=/absolute/path/to/backend/dir
```

The last variable is optional, `docker compose` will fall back to a default value if unset. However, it is recommended to set it for a better debugging experience.

### Pre-commit hooks
As the name implies, these hooks (scripts) are run before `git commit`. They won't allow you to commit your changes unless all tests pass. Some of them just fix formatting (e.g., remove trailing whitespaces), while others flag unusud variables, incorrect return types, etc. The same hooks are also run automatically on GitHub.

#### Install pre-commit hook
Copy the `pre-commit` hook from `.dev-setup/pre-commit` to `.git/hooks` and make it executable. E.g., on Linux:

```bash
cp .dev-setup/pre-commit .git/hooks
cmod +x .git/hooks/pre-commit
```

### Start the stack
From the project root:

```bash
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000 (FastAPI docs at /docs)

Edits to your code are reflected immediately because the repo is mounted into the containers.

### Stop the stack

```bash
docker compose down
```
