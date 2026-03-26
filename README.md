# boilerplate-fastapi

Repo contains APIs built on Python FastAPI Framework, please find following steps to setup environment.

## Prerequisite

- Docker
- Docker Compose
- Poerty

# Install dependencies

```poetry install```
```poetry add <package_name_1> <package_name_2>```

# Create .env file

- Create .env file in the root directory by refering the .env.example file.
- Any new variable that will be added in the .env file should be added in the .env.example file for future references.
- All the variables should be in CAPITAL_CAMEL_CASE.
- No values or example values should be provided in the .env.example file.

# Create Docker Build

```docker build . -t therapy-link```

# Using Docker Compose for Development

### Run all services
```docker-compose up```

### Debugging using VS Code
#### Prerequisite
- [VS Code Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [VS Code Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### Follow steps to start debugging
- click bottom-left of VS Code and select the option Remote-Containers: Reopen in Container from the dropdown menu, selecting From 'docker-compose.yml' and choose your container service (i.e. api).
- Once you landed in VS Code with Container source, you can start debugging.
- from the “Run” menu of VS Code, select “Add configuration…” and "Fase API”;
- Start debugging as normal

Mode Details - https://davidefiocco.github.io/debugging-containers-with-vs-code/


# DB Migrations

```docker-compose --profile liquibase up -d```

