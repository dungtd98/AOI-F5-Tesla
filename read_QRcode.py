import csv

def write_results2csv(type, area):
    with open("results.csv",'a',newline='') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerow([type, area])

data = [
    ['Ok', 2444],
    ['NG', 2441421],
    ['asdada',213232]
]

for item in data:
    write_results2csv(item[0], item[1])