#coding=UTF-8

from tools import Tools,Users




class Volunteer():

    def __init__():
        return "?"
    
    def VolunteerInfos(username,ID,SN,Time,Date,Place,Content,Grade,Class,render_template=None,request=None):
        L=['username','ID','SN','Time','Date','Place','Content','Grade','Class']
        l=[username[1:],ID[1:],SN[1:],Time[1:],Date[1:],Place[1:],Content[1:],Grade[1:],Class[1:]]
        Dictionary={}
        for i in range(len(L)):
            if l[i]: Dictionary.update({L[i]:l[i]})
        volunteerinfo=Tools.FilterVH(Dictionary)
        VI=[]
        for i in volunteerinfo:
            VI.append(['学号:'+i['SN']+'|'+i['Grade']+'级'+i['Class']+'班|用户名:'+i['username']+'|昵称:'+i['ID']+'|日期:'+i['Date']+'|地点:'+i['Place']+'|内容:'+i['Content']+'|时长:'+i['Time']+'分钟',i['EMFilename']])
        if len(VI)==0: VI='未找到符合要求的数据或筛选条件不符合要求!'
        else: VI.insert(0,'已找到符合要求的 {} 条数据'.format(len(volunteerinfo)))
        volunteerinfo=VI
        return volunteerinfo

    def VI(vi,request):
        l=[]
        strs=''
        for i in range(len(vi)):
            if vi[i]=='=': strs=''
            elif vi[i]=='|':
                l.append(strs)
                strs=''
            else: strs+=vi[i]
        l.append(strs)
        UserInfo={
            'username':l[2],
            'ID':l[3],
            'SN':l[0],
            'Time':l[7][:-2],
            'Date':l[4],
            'Place':l[5],
            'Content':l[6],
            'EM':l[8]
        }
        if request.method=='POST':
            VIs=['username','ID','SN','Time','Date','Place','Content','EM','AdminUsername','AdminPassword']
            for i in range(len(VIs)): VIs[i]=request.form.get(VIs[i])
            IsPass=False
            for i in range(len(VIs)):
                if i!=7 and not Tools.CheckStr(VIs[i]):
                    AlertInfo='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
                    IsPass=True
            if IsPass: pass
            else:
                if Users.Login(VIs[8],VIs[9])=='Admin':
                    AlertInfo=Tools.UpdateVH(VIs[0],VIs[3],VIs[4],VIs[5],VIs[6],VIs[7])
                    NewEM=VIs[0]+'$'+str(VIs[3])+'$'+str(VIs[4])+'$'+str(VIs[5])+'$'+str(VIs[6])
                    UserInfo={
                        'username':VIs[0],
                        'ID':VIs[1],
                        'SN':VIs[2],
                        'Time':VIs[3],
                        'Date':VIs[4],
                        'Place':VIs[5],
                        'Content':VIs[6],
                        'EM':NewEM
                    }
                else: AlertInfo='您似乎没有通过管理员验证，可能是账号或密码输入错误'
        else: AlertInfo=''
        return UserInfo,l,AlertInfo