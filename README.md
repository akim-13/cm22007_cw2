> [!IMPORTANT]
> All pull requests from other branches must be made to the `dev` branch before passing it onto the master branch.

## Development setup with Docker 

This project ships with a `docker-compose.yml` that runs both the backend (FastAPI) and the frontend (React).

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed on your machine
- An OpenAI API key (you can run w/o it, but AI won't work)

### Environment variables
Create a `.env` file in the repo root:

```bash
OPENAI_API_KEY=sk-yourkeyhere
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
