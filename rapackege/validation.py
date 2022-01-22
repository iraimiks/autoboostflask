def validate_Customer_car(carname):
    if carname is None or carname is '':
        return "Aizpildiet lauku"
    else:
        return "Šis registrācijas numurs eksistē"