var wave;
var rec=Recorder({
    onProcess:function(buffers,powerLevel,bufferDuration,bufferSampleRate){
        wave.input(buffers[buffers.length-1],powerLevel,bufferSampleRate);//输入音频数据，更新显示波形
    }
});
rec.open(function(){
    wave=Recorder.WaveView({elem:".elem"}); //创建wave对象，写这里面浏览器妥妥的
    
    rec.start();
});