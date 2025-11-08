## Creating Docker Container

- Verify you are in the root directory for the project.
- Root directory should be `etf-watchdog-api`.
- Add any files that you don't want in the container using the `.dockerignore` file.
- Verify that your `.env` has the appropriate fields filled out.
- Now run `docker build . -t <your_image_name>`.
- Wait for the image to build.
- Once built, run `docker run -p 8000:8000 --name <your_container_name> <your_image_name>`.

---

### Breakdown

`docker build . -t <your_image_name`
- `docker build` is the docker command to build an image.
- `.` means find the Dockerfile in the current directory.
- `-t <your_image_name` creates a tag/name for the image.

`docker run -p 8000:8000 --name <your_container_name> <your_image_name>`
- `docker run` is the command to start up a container using an image.
- `-p 8000:8000` run on port 8000 of the host and 8000 of the container.
- `--name <your_container_name>` names the container.
- `<your_image_name>` the docker image to build the container on.
