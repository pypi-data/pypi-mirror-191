'''
Date         : 2023-01-17 10:50:35
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-20 13:40:18
LastEditors  : BDFD
Description  : 
FilePath     : f:\github project\section5.2-pypi-wes_calculation\wes_calculation\preprocess\pre_greenampt.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..greenampt import greenampt

# def gumbel_calculation():
def pre_greenampt(original_input):
    """
        function name:Waterfront Engineering Studio Gumbel
        input function:wes.greenampt(thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3)
        Keyword arguments:thetai, thetas, Psi, K, dti, nin, dd, i, iyesno, ss1, ss2, ss3
        argument -- description
        Return Description: plot_url, data, eff, note, note2
    """ 
    # print("original_input before process",original_input)
    function_input = {}
    thetai = original_input["thetai"] # Initial soil moisture content
    thetai = s2dec(thetai)
    thetas = original_input["thetas"] # Soil moisture content at saturation (i.e. porosity)
    thetas = s2dec(thetas)
    Psi = original_input["Psi"] # Suction head (m)
    Psi = s2dec(Psi)
    K = original_input["K"] # Saturated hydraulic conductivity (cm/h)
    K = s2dec(K)
    dti= original_input["dti"] #6 time interval in the analysis, normally that used in hyetograph (min)
    dti = s2dec(dti)
    nin= original_input["nin"] # The number of time intervals to be considered in the anlysis
    nin = s2int(nin)
    iyesno = original_input["iyesno"]
    iyesno = s2int(iyesno)
    function_input.update({"thetai":thetai, "thetas":thetas, "Psi":Psi, "K":K, "dti":dti, "nin":nin}) 
    

    iyesno = original_input["iyesno"] # Whether to generate an effective hyetograph (0: No; 1: Yes)
    iyesno = s2int(iyesno)
    function_input.update({"iyesno":iyesno}) 
    
    dd = original_input["dd"]
    i = original_input["i"]
    ss1 = 0 #Special Scenario 1#20220313
    ss2 = 0 #Special Scenario 2#20220313
    ss3 = 0 #Special Scenario 2#20220313
    
    headings = []
    if iyesno == 1:
        dd = s2dec(dd)# Depression depth used in generating an effective hyetograph (mm), which has to be zero when iyesno=0.
        res = i.split(",")
        i = list(map(float, res))
        if sum(i) == 0:#20121226
            iyesno = 0#20220310
            ss3 = 1 #Special Scenario 1#20220310 
        else:    
            if sum(i)*dti/60 < dd:#20121226
                iyesno = 0#20220310
                ss1 = 1 #Special Scenario 1#20220310 
            else:
                headings = [" 时刻 (minute) ","  雨强 (mm/h) "]
    if iyesno == 0:
        i=[0 for j in range(nin)]# Hyetograph (mm/h) (The first value covers the period between time 0 and time 0+dti.)
        dd=0                
    function_input.update({"iyesno":iyesno,"dd":dd,"i":i,"ss1":ss1,"ss2":ss2,"ss3":ss3})
    ending = "---结果展示结束---"
    
    # print("original_input after process",original_input)
    # print("function input is",function_input)
    result = greenampt(function_input["thetai"], function_input["thetas"], function_input["Psi"], function_input["K"], function_input["dti"], function_input["nin"], function_input["dd"], function_input["i"], function_input["iyesno"], function_input["ss1"], function_input["ss2"], function_input["ss3"])
    
    plot_url = result[0]
    data = result[1]
    eff = result[2]
    note = result[3]
    note2 = result[4]

    return headings, ending, plot_url, data, eff, note, note2