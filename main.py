from flask import Flask, render_template, request,flash,redirect,url_for,flash,abort
import math
from csv import reader
from flask_talisman import Talisman

app = Flask(__name__)
app.secret_key = "asdasdas"
language="Türkce"

height_difference=0
Elbow=0

csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
    ]
}

Talisman(app, content_security_policy=None)


def debi_func(gas_type,DN,allowed_p_l):
## gaz tipine ve dn'e gore csv'e girip  Q'yu dönuyor

    #x=allowed_p_l
    csv_val=gas_type+'.csv'
    print(csv_val)

    row_check={16:[0,1], 20:[3,4], 25:[6,7], 32:[9,10], 40:[12,13], 50:[15,16]}
    row1=row_check[DN][0]
    row2=row_check[DN][1]
    print(row1,row2)

    with open(csv_val, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj,delimiter=';')
        # Iterate over each row in the csv using reader object
        set_dic={}

        for line in csv_reader:
            set_dic[line[row1].replace(",", ".")]=line[row2]

    if allowed_p_l in set_dic:
        return set_dic[allowed_p_l]
    else:
        print(allowed_p_l)
        return set_dic[str(max(x for x in filter(None, set_dic.keys()) if x!= 'ï»¿0.0000' if float(x) < float(allowed_p_l) ))]



@app.route('/english', methods=['GET', 'POST'])
def english():
    
    
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':
            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0


            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)
            Inlet_press=21
            drop=1
            print(Inlet_press)
            print(drop)
            
            if gas_type== "G20":
                display="Natural Gas G20 H"
                Inlet_press=21
                drop=1
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1


            if gas_type=="Propane":
                display="Propane"
                Inlet_press=37
                drop=2
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+2 ## pressure_drop=2
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

             ## new calorific value calculation
            if gas_type=='Propane':
                calorific_value=26.04
            else:
                calorific_value=10.35
            ##

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0
            print("Caloric value: ", calorific_value)


            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="You can use maximum  " + str(KW) + " kW"
                if KW<=0:
                    result="Height difference values is too high or too low."
                if abs(height_difference)>Line_Length:
                    result="Absolute value of height difference must be less than line length"

            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("english.html",basinc_kaybi=basinc_kaybi)

            return render_template("english.html",result=result,basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Inlet_press=Inlet_press,drop=drop,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        KW=0
        return render_template("english.html",KW=KW,basinc_kaybi=basinc_kaybi)
            


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':

            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0
            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Aardgas G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1

            if gas_type== "G25":
                display="Aardgas G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+1  

            if gas_type=="Propane":
                display="Propaan"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+1 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

            if gas_type=='G20': 
                    calorific_value=10.4
            if gas_type=='G25': 
                calorific_value=13.7
            if gas_type=='Propane': 
                calorific_value=13.8

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0

            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="You can use maximum  " + str(KW) + " kW"
                if KW<=0:
                    result="Height difference values is too high or too low."
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("english.html",basinc_kaybi=basinc_kaybi)

            return render_template("region.html",basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        return render_template("region.html",basinc_kaybi=basinc_kaybi)

    
            
            
@app.route('/francais', methods=['GET', 'POST'])
def francais():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':

            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0
            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Gaz Naturel G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1

            
            if gas_type== "G25":
                display="Gaz Naturel G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+1  

            if gas_type=="Propane":
                display="Propane"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+1 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            if gas_type=='G20': 
                calorific_value=10.4
            if gas_type=='G25': 
                calorific_value=13.7
            if gas_type=='Propane': 
                calorific_value=13.8

            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0

            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="Vous pouvez utiliser au maximum  " + str(KW) + " kW"
                if KW<=0:
                    result="Votre valeur de différence de hauteur est trop élevée ou trop faible"
                if abs(height_difference)>Line_Length:
                    result="La valeur absolue de la différence de hauteur doit être inférieure à la longueur de la ligne"
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("francais.html",basinc_kaybi=basinc_kaybi)

            return render_template("francais.html",result=result,basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        return render_template("francais.html",basinc_kaybi=basinc_kaybi)
   
@app.route('/belgium_french', methods=['GET', 'POST'])
def belgium_french():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':

            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0
            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Gaz Naturel G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1

            if gas_type== "G25":
                display="Gaz Naturel G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+1  

            if gas_type=="Propane":
                display="Propane"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+1 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            if gas_type=='G20': 
                calorific_value=11.99
            if gas_type=='G25': 
                calorific_value=10.45
            if gas_type=='Propane': 
                calorific_value=27.85

            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0

            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="Vous pouvez utiliser au maximum  " + str(KW) + " kW"
                if KW<=0:
                    result="Votre valeur de différence de hauteur est trop élevée ou trop faible"
                if abs(height_difference)>Line_Length:
                    result="La valeur absolue de la différence de hauteur doit être inférieure à la longueur de la ligne"
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("belgium_french.html",basinc_kaybi=basinc_kaybi)

            return render_template("belgium_french.html",result=result,basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        return render_template("belgium_french.html",basinc_kaybi=basinc_kaybi)           
            
@app.route('/dutch', methods=['GET', 'POST'])
def dutch():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':

            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0
            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Aardgas G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1

            if gas_type== "G25":
                display="Aardgas G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+1  

            if gas_type=="Propane":
                display="Propaan"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+1 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)
            print("Tee-Elbow: ", Elbow)

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            if gas_type=='G20': 
                calorific_value=11.99
            if gas_type=='G25': 
                calorific_value=10.45
            if gas_type=='Propane': 
                calorific_value=27.85

            print("Caloric value: ", calorific_value)
            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0

            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="U kunt maximaal  " + str(KW) + " kW gebruiken"
                if KW<=0:
                    result="Uw hoogteverschilwaarde is te hoog of te laag"
                if abs(height_difference)>Line_Length:
                    result="De absolute waarde van het hoogteverschil moet kleiner zijn dan de lijnlengte"
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("dutch.html",basinc_kaybi=basinc_kaybi)

            return render_template("dutch.html",result=result,basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        return render_template("dutch.html",basinc_kaybi=basinc_kaybi)

@app.route('/deutsch', methods=['GET', 'POST'])
def deutsch():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':
            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0

            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Erdgas G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+1

            if gas_type== "G25":
                display="Erdgas G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+1  

            if gas_type=="Propane":
                display="Propan"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+1 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type

            if gas_type=='G20': 
                calorific_value=10.4
            if gas_type=='G25': 
                calorific_value=13.7
            if gas_type=='Propane': 
                calorific_value=13.8

            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            KW=0

            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),4)
                KW=round(basinc_kaybi*(1.02)*calorific_value,1)
                result="You can use maximum  " + str(KW) + " kW"
                if KW<=0:
                    result="Height difference values is too high or too low."
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("english.html",basinc_kaybi=basinc_kaybi)
            
            return render_template("deutsch.html",basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,Elbow=Elbow,display=display)
    else:
        basinc_kaybi=0
        return render_template("deutsch.html",basinc_kaybi=basinc_kaybi)

@app.route('/turkce', methods=['GET', 'POST'])
def turkce():
    if request.method=="POST":
        if request.form['submit'] == 'hesapla':

            try:
                height_difference=float(request.form['height_difference'])
                
            except:
                height_difference=0
                
            try:
                Elbow=int(request.form['Elbow'])
            except:
                Elbow=0
            DN_=str(request.form.getlist('DN')[0])
            DN=int(DN_[2:])
            
            Line_Length=float(request.form['Line_Length'])
            gas_type=str(request.form.getlist('inlineRadioOptions')[0])
            print(gas_type)
            print(DN)

            if gas_type== "G20":
                display="Doğal gaz G20 H"
                Inlet_press=21
                height_difference_effect= 0.046*(height_difference)
                allowed_pressure_drop=height_difference_effect+0.8

            if gas_type== "G25":
                display="Doğal gaz G25 L"
                Inlet_press=25
                height_difference_effect= 0.048*(height_difference)
                allowed_pressure_drop=height_difference_effect+0.8 

            if gas_type=="Propane":
                display="Doğal gaz G20 H"
                Inlet_press=37
                height_difference_effect= (-0.048)*(height_difference)
                allowed_pressure_drop=height_difference_effect+0.8 ## pressure_drop=1
                
            
            tee_effected_total_length=Line_Length+(0.5*Elbow)
            allowed_p_l=round((allowed_pressure_drop)/(tee_effected_total_length),4)
            print("Inlet_Press: ",Inlet_press)
            print("height_difference_effect", height_difference_effect)
            print("tee_effected_total_length: ", tee_effected_total_length)
            print("allowed_p_l: ",allowed_p_l)

            if gas_type=='Propane':
                gas_type_2='G31'
            else:
                gas_type_2=gas_type
            
            print("({},{},{})".format(gas_type_2,DN,allowed_p_l))
            try:
                basinc_kaybi=round(float(debi_func(gas_type_2,DN,allowed_p_l).replace(",", ".")),2)
            except:
                print("error returned")
                basinc_kaybi=0
                return render_template("turkce.html",basinc_kaybi=basinc_kaybi)

            return render_template("turkce.html",basinc_kaybi=basinc_kaybi,height_difference=height_difference,DN=DN_,Line_Length=Line_Length,gas_type=gas_type,display=display)
    else:
        basinc_kaybi=0
        return render_template("turkce.html",basinc_kaybi=basinc_kaybi)
            
        
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=True)