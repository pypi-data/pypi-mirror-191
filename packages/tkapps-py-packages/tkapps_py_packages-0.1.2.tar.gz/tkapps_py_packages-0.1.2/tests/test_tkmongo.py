import json
import re
from src.tkaws.tkmongo import Tkmongo
from bson.json_util import loads, dumps

def regex_string_to_valid_bson(bson_string):
    object_id_regex = '(ObjectId\("+[a-zA-Z0-9]+"\))+'
    bson_output = ""
    object_id_matches = re.findall(object_id_regex, bson_string)
    string = object_id_matches
    for object in object_id_matches:
        object_id_regex = '("+[a-zA-Z0-9]+")+'
        object_id_values = re.findall(object_id_regex, object)
        object_id = object_id_values[0].strip('"')
        new_oid = {"$oid": object_id}
        bson_string = bson_string.replace(object, str(new_oid))
    # print(string)
    number_long_id_regex = '(NumberLong\("+[0-9]+"\))+'
    num_long_id_matches = re.findall(number_long_id_regex, bson_string)
    for longstr in num_long_id_matches:
        long_id_regex = '("+[0-9]+")+'
        long_values = re.findall(long_id_regex, longstr)
        long = long_values[0].strip('"')
        bson_string = bson_string.replace(longstr, long)
        # print(longstr)

    bson_object = json.dumps(bson_string.replace("'", '"'))
    print(bson_object)
    print(loads(str(dumps(json.loads(bson_object)))))
    return bson_object

def test_bson_util():
    BSON_STRING = '{"_id": ObjectId("63a20a6bdc0e8200064067ac"), "code": "_deleted_CP_1671628295079", "description": "Customer Pay", "formulas": [{"sourceCodeId": "Default", "expression": {"variableType": "list", "variable": "", "operator": "add","valueType": "percentage","value": "0"}}], "createdTime": NumberLong("1671563883003"), "modifiedTime": NumberLong("1671563883003"), "userId": "9bf9e89e-36fd-4947-a689-a6569c226c04", "lastModifiedByUserId": "9bf9e89e-36fd-4947-a689-a6569c226c04", "dealerId": "1790", "siteId": "-1_1790", "deleted": true, "wmsBeantype": "priceCode", "_class": "com.tekion.wms.service.pricesetup.beans.PriceCode"}'
    regex_string = regex_string_to_valid_bson(BSON_STRING)
    # json_data = Tkmongo("Gyaan").bson_to_json(BSON_STRING)
    return regex_string

test_bson_util()
