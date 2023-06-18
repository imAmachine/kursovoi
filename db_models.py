import psycopg2


class CombinedUser:
    def __init__(self, user, customer):
        self.username = user.username
        self.password = user.password
        self.role = ''
        self.customer_id = user.customer_id
        self.company_name = customer.company_name
        self.address = customer.address
        self.phone = customer.phone
        self.contact_person = customer.contact_person

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'customer_id': self.customer_id,
            'company_name': self.company_name,
            'address': self.address,
            'phone': self.phone,
            'contact_person': self.contact_person
        }


class User:
    def __init__(self, username, password, role='user', customer_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.customer_id = customer_id

    def save(self, db):
        result = db.insert(table='users', columns=('username', 'password_hash'), values=(self.username, self.password))
        return result

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role,
            'customer_id': self.customer_id
        }


class Customer:
    def __init__(self, company_name, address, phone, contact_person):
        self.company_name = company_name
        self.address = address
        self.phone = phone
        self.contact_person = contact_person

    def save(self, db):
        result = db.insert(table='customers', columns=('company_name', 'address', 'phone', 'contact_person'),
                           values=(self.company_name, self.address, self.phone, self.contact_person))
        return result

    def to_dict(self):
        return {
            'company_name': self.company_name,
            'address': self.address,
            'phone': self.phone,
            'contact_person': self.contact_person
        }


class Product:
    def __init__(self, name, price, delivery_available=False):
        self.name = name
        self.price = price
        self.delivery_available = delivery_available

    def save(self, db):
        result = db.insert(table='products', columns=('name', 'price', 'delivery_available'),
                           values=(self.name, self.price, self.delivery_available))
        return result

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'delivery_available': self.delivery_available
        }
