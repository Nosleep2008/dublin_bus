from dublin_bus import arrival_prediction
import time
import pandas
# 155 1595335500 4728
# 155 1595335500 768

def test_arr_pred_1():
    time.time()
    test_result = arrival_prediction.prediction('155', '1595335500','4728')
    print(test_result)
    assert test_result != None

def test_arr_pred_2():
    test_result = arrival_prediction.prediction('155', '1595335500', '768')
    print(test_result)
    assert test_result != None
