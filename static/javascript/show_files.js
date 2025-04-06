files=document.getElementById('files').innerHTML;
filelist=document.getElementById('filelist')
filelist=filelist.innerHTML;
filelist=filelist.replace(/\'/g,'|');
filelist=filelist.replace(/\"/g,"'")
filelist=filelist.replace(/\|/g,'"');
filelist=JSON.parse(filelist);
for(i=0;i<filelist.length;i++){
    var filetype=filelist[i].substring(filelist[i].lastIndexOf(".")+1);
    var EMs=document.getElementById('EMs');
    if(filetype=='pdf'||filetype=='PDF'){
        var new_iframe=document.createElement('iframe');
        new_iframe.src="/showfile/"+files+"/"+filelist[i]+"/";
        new_iframe.className='EM';
        EMs.appendChild(new_iframe);
    }else{
        var new_div=document.createElement('div');
        url="url('/showfile/"+files+"/"+filelist[i]+"')";
        new_div.style.backgroundImage=url;
        new_div.className='EM';
        new_div.id='EM'+i;
        new_div.onclick=function(){
            ShowImg(this.id)
        };
        EMs.appendChild(new_div);
    };
};

function ShowImg(id){
    var TopEM=document.getElementById('top_EM');
    var TopEMImg=document.getElementById('top_EM_image');
    var EM=document.getElementById(id);
    TopEMImg.style.backgroundImage=EM.style.backgroundImage;
    TopEM.style.display="block";
    TopEM.onclick=Hidden;
}

function Hidden(){
    var TopEM=document.getElementById('top_EM');
    TopEM.style.display="none";
}