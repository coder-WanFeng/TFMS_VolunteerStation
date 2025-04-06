#coding=UTF-8
import pymongo,os,shutil


from tools import Tools,Users




class AdminCheckEM():

    def __init__():
        return "????"
    
    def AdminCheckEM(Old_UI,Username,Time,Date,Place,Content,IsTrue):
        r=''
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        BeforeCheckVHs=db['BCVHs']
        User=Users.find_one({'username':Username})
        if User:
            Username=User['username']
            Password=User['password']
            Info={
                'username':str(Username),
                'password':str(Password),
                'Time':str(Time),
                'Date':str(Date),
                'Place':str(Place),
                'Content':str(Content)
            }
            Old_EM=Old_UI['EM']
            Old_UI={
                'username':Old_UI['username'],
                'Time':Old_UI['Time'],
                'Date':Old_UI['Date'],
                'Place':Old_UI['Place'],
                'Content':Old_UI['Content']
            }
            BeforeCheckVH=BeforeCheckVHs.find_one(Old_UI)
            BeforeCheckVH2=BeforeCheckVHs.find_one(Info)
            if BeforeCheckVH:
                if BeforeCheckVH==BeforeCheckVH2 or not BeforeCheckVH2:
                    if IsTrue=='True':
                        EvidentiartMaterialFileName=Username+'$'+str(Time)+'$'+str(Date)+'$'+str(Place)+'$'+str(Content)
                        r=Tools.InsertVH(Username,Password,Time,Date,Place,Content,EvidentiartMaterialFileName)
                        files=os.listdir('files/{}/'.format(Old_EM))
                        for file in range(len(list(files))):
                            os.rename("files/{}/{}".format(Old_EM,files[file]),"files/{}/{}".format(Old_EM,EvidentiartMaterialFileName+'$n'+str(file)+os.path.splitext(files[file])[1]))
                        os.rename('files/{}/'.format(Old_EM),'files/{}/'.format(EvidentiartMaterialFileName))
                        BeforeCheckVHs.delete_many(Old_UI)
                    elif IsTrue=='False':
                        filename=EvidentiartMaterialFileName=Username+'$'+str(Time)+'$'+str(Date)+'$'+str(Place)+'$'+str(Content)
                        file='files/'+filename
                        BeforeCheckVHs.delete_many(Old_UI)
                        shutil.rmtree(file)
                        r='删除完成!'
                    else:
                        r='错误的状态，服务器不清楚您是否通过该志愿服务信息'
                else:
                    r="已存在相同的志愿服务记录!"
            else:r='暂无符合要求的数据，可能是该志愿服务信息已审核完成，请尝试刷新并验证其它志愿服务信息!'
        else: r='用户不存在'
        return r

    def ACEM(vi,request):
        l=[]
        strs=''
        for i in range(len(vi)):
            if vi[i]=='=': strs=''
            elif vi[i]=='|':
                l.append(strs)
                strs=''
            else: strs+=vi[i]
        l.append(strs)
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        db_Users=db['Users']
        User=db_Users.find_one({'username':str(l[0])})
        UserInfo={
            'username':l[0],
            'SN':User['SN'],
            'ID':l[1],
            'Time':l[5][:-2],
            'Date':l[2],
            'Place':l[3],
            'Content':l[4],
            'EM':l[6]
        }
        if request.method=='POST':
            VIs=['username','ID','SN','Time','Date','Place','Content','EM','AdminUsername','AdminPassword','IsTrue']
            for i in range(len(VIs)): VIs[i]=request.form.get(VIs[i])
            IsPass=False
            for i in range(len(VIs)):
                if i!=7 and not Tools.CheckStr(VIs[i]):
                    AlertInfo='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
                    IsPass=True
            if IsPass:
                pass
            else:
                if Users.Login(VIs[8],VIs[9])=='Admin':
                    NewEM=VIs[0]+'$'+str(VIs[3])+'$'+str(VIs[4])+'$'+str(VIs[5])+'$'+str(VIs[6])
                    Old_UI=UserInfo
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
                    AlertInfo=AdminCheckEM.AdminCheckEM(Old_UI,UserInfo['username'],UserInfo['Time'],UserInfo['Date'],UserInfo['Place'],UserInfo['Content'],VIs[10])
                    BCVHs=Tools.ListBCVH()
                    if BCVHs:
                        BCVHs.insert(0,'还有{}条志愿服务信息没有审核'.format(len(BCVHs)))
                        for i in range(len(BCVHs)):
                            if i==0: continue
                            VI=BCVHs[i]
                            EMname=str(VI['username'])+'$'+str(VI['Time'])+'$'+str(VI['Date'])+'$'+str(VI['Place'])+'$'+str(VI['Content'])
                            BCVHs[i]=['用户名:'+VI['username']+'|昵称:'+VI['ID']+'|日期:'+VI['Date']+'|地点:'+VI['Place']+'|内容:'+VI['Content']+'|时长:'+VI['Time']+'分钟',EMname]
                    else: BCVHs='none'
                    return "Error",BCVHs,AlertInfo
                else:
                    AlertInfo='您似乎没有通过管理员验证，可能是账号或密码输入错误'
        else: AlertInfo=''
        return UserInfo,l,AlertInfo

    def BCVH():
        BCVHs=Tools.ListBCVH()
        if BCVHs:
            BCVHs.insert(0,'还有{}条志愿服务信息没有审核'.format(len(BCVHs)))
            for i in range(len(BCVHs)):
                if i==0: continue
                VI=BCVHs[i]
                EMname=str(VI['username'])+'$'+str(VI['Time'])+'$'+str(VI['Date'])+'$'+str(VI['Place'])+'$'+str(VI['Content'])
                BCVHs[i]=['用户名:'+VI['username']+'|昵称:'+VI['ID']+'|日期:'+VI['Date']+'|地点:'+VI['Place']+'|内容:'+VI['Content']+'|时长:'+VI['Time']+'分钟',EMname]
        else: BCVHs='none'
        return BCVHs