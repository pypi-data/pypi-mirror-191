import os, sys, json
from epkernel import epcam, BASE
from epkernel.Action import Information,Selection

def save_eps(job:str, path:str):
    try:
        filename = os.path.basename(path)
        suffix = os.path.splitext(filename)[1]
        if suffix == '.eps':
            BASE.setJobParameter(job,job)
            BASE.save_eps(job,path)
            return True
        else:
            pass
    except Exception as e:
        print(e)
    return False

def save_gerber( job:str, step:str, layer:str, filename:str,  resize:int, angle:float, scalingX:float, scalingY:float, mirror:bool, rotate:bool, scale:bool, cw:bool,  mirrorpointX:int, mirrorpointY:int, rotatepointX:int, rotatepointY:int, scalepointX:int, scalepointY:int, mirrorX:bool, mirrorY:bool, numberFormatL=2, numberFormatR=6, zeros=2, unit=0):
    try:
        _type = 0
        gdsdbu = 0.01
        profiletop = False
        cutprofile = True
        isReverse = False
        cut_polygon = []
        if mirrorX == True and mirrorY ==True:
            mirrordirection = 'XY'
        elif mirrorX==True and mirrorY ==False:
            mirrordirection = 'Y'
        elif mirrorX==False and mirrorY ==True:
            mirrordirection = 'X'
        else:
            mirrordirection = 'NO'
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

def save_excellon2(job:str, step:str, layer:str, path:str, isMetric:bool, number_format_l=2, number_format_r=6, zeroes=2, unit=0, tool_unit=1, x_scale=1, y_scale=1, x_anchor=0, y_anchor=0):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name']==layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] =='drill':
                BASE.drill2file(job, step, layer,path,isMetric,number_format_l,number_format_r,
                    zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, manufacator = '', tools_order = [])
                return True
    except Exception as e:
        print(e)
    return False

def save_rout(job:str, step:str, layer:str, path:str, number_format_l=2,number_format_r=6,zeroes=2,unit=0,tool_unit=1,x_scale=1,y_scale=1,x_anchor=0,y_anchor=0, break_arcs = False):
    try:
        layer_info = Information.get_layer_information(job)
        for i in range(0,len(layer_info)):
            if layer_info[i]['name'] == layer and layer_info[i]['context'] == 'board' and layer_info[i]['type'] == 'rout':
                repeat = BASE.get_all_step_repeat_steps(job,step)
                data = json.loads(repeat)
                step_repeat = []
                if  not data['steps'] == None:
                    for _step in data['steps']:
                        step_repeat.append(_step)
                step_repeat.append(step)
                can_back = True
                for j in range(0,len(step_repeat)):
                    _step = step_repeat[j]
                    Selection.reverse_select(job, _step, layer)
                    ret = Information.get_selected_features_infos(job,_step,layer)
                    if ret == None:
                        can_back=False
                        return False
                    Selection.clear_select(job, _step, layer)
                    if len(ret) == 0:
                        can_back=False
                        return False
                    for k in range(0,len(ret)):
                        attribute = ret[k]['attributes']
                        has_chain = False
                        for m in range(0,len(attribute)):
                            if  '.rout_chain' in attribute[m]:
                                has_chain = True
                        if  has_chain == False:
                                can_back=False
                                return False
                if can_back==True:
                    BASE.rout2file(job, step, layer,path,number_format_l,number_format_r,zeroes,unit,tool_unit,x_scale,y_scale,x_anchor,y_anchor, 0, 0, 0, 0, 0, break_arcs)
                return True
    except Exception as e:
        print(e)
    return False

def save_job(job:str,path:str)->bool:
    try:
        layers = Information.get_layers(job)
        steps = Information.get_steps(job)
        for step in steps:
            for layer in layers:
                BASE.load_layer(job,step,layer)
        BASE.save_job_as(job,path)
        return True
    except Exception as e:
        print(e)
    return False

def save_dxf(job:str,step:str,layers:list,savePath:str):
    try:
        _ret = BASE.dxf2file(job,step,layers,savePath)
        ret = json.loads(_ret)['paras']['result']
        return ret
    except Exception as e:
        print(e)
    return False

def save_pdf(job:str, step:str, layers:list, layercolors:list, outputpath:str, overlap:bool)->bool:
    try:
        (outputpath,pdfname) = os.path.split(outputpath)
        layer_sum = len(layers)
        colors_sum = len(layercolors)
        b = True
        if layer_sum != colors_sum:
            b = False
        else:
            for i in range(0,colors_sum):
                color = layercolors[i]
                if len(color) !=4:
                    b = False
                    break
        if b == True:
            _ret = BASE.output_pdf(job,step,layers,layercolors,outputpath,pdfname,overlap)
            ret = json.loads(_ret)['status']
            if ret == 'true':
                ret = True
            else:
                ret = False
            return ret
    except Exception as e:
        print(e)
    return False

def save_gds(job:str, step:str, layer:str, filename:str, gdsdbu:float):
    try:
        _type = 1
        resize = 0
        angle = 0
        scalingX = 1
        scalingY = 1
        isReverse = False
        mirror = False
        rotate = False
        scale = False
        profiletop =False
        cw = False
        cutprofile =   True
        mirrorpointX = 0
        mirrorpointY = 0
        rotatepointX = 0
        rotatepointY = 0
        scalepointX = 0
        scalepointY = 0
        mirrordirection = 'X'
        cut_polygon = []
        numberFormatL = 2
        numberFormatR = 6
        zeros = 0
        unit = 0
        _ret = BASE.layer_export(job, step, layer, _type, filename, gdsdbu, resize, angle, scalingX, scalingY, isReverse,
                    mirror, rotate, scale, profiletop, cw, cutprofile, mirrorpointX, mirrorpointY, rotatepointX,
                    rotatepointY, scalepointX, scalepointY, mirrordirection, cut_polygon,numberFormatL,numberFormatR,
                    zeros,unit)
        ret = json.loads(_ret)['status']
        if ret == 'true':
            ret = True
        else:
            ret = False
        return ret
    except Exception as e:
        print(e)
    return False

# 输出文件
def save_drill(job:str, step:str,data:list,filename:str, unit:bool, tool_unit:bool, number_format_l:int, number_format_r:int, zeroes:int, x_scale:float, y_scale:float, x_anchor:int, y_anchor:int):
  try:
    file = open(filename, 'w', encoding = 'utf-8')
    file.write('M48'+'\n')
    if unit == True:
        file.write('INCH')
    else:
        file.write('METRIC')
    if zeroes == 0:
        file.write(',LZ'+'\n')
    elif zeroes == 1:
        file.write(',TZ'+'\n')
    else:
        file.write('\n')
    file.write(';FILE_FORMAT='+str(number_format_l)+':'+str(number_format_r)+'\n')
    for n in data:
        toolIdx = n['iToolIdx']
        to = str(toolIdx).rjust(2,'0')
        size_nm = n['iHoleSize']
        if tool_unit == True:
            size_mm = BASE.nm2inch(size_nm)
        else:
            size_mm =BASE.nm2mm(size_nm)
        size = ('%.4f'%size_mm)
        content = 'T'+to+'C'+size
        file.write(content+'\n')
    file.write('%'+'\n'+'G93X0Y0'+'\n')
    if unit == True:
        x_anchor = BASE.nm2inch(x_anchor)
        y_anchor = BASE.nm2inch(y_anchor)
    else:
        x_anchor = BASE.nm2mm(x_anchor)
        y_anchor = BASE.nm2mm(y_anchor)
    for i in data:
        toolIdx = i['iToolIdx']
        to = str(toolIdx).rjust(2,'0')
        part = 'T'+to
        file.write(part+'\n')
        iSlotLenth = i['iSlotLenth']
        location = i['vLocations']
        if iSlotLenth!=0:
            for j in location:
                digital = BASE.slotLenth(job, step, 'drill.backup', j, unit, 0, False, number_format_l, number_format_r, zeroes, x_anchor, y_anchor, 0, 0, x_scale, y_scale)
                file.write(digital+'\n')
        else:
            for pad in location:
                xy = BASE.isPad(pad, unit, 0, False, number_format_l, number_format_r, zeroes, x_anchor, y_anchor, 0, 0, x_scale, y_scale)
                file.write(xy+'\n')
    file.write('M30')
    file.close()
    print("保存文件成功")
    return True
  except Exception as e:
    print(e)
  return False




def save_png(job:str, step:str, layers:list, xmin:int, ymin:int, xmax:int, ymax:int, picpath:str, backcolor:list, layercolors:list)->bool:
    try:
        (picpath,picname) = os.path.split(picpath)
        layer_sum = len(layers)
        color_sum = len(layercolors)
        back_sum = len(backcolor)
        b = True
        if  back_sum != 4:
            b = False
        else:
            if layer_sum != color_sum:
                b = False
            else:
                for i in range(0,color_sum):
                    color = layercolors[i]
                    if len(color) != 4:
                        b = False
                        break
        if b == True:
            _ret = BASE.save_png(job,step,layers,xmin,ymin,xmax,ymax,picpath,picname,backcolor,layercolors)
            ret = json.loads(_ret)['status']
            if ret == 'true':
                ret = True
            else:
                ret = False
            return ret
    except Exception as e:
        print(e)
    return False



