# Software Design IUST Backend

This repository contains the backend part of the Software Design project at the Iran University of Science and Technology (IUST). It serves as the backend server for the software application. It contains a Django REST API project that provides various endpoints for different functionalities. It includes multiple apps that handle different aspects of the API.

## Installation

To use this API, you need to follow these steps:

1. Clone the repository to your local machine using the following command:

   ```
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```
   cd backend
   ```

3. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Django REST API, follow these steps:

1. Apply the database migrations by running the following command:

   ```
   python manage.py migrate --run-syncdb
   ```

2. Start the development server by running the following command:

   ```
   python manage.py runserver
   ```

The API is now accessible at `http://localhost:8000/`.

## Main Apps

The API consists of the following main apps, each providing various endpoints:

- **Website**: Handles website-related functionality.
- **Admin**: Provides administrative functionality for managing the API.
- **Users**: Manages user-related operations.
- **Company**: Handles company-related functionality.
- **Dashboard**: Provides endpoints for the dashboard functionality.
- **Resume**: Manages resume-related operations.
- **Job**: Handles job-related functionality.
- **API Token Authentication**: Provides an authentication endpoint at `/api/token/`.

To access the APIs provided by each app, use the following URLs:

- Website: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`
- Users: `http://localhost:8000/users/`
- Company: `http://localhost:8000/company/`
- Dashboard: `http://localhost:8000/dashboard/`
- Resume: `http://localhost:8000/resume/`
- Job: `http://localhost:8000/job/`
- API Token Authentication: `http://localhost:8000/api/token/`

Feel free to explore and make use of the available endpoints as per your requirements.

## License

This project is licensed under the [MIT License](LICENSE).
