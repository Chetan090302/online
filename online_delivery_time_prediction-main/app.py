from flask import Flask,request,render_template
import pandas as pd
import numpy as np
import datetime as dt
from src.pipeline.prediction_pipeline import CustomData,PredictPipeline

app=Flask(__name__)

@app.route('/')
def show(): 
    return render_template('index.html')

@app.route("/review",methods=['GET','POST'])
def drone():
    if request.method=="POST":
        R = 6371
        age1=float(request.form['age'])
        # print(age1)
        rating1=float(request.form.get('ratings'))
        rlatitude=float(request.form.get('rlat'))
        rlongitude=float(request.form.get('rlon'))
        dlatitude=float(request.form.get('dlat'))
        dlongitude=float(request.form.get('dlon'))
        timeorder=pd.to_datetime(request.form.get('torder'))
        timepicked=pd.to_datetime(request.form.get('tpicked'))
        weather1=request.form.get('weather')
        traffic=request.form.get('road_traffic')
        vcond=int(request.form.get('vehicle_cond'))
        typorder=request.form.get('top')
        typvehicle=request.form.get('tov')
        md=float(request.form.get('multi_deli'))
        fest1=request.form.get('fest')
        city1=request.form.get('city')
        


        def deg_to_rad(degrees):
            return degrees*(np.pi/180)

        def distcalculate(lat1,lon1,lat2,lon2):
            d_lat=deg_to_rad(lat2-lat1)
            d_lon=deg_to_rad(lon2-lon1)
            a1=np.sin(d_lat/2)**2+np.cos(deg_to_rad(lat1))
            a2=np.cos(deg_to_rad(lat2))*np.sin(d_lon/2)**2
            a=a1*a2
            c=2*np.arctan2(np.sqrt(a),np.sqrt(1-a))
            return R*c



        distance=distcalculate(rlatitude,
                                rlongitude,
                                dlatitude,
                                dlongitude
                                        )
        
        timeduration=timepicked-timeorder
        timeduration=timeduration.seconds/60

        results=[age1,rating1,rlatitude,rlongitude,dlatitude,dlongitude,timeorder,timepicked,weather1,traffic,vcond,typorder,typvehicle,md,city1,distance,timeduration]

        good_res=[age1,rating1,weather1,traffic,vcond,typorder,typvehicle,md,fest1,city1,distance,timeduration]

        data=CustomData(Delivery_person_Age=age1,Delivery_person_Ratings=rating1,
                        Weather_conditions=weather1,
                        Road_traffic_density=traffic,
                        Vehicle_condition=vcond,
                        Type_of_order=typorder,
                        Type_of_vehicle=typvehicle,
                        multiple_deliveries=md,
                        Festival=fest1,
                        City=city1,
                        distance=distance,
                        time_diff=timeduration)
        
        final_data=data.get_data_as_dataframe()
        predict_pipeline=PredictPipeline()
        pred=int(predict_pipeline.predict(final_data))



        return render_template('results.html',final_result=pred)
    # else:   
    #     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
