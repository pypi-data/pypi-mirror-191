import os, json, tarfile
from epkernel import Configuration,  GUI, Input, Output, BASE
from epkernel.Action import Information, Selection
from epkernel.Edition import Layers, Matrix, Job
from epkernel.MI import stackup
import shutil

#指定step创建矩形profile
def create_rect_profile_jwApp(job:str, step:str, xmin:int, ymin:int, xmax:int, ymax:int):
    try:
        Matrix.create_layer(job,'profile__fz')
        Layers.add_line(job, step, ['profile__fz'], 'r1', xmin, ymin, xmin, ymax, True, [])
        Layers.add_line(job, step, ['profile__fz'], 'r1', xmax, ymin, xmax, ymax, True, [])
        Layers.add_line(job, step, ['profile__fz'], 'r1', xmax, ymax, xmin, ymax, True, [])
        Layers.add_line(job, step, ['profile__fz'], 'r1', xmax, ymin, xmin, ymin, True, [])
        Selection.reverse_select(job, step, 'profile__fz')
        Layers.create_profile(job,step,'profile__fz')
        Matrix.delete_layer(job,'profile__fz')
    except Exception as e:
        print(e)
    return 0

#直接根据属性去筛选
def set_featuretype_filter_jwApp(types:list=['line','pad','surface','arc','text'],polarity:list=['pos','neg']):
    try:
        if 'line' in types:
            line = True
        else:
            line = False
        if 'pad' in types:
            pad = True
        else:
            pad = False
        if 'surface' in types:
            surface = True
        else:
            surface = False
        if 'arc' in types:
            arc = True
        else:
            arc = False
        if 'text' in types:
            text = True
        else:
            text = False
        if 'pos' in polarity:
            positive = True
        else:
            positive = False
        if 'neg' in polarity:
            negative = True
        else:
            negative = False
        Selection.set_featuretype_filter(positive, negative, text, surface, arc, line, pad)
    except Exception as e:
        print(e)
    return 0

#输出料号的格式
def export_job_jwApp(job:str, path:str,type:list=['eps']):
    try:
        ifn = os.path.join(path, job)
        eps_path = ifn + '.eps'
        ofn = ifn + '.tar'
        if 'eps' in type:
            Output.save_eps(job,eps_path)
        if 'tar' in type:
            Output.save_job(job,path)
            with tarfile.open(ofn, 'w') as tar:
                tar.add(ifn, arcname=os.path.basename(ifn))
            shutil.rmtree(ifn)
        if 'tgz' in type:
            Output.save_job(job, path)
            ifn = os.path.join(path, job)
            ofn = ifn + '.tgz'
            with tarfile.open(ofn, 'w:gz') as tar:
                tar.add(ifn, arcname=os.path.basename(ifn))
            shutil.rmtree(ifn)
        if 'odb' in type:
            Output.save_job(job,path)
    except Exception as e:
        print(e)
    return 0

def add_surface_jwApp(job:str, step:str, layers:list, polarity:bool, attributes:dict, points_location:list):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        Layers.add_surface(job,step,layers,polarity,new,points_location)
    except Exception as e:
        print(e)
    return 0

def add_round_surface_jwApp(job:str, step:str, layers:list, polarity:bool, attributes:dict,center_x:int,center_y:int,radius:int):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        Layers.add_round_surface(job, step, layers, polarity, new,center_x,center_y,radius)
    except Exception as e:
        print(e)
    return 0

def add_text_jwApp(job:str, step:str, layers:list, symbol:str, fontname:str, text:str, xsize:int, ysize:int, linewidth:int, location_x:int, location_y:int,polarity:bool,orient:int,attributes:dict,special_angle:float=0):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        Layers.add_text(job,step,layers,symbol,fontname,text,xsize,ysize,linewidth,location_x,location_y,polarity,orient,new,special_angle)
    except Exception as e:
        print(e)
    return 0

def add_line_jwApp(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, polarity:bool, attributes:dict):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        Layers.add_line(job, step, layers, symbol, start_x, start_y, end_x, end_y, polarity, new)
    except Exception as e:
        print(e)
    return 0

def add_arc_jwApp(job:str, step:str, layers:list, symbol:str, start_x:int, start_y:int, end_x:int, end_y:int, center_x:int, center_y:int,cw:bool,polarity:bool, attributes:dict):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        Layers.add_arc(job, step, layers, symbol, start_x, start_y, end_x, end_y, center_x, center_y,cw,polarity, new)
    except Exception as e:
        print(e)
    return 0

def get_matrix_jwApp(job:str)->dict:
    try:
        step = Information.get_steps(job)
        layer = Information.get_layer_information(job)
        matrix_dict = {}
        matrix_dict['steps'] = step
        matrix_dict['info'] = layer
        return matrix_dict
    except Exception as e:
        print(e)
    return {} 

def get_selected_feature_infos_jwApp(job:str, step:str, layer:str)->list:
    try:
        select = Information.is_selected(job,step,layer)
        if select == True:
            ret = Information.get_selected_features_infos(job,step,layer)
        else:
            ret = Information.get_all_features_info(job,step,layer)
        return ret
    except Exception as e:
        print(e)
    return []

def get_selected_symbol_info_jwApp(job:str, step:str, layer:str)->dict:
    try:
        select = Information.is_selected(job, step, layer)
        if select == True:
            ret = Information.get_selected_symbol_info(job, step, layer)
        else:
            ret = Information.get_all_symbol_info(job, step, layer)
        return ret
    except Exception as e:
        print(e)
    return {}
     
def add_pad_jwApp(job:str, step:str, layers:list, symbol:str, location_x:int, location_y:int, polarity:bool, orient:int, attributes:dict,nx=1,ny=1,dx=0,dy=0,special_angle = 0):
    try:
        new = list()
        for i in attributes:
            new.append({i: attributes[i]})
        for m in range(0,nx):
            for n in range(0,ny):
                location_x1 = location_x + dx*m
                location_y1 = location_y + dy*n
                Layers.add_pad(job, step, layers, symbol, location_x1, location_y1, polarity, orient, new,special_angle)
    except Exception as e:
        print(e)
    return 0

def sr_tab_add(job:str, step:str, child_steps:list):
    try:
        info = Information.get_step_info(job, step)
        info.append(child_steps)
        Layers.step_repeat(job, step, info)
    except Exception as e:
        print(e)
    return 0







    