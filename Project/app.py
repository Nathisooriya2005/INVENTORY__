from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Product(db.Model):
    product_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Product {self.product_id}>'

class Location(db.Model):
    location_id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Location {self.location_id}>'

class ProductMovement(db.Model):
    movement_id = db.Column(db.String(50), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    from_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    to_location = db.Column(db.String(50), db.ForeignKey('location.location_id'), nullable=True)
    product_id = db.Column(db.String(50), db.ForeignKey('product.product_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    driver_name = db.Column(db.String(100), nullable=True)
    truck_number = db.Column(db.String(50), nullable=True)
    
    # Relationships
    product = db.relationship('Product', backref='movements')
    from_loc = db.relationship('Location', foreign_keys=[from_location], backref='outgoing_movements')
    to_loc = db.relationship('Location', foreign_keys=[to_location], backref='incoming_movements')
    
    def __repr__(self):
        return f'<ProductMovement {self.movement_id}>'

# Forms
class ProductForm(FlaskForm):
    product_id = StringField('Product ID', validators=[DataRequired()])
    name = StringField('Product Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Save Product')

class LocationForm(FlaskForm):
    location_id = StringField('Location ID', validators=[DataRequired()])
    name = StringField('Location Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Save Location')

class ProductMovementForm(FlaskForm):
    movement_id = StringField('Movement ID', validators=[DataRequired()])
    product_id = SelectField('Product', validators=[DataRequired()])
    from_location = SelectField('From Location', choices=[('', 'Select Location')])
    to_location = SelectField('To Location', choices=[('', 'Select Location')])
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    driver_name = StringField('Driver Name')
    truck_number = StringField('Truck Number')
    submit = SubmitField('Save Movement')
    
    def __init__(self, *args, **kwargs):
        super(ProductMovementForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.product_id, f"{p.product_id} - {p.name}") for p in Product.query.all()]
        location_choices = [('', 'Select Location')] + [(l.location_id, f"{l.location_id} - {l.name}") for l in Location.query.all()]
        self.from_location.choices = location_choices
        self.to_location.choices = location_choices

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# Product Routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        # Check if product already exists
        existing_product = Product.query.get(form.product_id.data)
        if existing_product:
            flash('Product ID already exists!', 'error')
            return render_template('product_form.html', form=form, title='Add Product')
        
        product = Product(
            product_id=form.product_id.data,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', form=form, title='Add Product')

@app.route('/product/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    form.product_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('product_form.html', form=form, title='Edit Product')

@app.route('/product/view/<product_id>')
def view_product(product_id):
    product = Product.query.get_or_404(product_id)
    movements = ProductMovement.query.filter_by(product_id=product_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('product_view.html', product=product, movements=movements)

# Location Routes
@app.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

@app.route('/location/add', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        # Check if location already exists
        existing_location = Location.query.get(form.location_id.data)
        if existing_location:
            flash('Location ID already exists!', 'error')
            return render_template('location_form.html', form=form, title='Add Location')
        
        location = Location(
            location_id=form.location_id.data,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', form=form, title='Add Location')

@app.route('/location/edit/<location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)
    form.location_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        location.name = form.name.data
        location.description = form.description.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('locations'))
    return render_template('location_form.html', form=form, title='Edit Location')

@app.route('/location/view/<location_id>')
def view_location(location_id):
    location = Location.query.get_or_404(location_id)
    incoming_movements = ProductMovement.query.filter_by(to_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    outgoing_movements = ProductMovement.query.filter_by(from_location=location_id).order_by(ProductMovement.timestamp.desc()).all()
    return render_template('location_view.html', location=location, 
                         incoming_movements=incoming_movements, outgoing_movements=outgoing_movements)

# Product Movement Routes
@app.route('/movements')
def movements():
    movements = ProductMovement.query.order_by(ProductMovement.timestamp.desc()).all()
    return render_template('movements.html', movements=movements)

@app.route('/movement/add', methods=['GET', 'POST'])
def add_movement():
    form = ProductMovementForm()
    if form.validate_on_submit():
        # Check if movement already exists
        existing_movement = ProductMovement.query.get(form.movement_id.data)
        if existing_movement:
            flash('Movement ID already exists!', 'error')
            return render_template('movement_form.html', form=form, title='Add Movement')
        
        # Validate that at least one location is provided
        if not form.from_location.data and not form.to_location.data:
            flash('At least one location (from or to) must be specified!', 'error')
            return render_template('movement_form.html', form=form, title='Add Movement')
        
        movement = ProductMovement(
            movement_id=form.movement_id.data,
            product_id=form.product_id.data,
            from_location=form.from_location.data if form.from_location.data else None,
            to_location=form.to_location.data if form.to_location.data else None,
            qty=form.qty.data,
            driver_name=form.driver_name.data or None,
            truck_number=form.truck_number.data or None
        )
        db.session.add(movement)
        db.session.commit()
        flash('Movement added successfully!', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', form=form, title='Add Movement')

@app.route('/movement/edit/<movement_id>', methods=['GET', 'POST'])
def edit_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    form = ProductMovementForm(obj=movement)
    form.movement_id.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        # Validate that at least one location is provided
        if not form.from_location.data and not form.to_location.data:
            flash('At least one location (from or to) must be specified!', 'error')
            return render_template('movement_form.html', form=form, title='Edit Movement')
        
        movement.product_id = form.product_id.data
        movement.from_location = form.from_location.data if form.from_location.data else None
        movement.to_location = form.to_location.data if form.to_location.data else None
        movement.qty = form.qty.data
        movement.driver_name = form.driver_name.data or None
        movement.truck_number = form.truck_number.data or None
        db.session.commit()
        flash('Movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    return render_template('movement_form.html', form=form, title='Edit Movement')

@app.route('/movement/view/<movement_id>')
def view_movement(movement_id):
    movement = ProductMovement.query.get_or_404(movement_id)
    return render_template('movement_view.html', movement=movement)

# Balance Report
@app.route('/balance_report')
def balance_report():
    # Calculate balance for each product in each location
    balance_data = {}
    
    # Get all movements
    movements = ProductMovement.query.all()
    
    for movement in movements:
        product_id = movement.product_id
        qty = movement.qty
        
        # Initialize product in balance_data if not exists
        if product_id not in balance_data:
            balance_data[product_id] = {}
        
        # Handle incoming movements (to_location)
        if movement.to_location:
            if movement.to_location not in balance_data[product_id]:
                balance_data[product_id][movement.to_location] = 0
            balance_data[product_id][movement.to_location] += qty
        
        # Handle outgoing movements (from_location)
        if movement.from_location:
            if movement.from_location not in balance_data[product_id]:
                balance_data[product_id][movement.from_location] = 0
            balance_data[product_id][movement.from_location] -= qty
    
    # Convert to list format for template
    balance_list = []
    products = {p.product_id: p.name for p in Product.query.all()}
    locations = {l.location_id: l.name for l in Location.query.all()}
    
    for product_id, location_balances in balance_data.items():
        for location_id, balance in location_balances.items():
            if balance != 0:  # Only show non-zero balances
                balance_list.append({
                    'product_id': product_id,
                    'product_name': products.get(product_id, 'Unknown'),
                    'location_id': location_id,
                    'location_name': locations.get(location_id, 'Unknown'),
                    'balance': balance
                })
    
    return render_template('balance_report.html', balance_list=balance_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
