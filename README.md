## First Command to Run

``` bash
# Bootstraps the repo and starts it
# This should be the only command need to run the first time
make boot 

# After initial boot, we use the commands it uses on our own

# Restart docker compose
make restart 

# Stop and remove containers
make clean

# Build images again
make build

# Install all package
make install
# Install npm packages
make npm
# Install pip packages
make pip

# Go into a bash console in a container
make c C=backend
make c C=frontend
```

## Environment Variables

A `.env` file will be created on `make boot`.

You only need to add the following env vars:

```
OPENAI_API_KEY=
```
