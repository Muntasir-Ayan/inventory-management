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
- **PostgreSQL 13+** with **PostGIS** extension  
- **Docker** 