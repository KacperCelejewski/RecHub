# RecHub - [![Flask](https://github.com/KacperCelejewski/RecHub/actions/workflows/flask.yml/badge.svg)](https://github.com/KacperCelejewski/RecHub/actions/workflows/flask.yml)

RecHub is a user-friendly web application that empowers users to search for their future employees or companies. It provides a platform where users can not only find potential candidates or organizations, but also read and share valuable opinions and recommendations from each other. This fosters a collaborative environment where users can make informed decisions based on real experiences and insights.

## Technologies Used

- Python Flask
- PostgreSQL with SQLAlchemy as ORM
- Docker
- Docker - Compose
- PyTest - Unit Testing
- AWS Elastic Beanstalk for deployment
- Amazon RDS for PostgreSQL database
- AWS CodePipeline for CI/CD
- Vue.js for Frontend in another repository (RecHub - Frontend) -> Multirepo solution

## Getting Started

To get started with RecommendationHub, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/KacperCelejewski/Recommendation-Hub.git
   ```

2. Install the dependencies from the requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database. Make sure you have PostgreSQL installed and running. Then, create a new database and update the database configuration in the `config.py` and '.env' file.

4. Run the application:

   ```bash
   python -m application
   ```

5. Access the application in your web browser at `http://localhost:5000`.

## Contributing

If you would like to contribute to RecommendationHub, please follow these guidelines:

1. Fork the repository.

2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add your commit message"
   ```

4. Push your changes to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
