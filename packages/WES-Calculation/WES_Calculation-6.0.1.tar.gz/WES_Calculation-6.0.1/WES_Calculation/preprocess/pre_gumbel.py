'''
Date         : 2023-01-17 19:23:01
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-01-20 12:51:45
LastEditors  : BDFD
Description  : 
FilePath     : \WES_Calculation\preprocess\pre_gumbel.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''
from execdata import convint as s2int, convfloat as s2dec
from ..gumbel import gumbel

# def gumbel_calculation():
def pre_gumbel(original_input):
    """
        function name:Waterfront Engineering Studio Gumbel
        input function:wes.gumbel(pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist)
        Keyword arguments:pq, unitt, unitx, i1, i2, i3, meanx, sdx, n, dataolist
        argument -- description
        Return Description: plot_url, nCl2, nlen, note1, note2, note3, data3, note4, data4, note5, data5, data6, heading1, heading2, ending
    """ 
    # print("original_input before process",original_input)
    function_input = {}
    
    pq_default = "物理量"
    unitx_default = "无单位"
    unitt_default = "单位时段"
    
    pq = original_input["pq"]
    if not pq:
            pq = pq_default
    elif not pq.strip():
        pq = pq_default
    else:
        pq = pq

    unitx = original_input["unitx"]
    if not unitx:
        unitx = unitx_default
    elif not unitx.strip():
        unitx = unitx_default
    else:
        unitx = unitx

    unitt = original_input["unitt"]
    if not unitt:
        unitt = unitt_default
    elif not unitt.strip():
        unitt = unitt_default
    else:
        unitt = unitt
    original_input.update({"pq":pq, "unitx":unitx, "unitt":unitt})
    function_input.update({"pq":pq, "unitx":unitx, "unitt":unitt})

    i1 = original_input["i1"]
    i1 = s2int(i1)
    original_input.update({"i1":i1})
    function_input.update({"i1":i1})

    i2 = original_input["i2"]
    i2 = s2int(i2)
    original_input.update({"i2":i2})
    function_input.update({"i2":i2})
    
    meanx = original_input["meanx"]
    sdx = original_input["sdx"]
    n = original_input["n"]
    i3 = original_input["i3"]
    dataolist = original_input["dataolist"]
    function_input.update({"meanx":meanx, "sdx":sdx, "n":n, "i3":i3, "dataolist":dataolist})

    if i2 == 1:
        meanx = s2dec(meanx)
        sdx = s2dec(sdx)
        n = s2int(n)
        function_input.update({"meanx":meanx, "sdx":sdx, "n":n})

    if i2 == 2:
        i3 = s2int(i3)
        # dataolist = dataolist #可加可不加
        original_input.update({"i3":i3}) 
        function_input.update({"i3":i3, "dataolist":dataolist}) 

    # print("original_input after process",original_input)
    # print("function input is",function_input)
    result = gumbel(function_input["pq"], function_input["unitt"], function_input["unitx"], function_input["i1"], function_input["i2"], function_input["i3"], function_input["meanx"], function_input["sdx"], function_input["n"], function_input["dataolist"])

    plot_url = result[0]
    nCl2 = result[1]
    nlen = result[2]
    note1 = result[3]
    note2 = result[4]
    note3 = result[5]
    data3 = result[6]
    note4 = result[7]
    data4 = result[8]
    note5 = result[9]
    data5 = result[10]
    data6 = result[11]
    heading1 = result[12]
    heading2 = result[13]
    ending = result[14]

    return plot_url, nCl2, nlen, note1, note2, note3, data3, note4, data4, note5, data5, data6, heading1, heading2, ending
