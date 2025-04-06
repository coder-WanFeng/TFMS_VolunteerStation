$(document).ready(function() {  
    $('.Date').on('input', function() {  
        $('.Date').val($(this).val());  
    });  
});
$(document).ready(function() {  
    $('.Time').on('input', function() {  
        $('.Time').val($(this).val());  
    });  
});
$(document).ready(function() {  
    $('.Place').on('input', function() {  
        $('.Place').val($(this).val());  
    });  
});
$(document).ready(function() {  
    $('.Content').on('input', function() {  
        $('.Content').val($(this).val());  
    });  
});

var AlertDivExit=document.getElementById('AlertDivExit');
if(AlertDivExit){
    AlertDivExit.onclick=AlertExit
};
function AlertExit(){
    var AlertDiv=document.getElementById('AlertDiv');
    AlertDiv.style.display='none';
};

var CLS_True=document.getElementById('CLS');
var CLS_False=document.getElementById('CLS-False');
CLS_True.onclick=RVIT;
CLS_False.onclick=RVIF;
function RVIT(){
    RVI('True');
};
function RVIF(){
    RVI('False');
};
function RVI(IsTrue){
    var VHIsTrue=document.getElementById('VHIsTrue');
    VHIsTrue.value=String(IsTrue);
};