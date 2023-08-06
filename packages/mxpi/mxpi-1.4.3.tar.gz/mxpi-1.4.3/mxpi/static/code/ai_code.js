Blockly.Python.yolo_fast_init=function(a){
    Blockly.Python.definitions_['yolo_fast_init'] = 'from Mx import yolo_fast';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var label = Blockly.Python.valueToCode(this,'LABEL',Blockly.Python.ORDER_ASSIGNMENT);
    var WH = Blockly.Python.valueToCode(this,'WH',Blockly.Python.ORDER_ASSIGNMENT);
    var obj = Blockly.Python.valueToCode(this,'OBJ',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'yolo_fast.init('+model+','+label+','+WH+','+obj+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.yolo_fast_process=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_face_detection=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var value = Blockly.Python.valueToCode(this,'VALUE',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.face_detection('+value+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_run=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_face_mesh=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.face_mesh('+max+','+dete+','+track+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_hands=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var model = this.getFieldValue('MODEL')
    var num = Blockly.Python.valueToCode(this,'NUM',Blockly.Python.ORDER_ASSIGNMENT);
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.hands('+model+','+num+','+dete+','+track+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mp_pose=function(a){
    Blockly.Python.definitions_['MediaPipe_MX'] = 'from Mx import MPipe';
    var model = this.getFieldValue('MODEL')
    var dete = Blockly.Python.valueToCode(this,'DETE',Blockly.Python.ORDER_ASSIGNMENT);
    var track = Blockly.Python.valueToCode(this,'TRACK',Blockly.Python.ORDER_ASSIGNMENT);
    var seg = Blockly.Python.valueToCode(this,'SEG',Blockly.Python.ORDER_ASSIGNMENT);
    var vis = Blockly.Python.valueToCode(this,'VIS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'MPipe.pose('+model+','+dete+','+track+','+seg+','+vis+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.audio_classify=function(a){
    Blockly.Python.definitions_['audio_classify'] = 'from Mx import audio_classify';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'audio_classify.init('+model+','+max+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.audio_classify_run=function(a){
    var name = Blockly.Python.valueToCode(this,'VAR',Blockly.Python.ORDER_ASSIGNMENT);
    var wav = Blockly.Python.valueToCode(this,'WAV',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+wav+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.SoundThread=function(a){
    Blockly.Python.definitions_['audio_classify'] = 'from Mx import audio_classify';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var max = Blockly.Python.valueToCode(this,'MAX',Blockly.Python.ORDER_ASSIGNMENT);
    var score = Blockly.Python.valueToCode(this,'SCORE',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'audio_classify.init_continue('+model+','+max+','+score+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mxpit_sound_p_b_run=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.predict()';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.classifier_win_init=function(a){
    Blockly.Python.definitions_['yolo_fast_init'] = 'from Mx.classifier import classifier as cls';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var label = Blockly.Python.valueToCode(this,'CLASS',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'cls(r'+model+','+label+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.class_process=function(a){
    var name = Blockly.Python.valueToCode(this,'NAME',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= name+'.run('+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mxpit_FastestDet = function () {
    Blockly.Python.definitions_['MXPIT_YOLO'] = 'from mxpit import object_detection as yolo';
    var img_path = Blockly.Python.valueToCode(this,'IMG_PATH',Blockly.Python.ORDER_ASSIGNMENT);
    var xml_path = Blockly.Python.valueToCode(this,'XML_PATH',Blockly.Python.ORDER_ASSIGNMENT);
    var save_path = Blockly.Python.valueToCode(this,'SAVE_PATH',Blockly.Python.ORDER_ASSIGNMENT);
    var label = Blockly.Python.valueToCode(this,'LABEL',Blockly.Python.ORDER_ASSIGNMENT);
    var batch_size = Blockly.Python.valueToCode(this,'BATCH_SIZE',Blockly.Python.ORDER_ASSIGNMENT);
    var lr = Blockly.Python.valueToCode(this,'LR',Blockly.Python.ORDER_ASSIGNMENT);
    var max_epoch = Blockly.Python.valueToCode(this,'EPOCH',Blockly.Python.ORDER_ASSIGNMENT);
    var code = 'if __name__ == "__main__":\n'+
                '\timg_path=r'+img_path+'\n'+
                '\txml_path=r'+xml_path+'\n'+
                '\tsave_path=r'+save_path+'\n'+
                '\tlabel='+label+'\n'+
                '\tbatch_size='+batch_size+'\n'+
                '\tlr='+lr+'\n'+
                '\tepoch='+max_epoch+'\n'+
                '\tmodel = yolo.FastestDet(img_path,xml_path,save_path,label,batch_size,lr,epoch)\n'+
                '\tmodel.train()\n';
    return code;
};

Blockly.Python.mxpit_FastestDet_p=function(a){
    Blockly.Python.definitions_['MXPIT_YOLO'] = 'from mxpit import object_detection as yolo';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'yolo.predict_onnx('+model+','+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}


Blockly.Python.mxpit_cls = function () {
    Blockly.Python.definitions_['MXPIT_CLS'] = 'from mxpit import image_classification as imgcls';
    var data_path = Blockly.Python.valueToCode(this,'DATA_PATH',Blockly.Python.ORDER_ASSIGNMENT);
    var save_path = Blockly.Python.valueToCode(this,'SAVE_PATH',Blockly.Python.ORDER_ASSIGNMENT);
    var batch_size = Blockly.Python.valueToCode(this,'BATCH_SIZE',Blockly.Python.ORDER_ASSIGNMENT);
    var lr = Blockly.Python.valueToCode(this,'LR',Blockly.Python.ORDER_ASSIGNMENT);
    var max_epoch = Blockly.Python.valueToCode(this,'EPOCH',Blockly.Python.ORDER_ASSIGNMENT);
    var onnx = Blockly.Python.valueToCode(this,'ONNX',Blockly.Python.ORDER_ASSIGNMENT);
    var code = 'if __name__ == "__main__":\n'+
                '\tdata_path=r'+data_path+'\n'+
                '\tsave_path=r'+save_path+'\n'+
                '\tbatch_size='+batch_size+'\n'+
                '\tlr='+lr+'\n'+
                '\tmax_epochs='+max_epoch+'\n'+
                '\tonnx='+onnx+'\n'+
                '\tmodel=imgcls.cls(data_path,save_path,batch_size,lr,max_epochs,onnx)\n'+
                '\tmodel.train()'
    return code;
};

Blockly.Python.mxpit_cls_p_p=function(a){
    Blockly.Python.definitions_['MXPIT_CLS'] = 'from mxpit import image_classification as imgcls';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'imgcls.predict_pth('+model+','+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mxpit_cls_p_onnx=function(a){
    Blockly.Python.definitions_['MXPIT_CLS'] = 'from mxpit import image_classification as imgcls';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'imgcls.predict_onnx('+model+','+img+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mxpit_sound = function () {
    Blockly.Python.definitions_['MXPIT_SOUND_CLS'] = 'from mxpit import sound_classification as soundcls';
    var path = Blockly.Python.valueToCode(this,'DATA',Blockly.Python.ORDER_ASSIGNMENT);
    var save_path = Blockly.Python.valueToCode(this,'SAVE',Blockly.Python.ORDER_ASSIGNMENT);
    var batch_size = Blockly.Python.valueToCode(this,'BATCH',Blockly.Python.ORDER_ASSIGNMENT);
    var lr = Blockly.Python.valueToCode(this,'LR',Blockly.Python.ORDER_ASSIGNMENT);
    var max_epoch = Blockly.Python.valueToCode(this,'EPOCH',Blockly.Python.ORDER_ASSIGNMENT);
    var chunk = Blockly.Python.valueToCode(this,'CHUNK',Blockly.Python.ORDER_ASSIGNMENT);
    var code = 'if __name__ == "__main__":\n'+
                "\tdata_path=r"+path+'\n'+
                "\tsave_path=r"+save_path+'\n'+
                "\tbatch_size="+batch_size+'\n'+
                "\tlr="+lr+'\n'+
                "\tmax_epochs="+max_epoch+'\n'+
                "\tchunk="+chunk+'\n'+
                "\tmodel=soundcls.cls(data_path,save_path,batch_size,lr,max_epochs,chunk)\n"+
                "\tmodel.train()"
    return code;
};

Blockly.Python.mxpit_sound_p=function(a){
    Blockly.Python.definitions_['MXPIT_SOUND_CLS_P'] = 'from mxpit.sound_classification import predict as sound_predict';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var wav = Blockly.Python.valueToCode(this,'SOUND',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'sound_predict('+model+','+wav+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.mxpit_sound_p_b=function(a){
    Blockly.Python.definitions_['MXPIT_SOUND_CLS_P_b'] = 'from Mx.audio_classify import Sound_pre';
    var model = Blockly.Python.valueToCode(this,'MODEL',Blockly.Python.ORDER_ASSIGNMENT);
    var time = Blockly.Python.valueToCode(this,'TIME',Blockly.Python.ORDER_ASSIGNMENT);
    var code= "Sound_pre("+model+","+time+")";
    return [code,Blockly.Python.ORDER_ATOMIC];
}

