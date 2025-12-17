from datetime import datetime
from decimal import Decimal
import csv
from sqlalchemy.orm import joinedload
from database import SessionLocal
from models import Client, Equipment, Location
from schema import (
    ClientCreate,
    ClientRead,
    EquipmentCreate,
    EquipmentRead,
    LocationCreate,
    LocationRead,
)


class DatabaseManager:
    def create_client(self, data: ClientCreate):
        with SessionLocal() as session:
            client = Client(**data.model_dump())
            session.add(client)
            session.commit()

    def create_equipment(self, data: EquipmentCreate):
        with SessionLocal() as session:
            equipment = Equipment(**data.model_dump())
            session.add(equipment)
            session.commit()

    def create_location(self, data: LocationCreate):
        with SessionLocal() as session:
            location = Location(**data.model_dump())
            session.add(location)
            session.commit()

    def get_clients(self):
        with SessionLocal() as session:
            clients = session.query(Client).all()
            return [ClientRead.model_validate(c) for c in clients]

    def get_equipments(self):
        with SessionLocal() as session:
            equipments = session.query(Equipment).all()
            return [EquipmentRead.model_validate(e) for e in equipments]

    def get_locations(self):
        with SessionLocal() as session:
            stmt = session.query(Location).options(
                joinedload(Location.client), joinedload(Location.equipment)
            )

            locations = stmt.all()

            return [LocationRead.model_validate(loc) for loc in locations]

    def get_available_equipments(self):
        pass

    def get_client_by_id(self, id):
        pass

    def get_equipment_by_id(self, id):
        pass

    def get_location_by_id(self, id):
        pass

    def get_client_by_phone(self, phone):
        pass

    def get_equipment_by_name(self, name):
        pass

    def get_location_by_client_id(self, id_client):
        pass

    def get_location_by_equipment_name(self, id_equipment):
        pass

    def seed(self):
        """
        Seed the database with mock data from the data folder
        """
        try:
            with open("data/clients.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.create_client(ClientCreate(**row))

            with open("data/equipments.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    e = EquipmentCreate(
                        name=row["name"],
                        cost_per_day=Decimal(row["cost_per_day"]),
                        is_available=row["is_available"].lower() == "true",
                    )
                    self.create_equipment(e)

            with open("data/locations.csv", "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    loc = LocationCreate(
                        id_client=int(row["id_client"]),
                        id_equipment=int(row["id_equipment"]),
                        start_date=datetime.strptime(row["start_date"], "%Y-%m-%d"),
                        end_date=datetime.strptime(row["end_date"], "%Y-%m-%d"),
                        is_returned=row["is_returned"].lower() == "true",
                    )
                    self.create_location(loc)

        except Exception as e:
            print(f"Error when seeding the db: {e}")
