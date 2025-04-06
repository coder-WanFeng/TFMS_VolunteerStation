//检测是否为移动端(参考app.py)
if((innerWidth/innerHeight)<=1){TurnMobile()};//  宽<=长则判断为移动端
//if(/mobile/i.test(navigator.userAgent)){TurnMobile()};
//初始部分内容
//  获取元素
var More=document.getElementById('More');
var LoginExit=document.getElementById('LoginExit');
var AlertDivExit=document.getElementById('AlertDivExit');
var ARUExit=document.getElementById('ARUExit');
var ACEMExit=document.getElementById('ACEMExit');
var ASVHExit=document.getElementById('ASVHExit');
var ASACExit=document.getElementById('ASACExit');
var ACUPExit=document.getElementById('ACUPExit');
var CreateVSAExit=document.getElementById('CreateVSAExit');
var ChangeVSAExit=document.getElementById('ChangeVSAExit');
var LookforVSAExit=document.getElementById('LookforVSAExit');
var UUVHExit=document.getElementById('UUVHExit');
var UCIDExit=document.getElementById('UCIDExit');
var UCPExit=document.getElementById('UCPExit');
var UserLookforVSAExit=document.getElementById('UserLookforVSAExit');
var LoginDiv=document.getElementById('LoginDiv');
var LoginButton=document.getElementById('LoginButton');
var IsAdmin=document.getElementById('IsAdmin');
var SetVHPageButton=document.getElementById('SetVHPageButton');
var PageMinus1=document.getElementById('PageMinus1');
var PagePlus1=document.getElementById('PagePlus1');
var AdminRegUserButton=document.getElementById('Reg');
var AdminCheckEMButton=document.getElementById('Check');
var AdminSearchVHButton=document.getElementById('Search');
var AdminOuputAllButton=document.getElementById('Output');
var AdminDownloadAllButton=document.getElementById('Download');
var AdminSearchAndChangeButton=document.getElementById('S&C');
var AdminChangeUserPassword=document.getElementById('ACUP');
var AdminCreateVolunteerButton=document.getElementById('Create');
var AdminChangeVolunteerButton=document.getElementById('Change');
var AdminLookforVolunteerButton=document.getElementById('LookFor');
var UserUploadVHButton=document.getElementById('Upload');
var UserChangeIDButton=document.getElementById('ChangeID');
var UserChangePasswordButton=document.getElementById('ChangePassword');
var UserLookforVolunteerButton=document.getElementById('UserLookfor');
var POST_Username=document.getElementsByClassName('POST-Username');
var BC_SetVHPageButton=document.getElementById('BC-SetVHPageButton');
var BC_PageMinus1=document.getElementById('BC-PageMinus1');
var BC_PagePlus1=document.getElementById('BC-PagePlus1');
var Replace=document.getElementById('Replace');
var AlertDiv=document.getElementById('AlertDiv');
var AdminSearchAndChange=document.getElementById('AdminSearchAndChange');
var LookforVolunteerServiceActivities=document.getElementById('LookforVolunteerServiceActivities');
var UserLookforVolunteerServiceActivities=document.getElementById('UserLookforVolunteerServiceActivities');
var ARUButton=document.getElementById('ARUButton');
var UVTime=document.getElementById('VTime');
//  初始变量
var IsShowVH='False';
var VHPage=1;
var VHEPM=30;
//  初始函数
window.onload=function(){
    // if(innerHeight<768){
    //     alert("建议使用网页部分虚拟高度>768的浏览器,\n否则可能出现样式错误!(当前虚拟高度"+innerHeight+")\n(可尝试通过ctrl+滚轮等方式缩放,这也许能解决部分样式问题)")
    // };
};
if(Replace.innerHTML){
    if(AlertDiv){
        var AlertDivExit=document.getElementById('AlertDivExit');
        href='/'+Replace.innerHTML.slice(1);
        AlertDivExit.onclick=window.open(href)
        if(Replace.innerHTML[0]=='1'){window.open(href)}else{window.location.replace(href)};
    }else{
        href='/'+Replace.innerHTML.slice(1);
        if(Replace.innerHTML[0]=='1'){window.open(href)}else{window.location.replace(href)};
    }
};
if(LoginDiv){LoginDiv.style.display='none';};
if(AdminSearchAndChange){
    AdminSearchAndChange.addEventListener('submit', function(event) {
        /*var ASACButton=document.getElementById('ASACButton');
        if(ASACButton.value=='查询'){
            ASACButton.value='返回'
        }else{
            ASACButton.value='查询'
        };*/
        event.preventDefault();
        ASACB();
    });
};
if(LookforVolunteerServiceActivities){
    LookforVolunteerServiceActivities.addEventListener('submit', function(event) {
        /*var ASACButton=document.getElementById('ASACButton');
        if(ASACButton.value=='查询'){
            ASACButton.value='返回'
        }else{
            ASACButton.value='查询'
        };*/
        event.preventDefault();
        LookforVSAB();
    });
};if(UserLookforVolunteerServiceActivities){
    UserLookforVolunteerServiceActivities.addEventListener('submit', function(event) {
        /*var ASACButton=document.getElementById('ASACButton');
        if(ASACButton.value=='查询'){
            ASACButton.value='返回'
        }else{
            ASACButton.value='查询'
        };*/
        event.preventDefault();
        UserLookforVSAB();
    });
};
if(IsAdmin){
    if(IsAdmin.innerHTML=='User'){
        SetVHPage(VHPage)
    };
}
if(POST_Username){
    var RUN=document.getElementById('RUN');
    for(i=0;i<POST_Username.length;i++){
        POST_Username[i].value=RUN.innerHTML;
    };
};
if(UVTime){
    UVT1=UVTime.innerHTML;
    UVT=parseFloat(UVT1);
    UVT_Hours=Math.floor(UVT/60);
    if(parseFloat(UVT)==parseInt(UVT)){
        UVT_Min=parseInt(UVT)-UVT_Hours*60;
    }else{
        UVT_Min=parseFloat(UVT)-UVT_Hours*60;
    }
    UVTime.innerHTML='志愿服务时长: '+UVT_Hours+'小时'+UVT_Min+'分钟 | '+UVT1+'/2400（分钟）';
}
//鼠标点击
if(More){More.onclick=TryShowLogin;};
if(LoginExit){LoginExit.onclick=TryShowLogin;};
if(AlertDivExit){AlertDivExit.onclick=AlertExit};//如果有AlertDivExit，则判断点击
if(SetVHPageButton){SetVHPageButton.onclick=SVHPButton};
if(PageMinus1){PageMinus1.onclick=PM1};
if(PagePlus1){PagePlus1.onclick=PP1};
if(BC_SetVHPageButton){BC_SetVHPageButton.onclick=BC_SVHPButton};
if(BC_PageMinus1){BC_PageMinus1.onclick=BC_PM1};
if(BC_PagePlus1){BC_PagePlus1.onclick=BC_PP1};
if(AdminRegUserButton){AdminRegUserButton.onclick=ARU};
if(AdminCheckEMButton){AdminCheckEMButton.onclick=ACEM};
if(AdminSearchVHButton){AdminSearchVHButton.onclick=ASVH};
if(AdminOuputAllButton){AdminOuputAllButton.onclick=AOA};
if(AdminDownloadAllButton){AdminDownloadAllButton.onclick=ADA};
if(AdminSearchAndChangeButton){AdminSearchAndChangeButton.onclick=ASAC};
if(AdminChangeUserPassword){AdminChangeUserPassword.onclick=ACUP}
if(AdminCreateVolunteerButton){AdminCreateVolunteerButton.onclick=ACreateV};
if(AdminChangeVolunteerButton){AdminChangeVolunteerButton.onclick=AChangeV};
if(AdminLookforVolunteerButton){AdminLookforVolunteerButton.onclick=ALookforV};
if(UserUploadVHButton){UserUploadVHButton.onclick=UUVH};
if(UserChangeIDButton){UserChangeIDButton.onclick=UCID};
if(UserChangePasswordButton){UserChangePasswordButton.onclick=UCP};
if(UserLookforVolunteerButton){UserLookforVolunteerButton.onclick=ULookforV};
if(ARUExit){ARUExit.onclick=ARUE};
if(ACEMExit){ACEMExit.onclick=ACEME};
if(ASVHExit){ASVHExit.onclick=ASVHE};
if(ASACExit){ASACExit.onclick=ASACE};
if(ACUPExit){ACUPExit.onclick=ACUPE};
if(CreateVSAExit){CreateVSAExit.onclick=ACreateVE};
if(ChangeVSAExit){ChangeVSAExit.onclick=AChangeVE};
if(LookforVSAExit){LookforVSAExit.onclick=ALookforVE};
if(UUVHExit){UUVHExit.onclick=UUVHE};
if(UCIDExit){UCIDExit.onclick=UCIDE};
if(UCPExit){UCPExit.onclick=UCPE};
if(UserLookforVSAExit){UserLookforVSAExit.onclick=ULookforVE}
if(ARUButton){ARUButton.onclick=ReLogin};
//临时函数<起>
function ACreateV(){};
function AChangeV(){};
function ULV(){};
//临时函数<终>
//LoginButton.onclick=LOGIN;
//函数
//  转调至移动端
function TurnMobile(){
    window.location.replace('/mobile')
};
//  时停
function sleep(d){
    for(var t = Date.now();Date.now() - t <= d;);
};
//  关闭该页面
function close(){
    window.opener=null;
    window.open('','_self');
    window.close();
};
//  重新登录
function ReLogin(){
    var LoginDiv=document.getElementById('LoginDiv');
    LoginDiv.submit();
}
//  form提交
function Submit(){
    $('.ToolDiv').each(function(){  
        $(this).load(window.location.href+".ToolDiv"); // 重新加载当前页面中的 .tool 元素  
    });
};
//  上方展示信息
function ShowInfo(Info){
    var new_div=document.createElement('div');
    var top=document.getElementById('top');
    new_div.id='ShowInfo';
    new_div.innerHTML=Info;
    new_div.style.animation='showinfo 3s ease 1';
    new_div.style.animationFillMode='forwards';
    top.appendChild(new_div);
};
//  退出中间提示框
function AlertExit(){
    var AlertDiv=document.getElementById('AlertDiv');
    AlertDiv.style.display='none';
    var AlertDivInfo=document.getElementById('AlertDivInfo').innerHTML;
    if(AlertDivInfo=='无该用户!'||AlertDivInfo=='密码错误!'||AlertDivInfo=='文件不存在'){

    }else{
        ReLogin();
    }
};
//  检测登录
function TryShowLogin(){
    if(IsAdmin.innerHTML){
        window.location.replace('/')
        ShowInfo('您已登录')
    }
    else{
        ShowLogin()
    };
};
//  展示登录界面
function ShowLogin(){
    if(LoginDiv.style.display=='none'){
        LoginDiv.style.animation="fadeIn 0.2s linear 1 forwards";
        LoginDiv.style.display='block';
    }
    else{
        setTimeout(function(){LoginDiv.style.display='none'},200);
        LoginDiv.style.animation="fadeOut 0.2s linear 1 forwards";
    };
};
//  按下搜索键
function ASACB(){
    var username=document.getElementById('ASAC-SearchUsername').value;
    var ID=document.getElementById('ASAC-SearchID').value;
    var SN=document.getElementById('ASAC-SearchSN').value;
    var Time=document.getElementById('ASAC-SearchTime').value;
    var Date=document.getElementById('ASAC-SearchDate').value;
    var Place=document.getElementById('ASAC-SearchPlace').value;
    var Content=document.getElementById('ASAC-SearchContent').value;
    var Grade=document.getElementById('ASAC-SearchGrade').value;
    var Class=document.getElementById('ASAC-SearchClass').value;
    var VI_iframe=document.getElementById('VI-iframe');
    VI_iframe.src='/volunteerinfo/0'+username+'/1'+ID+'/2'+SN+'/3'+Time+'/4'+Date+'/5'+Place+'/6'+Content+'/7'+Grade+'/8'+Class+'/';
    VI_iframe.style.display='block';
};
function LookforVSAB(){//NPCSET
    var Name=document.getElementById('LookforVSA-SearchUsername').value;
    var StartTime=document.getElementById('LookforVSA-SearchStartTime').value;
    var Time=document.getElementById('LookforVSA-SearchTime').value;
    var EndTime=document.getElementById('LookforVSA-SearchEndTime').value;
    var Place=document.getElementById('LookforVSA-SearchPlace').value;
    var Content=document.getElementById('LookforVSA-SearchContent').value;
    var VSA_iframe=document.getElementById('LookforVSA-iframe');
    VSA_iframe.src='/VSA_info/Admin/0'+Name+'/1'+Place+'/2'+Content+'/3'+StartTime+'/4'+EndTime+'/5'+Time+'/';
    VSA_iframe.style.display='block';
};
function UserLookforVSAB(){//NPCSET
    var Name=document.getElementById('UserLookforVSA-SearchUsername').value;
    var StartTime=document.getElementById('UserLookforVSA-SearchStartTime').value;
    var Time=document.getElementById('UserLookforVSA-SearchTime').value;
    var EndTime=document.getElementById('UserLookforVSA-SearchEndTime').value;
    var Place=document.getElementById('UserLookforVSA-SearchPlace').value;
    var Content=document.getElementById('UserLookforVSA-SearchContent').value;
    var VSA_iframe=document.getElementById('UserLookforVSA-iframe');
    VSA_iframe.src='/VSA_info/User/0'+Name+'/1'+Place+'/2'+Content+'/3'+StartTime+'/4'+EndTime+'/5'+Time+'/';
    VSA_iframe.style.display='block';
};
//  关闭所有右侧页面

function Admin_HiddenAll(){
    ARUE();
    ACEME();
    ASVHE();
    ASACE();
    ACUPE();
    ACreateVE();
    AChangeVE();
    ALookforVE();
};
function User_HiddenAll(){
    UUVHE();
    UCIDE();
    UCPE();
    ULookforVE();
    
};
//  管理员注册用户
function ARU(){
    Admin_HiddenAll();
    var AdminRegUser=document.getElementById('AdminRegUser');
    AdminRegUser.style.display='block';
    AdminRegUser.style.animation="fadeIn 0.2s linear 1 forwards";
};
//  管理员审核志愿服务信息
function ACEM(){
    Admin_HiddenAll();
    var AdminCheckEM=document.getElementById('AdminCheckEM');
    AdminCheckEM.style.display='block';
    AdminCheckEM.style.animation="fadeIn 0.2s linear 1 forwards";
};
//  管理员查改志愿服务信息
function ASAC(){
    Admin_HiddenAll();
    var AdminSearchAndChange=document.getElementById('AdminSearchAndChange');
    AdminSearchAndChange.style.display='flex';
    AdminSearchAndChange.style.animation="fadeIn 0.2s linear 1 forwards";
}
//  管理员查询用户信息
function ASVH(){
    Admin_HiddenAll();
    var AdminSearchVH=document.getElementById('AdminSearchVH');
    AdminSearchVH.style.display='block';
    AdminSearchVH.style.animation="fadeIn 0.2s linear 1 forwards";
};
//  管理员修改用户密码
function ACUP(){
    Admin_HiddenAll();
    var AdminChangeUserPassword=document.getElementById('AdminChangeUserPassword');
    AdminChangeUserPassword.style.display='block';
    AdminChangeUserPassword.style.animation="fadeIn 0.2s linear 1 forwards";
};
// 管理员创建志愿服务活动
function ACreateV(){
    Admin_HiddenAll();
    var CreateVolunteerServiceActivities=document.getElementById('CreateVolunteerServiceActivities');
    CreateVolunteerServiceActivities.style.display='block';
    CreateVolunteerServiceActivities.style.animation="fadeIn 0.2s linear 1 forwards";
};
// 管理员修改志愿服务活动
function AChangeV(){
    Admin_HiddenAll();
    var ChangeVolunteerServiceActivities=document.getElementById('ChangeVolunteerServiceActivities');
    ChangeVolunteerServiceActivities.style.display='block';
    ChangeVolunteerServiceActivities.style.animation="fadeIn 0.2s linear 1 forwards";
};
//  管理员查询志愿服务活动
function ALookforV(){
    Admin_HiddenAll();
    var LookforVolunteerServiceActivities=document.getElementById('LookforVolunteerServiceActivities');
    LookforVolunteerServiceActivities.style.display='flex';
    LookforVolunteerServiceActivities.style.animation="fadeIn 0.2s linear 1 forwards";
};
//  管理员查看志愿服务记录txtt
function AOA(){
    window.open('/output/txt');
};
//  管理员导出志愿服务记录xlsx 
function ADA(){
    window.open('/output/xlsx');
};
//  退出注册账号
function ARUE(){
    var AdminRegUser=document.getElementById('AdminRegUser');
    AdminRegUser.style.display='none';
    // setTimeout(function(){AdminRegUser.style.display='none'},200);
    AdminRegUser.style.animation="fadeOut 0.2s linear 1 forwards";
};
//  退出审核志愿服务
function ACEME(){
    var AdminCheckEM=document.getElementById('AdminCheckEM');
    AdminCheckEM.style.display='none';
    IsShowBCVH='False';
    var BCVH_iframe=document.getElementById('BCVH-iframe');
    BCVH_iframe.src='/BCVH';
    // setTimeout(function(){AdminCheckEM.style.display='none'},200);
    AdminCheckEM.style.animation="fadeOut 0.2s linear 1 forwards";
};
//  退出查询用户信息
function ASVHE(){
    var AdminSearchVH=document.getElementById('AdminSearchVH');
    AdminSearchVH.style.display='none';
    // setTimeout(function(){AdminSearchVH.style.display='none'},200);
    AdminSearchVH.style.animation="fadeOut 0.2s linear 1 forwards";
};
//  退出查改志愿服务信息
function ASACE(){
    var AdminSearchAndChange=document.getElementById('AdminSearchAndChange');
    AdminSearchAndChange.style.display='none'
    // setTimeout(function(){AdminSearchAndChange.style.display='none'},200);
    AdminSearchAndChange.style.animation="fadeOut 0.2s linear 1 forwards";
}
//  退出管理员修改用户密码
function ACUPE(){
    var AdminChangeUserPassword=document.getElementById('AdminChangeUserPassword');
    AdminChangeUserPassword.style.display='none';
    // setTimeout(function(){AdminChangeUserPassword.style.display='none'},200);
    AdminChangeUserPassword.style.animation="fadeOut 0.2s linear 1 forwards";
}
//  用户上传志愿服务信息
function UUVH(){
    User_HiddenAll();
    var UserUploadVH=document.getElementById('UserUploadVH');
    UserUploadVH.style.display='block';
};
//  用户修改昵称
function UCID(){
    User_HiddenAll();
    var UserChangeID=document.getElementById('UserChangeID');
    UserChangeID.style.display='block';
}
//  用户修改密码
function UCP(){
    User_HiddenAll();
    var UserChangePassword=document.getElementById('UserChangePassword');
    UserChangePassword.style.display='block';
}
//  用户查询志愿服务活动
function ULookforV(){
    User_HiddenAll();
    var UserLookforVolunteerServiceActivities=document.getElementById('UserLookforVolunteerServiceActivities');
    UserLookforVolunteerServiceActivities.style.display='flex';
};
//  退出上传志愿服务信息
function UUVHE(){
    var UserUploadVH=document.getElementById('UserUploadVH');
    UserUploadVH.style.display='none';
};
function UCIDE(){
    var UserChangeID=document.getElementById('UserChangeID');
    UserChangeID.style.display='none';
};
function UCPE(){
    var UserChangePassword=document.getElementById('UserChangePassword');
    UserChangePassword.style.display='none';
};
//  退出创建志愿服务活动
function ACreateVE(){
    var CreateVolunteerServiceActivities=document.getElementById('CreateVolunteerServiceActivities');
    CreateVolunteerServiceActivities.style.display='none';
};
//  退出修改志愿服务活动
function AChangeVE(){
    var ChangeVolunteerServiceActivities=document.getElementById('ChangeVolunteerServiceActivities');
    ChangeVolunteerServiceActivities.style.display='none';
};
//  管理员退出查询志愿服务活动
function ALookforVE(){
    var LookforVolunteerServiceActivities=document.getElementById('LookforVolunteerServiceActivities');
    LookforVolunteerServiceActivities.style.display='none';
};
//  用户退出查询志愿服务活动
function ULookforVE(){
    var UserLookforVolunteerServiceActivities=document.getElementById('UserLookforVolunteerServiceActivities');
    UserLookforVolunteerServiceActivities.style.display='none';
};
//  展示志愿服务记录
function ShowVH(VHPage){
    if(IsShowVH=='False'){
        var VH=document.getElementById('History');
        var VHD=document.getElementById('VHistoryDiv');
        var VHP=document.getElementById('VHPage');
        var VHTip=document.getElementById('VHTip');
        VH=VH.innerHTML;
        VH=VH.replace(/\'/g,'|');
        VH=VH.replace(/\"/g,"'")
        VH=VH.replace(/\|/g,'"');
        VH=JSON.parse(VH);
        if(VH.length==0){
            var new_div=document.createElement('div');
            var VHistoryDiv=document.getElementById('VHistoryDiv');
            new_div.className='VH';
            new_div.id='VH0';
            new_div.innerHTML='(｀・ω・´)您还没有做过志愿服务哦';
            new_div.style.animation='ShowVH 0.3s ease 1';
            new_div.style.animationFillMode='forwards';
            VHistoryDiv.appendChild(new_div);
        }else{
            if(VH.length>=VHPage*VHEPM){
                imax=VHPage*VHEPM;
            }else{
                imax=VH.length
            };
            for(i=(VHPage-1)*VHEPM;i<imax;i++){
                VHInfo=VH[i];
                var new_a=document.createElement('a');
                var VHistoryDiv=document.getElementById('VHistoryDiv');
                new_a.className='VH';
                new_a.id=('VH'+String(i+1));
                if(String(i+1).length<=4){
                    if(String(i+1).length==1){
                        t1='000'+(Number(i)+1);
                    }else if(String(i+1).length==2){
                        t1='00'+(Number(i)+1);
                    }else if(String(i+1).length==3){
                        t1='0'+(+Number(i)+1);
                    }else{
                        t1=(+Number(i)+1);
                    };
                    t2=VHInfo[1]
                    t3=VHInfo[2]
                    if(t3.length>=8){
                        t3_=t3.slice(0,6)+'..';
                    }else{
                        t3_=t3;
                    };
                    t4=VHInfo[3]
                    if(t4.length>=8){
                        t4_=t4.slice(0,6)+'..';
                    }else{
                        t4_=t4;
                    };
                    t5=VHInfo[0];
                    text='志愿服务'+t1+'|日期:'+t2+'|地点:'+t3_+'|内容:'+t4_+'|时长:'+t5+'分钟';
                }else{
                    text='?10000多次志愿服务?';
                };
                var Username=document.getElementById('RUN').innerHTML;
                new_a.href='/file/'+Username+'$'+t5+'$'+t2+'$'+t3+'$'+t4
                new_a.innerHTML=text;
                new_a.style.animation='ShowVH 0.3s ease 1';
                new_a.style.animationFillMode='forwards';
                new_a.target="_blank";
                VHistoryDiv.appendChild(new_a);
            };
        };
        VHD.style.height='64vh';
        VHTip.style.display='block';
        VHP.style.display='block';
        ShowVHButton.innerHTML='志愿服务记录';
        IsShowVH='True';
    };
};
//  VH按下转跳换页键函数
function SVHPButton(){
    var InputVHP=document.getElementById('InputVHP');
    P=InputVHP.value;
    SetVHPage(Number(P));
};
//  VH左一页
function PM1(){
    NowVHPage=document.getElementById('NowVHPage');
    NowVHPage=NowVHPage.innerHTML;
    NowPage='';
    for(i=0;i<NowVHPage.length;i++){
        if(NowVHPage.slice(i,i+1)=='/'){
            break
        };
        NowPage=NowPage+NowVHPage.slice(i,i+1);
    };
    SetVHPage(Number(NowPage)-1)
};
//  VH右一页
function PP1(){
    NowVHPage=document.getElementById('NowVHPage');
    NowVHPage=NowVHPage.innerHTML;
    NowPage='';
    for(i=0;i<NowVHPage.length;i++){
        if(NowVHPage.slice(i,i+1)=='/'){
            break
        };
        NowPage=NowPage+NowVHPage.slice(i,i+1);
    };
    SetVHPage(Number(NowPage)+1)
};
//  VH切换志愿服务信息页码
function SetVHPage(Page){
    var NowVHPage=document.getElementById('NowVHPage');
    var VH=document.body.getElementsByClassName('VH');
    var VTimes=document.getElementById('Times');
    var InputVHP=document.getElementById('InputVHP');
    VTimes=VTimes.innerHTML;
    Page=Number(Page)
    if(Number(VTimes)%VHEPM==0){
        var MaxVHPage=Number(VTimes)%VHEPM;
    }else{
        var MaxVHPage=Math.ceil(Number(VTimes)/VHEPM);
    };
    if(Number(VTimes)/VHEPM>334){
        var MaxVHPage=334;
    };
    if(Number(VTimes)==0){
        var MaxVHPage=1;
    };
    if(!Number.isInteger(Page)){
        ShowInfo('页码必须是整数哦');
    }else{
        if(Page>MaxVHPage||Page<1){
            ShowInfo('页码超过允许范围了哦');
        }else{
            InputVHP.value=Page;
            NowVHPage.innerHTML=Page+'/'+MaxVHPage;
            VHPage=Page;
            IsShowVH='False';
            for(i=0;i<VH.length;i){
                VH[i].parentNode.removeChild(VH[i]);
            };
            ShowVH(VHPage);
        };
    };
};
//  发送账号密码信息给后端(弃用)
function LOGIN(){
    $.ajax({
        type: 'POST',
        url: '/',
        dataType: 'text',
        success: function(res){
           $('#LR').text(res['UserInfo']);
        },  
        error: function(){
            alert('error')  
        }  
     })
    var Username=document.getElementById('Username').value;
    var Password=document.getElementById('Password').value;
    var xmlhttp;
    if (window.XMLHttpRequest)
    {
      // IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
      xmlhttp=new XMLHttpRequest();
    }
    else
    {
      // IE6, IE5 浏览器执行代码
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open('POST','/',true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlhttp.send("Username="+Username+'&Password='+Password);
};
//  检测账号密码合法性(弃用)
function check(){
    var username = $('.ele-username').val();
    var password = $('.ele-password').val();
    if(!varify(username,/^[a-zA-Z][a-zA-Z0-9]{11,18}$/)){
        $('.regist-username .error-msg').html('用户名为3位以上数字和字母');
        return false;
    }
    if(!varify(password,/^[a-zA-Z0-9]{4,10}$/)){
        $('.regist-password .error-msg').html('请输入4-10位密码');
        return false;
    }
    return true;
};
//  忘了干嘛了，弃用
function varify(value,reg){
    $('.error-msg').html('');
    return reg.test(value)
};