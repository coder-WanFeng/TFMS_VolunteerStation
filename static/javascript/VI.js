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