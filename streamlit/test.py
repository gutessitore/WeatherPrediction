from utils import get_irradiation_data, predict_city_irradiation

irrad_past = get_irradiation_data(-23.55, -46.64)

irrad_pred = predict_city_irradiation(irrad_past)
