other_test = {}

test_dict = {
    "a":"12",
    "b":"44",
    "c":"56",
    "d":"19",
    "e":"45"
}

for name, time in test_dict.items():
    print(time[0:2], time[3:5])
    other_test[name] = int(time[0:2]) * 60 + int(time[3:5])
print(other_test)
sorted_list = dict(sorted(other_test.items(), key=lambda item: item[1]))
print(sorted_list)