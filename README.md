## Social Media API

This project is a Social Media API built with Django and Docker, providing RESTful APIs for managing various entities such as Users, Posts, Hashtags, Likes, Comments & Follows.

## Running with Docker

To run the project with Docker, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/paashkovaaa/social-media-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd social-media-api
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Access the API endpoints via `http://localhost:8000/`.

## Running on Machine

To run the project on your local machine without Docker, follow these steps:

1. Ensure you have Python installed (preferably version 3.7 or later).

2. Clone the repository:

    ```bash
    git clone https://github.com/paashkovaaa/social-media-api.git
    ```

3. Navigate to the project directory:

    ```bash
    cd social-media-api
    ```

4. Install the Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

7. Access the API endpoints via `http://localhost:8000/`.

## Swagger Documentation:
  - `/api/doc/swagger/`
    - Provides the Swagger UI interface for interactive documentation of the API endpoints. Developers can explore and test the endpoints directly from the browser.

- **Redoc Documentation**:
  - `/api/doc/redoc/`
    - Offers the Redoc interface for API documentation, providing an alternative layout and styling for viewing and interacting with the API documentation.


## API Endpoints

Below is a summary of the API endpoints provided by the project:

- **Hashtags**: `/api/social_media/hastags/`
- **Posts**: `/api/social_media/posts/`
- **Likes**: `/api/social_media/likes/`
- **Comments**: `/api/social_media/comments/`
- **Follows**: `/api/social_media/follows/`
- **Users**: `/api/user/register`,`/api/user/me` `/api/user/token`, `/api/user/token/refresh`, `/api/user/token/verify`, `/api/user/users`

Each endpoint supports various operations such as listing, creation, retrieval, and updating of resources.