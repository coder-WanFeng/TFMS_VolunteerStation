window.onload=function(){
    var VSAs=document.getElementById('VSAs');
    VSAs=VSAs.innerHTML;
    var is_admin=document.getElementById('is_admin');
    is_admin=is_admin.innerHTML;
    if(is_admin.toLowerCase()=='admin'){
        base_url='/VSA/'
    }else{
        base_url='/show_VSA/'
    }
    if(VSAs=='未找到符合要求的数据或筛选条件不符合要求!'||VSAs=='错误的筛选条件!'){
        var new_div=document.createElement('div');
        var VInfoDiv=document.getElementById('VolunteerInfo');
        new_div.innerHTML=VSAs;
        new_div.style.animation='ShowVI 0.3s ease 1';
        new_div.style.animationFillMode='forwards';
        VInfoDiv.appendChild(new_div);
    }else{
        VSAs=VSAs.replace(/\'/g,'^');
        VSAs=VSAs.replace(/\"/g,"'")
        VSAs=VSAs.replace(/\^/g,'"');
        VSAs=JSON.parse(VSAs);
        for(i=0;i<VSAs.length;i++){//['地点:陵园|内容:扫墓|时长:120|活动时间:120']
            var new_a=document.createElement('a');
            var VInfoDiv=document.getElementById('VSA_Info');
            if(i==0){
                new_a.innerHTML=VSAs[i];
            }else{
                new_a.innerHTML=VSAs[i][0];
                // t1=VSAs[i][1].replace(/\$/g,'/');
                // t1=t1.replace(/\:/g,'_');
                t2='filename='+VSAs[i][1];
                // new_a.href=base_url+t1;
                //new_a.target="_blank";
            };
            new_a.className='VSA';
            new_a.id='VI'+i;
            new_a.style.animation='ShowVI 0.3s ease 1';
            new_a.style.animationFillMode='forwards';
            VInfoDiv.appendChild(new_a);
        };
    };
}