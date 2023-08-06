'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-20 12:50:53
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_windspeed.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..windspeed import windspeed

# def windspeed_calculation():
def pre_windspeed(original_input):
    """
        function name:Waterfront Engineering Studio Windspeed
        input function:wes.windspeed(o2, input_zw, input_Xlat, input_X, input_Rg, input_beta, input_atm, input_Ta, input_zt, input_Tw, input_Taa, input_wdu, input_zu)
        Keyword arguments:o2, input_zw, input_Xlat, input_X, input_Rg, input_beta, input_atm, input_Ta, input_zt, input_Tw, input_Taa, input_wdu, input_zu
        argument -- description
        Return Description: img_stream, heading, section1, section2, section2_note, section3, section4, section5, section6, section7, ending
    """ 
    # print("original_input before process",original_input)
    function_input = {}
    
    o2 = original_input["o2"]
    o2 = s2int(o2)
    original_input.update({"o2":o2})
    function_input.update({"o2":o2})

    if o2 == 1:
        zw = original_input["zw_1"]
        zw = s2dec(zw)
        input_Xlat = None
        input_X = None
        input_Rg = None
        function_input.update({"zw":zw, "Xlat":input_Xlat, "X":input_X, "Rg":input_Rg})

    if o2 == 2:
        zw = original_input["zw_2"]
        zw = s2dec(zw)
        input_Xlat = None
        X = original_input["X_2"]
        X = s2dec(X)
        input_Rg = None
        function_input.update({"zw":zw, "Xlat":input_Xlat, "X":X, "Rg":input_Rg})

    if o2 == 3:    
        zw = original_input["zw_3"]
        zw = s2dec(zw)
        Xlat = original_input["Xlat_3"]
        Xlat = s2dec(Xlat)
        X= original_input["X_3"]
        X= s2dec(X)
        input_Rg = None
        function_input.update({"zw":zw, "Xlat":Xlat, "X":X, "Rg":input_Rg})
    
    if o2 == 4:
        input_zw = None    
        #Xlat = original_input["Xlat"]
        Xlat = original_input["Xlat_4"]
        Xlat = s2dec(Xlat)
        input_X= None
        #Rg = original_input["Rg"]
        Rg = original_input["Rg_4"]
        Rg = s2dec(Rg)
        #function_input.update({"zw":input_zw, "Xlat":input_Xlat, "X":input_X, "Rg":Rg})
        function_input.update({"zw":input_zw, "Xlat":Xlat, "X":input_X, "Rg":Rg})
        

    beta = original_input["beta"]
    beta = s2dec(beta)
    atm = original_input["atm"]
    atm = s2dec(atm)
    Ta = original_input["Ta"]
    Ta = s2dec(Ta)
    zt = original_input["zt"]
    zt = s2dec(zt)
    Tw = original_input["Tw"]
    Tw = s2dec(Tw)
    Taa = original_input["Taa"]
    if not Taa:
        Taa = ""
        input_Taa = None
    else:
        Taa = Taa
        input_Taa = s2dec(Taa)
    wdu = original_input["wdu"]
    wdu = s2dec(wdu)
    zu = original_input["zu"]
    zu = s2int(zu)
    original_input.update({"Taa":Taa})
    function_input.update({"beta":beta, "atm":atm, "Ta":Ta, "zt":zt, "Tw":Tw, "Taa":input_Taa, "wdu":wdu, "zu":zu})

    # print("original_input after process",original_input)
    # print("function input is",function_input)
    result = windspeed(function_input["o2"], function_input["zw"], function_input["Xlat"], function_input["X"], function_input["Rg"], function_input["beta"], function_input["atm"], function_input["Ta"], function_input["zt"], function_input["Tw"], function_input["Taa"], function_input["wdu"], function_input["zu"])
    plot_url = result[0]
    heading = result[1]
    section1 = result[2]
    section2 = result[3]
    section2_note = result[4]
    section3 = result[5] 
    section4 = result[6] 
    section5 = result[7]
    section6 = result[8]
    section7 = result[9]
    ending = result[10] 
    return plot_url, heading, section1, section2, section2_note, section3, section4, section5, section6, section7, ending