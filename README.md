## Overview  
This project involves developing a **Property Management System** using **Django**, **PostgreSQL**, and **PostGIS** for geospatial data management. The system is designed for managing property information through a robust backend interface and a user-friendly public-facing page for property owners.  

---

## Features  
1. **Geospatial Data Management:**  
   - Utilizes **PostGIS** for storing and querying geolocation data.  
2. **Hierarchical Location Structure:**  
   - Locations organized by continent, country, state, and city.  
3. **Property Management:**  
   - Properties with attributes like bedrooms, review scores, amenities, and more.  
4. **Localized Content Support:**  
   - Multi-language support for property descriptions and policies.  
5. **Admin Interface:**  
   - Admin panel with filtering, search, and listing capabilities.  
6. **User Permissions:**  
   - Property Owners group with restricted access to their properties.  
7. **Sitemap Generation:**  
   - Command-line utility to generate a geolocation-based sitemap in JSON format.  

---

## Prerequisites  
- **Python 3.8+**  
- **Django 4.x**  
- **Docker**

---

## Project Architecture

The project directory is structured as follows:

```plaintext
inventory-management/
│
├── inventory_management/           # User-related operations (register, login, profile)
│   ├── __init__.py              # Main application file
│   ├── asgi.py/             # Stores user data in JSON
│   ├── settings.py/              # Unit tests for user service
│   ├── urls.py/              # Unit tests for user service
│   ├── wsgi.py/              # Unit tests for user service
│
├── inventory/    # Handles hotel destination information
│   ├── __init__.py              # Main application file
│   ├── templates/inventory              # Unit tests for user service
|                 ├── signup.html 
│   ├── management/              # Unit tests for user servic
|       ├── commands 
|             ├── add_data.py
|             ├── sitemap_generator.py 
│   ├── migrations/              # Unit tests for user service
│   ├── apps.py/              # Unit tests for user service
│   ├── admin.py/             # Stores user data in JSON
│   ├── forms.py/              # Unit tests for user service
│   ├── models.py/              # Unit tests for user service
│   ├── tests.py/              # Unit tests for user service
│   ├── urls.py/              # Unit tests for user service
│   ├── views.py/              # Unit tests for user service
│
├── docker-compose.yml           # Authentication microservice
├── Dockerfile              # Main application file
├── .env              # Main application file
├── .gitignore              # Ignore unnecessary files from version control
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
```
---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Muntasir-Ayan/inventory-management.git
   cd inventory-management

2. **Create and activate a virtual environment**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate     # Windows
3. **Install project dependencies**:
   ```bash
    pip install -r requirements.txt
4. **Docker Running command**:
   ```bash
    docker-compose build
    docker-compose up
   ```
   this will running on http://127.0.0.1:8000 and signup landing page.
   
5. **Docker Migrations command**:
   Open another new terminal
   ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate

6. **Creating Superuser or Admin**:
   ```bash
      docker-compose exec web python manage.py createsuperuser
Admin can login http://127.0.0.1:8000/admin in this url.
   
6. **Testing**:
   ```bash
    docker-compose exec web coverage run manage.py test
    docker-compose exec web coverage report
    docker-compose exec web coverage html

7. **sitemap_generations**:
   ```bash
       docker exec -it inventory-management-web-1 python manage.py sitemap_generator

8. **Adding some dummy data**:
   ```bash
       docker-compose exec web python manage.py add_data

### Location Model  
| **Field**       | **Type**            | **Description**                          |
|-----------------|---------------------|------------------------------------------|
| `id`            | `String (20)`       | Primary key                              |
| `title`         | `String (100)`      | Name of the location                     |
| `center`        | `PostGIS Point`     | Geolocation                              |
| `parent_id`     | `Foreign Key`       | Reference to parent location             |
| `location_type` | `String (20)`       | Location type (e.g., city, state)        |
| `country_code`  | `String (2)`        | ISO country code                         |
| `state_abbr`    | `String (3)`        | State abbreviation                       |
| `city`          | `String (30)`       | City name                                |
| `created_at`    | `Auto timestamp`    | Creation timestamp                       |
| `updated_at`    | `Auto timestamp`    | Update timestamp                         |

---

### Accommodation Model  
| **Field**       | **Type**              | **Description**                          |
|-----------------|-----------------------|------------------------------------------|
| `id`            | `String (20)`         | Primary key                              |
| `title`         | `String (100)`        | Property name                            |
| `bedroom_count` | `Unsigned Integer`    | Number of bedrooms                       |
| `review_score`  | `Decimal (1 place)`   | Review score (default 0)                 |
| `usd_rate`      | `Decimal (2 places)`  | Price rate in USD                        |
| `center`        | `PostGIS Point`       | Geolocation                              |
| `published`     | `Boolean`             | Publication status (default False)       |

---

### LocalizeAccommodation Model  
| **Field**       | **Type**              | **Description**                          |
|-----------------|-----------------------|------------------------------------------|
| `id`            | `Auto-increment`      | Primary key                              |
| `language`      | `String (2)`          | Language code                            |
| `description`   | `Text`                | Localized property description           |
| `policy`        | `JSONB`               | Localized property policies              |
