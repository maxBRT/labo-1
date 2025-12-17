from database import SessionLocal


class DatabaseManager:
    def __init__(self):
        pass

    def create_client(self, name, email, phone):
        pass

    def create_equipment(self, name, cost_per_day, is_available):
        pass

    def create_location(
        self, id_client, id_equipment, start_date, end_date, is_returned
    ):
        pass

    def get_clients(self):
        pass

    def get_equipments(self):
        pass

    def get_available_equipments(self):
        pass

    def get_locations(self):
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
