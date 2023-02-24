"""Adoption Agency application."""

from flask import Flask, request, redirect, render_template, flash, get_flashed_messages
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "my_adopt"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def show_homepage():
    """Show the adoption agency homepage, listing all pets with their name, photo, and status."""

    # grab all pets' name, photo URL, and status
    pets = db.session.query(Pet.id, Pet.name, Pet.species, Pet.photo_url, Pet.available)

    return render_template('pets.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Show the form to add a new pet to the adoption registry. Handle new pet submission."""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes)

        db.session.add(pet)
        db.session.commit()

        flash(f"Added {name} the {age} year old {species} to the adoption registry!")

        return redirect('/')

    else:
        return render_template('addPet.html', form=form)
    
@app.route('/<int:pet_id>', methods=["GET", "POST"])
def show_pet_details(pet_id):
    """
    Show details about the specified pet and display a form to update pet details.
    Handle submission of updates to pet details.
    """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data

        db.session.commit()

        flash(f"Updated details for {pet.name}!")

        return redirect(f'/{pet.id}')
    else:
        return render_template('petDetails.html', form=form, pet=pet)