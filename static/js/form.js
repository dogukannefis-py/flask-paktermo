var gas_type_r= '{{gas_type}}';
        document.getElementById("G20").addEventListener("click", myFunction);
        document.getElementById("G25").addEventListener("click", myFunction2);
        document.getElementById("Propane").addEventListener("click", myFunction3);


        function myFunction() {

            document.getElementById("inlet_pres").innerHTML = "21mbar";
            document.getElementById("pres").innerHTML = "1mbar";
            document.getElementById("calorific_val").innerHTML = "11.72 kWh/m³";
            
            
        }

        function myFunction2() {
            document.getElementById("inlet_pres").innerHTML = "25mbar";
            document.getElementById("pres").innerHTML = "1mbar";
            document.getElementById("calorific_val").innerHTML = "10.14 kWh/m³";
            
        }
        function myFunction3() {
            document.getElementById("inlet_pres").innerHTML = "37mbar";
            document.getElementById("pres").innerHTML = "2mbar";
            document.getElementById("calorific_val").innerHTML = "27.54 kWh/m³";
            
        }

        function gasFunction() {   //window loading apge function
            var gas_type_r= '{{gas_type}}';
            if(gas_type_r){
                document.getElementById(gas_type_r).checked=true;
                if (gas_type_r == "G20") {
                myFunction();
                } else if (gas_type_r == "Propane") {
                myFunction3();
                } else {
                myFunction2();
                }
            }
            else {
                document.getElementById("G20").checked=true;
            }
        }