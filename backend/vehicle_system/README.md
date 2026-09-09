# Vehicle Inventory & Booking REST API

A Django REST Framework backend for managing a vehicle rental inventory and handling customer bookings, built as part of the AI and Python Django Intern Task for Vynzora Pvt. Ltd.

## Features

- Vehicle inventory management (CRUD)
- Booking creation with real-world business logic:
  - No double-booking (overlapping date validation)
  - Auto-calculated total amount (days × price per day)
  - Start date cannot be in the past
  - End date must be after start date
  - Phone number must be exactly 10 digits
- Filtering vehicles by brand, fuel type, and availability
- Django admin panel for the vehicle owner to manage vehicles and view bookings

## Tech Stack

- Python, Django, Django REST Framework
- MySQL
- django-filter (query param filtering)
- python-decouple (environment variable management)

## Project Setup

### 1. Clone the repository
```bash
git clone https://github.com/MuhammedFahizM/Vehicle_inventory.git
cd Vehicle_inventory/backend/vehicle_system
```

### 2. Create and activate a virtual environment
```bash
python -m venv myenv
myenv\Scripts\activate.bat      # Windows (cmd)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your actual values:
```bash
copy .env.example .env
```
Required variables:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DB_NAME=vehiclesystem_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
```

### 5. Create the MySQL database
In MySQL Workbench or CLI:
```sql
CREATE DATABASE vehiclesystem_db;
```

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser (for admin panel access)
```bash
python manage.py createsuperuser
```

### 8. Run the development server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/api/`
Admin panel: `http://127.0.0.1:8000/admin/`

## How to Test the APIs

Use Postman or any API client. Set a base URL variable, e.g. `http://127.0.0.1:8000/`.

## API Endpoints

### Vehicle Endpoints
| Method | Endpoint              | Description         |
|--------|------------------------|----------------------|
| GET    | /api/vehicles/          | List all vehicles   |
| POST   | /api/vehicles/          | Add a new vehicle   |
| GET    | /api/vehicles/<id>/     | Get vehicle details |
| PUT    | /api/vehicles/<id>/     | Update a vehicle    |
| DELETE | /api/vehicles/<id>/     | Delete a vehicle    |

### Booking Endpoints
| Method | Endpoint              | Description          |
|--------|------------------------|-----------------------|
| GET    | /api/bookings/          | List all bookings    |
| POST   | /api/bookings/          | Create a new booking |
| GET    | /api/bookings/<id>/     | Get booking details  |

### Filtering (Vehicles)
```
GET /api/vehicles/?brand=Toyota
GET /api/vehicles/?fuel_type=Electric
GET /api/vehicles/?is_available=true
```
Filters can be combined:
```
GET /api/vehicles/?brand=Toyota&fuel_type=Petrol&is_available=true
```

## Sample JSON — Create a Vehicle
```json
{
    "name": "Defender 110",
    "brand": "Land Rover",
    "year": 2025,
    "price_per_day": "24000.00",
    "fuel_type": "Diesel",
    "is_available": true
}
```

## Sample JSON — Create a Booking
```json
{
    "vehicle": 1,
    "customer_name": "Test User",
    "customer_phone": "9876543210",
    "start_date": "2026-09-15",
    "end_date": "2026-09-18"
}
```
`total_amount` is calculated automatically by the server and does not need to be (and cannot be) set manually.

## Booking Validation Rules
- A vehicle cannot be booked for overlapping date ranges.
- `start_date` cannot be in the past.
- `end_date` must be after `start_date`.
- `customer_phone` must be exactly 10 digits.

## Demo Video
https://youtu.be/Tko8ygzbUn0

## Live Deployment
https://vehicle-inventory-0wgr.onrender.com

Note : *Base URL has no frontend — test endpoints directly, e.g. https://vehicle-inventory-0wgr.onrender.com/api/vehicles/*