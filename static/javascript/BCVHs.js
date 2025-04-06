window.onload=function(){
    var VIs=document.getElementById('VIs');
    VIs=VIs.innerHTML;
    if(VIs=='none'){
        var new_div=document.createElement('div');
        var VInfoDiv=document.getElementById('VolunteerInfo');
        new_div.innerHTML='(｀・ω・´)志愿服务记录都审核完成了哦';
        new_div.style.animation='ShowVI 0.3s ease 1';
        new_div.style.animationFillMode='forwards';
        VInfoDiv.appendChild(new_div);
    }else{
        VIs=VIs.replace(/\'/g,'^');
        VIs=VIs.replace(/\"/g,"'")
        VIs=VIs.replace(/\^/g,'"');
        VIs=JSON.parse(VIs);
        for(i=0;i<VIs.length;i++){
            var new_a=document.createElement('a');
            var VInfoDiv=document.getElementById('VolunteerInfo');
            if(i==0){
                new_a.innerHTML=VIs[i];
            }else{
                new_a.innerHTML=VIs[i][0];
                t1=VIs[i][0].replace(/\|/g,'&');
                t1=VIs[i][0].replace(/\:/g,'=');
                t2='filename='+VIs[i][1]
                new_a.href='/ACEM/'+t1+'|'+t2;
                //new_a.target="_blank";
            };
            new_a.className='VI';
            new_a.id='VI'+i;
            new_a.style.animation='ShowVI 0.3s ease 1';
            new_a.style.animationFillMode='forwards';
            VInfoDiv.appendChild(new_a);
        };
    };
    var AlertDivExit=document.getElementById('AlertDivExit');
    if(AlertDivExit){
        AlertDivExit.onclick=AlertExit
    };
    function AlertExit(){
        var AlertDiv=document.getElementById('AlertDiv');
        AlertDiv.style.display='none';
    };
};