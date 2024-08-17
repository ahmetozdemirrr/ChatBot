
# Rasa Chatbot Project with Flask and Redis

This project is a Rasa-based chatbot integrated with Flask for the frontend and Redis for session management. The project is containerized using Docker and can be easily deployed and run using Docker Compose.

## Prerequisites

Make sure you have the following installed on your machine:

- Docker
- Docker Compose

## Project Structure

- **rasa**: This service runs the Rasa server with API enabled.
- **action_server**: This service runs the custom actions for Rasa.
- **flask**: This service runs the Flask server that serves the frontend.
- **redis**: This service runs Redis, used for session management.

## Configuration

The project uses environment variables defined in a `.env` file to set port numbers and other configurations.

### `.env` File

Create a `.env` file in the root directory of the project with the following content:

```bash
RASA_PORT=5005
ACTION_SERVER_PORT=5055
FLASK_PORT=5000
REDIS_PORT=6379
```

You can change the port numbers according to your needs.

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and start the services**:
   ```bash
   docker-compose up --build
   ```

   This will build and start all the services defined in the `docker-compose.yml` file.

3. **Access the Flask frontend**:
   Open your browser and go to `http://localhost:${FLASK_PORT}` (replace `${FLASK_PORT}` with the actual port number defined in your `.env` file).

## Custom Actions

Custom actions are defined in the `actions` directory. You can modify or add new actions as needed. After making changes, rebuild the `action_server` service:

```bash
docker-compose build action_server
docker-compose up
```

## Volumes

- `./models:/app/models`: Syncs your local `models` directory with the Rasa service.
- `./endpoints.yml:/app/endpoints.yml`: Mounts your local `endpoints.yml` file to the Rasa service.
- `./actions:/app/actions`: Syncs your local `actions` directory with the action server.
- `./Server/templates:/app/templates`: Syncs your Flask templates directory with the Flask service.
- `./static:/app/static`: Syncs your static files (e.g., images) with the Flask service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Rasa](https://rasa.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Redis](https://redis.io/)

