#coding=UTF-8
import json,pymongo,os




class Tools():

    def __init__():
        return
    
    def CheckStr(text):
        IsTrue=True
        for i in text:
            if i in list('!@#$%^&*|'):
                IsTrue=False
        return IsTrue
    
    def LoadConfig():
        with open('config.json','r') as f:
            config=f.read()
            f.close()
            return json.loads(config)
    
    def LoadUser():
        config=Tools.LoadConfig()
        UserIP=config['Data-IP']
        UserPORT=int(config['Data-PORT'])
        return UserIP,UserPORT

    def LoginAndAlertInfo(Username,AlertInfo,Replace,render_template):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username)})
        if User: Password=User['password']
        else: return render_template('index.html',AlertInfo='账号不存在',Replace=Replace)
        from tools import Users
        return Users.login(Username,Password,AlertInfo,Replace,render_template)
    
    def Search(POST_Username,Username,render_template):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username)})
        if User:
            if User['IsAdmin']=='Admin': r=Tools.LoginAndAlertInfo(POST_Username,'您不能查询管理员志愿服务信息!','',render_template)
            else: r=Tools.LoginAndAlertInfo(Username,'已转跳至查询账号!','',render_template)
        else:
            r=Tools.LoginAndAlertInfo(POST_Username,'账号不存在','',render_template)
        return r
    
    def TryIntOrFloatStr(value):  
        try:
            return int(value)
        except ValueError:  
            try:
                return float(value)
            except ValueError:
                return value

    def is_match(item, key, value):
        if isinstance(value, str) and ('{' in value or '[' in value):
            conditions = value.split('}')
            ranges = [c for c in conditions if c.startswith('{')]
            exacts = [c for c in conditions if c.startswith('[')]
            range_matches = all(map(lambda r: Tools.is_range_match(item, key, r), ranges))
            exact_matches = all(map(lambda e: Tools.is_exact_match(item, key, e), exacts))
            return range_matches and exact_matches
        return item.get(key, None) == value
    
    def is_range_match(item, key, range_str):
        m, n = map(float, range_str[1:].split(','))
        return m <= float(item.get(key, '-inf')) <= n
    
    def is_exact_match(item, key, exact_str):
        value = exact_str[1:-1]
        return item.get(key, None) == value
    
    def parse_range(range_str):
        if range_str.startswith('{') and range_str.endswith('}'):
            range_str = range_str[1:-1]
            values = range_str.split(',')
            return (Tools.TryIntOrFloatStr(values[0]), Tools.TryIntOrFloatStr(values[1]))
        return None

    def matches_criteria(item, key, value):
        item_value = Tools.TryIntOrFloatStr(item.get(key, ''))
        if isinstance(value, str):
            range_value = Tools.parse_range(value)
            if range_value:
                return range_value[0] <= item_value <= range_value[1]
        return item_value == value

    def parse_condition(condition):
        if condition.startswith('{') and condition.endswith('}'):
            # 处理集合形式,即形如{m,n}的条件
            values_str = condition[1:-1]
            # 判断集合是否为空
            if len(values_str) != 0:
                # 生成集合内容列表
                values_list = values_str.split(',')
                # 判断是否符合并返回
                return lambda x: x in values_list
        elif condition.startswith('[') and condition.endswith(']'):
            # 处理区间形式,即形如[M,N]的条件
            values_str = condition[1:-1]
            # 判断区间是否为空
            if len(values_str) != 0:
                # 生成集合内容列表
                values_list = values_str.split(',')
                # 判断集合是否为1项(若1项，视为选定该目标(例如[0]视为筛选0))
                if len(values_list) == 1:
                    return lambda x: x == condition
                # 判断集合是否为1项
                elif len(values_list) == 2:
                    # 生成最大值和最小值
                    M=float(values_list[0])
                    N=float(values_list[1])
                    # 判断是否符合并返回
                    return lambda x: M <= float(x) <= N
        else:
            # 处理直接写入形式，即精准查找
            return lambda x: x == condition

    def FilterVH(dictionary):
        # 获取用户信息
        UserIP, UserPORT = Tools.LoadUser()
        client = pymongo.MongoClient(UserIP, UserPORT)
        db = client['Users']
        Users = db['Users']
        User = Users.find()
        # 创建候选列表
        VHs = []
        # 对符合要求的用户循环
        for i in User:
            # 获取义工次数
            VTimes = len(list(i['VolunteerHistory']))
            # 对义工次数进行循环
            for vh in range(VTimes):
                # 获取该次义工信息
                VTime = float(list(i['VolunteerHistory'])[vh][0])
                VDate = list(i['VolunteerHistory'])[vh][1]
                VPlace = list(i['VolunteerHistory'])[vh][2]
                VContent = list(i['VolunteerHistory'])[vh][3]
                VEMF = list(i['VolunteerHistory'])[vh][4]
                # 尝试将义工时长转为整数
                if float(VTime) == int(VTime):
                    VTime = int(VTime)
                # 生成义工信息字典
                VInfo = {
                    'username': i['username'],
                    'password': i['password'],
                    'IsAdmin': i['IsAdmin'],
                    'ID': i['ID'],
                    'SN': i['SN'],
                    'Time': str(VTime),
                    'Date': VDate,
                    'Place': VPlace,
                    'Content': VContent,
                    'EMFilename': VEMF,
                    'Grade': i['SN'][0:4],
                    'Class': str(int(i['SN'][4:6]))
                }
                # 将义工信息字典加入候选列表
                VHs.append(VInfo)
        
        # 创建筛选列表
        filtered_VHs = []
        # 对候选列表循环
        for item in VHs:
            # 判断该次义工是否符合要求
            if all(Tools.parse_condition(str(value))(item.get(key, '')) for key, value in dictionary.items()):
                # 将该次义工加入筛选列表
                filtered_VHs.append(item)
        # 返回筛选列表
        return filtered_VHs


    def UpdateVH(Username,Time,Date,Place,Content,EM):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        BeforeCheckVHs=db['BCVHs']
        User=dict(Users.find_one({'username':str(Username)}))
        if User:
            Password=User['password']
            try:
                Time=float(Time)
                if Time>=10000 or Time!=int(Time) or Time<1:
                    return '志愿服务时长应是1~9999的整数!'
                Upload_VH=[str(Time),str(Date),str(Place),str(Content)]
                for i in Upload_VH:
                    if not i: return '数据异常，所有内容不能为空'
                    elif len(i)>12:  return '内容长度限制:12字符及以下!'
            except:
                return '数据格式异常'
            if Time==int(Time):
                Time=int(Time)
            Newfilename=Username+'$'+str(Time)+'$'+str(Date)+'$'+str(Place)+'$'+str(Content)
            VH=User['VolunteerHistory']
            NewVH=[str(Time),str(Date),str(Place),str(Content),Newfilename]
            VInfo={
                'username':str(Username),
                'password':str(Password),
                'Time':str(Time),
                'Date':str(Date),
                'Place':str(Place),
                'Content':str(Content),
            }
            for i in range(len(VH)):
                if VH[i][4]==EM:
                    for j in VH:
                        if NewVH[0:len(NewVH)-1]==j[0:len(j)-1] or NewVH[0:len(NewVH)-1] in j[0:len(j)-1]: return '存在完全相同的记录!(已验证)'
                    if BeforeCheckVHs.find_one(VInfo): return '存在完全相同的记录!(未验证)'
                    User['VolunteerHistory'][i]=NewVH
                    file_names=os.listdir('files/'+EM)
                    n=0
                    for name in file_names:
                        n+=1
                        old_file_name = os.path.join('files/'+EM,name)
                        new_file_name = os.path.join('files/'+EM,Newfilename+'n{}.'.format(n)+old_file_name.split(".")[1])
                        os.rename(old_file_name,new_file_name)
                    os.rename('files/'+EM,'files/'+Newfilename)
                    Users.delete_one({'username':str(Username)})
                    Users.insert_one(User)
                    r='修改成功'
                    break
        else:  r='修改失败，账号不存在'
        return r
    
    def ListBCVH():
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        BCVHs=db['BCVHs']
        BCVH=BCVHs.find({})
        BCVHList=[]
        for i in BCVH:
            VI=dict(i)
            Users=db['Users']
            username=VI['username']
            User=Users.find_one({'username':username})
            UserID=User['ID']
            VI.update({'ID':UserID})
            BCVHList.append(VI)
        return BCVHList
    
    def InsertVH(Username,Password,Time,Date,Place,Content,EvidentiartMaterial):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username),'password':str(Password)})
        if not Users.find_one({'username':str(Username)}): r='用户不存在'
        elif User:
            NewVH=[str(Time),str(Date),str(Place),str(Content),str(EvidentiartMaterial)]
            VH=User['VolunteerHistory']
            VH.append(NewVH)
            UserInfo={
                'username':User['username'],
                'password':User['password'],
                'IsAdmin':User['IsAdmin'],
                'ID':User['ID'],
                'SN':User['SN'],
                'VolunteerHistory':VH,
                }
            Users.delete_one({'username':str(Username),'password':str(Password)})
            Users.insert_one(UserInfo)
            r='志愿服务记录添加成功!'
        else: r='密码错误'
        return r
    
    def GetVSA(requirements):
        res=Tools.FilterVH(requirements)
        return res


class Users():

    def __init__():
        return
    
    def Reg(username,password,IsAdmin,ID,SN):
        if not username:
            r='"账号名"不能为空'
        elif not password:
            r='"密码"不能为空'
        elif not IsAdmin:
            r='"身份"不能为空'
        elif not ID:
            r='"昵称"不能为空'
        elif not SN:
            r='"学号"不能为空'
        else:
            UserIP,UserPORT=Tools.LoadUser()
            clict=pymongo.MongoClient(UserIP,UserPORT)
            db=clict['Users']
            Users=db['Users']
            if str(IsAdmin) in ['User','Admin']:
                if Users.find_one({'username':str(username)}): r='用户名已被注册(若您不需要继续注册新账号,建议退出登录后重新登录,否则可能会因刷新时自动重新提交表单而重新注册该账号)'
                elif Users.find_one({'SN':str(SN)}): r='学号已被注册(若您不需要继续注册新账号,建议退出登录后重新登录,否则可能会因刷新时自动重新提交表单而重新注册该账号)'
                else:
                    try:
                        Users.insert_one({'username':str(username),'password':str(password),'IsAdmin':str(IsAdmin),'ID':str(ID),'SN':str(SN),'VolunteerHistory':[]})
                        r='注册成功(若您不需要继续注册新账号,建议退出登录后重新登录,否则可能会因刷新时自动重新提交表单而重新注册该账号)'
                    except: r='数据努库遇到未知错误，无法注册用户'
            else: r='"身份"仅允许填写"Admin"或"User"'
        return r
    
    def RegUser(Username,RegUsername,RegPassword,IsAdmin,ID,SN,render_template):
        AlertInfo=Users.Reg(RegUsername,RegPassword,IsAdmin,ID,SN)
        return Tools.LoginAndAlertInfo(Username,AlertInfo,'',render_template)
    
    def login(Username,Password,AlertInfo,Replace,render_template):
        UserInfo={'ID':'无该用户','VTime':'无该用户','VTimes':'无该用户','VH':'无该用户','SN':'无该用户'}
        LoginResult=Users.Login(Username,Password)
        if LoginResult=='None':
            return render_template('index.html',AlertInfo='无该用户!')
        elif LoginResult=='wrong password':
            return render_template('index.html',AlertInfo='密码错误!')
        elif LoginResult=='Admin':
            UserInfo=Users.GetAdminInfo(Username,Password)
            VTime='Infinity'
            RVH='Null'
        elif LoginResult=='User':
            UserInfo=Users.GetUserInfo(Username,Password)
            VH=UserInfo['VHistory']
            RVH=[]
            for i in VH:
                i[0]=float(i[0])
                if int(i[0])==i[0]: i[0]=int(i[0])
                else: i[0]='Null'
                RVH.append(i[0:len(i)])
            UserInfo['VHistory']=RVH
            VTime=UserInfo['VTime']
            if int(VTime)==float(VTime): VTime=int(VTime)
            else: VTime='Null'
        if AlertInfo: r=render_template('index.html',IsAdmin=LoginResult,UserID=UserInfo['ID'],VTime=VTime,VTimes=UserInfo['VTimes'],VH=RVH,SN=UserInfo['SN'],Username=Username,AlertInfo=AlertInfo,Replace=Replace,username=Username,password=Password)
        else: r=render_template('index.html',IsAdmin=LoginResult,UserID=UserInfo['ID'],VTime=VTime,VTimes=UserInfo['VTimes'],VH=RVH,SN=UserInfo['SN'],Username=Username,Replace=Replace,username=Username,password=Password)
        return r
    
    def Login(username,password):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        UserInfo=Users.find_one({'username':username})
        if UserInfo:
            if UserInfo['password']==password:
                if UserInfo['IsAdmin']=='Admin': r='Admin'
                else: r='User'
            else:
                r='wrong password'
        else:
            r='None'
        return r

    def GetAdminInfo(Username,Password):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username),'password':str(Password)})
        if User:
            result={
                'IsAdmin':User['IsAdmin'],
                'ID':User['ID'],
                'SN':list(User['SN']),
                'VTime':'Infinity',
                'VTimes':'Null',
                'VHistory':'Null',
                }
        else: result='账号或密码错误!'
        return result
    
    def GetUserInfo(Username,Password):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username),'password':str(Password)})
        VTimes=len(list(User['VolunteerHistory']))
        VTime=0
        for i in range(VTimes):
            VTime+=float(list(User['VolunteerHistory'])[i][0])
        if float(VTime)==int(VTime): VTime=int(VTime)
        else:VTime='Null'
        result={
            'IsAdmin':User['IsAdmin'],
            'ID':User['ID'],
            'SN':User['SN'],
            'VTime':VTime,
            'VTimes':VTimes,
            'VHistory':User['VolunteerHistory'],
            }
        return result
    
    def UserUpLoad(Username,Password,Time,Date,Place,Content,EvidentiartMaterial):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'username':str(Username),'password':str(Password)})
        if not Users.find_one({'username':str(Username)}): r='账号不存在'
        elif User:
            VH=User['VolunteerHistory']
            IVH={
                'username':str(Username),
                'password':str(Password),
                'Time':str(Time),
                'Date':str(Date),
                'Place':str(Place),
                'Content':str(Content),
            }
            UVH=[str(Time),str(Date),str(Place),str(Content)]
            for k in VH:
                if UVH[0:len(UVH)]==k[0:len(k)-1] or UVH[0:len(UVH)] in k[0:len(k)-1]: return '存在完全相同的记录!(已验证)'
            BeforeCheckVHs=db['BCVHs']
            if BeforeCheckVHs.find_one(IVH): return '存在完全相同的记录!(未验证)'
            try:
                Time=float(Time)
                if Time>=10000 or Time!=int(Time) or Time<1:
                    return '志愿服务时长应是1~9999的整数!'
                Upload_VH=[str(Time),str(Date),str(Place),str(Content)]
                for i in Upload_VH:
                    if not i: return '数据异常，所有内容不能为空'
                    elif len(i)>12:  return '内容长度限制:12字符及以下!'
            except:
                return '数据格式异常'
            if Time==int(Time):
                Time=int(Time)
            filename=Username+'$'+str(Time)+'$'+str(Date)+'$'+str(Place)+'$'+str(Content)
            for i in EvidentiartMaterial:
                if not '.' in i.filename: return '错误的文件格式'
            n=0
            os.makedirs('files/{}'.format(filename))
            for j in EvidentiartMaterial:
                last=j.filename.split('.')
                fnl=last[-1]
                j.save('files/{}/{}.{}'.format(filename,str(filename)+'$n'+str(n),fnl))
                n+=1
            BeforeCheckVHs.insert_one(IVH)
            r='上传成功，请等待管理员进行验证'
        else:  r='上传失败，可能是账号或密码错误'
        return r
    
    def UUL(Username,Time,Date,Place,Content,EM,render_template):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        db_Users=db['Users']
        User=db_Users.find_one({'username':str(Username)})
        if User:
            Password=User['password']
            UploadResult=Users.UserUpLoad(Username,Password,Time,Date,Place,Content,EM)
        else:
            UploadResult='账号不存在!'
        return Tools.LoginAndAlertInfo(Username,UploadResult,'',render_template)
    
    def ChangeID(username,NewID):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        BCVHs=db['BCVHs']
        User=dict(Users.find_one({'username':username}))
        UserID=User['ID']
        if str(NewID)==str(UserID):
            r='您要修改的昵称与您现在的昵称相同!'
        else:
            User['ID']=str(NewID)
            Users.delete_one({'username':username})
            Users.insert_one(User)
            r='昵称修改成功!'
        return r
    
    def ChangePassword(username,nowpassword,newpassword):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        BCVHs=db['BCVHs']
        User=dict(Users.find_one({'username':username}))
        if str(nowpassword)==str(newpassword):
            r='当前密码不能等于新的密码!'
        elif User['password']==str(nowpassword):
            User['password']=str(newpassword)
            UserBCVHs=BCVHs.find({'username':username})
            for i in UserBCVHs:
                del i['_id']
                BCVH=i
                BCVH['password']=str(newpassword)
                BCVHs.delete_one(i)
                BCVHs.insert_one(BCVH)
            Users.delete_one({'username':username})
            Users.insert_one(User)
            r='密码修改成功!'
        else: r='密码错误'
        return r
    
    def AdminChangeUserPassword(SN,Password):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        User=Users.find_one({'SN':SN})
        if User:
            if User['password']==Password: r='当前密码与新的密码相同!'
            else:
                UserInfo={
                    'username':User['username'],
                    'password':Password,
                    'IsAdmin':User['IsAdmin'],
                    'ID':User['ID'],
                    'SN':User['SN'],
                    'VolunteerHistory':User['VolunteerHistory'],
                    }
                Users.delete_one({'SN':SN})
                Users.insert_one(UserInfo)
                r='修改成功'
        else: r='学号不存在'
        return r
    
class VSAs():

    def __init__():
        return
    
    def CreateVSA(VSA_Info):
        search_VSA_Info=VSA_Info.copy()
        del search_VSA_Info['PromotionPoster']
        is_allow=[Tools.CheckStr(i) for i in list(VSA_Info.values())[:-1]]
        if False in is_allow:
            r='含有禁止使用的字符(禁止使用的字符包括:!@#$%^&*|)'
        else:
            if list(Tools.GetVSA(search_VSA_Info))==[]:
                UserIP,UserPORT=Tools.LoadUser()
                clict=pymongo.MongoClient(UserIP,UserPORT)
                db=clict['Users']
                VSAs=db['VSAs']
                files=VSA_Info['PromotionPoster']
                FileNames=[]
                os.makedirs('files/VSAs/{}'.format((str(VSA_Info['Name'])+'$'+str(VSA_Info['Place'])+'$'+str(VSA_Info['Content'])+'$'+str(VSA_Info['StartTime'])+'$'+str(VSA_Info['EndTime'])+'$'+str(VSA_Info['Time'])).replace(":","_")))
                if files:
                    for i in range(len(list(files))):
                        if not "." in files[i].filename:
                            r='文件格式错误!'
                        elif not Tools.CheckStr(files[i].filename):
                            r='文件名不符合要求!'
                        elif not files[i].filename[-4:].lower() in ['.jpg','.jpe','jpeg','jfif','.bmp','.gif','tiff','.tif','.png']:
                            r='文件格式不符合要求!'
                        else:
                            filename=(str(VSA_Info['Name'])+'$'+str(VSA_Info['Place'])+'$'+str(VSA_Info['Content'])+'$'+str(VSA_Info['StartTime'])+'$'+str(VSA_Info['EndTime'])+'$'+str(VSA_Info['Time'])).replace(":","_")
                            last=files[i].filename.split('.')
                            fnl=last[-1]
                            files[i].save('files/VSAs/{}/{}.{}'.format(filename,str(filename)+'$n'+str(i),fnl))
                            FileNames.append(filename+'$n'+str(i)+"."+fnl)
                    VSA_Info['PromotionPoster']=FileNames
                    VSAs.insert_one(VSA_Info)
                    r="发布志愿服务活动成功"
                else:
                    r='只能上传png、jpg文件!'
            else:
                r="已经存在完全相同的志愿服务活动了"
        return r
    
    def ChangeVSA(VSA_Info,new_VSA_Info):
        search_VSA_Info=VSA_Info.copy()
        del search_VSA_Info['PromotionPoster']
        search_new_VSA_Info=new_VSA_Info.copy()
        del search_new_VSA_Info['PromotionPoster']
        if list(Tools.GetVSA(search_VSA_Info))!=[]:
            if list(Tools.GetVSA(search_new_VSA_Info))==[]:
                UserIP,UserPORT=Tools.LoadUser()
                clict=pymongo.MongoClient(UserIP,UserPORT)
                db=clict['Users']
                VSAs=db['VSAs']
                oldPP=(str(VSA_Info['Name'])+'$'+str(VSA_Info['Place'])+'$'+str(VSA_Info['Content'])+'$'+str(VSA_Info['StartTime'])+'$'+str(VSA_Info['EndTime'])+'$'+str(VSA_Info['Time'])).replace(":","_")
                PP=(str(new_VSA_Info['Name'])+'$'+str(new_VSA_Info['Place'])+'$'+str(new_VSA_Info['Content'])+'$'+str(new_VSA_Info['StartTime'])+'$'+str(new_VSA_Info['EndTime'])+'$'+str(new_VSA_Info['Time'])).replace(":","_")
                files=os.listdir('files/VSAs/{}/'.format(oldPP))
                for file in range(len(list(files))):
                    os.rename("files/VSAs/{}/{}".format(oldPP,files[file]),"files/VSAs/{}/{}".format(oldPP,PP+'$n'+str(file)+os.path.splitext(files[file])[1]))
                os.rename('files/VSAs/{}/'.format(oldPP),'files/VSAs/{}/'.format(PP))
                new_VSA_Info['PromotionPoster']=os.listdir('files/VSAs/{}/'.format(PP))
                VSAs.delete_many(VSA_Info)
                VSAs.insert_one(new_VSA_Info)
                r="修改志愿服务活动成功"
            else:
                r="已存在完全相同的志愿服务活动"
        else:
            r="原始志愿服务活动不存在，可能已被修改或删除"
        return r
    
    def DeleteVSA(VSA_Info):
        search_VSA_Info=VSA_Info.copy()
        del search_VSA_Info['PromotionPoster']
        if list(Tools.GetVSA(search_VSA_Info))!=[]:
            UserIP,UserPORT=Tools.LoadUser()
            clict=pymongo.MongoClient(UserIP,UserPORT)
            db=clict['Users']
            VSAs=db['VSAs']
            VSAs.delete_one(VSA_Info)
            r="删除志愿服务活动成功"
        else:
            r="原始志愿服务活动不存在，可能已被修改或删除"
        return r
    
    def Show_VSA(Name,Place,Content,StartTime,EndTime,Time):
        VSA_Info={
            "Name":Name,
            "Place":Place,
            "Content":Content,
            "StartTime":StartTime.replace("_",":"),
            "EndTime":EndTime.replace("_",":"),
            "Time":Time,
        }
        print(VSA_Info)
        need_del=[]
        for key in VSA_Info.keys():
            if VSA_Info[key]==None or VSA_Info[key]=="":
                need_del.append(key)
        print(need_del)
        for del_key in need_del:
            del VSA_Info[del_key]
        print(VSA_Info)
        VSAs=Tools.GetVSA(VSA_Info)
        r=list(VSAs) if list(VSAs) else "未查询到符合条件的志愿服务活动"
        return r
    
    def Search_VSA(Name,Place,Content,StartTime,EndTime,Time):
        VSA_list=VSAs.Show_VSA(Name[1:],Place[1:],Content[1:],StartTime[1:],EndTime[1:],Time[1:])
        if type(VSA_list)==type(""):
            VSA_list=[VSA_list]
        else:
            print(VSA_list)
            VSA_list=[["地点:{}|内容:{}|时长:{}|活动时间:{}".format(VSA['Place'],VSA['Content'],VSA['Time'],VSA['Date'])] for VSA in VSA_list]
            VSA_list=["已找到符合要求的{}条数据".format(len(VSA_list))]+VSA_list if len(VSA_list)>0 else VSA_list
        return VSA_list
    
    def VSA_change(Name,Place,Content,StartTime,EndTime,Time,request):
        old_VSA_Info={
            "Name":Name,
            "Place":Place,
            "Content":Content,
            "StartTime":StartTime.replace("_",":"),
            "EndTime":EndTime.replace("_",":"),
            "Time":Time,
        }
        VSA_Info={
            "Name":request.form.get('ChangeVSA-Name'),
            "Place":request.form.get('ChangeVSA-Place'),
            "Content":request.form.get('ChangeVSA-Content'),
            "StartTime":request.form.get('ChangeVSA-StartTime').replace("_",":"),
            "EndTime":request.form.get('ChangeVSA-EndTime').replace("_",":"),
            "Time":request.form.get('ChangeVSA-Time'),
        }
        old_VSA_Info["PromotionPoster"]=Tools.GetVSA(old_VSA_Info)[0]["PromotionPoster"]
        VSA_Info["PromotionPoster"]=Tools.GetVSA(old_VSA_Info)[0]["PromotionPoster"]
        if request.form.get('isTrue')=='True':
            r=VSAs.ChangeVSA(old_VSA_Info,VSA_Info)
        else:
            r=VSAs.DeleteVSA(old_VSA_Info)
        return r,VSA_Info