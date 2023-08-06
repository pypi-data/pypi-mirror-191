'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-20 12:51:19
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_wavespectra.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..wavespectra import wave

# def gumbel_calculation():
def pre_wavespectra(original_input):
    """
        function name:Waterfront Engineering Studio WaveSpectra
        input function: wes.wave(c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp)
        Keyword arguments:c1, d, X, U, el, gamma, Hs, Tz, Ts, Tp
        argument -- description
        Return Description: img_stream, heading, data1, data1_heading, data2, data2_heading, content, ending
    """ 
    # print("original_input before process",original_input)
    function_input = {}
    c1 = original_input["c1"]
    c1 = s2int(c1)
    original_input.update({"c1":c1})        
    function_input.update({"c1":c1})


    if c1 == 1:
        d_1 = original_input["d_1"]
        if not d_1:
                d_1 = ""
                d = None
        else:
            d_1 = d_1
            d = s2dec(d_1)
        
        X_1 = original_input["X_1"]
        if not X_1:
            X_1 = ""
            X = None
        else:
            X_1 = X_1
            X = s2dec(X_1)*1000    

        U_1 = original_input["U_1"]  # wind speed (m/s)
        if not U_1:
            U_1 = ""
            U = None
        else:
            U_1 = U_1
            U = s2dec(U_1)       

        el_1 = original_input["el_1"]   # the elevation of the wind speed (m)
        if not el_1:
            el_1 = ""
            el = None
        else:
            el_1 = el_1
            el = s2dec(el_1)                               

        gamma_1 = original_input["gamma_1"]   # peakedness parameter for JONSWAP (between 1 and 7, but 3.30 is normally recommended)
        if not gamma_1:
            gamma_1 = ""
            gamma = None
        else:
            gamma_1 = gamma_1
            gamma = s2dec(gamma_1) 
        
        Hs_1 = original_input["Hs_1"]   # significant wave height (m)
        if not Hs_1:
            Hs_1 = ""
            Hs = None
        else:
            Hs_1 = Hs_1
            Hs = s2dec(Hs_1)  

        Tz_1 = original_input["Tz_1"]  # average zero-crossing period from data (s)
        if not Tz_1:
            Tz_1 = ""
            Tz = None
        else:
            Tz_1 = Tz_1
            Tz = s2dec(Tz_1)  

        Ts_1 = original_input["Ts_1"] # significant wave period (s)
        if not Ts_1:
            Ts_1 = ""
            Ts = None
        else:
            Ts_1 = Ts_1
            Ts = s2dec(Ts_1) 
        
        Tp_1 = original_input["Tp_1"]
        Tp = Tp_1

        original_input.update({"d_1":d_1, "X_1":X_1, "U_1":U_1, "el_1":el_1, "gamma_1":gamma_1, "Hs_1":Hs_1, "Tz_1":Tz_1, "Ts_1":Ts_1, "Tp_1":Tp_1})        
        function_input.update({"d":d, "X":X, "U":U, "el":el, "gamma":gamma, "Hs":Hs, "Tz":Tz, "Ts":Ts, "Tp":Tp})
    
    if c1 == 2:
        d_2 = original_input["d_2"]
        d = d_2

        X_2 = original_input["X_2"]
        if X_2 == "None":
            X_2_Replace = "不考虑"
            X_2 = "None"
            X = None
            original_input.update({"X_2_Replace":X_2_Replace})
        else:
            X_2 = X_2
            X = s2dec(X_2)*1000

        U_2 = original_input["U_2"]  # wind speed (m/s)
        if not U_2:
            U_2 = ""
            U = None
        else:
            U_2 = U_2
            U = s2dec(U_2) 
              
        el_2 = original_input["el_2"]   # the elevation of the wind speed (m)
        if not el_2:
            el_2 = ""
            el = None
        else:
            el_2 = el_2
            el = s2dec(el_2)
        
        gamma_2 = original_input["gamma_2"]   # peakedness parameter for JONSWAP (between 1 and 7, but 3.30 is normally recommended)
        if not gamma_2:
            gamma_2 = ""
            gamma = None
        else:
            gamma_2 = gamma_2
            gamma = s2dec(gamma_2)
        
        Hs_2 = original_input["Hs_2"]   # significant wave height (m)
        if not Hs_2:
            Hs_2 = ""
            Hs = None
        else:
            Hs_2 = Hs_2
            Hs = s2dec(Hs_2)

        Tz_2 = original_input["Tz_2"]  # average zero-crossing period from data (s)
        if not Tz_2:
            Tz_2 = ""
            Tz = None
        else:
            Tz_2 = Tz_2
            Tz = s2dec(Tz_2)
        
        Ts_2 = original_input["Ts_2"] # significant wave period (s)
        if not Ts_2:
            Ts_2 = ""
            Ts = None
        else:
            Ts_2 = Ts_2
            Ts = s2dec(Ts_2) 

        Tp_2 = original_input["Tp_2"] # significant wave period (s)
        if not Tp_2:
            Tp_2 = ""
            Tp = None
        else:
            Tp_2 = Tp_2
            Tp = s2dec(Tp_2) 
        original_input.update({"d_2":d_2, "X_2":X_2, "U_2":U_2, "el_2":el_2, "gamma_2":gamma_2, "Hs_2":Hs_2, "Tz_2":Tz_2, "Ts_2":Ts_2, "Tp_2":Tp_2})            
        function_input.update({"d":d, "X":X, "U":U, "el":el, "gamma":gamma, "Hs":Hs, "Tz":Tz, "Ts":Ts, "Tp":Tp})
    
    # print("original_input after process",original_input)
    # print("function input is",function_input)
    result = wave(function_input["c1"], function_input["d"], function_input["X"], function_input["U"], function_input["el"], function_input["gamma"], function_input["Hs"], function_input["Tz"], function_input["Ts"], function_input["Tp"])
    # print("pre input_list:",input_list) 
    plot_url = result[0]
    heading = result[1]
    data1 = result[2]
    data1_heading = result[3]
    data2 = result[4] 
    data2_heading = result[5] 
    content = result[6] 
    ending = result[7]
    return plot_url, heading, data1, data1_heading, data2, data2_heading, content, ending