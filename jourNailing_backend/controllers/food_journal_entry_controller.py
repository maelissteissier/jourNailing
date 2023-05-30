from flask import Blueprint, jsonify, request, abort
from jourNailing_backend.database.database import db, FoodJournalEntry, JournalCategory, FoodRef
from datetime import datetime, date, timedelta

foodJournalEntry_bp = Blueprint('foodJournalEntry', __name__)

# POST new entry
@foodJournalEntry_bp.route('/food-journal-entry', methods=['POST'])
def create_food_journal_entry():
    if not request.json:
        abort(400)

    data = request.json
    journal_category_id = data['journal_category']['id']
    journal_category = JournalCategory.query.get(journal_category_id)

    # FoodRef isn't required so returns error only in case there is one and it doesn't exists
    food_ref = None
    try:
        if data['food_ref'] is not None:
            food_ref_id = data['food_ref']['id']
            food_ref = FoodRef.query.get(food_ref_id)
            # If the FoodRef doesn't exist
            if food_ref is None:
                return jsonify({'error': 'FoodRef not found'}), 404
    except KeyError:
        pass

    # If the JournalCategory doesn't exist (required)
    if journal_category is None:
        return jsonify({'error': 'JournalCategory not found'}), 404

    try:
        entry_date = datetime.strptime(data['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    new_entry = FoodJournalEntry(
        date=entry_date,
        quantity=data['quantity'],
        quantity_type=data['quantity_type'],
        calories=data['calories'],
        thoughts=data['thoughts'],
        name=data['name'],
        foodRef=food_ref,
        journalCategory=journal_category
    )

    if not isinstance(new_entry.quantity, int) or not isinstance(new_entry.calories, int):
        return jsonify({'error': 'original_calory or original_quantity not an int'}), 400

    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_json()), 201


# Get one entry
@foodJournalEntry_bp.route('/food-journal-entry/<entry_id>', methods=['GET'])
def get_food_journal_entry(entry_id):
    entry = FoodJournalEntry.query.get(entry_id)
    if entry is None:
        return jsonify({'error': 'Entry not found'}), 404
    return jsonify(entry.to_json()), 200


# GET all entries
@foodJournalEntry_bp.route('/food-journal-entries', methods=['GET'])
def get_all_food_journal_entries():
    entries = FoodJournalEntry.query.all()
    entries_json = [entry.to_json() for entry in entries]
    return jsonify(entries_json), 200


# Get all entries by date (one day)
@foodJournalEntry_bp.route('/food-journal-entries/date', methods=['GET'])
def get_entries_by_date():
    # Get the date from the request parameters or use today's date as default
    date_str = request.args.get('date')
    if date_str:
        try:
            query_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    else:
        query_date = date.today()

    # Query the database for entries matching the specified date
    entries = FoodJournalEntry.query.filter(FoodJournalEntry.date >= query_date,
                                            FoodJournalEntry.date < query_date + timedelta(days=1)).all()

    # Convert entries to JSON format
    entries_json = [entry.to_json() for entry in entries]

    return jsonify(entries_json), 200


@foodJournalEntry_bp.route('/food-journal-entry/<entry_id>', methods=['DELETE'])
def delete_food_journal_entry(entry_id):
    entry = FoodJournalEntry.query.get(entry_id)
    if entry is None:
        return jsonify({'error': 'Entry not found'}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Entry deleted successfully'}), 200


@foodJournalEntry_bp.route('/food-journal-entry/<entry_id>', methods=['PUT'])
def edit_food_journal_entry(entry_id):
    entry = FoodJournalEntry.query.get(entry_id)
    if entry is None:
        return jsonify({'error': 'Entry not found'}), 404
    data = request.json
    entry.date = data['date']
    entry.quantity = data['quantity']
    entry.quantity_type = data['quantity_type']
    entry.calories = data['calories']
    entry.mealRef_id = data['mealRef_id']
    entry.journalCategory_id = data['journalCategory_id']
    db.session.commit()
    return jsonify(entry.to_json()), 200