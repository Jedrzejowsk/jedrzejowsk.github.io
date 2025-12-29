#This updater was created by G. Jedrzejowski
#It takes as an input a CSV file downloaded from wartosci punktowe google sheet - Regulamin tab
#It outputs a JSON file named "points_new.json" which is supposed to be placed in the judge_rnaut/assets directory
#Make sure you are running the script from the point_updater directory


import subscripts.openCSV as openCSV
import subscripts.convertData as convertData
import subscripts.makeJSON as makeJSON


csv_path = openCSV.get_csv_path()

if csv_path:
    print(f"Starting to process: {csv_path}")
    data = convertData.convert_csv_to_data(csv_path)
    makeJSON.write_json(data=data) 
else:
    print("Process cancelled.")




