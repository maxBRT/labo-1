from datetime import datetime
from decimal import Decimal
import csv
from sqlalchemy.orm import joinedload
from .database import SessionLocal
from .models import Client, Equipment, Location
from .schema import (
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

    def update_client(self, client_id: int, data: ClientCreate):
        with SessionLocal() as session:
            client = session.query(Client).get(client_id)

            if client is None:
                raise Exception("Client not found")

            client.name = data.name
            client.email = data.email
            client.phone = data.phone
            session.commit()

    def create_equipment(self, data: EquipmentCreate):
        with SessionLocal() as session:
            equipment = Equipment(**data.model_dump())
            session.add(equipment)
            session.commit()

    def update_equipment(self, equipment_id: int, data: EquipmentCreate):
        with SessionLocal() as session:
            equipment = session.query(Equipment).get(equipment_id)

            if equipment is None:
                raise Exception("Equipment not found")

            equipment.name = data.name
            equipment.cost_per_day = data.cost_per_day
            equipment.is_available = data.is_available
            session.commit()

    def create_location(self, data: LocationCreate):
        with SessionLocal() as session:
            equipment = session.query(Equipment).get(data.id_equipment)

            if equipment is None:
                raise Exception("Equipment not found")

            equipment.is_available = False

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

    def return_location(self, id):
        with SessionLocal() as session:
            location = session.query(Location).get(id)

            if location is None:
                raise Exception("Location not found")

            location.is_returned = True
            equipment = session.query(Equipment).get(location.id_equipment)

            if equipment is None:
                raise Exception("Equipment not found")

            equipment.is_available = True
            session.commit()

    def get_available_equipments(self):
        with SessionLocal() as session:
            stmt = session.query(Equipment).filter(Equipment.is_available)
            equipments = stmt.all()
            return [EquipmentRead.model_validate(e) for e in equipments]

    def get_client_by_id(self, id):
        with SessionLocal() as session:
            client = session.query(Client).get(id)
            if client is None:
                return None
            return ClientRead.model_validate(client)

    def get_equipment_by_id(self, id):
        with SessionLocal() as session:
            equipment = session.query(Equipment).get(id)
            if equipment is None:
                return None
            return EquipmentRead.model_validate(equipment)

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

            print("\n")
            print("====================================================")
            print("         Database seeded successfully")
            print("====================================================")
        except Exception as e:
            print(f"Error when seeding the db: {e}")
