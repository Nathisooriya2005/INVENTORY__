# Inventory Management System

A comprehensive Flask-based web application for managing inventory across multiple warehouse locations. This system allows you to track products, locations, and product movements with a clean, modern user interface.

## Features

### Core Functionality
- **Product Management**: Add, edit, and view products with unique IDs and descriptions
- **Location Management**: Manage warehouse locations where products are stored
- **Movement Tracking**: Record product movements between locations with support for:
  - Inbound movements (receiving stock)
  - Outbound movements (shipping stock)
  - Internal transfers between locations
- **Balance Reports**: Real-time inventory balance reporting with visual indicators

### User Interface
- Modern, responsive Bootstrap-based UI
- Intuitive navigation with clear visual indicators
- Dashboard with quick access to all features
- Print-friendly balance reports
- Flash message notifications for user feedback

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Font Awesome icons
- **Forms**: Flask-WTF with WTForms validation

## Database Schema

### Tables
1. **Product**
   - `product_id` (Primary Key, VARCHAR)
   - `name` (VARCHAR, NOT NULL)
   - `description` (TEXT)

2. **Location**
   - `location_id` (Primary Key, VARCHAR)
   - `name` (VARCHAR, NOT NULL)
   - `description` (TEXT)

3. **ProductMovement**
   - `movement_id` (Primary Key, VARCHAR)
   - `timestamp` (DATETIME, NOT NULL)
   - `from_location` (VARCHAR, Foreign Key to Location, nullable)
   - `to_location` (VARCHAR, Foreign Key to Location, nullable)
   - `product_id` (VARCHAR, Foreign Key to Product, NOT NULL)
   - `qty` (INTEGER, NOT NULL)

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download
Download the project files to your local machine.

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database with Sample Data
```bash
python sample_data.py
```

This will create:
- 4 sample products (laptops, mouse, keyboard, monitor)
- 4 sample locations (2 warehouses, 2 retail stores)
- 20+ sample movements demonstrating various scenarios

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Usage Guide

### Getting Started
1. **Dashboard**: Overview of all system components with quick access buttons
2. **Products**: Manage your inventory items
3. **Locations**: Set up warehouse and store locations
4. **Movements**: Record all product transfers and stock changes
5. **Balance Report**: View current inventory levels across all locations

### Adding Data

#### Products
- Navigate to Products → Add New Product
- Enter unique Product ID, name, and optional description
- Product IDs must be unique across the system

#### Locations
- Navigate to Locations → Add New Location
- Enter unique Location ID, name, and optional description
- Location IDs must be unique across the system

#### Movements
- Navigate to Movements → Add New Movement
- Select product and specify movement details:
  - **Inbound**: Leave "From Location" empty, specify "To Location"
  - **Outbound**: Specify "From Location", leave "To Location" empty
  - **Transfer**: Specify both "From Location" and "To Location"

### Balance Report
The balance report shows current inventory levels by calculating:
- **Positive Balance**: More items moved in than out
- **Negative Balance**: More items moved out than in (indicates shortage)
- **Zero Balance**: Equal in and out movements

## Sample Data

The system includes sample data demonstrating:

### Products
- LAPTOP001: Dell Laptop XPS 13
- MOUSE001: Wireless Mouse
- KEYBOARD001: Mechanical Keyboard
- MONITOR001: 24" LED Monitor

### Locations
- WH001: Main Warehouse
- WH002: Secondary Warehouse
- STORE001: Retail Store Downtown
- STORE002: Retail Store Mall

### Movement Scenarios
- Initial stock receiving
- Inter-warehouse transfers
- Store replenishment
- Customer shipments
- Store-to-store transfers

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Main dashboard with quick access to all features*

### Products Management
![Products](screenshots/products.png)
*Product listing with add, edit, and view options*

### Product Form
![Product Form](screenshots/product_form.png)
*Clean form interface for adding/editing products*

### Locations Management
![Locations](screenshots/locations.png)
*Location management with warehouse and store tracking*

### Movements Tracking
![Movements](screenshots/movements.png)
*Comprehensive movement tracking with type indicators*

### Movement Form
![Movement Form](screenshots/movement_form.png)
*Intuitive movement form with helpful guidance*

### Balance Report
![Balance Report](screenshots/balance_report.png)
*Professional balance report with summary statistics*

## Key Features Demonstrated

### Movement Types
1. **Inbound Movements**: Receiving stock from suppliers
2. **Outbound Movements**: Shipping to customers
3. **Internal Transfers**: Moving stock between locations

### Data Validation
- Unique ID constraints for products, locations, and movements
- Required field validation
- Quantity validation (positive numbers only)
- At least one location required for movements

### User Experience
- Responsive design works on desktop and mobile
- Clear visual indicators for different movement types
- Flash messages for user feedback
- Breadcrumb navigation
- Print-friendly reports

## Development Notes

### Code Organization
- **app.py**: Main application file with routes and models
- **templates/**: HTML templates with Bootstrap styling
- **sample_data.py**: Sample data generation script
- **requirements.txt**: Python dependencies

### Security Features
- CSRF protection on all forms
- Input validation and sanitization
- SQL injection prevention through ORM

### Extensibility
The application is designed for easy extension:
- Add new fields to existing models
- Implement user authentication
- Add more report types
- Integrate with external systems
- Add API endpoints

## Troubleshooting

### Common Issues
1. **Database errors**: Delete `inventory.db` and run `sample_data.py` again
2. **Port conflicts**: Change the port in `app.run(port=5001)` in app.py
3. **Template errors**: Ensure all template files are in the `templates/` directory

### Support
For issues or questions about the codebase, please refer to the code comments and Flask documentation.

## License

This project is created for educational and demonstration purposes.

---

**Note**: This application demonstrates a complete inventory management system suitable for small to medium businesses. The clean architecture and comprehensive feature set make it an excellent foundation for real-world applications.
