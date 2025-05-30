import json
from datetime import datetime
from app import create_app
from app.models import Event, Contact
from app.extensions import db

app = create_app()


def import_events(json_file_path):
    """Import events from a JSON file into the database."""
    with app.app_context():
        # Load JSON data
        with open(json_file_path) as f:
            events_data = json.load(f)

        # Process each event
        for event_data in events_data:
            # Convert date string to Python date object
            event_date = datetime.strptime(event_data["date"], "%Y-%m-%d").date()

            # Create Event instance
            event = Event(
                event=event_data["event"],
                date=event_date,
                country=event_data["country"],
                region=event_data.get("region", ""),  # Using .get() for optional fields
                description=event_data["description"],
                image_link=event_data.get("image_link", ""),
                lat=str(event_data["lat"]),  # Ensure string type
                long=str(event_data["long"]),
            )

            # Add to session
            db.session.add(event)

        # Commit all events
        try:
            db.session.commit()
            print(f"Successfully imported {len(events_data)} events")
        except Exception as e:
            db.session.rollback()
            print(f"Error importing events: {str(e)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python import_events.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    import_events(json_file_path)
