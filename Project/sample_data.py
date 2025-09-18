"""
Sample data script for the Inventory Management System
Run this script to populate the database with sample products, locations, and movements
"""

from app import app, db, Product, Location, ProductMovement
from datetime import datetime, timedelta
import random

def create_sample_data():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # Create Products
        products = [
            Product(product_id='LAPTOP001', name='Dell Laptop XPS 13', description='High-performance ultrabook for business use'),
            Product(product_id='MOUSE001', name='Wireless Mouse', description='Ergonomic wireless optical mouse'),
            Product(product_id='KEYBOARD001', name='Mechanical Keyboard', description='RGB backlit mechanical gaming keyboard'),
            Product(product_id='MONITOR001', name='24" LED Monitor', description='Full HD LED monitor with HDMI connectivity')
        ]
        
        for product in products:
            db.session.add(product)
        
        # Create Locations
        locations = [
            Location(location_id='WH001', name='Main Warehouse', description='Primary storage facility'),
            Location(location_id='WH002', name='Secondary Warehouse', description='Overflow storage facility'),
            Location(location_id='STORE001', name='Retail Store Downtown', description='Main retail location'),
            Location(location_id='STORE002', name='Retail Store Mall', description='Shopping mall location')
        ]
        
        for location in locations:
            db.session.add(location)
        
        db.session.commit()
        print(f"Created {len(products)} products and {len(locations)} locations")
        
        # Helper data for drivers and trucks
        drivers = [
            'John Doe', 'Priya Sharma', 'Carlos Mendez', 'Aisha Khan',
            'Ravi Kumar', 'Emily Chen', 'Ahmed Ali', 'Sara Thompson'
        ]
        trucks = [
            'KA-01-AB-1234', 'TN-09-XY-5678', 'MH-12-CD-9012', 'DL-04-EF-3456',
            'GJ-18-GH-7890', 'RJ-27-IJ-2345', 'UP-32-KL-6789', 'WB-20-MN-1122'
        ]
        
        # Create Product Movements
        movements = []
        movement_counter = 1
        
        # Initial stock movements (inbound to warehouses)
        base_date = datetime.now() - timedelta(days=30)
        
        for i, product in enumerate(products):
            # Initial stock to main warehouse
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=i),
                from_location=None,
                to_location='WH001',
                product_id=product.product_id,
                qty=random.randint(50, 100),
                driver_name=random.choice(drivers),
                truck_number=random.choice(trucks)
            )
            movements.append(movement)
            movement_counter += 1
            
            # Additional stock to secondary warehouse
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=i+1),
                from_location=None,
                to_location='WH002',
                product_id=product.product_id,
                qty=random.randint(30, 70),
                driver_name=random.choice(drivers),
                truck_number=random.choice(trucks)
            )
            movements.append(movement)
            movement_counter += 1
        
        # Transfer movements between warehouses and stores
        for i in range(12):  # 12 more movements to reach ~20 total
            product = random.choice(products)
            days_offset = random.randint(5, 25)
            
            # Random movement type
            movement_type = random.choice(['warehouse_to_store', 'store_to_store', 'warehouse_to_warehouse', 'outbound'])
            
            if movement_type == 'warehouse_to_store':
                from_loc = random.choice(['WH001', 'WH002'])
                to_loc = random.choice(['STORE001', 'STORE002'])
            elif movement_type == 'store_to_store':
                from_loc = 'STORE001'
                to_loc = 'STORE002'
            elif movement_type == 'warehouse_to_warehouse':
                from_loc = 'WH001'
                to_loc = 'WH002'
            else:  # outbound (Not Sold)
                from_loc = random.choice(['WH001', 'WH002', 'STORE001', 'STORE002'])
                to_loc = None
            
            movement = ProductMovement(
                movement_id=f'MOV{movement_counter:03d}',
                timestamp=base_date + timedelta(days=days_offset, hours=random.randint(8, 18)),
                from_location=from_loc,
                to_location=to_loc,
                product_id=product.product_id,
                qty=random.randint(5, 25),
                driver_name=random.choice(drivers),
                truck_number=random.choice(trucks)
            )
            movements.append(movement)
            movement_counter += 1
        
        # Add all movements to database
        for movement in movements:
            db.session.add(movement)
        
        db.session.commit()
        print(f"Created {len(movements)} product movements")
        print("Sample data creation completed!")
        
        # Print summary
        print("\n=== SAMPLE DATA SUMMARY ===")
        print("Products:")
        for product in products:
            print(f"  - {product.product_id}: {product.name}")
        
        print("\nLocations:")
        for location in locations:
            print(f"  - {location.location_id}: {location.name}")
        
        print(f"\nTotal Movements: {len(movements)}")
        print("\nYou can now run the Flask application and explore the inventory system!")

if __name__ == '__main__':
    create_sample_data()
