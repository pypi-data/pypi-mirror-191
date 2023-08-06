class Residence(dict):

    def __init__(self, is_actual: bool, country: str, city: str, street: str):
        super().__init__()
        self.actual = is_actual
        self.country = country
        self.city = city
        self.street = street
        self.department = None
        self.province = None
        self.number = None
        self.floor = None
        self.letter = None
        self.door_key_signal = None
        self.door_key_pin = None


class Pleasure(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.type = None
        self.name = None
        self.description = None


class Trips(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.place = None
        self.start_date = None
        self.finish_date = None
        self.companion = None
        self.country = None
        self.city = None
        self.vehicle = None


class HabitualPlace(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.location_name = None
        self.latitude = None
        self.longitude = None
        self.description = None
        self.frequency = None
        self.reason = None


class Multimedia(dict):

    def __init__(self):
        super().__init__()
        self.name = None
        self.description = None
        self.date = None
        self.longitude = None
        self.latitude = None
        self.image_size = None
        self.data_size = None
        self.secrecy = None
        self.hash = None


class DNI(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.code = None
        self.front_image = None
        self.back_image = None
        self.selfie_image = None


class Passport(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.code = None
        self.country = None
        self.front_image = None
        self.back_image = None
        self.selfie_image = None


class Vehicle(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.type = None
        self.plate = None
        self.brand = None
        self.model = None
        self.color = None


class Family(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.type = None
        self.id = None
        self.relationship_level = None


class AccountWebsites(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.name = None
        self.url = None
        self.password = None
        self.user = None
        self.alias = None


class Account(dict):

    def __init__(self, account):
        super().__init__()
        self.account = account
        self._websites = []

    def add_account(self, acc: AccountWebsites):
        if (acc.url, acc.user) not in [(a.url, a.user) for a in self._websites]:
            self._websites.append(acc)


class PhoneNumber(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.number = None
        self.country_code = None
        self.isp = None


class Device(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.type = None
        self.alias = None
        self.pin = None
        self.model = None
        self.description = None
        self.ip = None
        self.mac = None
        self.components = list()


class Card(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.number = None
        self.iban = None
        self.bank = None
        self.country = None
        self.expiration_month = None
        self.expiration_year = None
        self.cvv = None
        self.name_surnames = None
        self.pin = None


class Work(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.start_date = None
        self.finish_date = None
        self.description = None
        self.salary = None
        self.company = None
        self.responsibility = None
        self.city = None
        self.remote = None
        self.schedule = None
        self.holidays = None


class Study(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.name = None
        self.start_date = None
        self.finish_date = None
        self.description = None
        self.school = None
        self.grade = None
        self.city = None
        self.remote = None
        self.finished = None
        self.schedule = None
        self.holidays = None


class Person(dict):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.surnames = None
        self.alias = None
        self.birth_date = None
        self.telegram_id = None
        self.citizenship = list()
        self.accounts = list()
        self.dni = None
        self.passport = list()
        self.residence = list()
        self.pleasures = list()
        self.trips = list()
        self.habitual_places = list()
        self.multimedia = dict()
        self.vehicles = list()
        self.family = list()
        self.phone_numbers = list()
        self.devices = list()
        self.cards = list()
        self.works = list()
        self.studies = list()

    def add_account(self, email_address, service: AccountWebsites = None):
        if email_address not in [acc.account for acc in self.accounts]:
            new_acc = Account(email_address)
            if service:
                new_acc.add_account(service)
            self.accounts.append(new_acc)
            return
        existing_acc = [acc for acc in self.accounts if acc.account == email_address][0]
        existing_acc.add_account(service)

    def add_dni(self, dni: DNI):
        self.dni = dni

    def add_surnames(self, surnames: list):
        self.surnames = surnames

    def add_alias(self, alias: str = ""):
        if not alias:
            alias = self.name
        self.alias = alias

    def add_telegram_id(self, telegram_id: str):
        self.telegram_id = telegram_id

    def add_birth_date(self, birth_date: str):
        self.birth_date = birth_date

    def add_passport(self, passport: Passport):
        if passport.code not in [tmp_pass.code for tmp_pass in self.passport]:
            self.passport.append(passport)

    def add_citizenship(self, country: str):
        if country not in self.citizenship:
            self.citizenship.append(country)

    def add_residence(self, residence: Residence):
        if (residence.country, residence.city, residence.street) \
                not in [(a.country, a.city, a.street) for a in self.residence]:
            self.residence.append(residence)

    def add_pleasure(self, pleasure: Pleasure):
        if (pleasure.type, pleasure.name) \
                not in [(a.type, a.name) for a in self.pleasures]:
            self.pleasures.append(pleasure)

    def add_trip(self, trip: Trips):
        if (trip.start_date, trip.place) \
                not in [(a.start_date, a.place) for a in self.trips]:
            self.trips.append(trip)

    def add_habitual_place(self, habitual_place: HabitualPlace):
        if (habitual_place.location_name, habitual_place.description) \
                not in [(a.location_name, a.description) for a in self.habitual_places]:
            self.habitual_places.append(habitual_place)

    def add_multimedia(self, multimedia_type: str, multimedia: Multimedia):
        if multimedia_type not in self.multimedia:
            self.multimedia[multimedia_type] = list()
        if multimedia.hash not in [a.hash for a in self.multimedia.get(multimedia_type)]:
            self.multimedia[multimedia_type].append(multimedia)

    def add_vehicle(self, vehicle: Vehicle):
        if (vehicle.plate, vehicle.model, vehicle.type) \
                not in [(a.plate, a.model, a.type) for a in self.vehicles]:
            self.vehicles.append(vehicle)

    def add_familiar(self, familiar: Family):
        if (familiar.type, familiar.id) \
                not in [(a.type, a.id) for a in self.family]:
            self.family.append(familiar)

    def add_phone_number(self, phone_number: PhoneNumber):
        if phone_number.number not in [a.number for a in self.phone_numbers]:
            self.phone_numbers.append(phone_number)

    def add_device(self, device: Device):
        if (device.type, device.alias) \
                not in [(a.type, a.alias) for a in self.devices]:
            self.devices.append(device)

    def add_card(self, card: Card):
        exists = False
        for tmp_card in self.cards:
            if card.bank == tmp_card.bank and (card.iban == tmp_card.iban or card.number == tmp_card.number):
                exists = True
        if not exists:
            self.cards.append(card)

    def add_work(self, work: Work):
        if (work.company, work.responsibility, work.start_date) \
                not in [(a.company, a.responsibility, a.start_date) for a in self.works]:
            self.devices.append(work)

    def add_study(self, study: Study):
        if (study.name, study.school, study.grade) \
                not in [(a.name, a.school, a.grade) for a in self.studies]:
            self.studies.append(study)
