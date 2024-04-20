from flask import request, jsonify
from config import app, db
from models import Contact


# Decorator for get_contacts().
@app.route("/contacts", methods=["GET"])
def get_contacts():
    """Get all contacts from the database."""
    # Get all Contacts.
    contacts = Contact.query.all()
    # Convert the contacts to json.
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    # Return the json formatted contacts.
    return jsonify({"contacts": json_contacts})


# Decorator for create_contact().
@app.route("/create_contact", methods=["POST"])
def create_contact():
    '''Create a contact.'''
    # Get the contact info from the user.
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    phone_number = request.json.get("phoneNumber")

    # Error handleing before trying to POST to database, status 400.
    if not first_name or not last_name or not email or not phone_number:
        return (
            jsonify(
                {
                    "message": "You must include a first name, last name, and phone number"
                }
            ),
            400,
        )
    # Create the new Contact
    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
    )

    # Error handeling for POST to database.
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    # Return message and '201' code
    return jsonify({"message": "User created!"}), 201 

# Decorator for update_contact() inculding passing user id.
@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    '''Update an existing contacts information.'''
    contact = Contact.query.get(user_id)

    # Error handling if contact not found, status 404.
    if not contact:
        return jsonify({"message": "User not found!"}), 404
    
    # Update contact information
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    contact.phone_number = data.get("phoneNumber", contact.phone_number)

    # Commit the update to the database.
    db.session.commit()

    # Return message with code 200.
    return jsonify({"message": "User Updated!"}), 200

# Decorator for delete_contact() with passing of user_id.
@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    '''Delete a contact.'''
    contact = Contact.query.get(user_id)

    # Error handling if contact not found, status 404
    if not contact:
        return jsonify({"message": "User not found!"}), 404
    
    # Delete the contact and commit to database.
    db.session.delete(contact)
    db.session.commit()

    # Return message with status 200
    return jsonify({"message": "User Deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
