//检测是否为移动端(参考app.py)
if( ((innerWidth/innerHeight)>1)/* && (!(/mobile/i.test(navigator.userAgent)))*/){//宽<=长则判断为移动端
    TurnIndex()
}
else{
    document.getElementById("bottom_texts").style.display="none";
    alert("正在启用横屏兼容模式,可能存在错误哦~");
};
function TurnIndex(){
    window.location.replace('/')
};
