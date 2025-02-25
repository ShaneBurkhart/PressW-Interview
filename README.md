## Work Log

Before starting, I created `INIT.txt` which contains all of my initial thoughts. I also updated it along the way.

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

## Authentication

- I didn't get to authentication but I would implement email and password for users.
- I would hash passwords with bcrypt.
- When a user successfully logs in, I would generate a JWT and return it to the client.
- I would save the JWT to a http only cookie so only the server can see it.
- On a fresh page load, we make a /check_login request that either gives us the JWT or we redirect to login.
- Then all API calls include the JWT for the user. 

## Deployment

- If we need a full AWS deployment using Terraform, then I would build a separate repo for terraform and deploying
- This repo would build artifacts (Docker images), test them, and then push them to ECR
- Then the Terraform repo would deploy those artifacts based on the artifact version

- For something simple to start, I would create a `docker-compose.prod.yml` and a make command for running in production.
- Then I would simple SSH into the server and run `make prod`
- This command would migrate the database, pull images and restart the server.
- This could all sit on one server with no problem. For scale, we would want load balancers.
- Depending on threading, we could probably get away with multiple backend containers running on one EC2.

- I would use managed Postgres for my database like RDS. I have done it manually but it's way easier with RDS.

## Frontend State Management

- This app is simple so I just have chat history state and state for the input. 
- I send the full history on every backend request. 
- In a more complex app, I would create a ChatContext that holds all logic for talking to the backend
- Then components can use that data wherever needed. 
- I use useQuery for this kind of request.
- Next.js also allows for server side rendering so I would need to use the `page.tsx` file to load initial data.
- Then I could pass that into the Context as initial data. useQuery takes over from there.

## Timeboxing Explanation

- My thinking for time was that I wanted to get a hello world built as soon as possible
- This way I know all of my basics are working and then I can focus on application
- Then I start with the basic requirements of creating a chat interface and streaming it
- Once that is working, I looked at the time. I had about 50 mins lefts. 
- The UI was not polished enough for even an MVP so I did that next.
- The tedium took a little longer than expected. 
- I was left with 20-30 mins left after fixing bugs. 
- I wanted to make sure to document my thinking for the project requirements.
- As well as make sure the project will run from one command from scratch.