# GraphQL API with Flask and PostgreSQL

This project demonstrates a basic GraphQL API built with Flask, Graphene, and PostgreSQL.

## Features

*   **GraphQL API:** Exposes endpoints for querying and mutating data.
*   **Flask Framework:** Provides the web framework for the API.
*   **Graphene Library:**  Facilitates building the GraphQL schema and resolvers.
*   **PostgreSQL Database:**  Stores the application data.
*   **Docker:** Containerizes the application and database for easy deployment.

## Data Model

The API includes the following types:

*   **Professional:** Represents a professional with an ID, name, and position.
*   **Position:** Represents a job position with an ID and description.

## Getting Started

### Prerequisites

*   Python3
*   Database with tables created (tables.sql)

### Installation

1.  Clone the repository: `git clone <repository_url>`
2.  Navigate to the project directory: `cd <project_directory>`
3.  Build and run the Docker containers: `docker-compose up -d`

### Usage

Once the application is running, you can access the GraphQL API at `http://localhost:5000/graphql`.

You can use a GraphQL client like GraphiQL or Insomnia to interact with the API.

## Example Queries

**Fetch all professionals:**

```graphql
query {
  allProfessionals {
    id
    name
    position {
      id
      description
    }
  }
}
