from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['post', 'get'])
def index():
    if request.method == 'POST':
        pesel = request.form.get('pesel')
        if pesel:
            return render_template("index.html", pesel_valid=validate_pesel(pesel), pesel=pesel)
    return render_template("index.html", pesel_valid=None, pesel=None)


def validate_pesel(pesel):
    weights = "13791379131"
    if not isinstance(pesel, str):
        pesel = str(pesel).zfill(11)
    if not pesel.isdigit() or len(pesel) != 11:
        return False
    weighted_sum = 0
    for x, y in zip(pesel, weights):
        weighted_sum += int(x) * int(y)
    return not weighted_sum % 10


if __name__ == '__main__':
    app.run()
