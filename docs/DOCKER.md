## Creating Docker Container

Follow these steps to build and run your Docker container for the project.

### 1. Prepare the Project Directory

- Ensure you are in the root directory of the project: `etf-watchdog-api`.
- Add any files or directories you want to exclude from the Docker image to the `.dockerignore` file.
- Check that your `.env` file exists and contains all the necessary environment variables.

### 2. Build the Docker Image

Run the following command to build your Docker image:

```bash
docker build . -t <your_image_name>
```

- `docker build` — Command to build a Docker image.
- `.` — Specifies the current directory (where your Dockerfile is located).
- `-t <your_image_name>` — Tags the image with a name for easy reference.

### 3. Run the Docker Container

After the image is built, start a container with:

```bash
docker run -p 8000:8000 --name <your_container_name> <your_image_name>
```

- `docker run` — Starts a new container from the specified image.
- `-p 8000:8000` — Maps port 8000 on your host to port 8000 in the container.
- `--name <your_container_name>` — Assigns a custom name to your container.
- `<your_image_name>` — The name of the image you built in the previous step.

---

### Example

```bash
docker build . -t etf-watchdog
docker run -p 8000:8000 --name etf-watchdog-container etf-watchdog
```
