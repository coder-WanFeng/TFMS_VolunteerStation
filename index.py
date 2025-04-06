#coding=UTF-8

from tools import Tools,Users,VSAs


class Index():
    def __init__():
        return "[post,get]"
    def post(request,render_template):
        type=request.form.get('post_type')
        if type=='login':
            Username=request.form.get('Username')
            Password=request.form.get('Password')
            if Tools.CheckStr(Username) and Tools.CheckStr(Password):
                r=Users.login(Username,Password,'','',render_template)
            else: r=render_template('index.html',AlertInfo='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)',username=Username,password=Password)
        elif type=='reg':
            Username=request.form.get('POST-Username')
            RegUsername=request.form.get('RegUsername')
            RegPassword=request.form.get('RegPassword')
            IsAdmin=request.form.get('RegIA')
            ID=request.form.get('RegID')
            SN=request.form.get('RegSN')
            if Tools.CheckStr(Username):
                if Tools.CheckStr(RegUsername) and Tools.CheckStr(RegPassword) and Tools.CheckStr(IsAdmin) and Tools.CheckStr(ID) and Tools.CheckStr(SN):
                    r=Users.RegUser(Username,RegUsername,RegPassword,IsAdmin,ID,SN,render_template)
                else: r=Tools.LoginAndAlertInfo(Username,'含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)','',render_template)
        elif type=='check':#这段...没用...
            Username=request.form.get('POST-Username')
            RegUsername=request.form.get('RegUsername')
            RegPassword=request.form.get('RegPassword')
        elif type=='search':
            POST_Username=request.form.get('POST-Username')
            Search_Username=request.form.get('SearchUsername')
            if Tools.CheckStr(POST_Username):
                if Tools.CheckStr(Search_Username):
                    r=Tools.Search(POST_Username,Search_Username,render_template)
                else: r=Tools.LoginAndAlertInfo(POST_Username,'含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)','',render_template)
        elif type=='upload':
            if request.files.getlist('UploadEM'):
                file=request.files.getlist('UploadEM')
                Username=request.form.get('POST-Username')
                if file:
                    for i in file:
                        if not Tools.CheckStr(i.filename): return Tools.LoginAndAlertInfo(Username,'文件名不符合要求!','',render_template)
                        elif not i.filename[-4:].lower() in ['.pdf','.jpg','.jpe','jpeg','jfif','.bmp','.gif','tiff','.tif','.png']: return Tools.LoginAndAlertInfo(Username,'文件格式不符合要求!','',render_template)
                    UploadDate=request.form.get('UploadDate')
                    UploadTime=request.form.get('UploadTime')
                    UploadPlace=request.form.get('UploadPlace')
                    UploadContent=request.form.get('UploadContent')
                    if Tools.CheckStr(UploadDate) and Tools.CheckStr(UploadTime) and Tools.CheckStr(UploadPlace) and Tools.CheckStr(UploadContent):
                        r=Users.UUL(Username,UploadTime,UploadDate,UploadPlace,UploadContent,file,render_template)
                    else: r=Tools.LoginAndAlertInfo(Username,'含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)','',render_template)
                else:
                    r=Tools.LoginAndAlertInfo(Username,'只能上传pdf、png、jpg文件!','',render_template)
            else:
                Username=request.form.get('POST-Username')
                r=Tools.LoginAndAlertInfo(Username,'证明材料是必填项','',render_template)
        elif type=='ChangeID':
            Username=request.form.get('POST-Username')
            NewID=request.form.get('NewID')
            if Tools.CheckStr(Username):
                if Tools.CheckStr(NewID):
                    Info=Users.ChangeID(Username,NewID)
                else: Info='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
            r=Tools.LoginAndAlertInfo(Username,Info,'',render_template)
        elif type=='ChangePassword':
            Username=request.form.get('POST-Username')
            NowPassword=request.form.get('NowPassword')
            NewPassword=request.form.get('NewPassword')
            if Tools.CheckStr(Username):
                if Tools.CheckStr(NowPassword) and Tools.CheckStr(NewPassword):
                    Info=Users.ChangePassword(Username,NowPassword,NewPassword)
                else: Info='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
            r=Tools.LoginAndAlertInfo(Username,Info,'',render_template)
        elif type=='acup':
            Username=request.form.get('POST-Username')
            UserSN=request.form.get('ACUP-SN')
            NewPassword=request.form.get('ACUP-Password')
            if Tools.CheckStr(Username):
                if Tools.CheckStr(UserSN) and Tools.CheckStr(UserSN):
                    Info=Users.AdminChangeUserPassword(UserSN,NewPassword)
                else: Info='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
            r=Tools.LoginAndAlertInfo(Username,Info,'',render_template)
        elif type=='s&c':
            Username=request.form.get('POST-Username')
            r=Tools.LoginAndAlertInfo(Username,'这是一个没有作用的提示框','',render_template)
        elif type=='create-vsa':
            Username=request.form.get('POST-Username')
            VSA_Info={
                "Name":request.form.get('CreateVSA-Name'),
                "Place":request.form.get('CreateVSA-Place'),
                "Content":request.form.get('CreateVSA-Content'),
                "StartTime":request.form.get('CreateVSA-StartTime'),
                "EndTime":request.form.get('CreateVSA-EndTime'),
                "Time":request.form.get('CreateVSA-Time'),
                "PromotionPoster":request.files.getlist('CreateVSA-PromotionPoster'),
            }
            AlertInfo=VSAs.CreateVSA(VSA_Info)
            r=Tools.LoginAndAlertInfo(Username,AlertInfo,'',render_template)
        elif type=='change-vsa':
            Username=request.form.get('POST-Username')
            r=Tools.LoginAndAlertInfo(Username,'这是一个没有作用的提示框','',render_template)
        elif type=='create-vsa':
            Username=request.form.get('POST-Username')
            r=Tools.LoginAndAlertInfo(Username,'这是一个没有作用的提示框','',render_template)
        else:
            r=render_template('index.html',AlertInfo='错误的请求类型,请重试并联系管理员')
        return r
    
    def get(render_template):
        return render_template('index.html')