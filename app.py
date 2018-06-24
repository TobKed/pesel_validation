from flask import Flask, render_template, request
from collections import OrderedDict

app = Flask(__name__)


@app.route("/", methods=['post', 'get'])
def index():
    if request.method == 'POST':
        pesel = request.form.get('pesel')
        pesel = pesel.strip()  # cut leading and trailing whitespaces
        if pesel:
            pesel_data = validate_pesel(pesel)
            pesel_valid = pesel_data.get('valid')
            gender = pesel_data.get('gender')
            birth_date = pesel_data.get('birth_date')
            return render_template("index.html", pesel_valid=pesel_valid, pesel=pesel,
                                   gender=gender, birth_date=birth_date)
    return render_template("index.html", pesel_valid=None, pesel=None)


def validate_pesel(pesel):
    weights = "13791379131"
    if not isinstance(pesel, str):
        pesel = str(pesel).zfill(11)
    if not pesel.isdigit() or len(pesel) != 11:
        return {"valid": False}
    weighted_sum = 0
    for x, y in zip(pesel, weights):
        weighted_sum += int(x) * int(y)
    pesel_data = {
        "valid": not weighted_sum % 10,
        "gender": get_gender(pesel[-2]),
        "birth_date": get_birthdate(pesel[:7])
    }
    return pesel_data


def get_gender(number_str):
    if int(number_str) % 2:
        return "Man"
    return "Woman"


def get_birthdate(number_str):
    day = int(number_str[4:6])
    month = int(number_str[2:4])
    year = int(number_str[:2])
    birth_code = OrderedDict([(80, 18), (60, 22), (40, 21), (20, 20), (0, 19)])
    for month_addition, years in birth_code.items():
        if month > month_addition:
            month -= month_addition
            year += years*100
            return "{}.{:02d}.{}".format(day, month, year)


if __name__ == '__main__':
    app.run(debug=True)
