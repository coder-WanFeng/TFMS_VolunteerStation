#coding=UTF-8
import flask,pymongo,json,os,time,shutil,ast
from flask import Flask,render_template,request,send_file,redirect,url_for,session
from openpyxl import Workbook,load_workbook
from threading import Thread
#
from index import Index
from volunteer import Volunteer
from checkEM import AdminCheckEM
from output import Output
from tools import Users,VSAs
#from update import thread_update
#数据演示
'''
用户数据与管理员数据:{
    'username':str,     #用户名(手机号&身份证号)
    'password':str,     #密码
    'IsAdmin':str,      #(是否是管理员)
    'ID':str,           #昵称(真名)
    'SN':str,           #学号
    'VolunteerHistory':list     #志愿服务历史记录
    }

VolunteerHistory二维列表:
[
    [时长,时间,地点,内容,证明],
    [时长,时间,地点,内容,证明],
    .......
]

[时长,时间,地点,内容,证明]列表:
[
    时长,       #义工时长，单位为分钟
    时间,       #义工开始时间，格式为" 年-月-日 "
    地点,       #义工地点
    内容,       #义工内容
    证明        #义工证明，可以是文件
]
'''


#函数
#  获取配置
#    config.json
def LoadConfig():
    with open('config.json','r') as f:
        config=f.read()
        f.close()
        return json.loads(config)
#    用户数据库相关信息
def LoadUser():
    config=LoadConfig()
    UserIP=config['Data-IP']
    UserPORT=int(config['Data-PORT'])
    return UserIP,UserPORT
#  初始化数据库
def InitDB():
    UserIP,UserPORT=LoadUser()
    clict=pymongo.MongoClient(UserIP,UserPORT)
    db=clict['Users']
    if not 'Users' in clict.list_database_names(): db.create_collection('Users')
#  初始化FLASK
def InitFLASK():
    global DeBug,HOST,PORT
    config=LoadConfig()
    DeBug=bool(config['DeBug'])
    HOST=config['HOST']
    PORT=int(config['PORT'])

#  初始化函数
def Init():
    #thread_update()
    InitDB()
    InitFLASK()
    Users.Reg('TFMS','tedayz','Admin','泰达一中','00000000')
#初始化
Init()

#app
app=Flask(__name__)
#路由
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        return Index.post(request,render_template)
    else:
        return Index.get(render_template)

@app.route('/mobile/',methods=['GET', 'POST'])
def index_mobile():
    return render_template('index_mobile.html')

@app.route('/volunteerinfo/<username>/<ID>/<SN>/<Time>/<Date>/<Place>/<Content>/<Grade>/<Class>/',methods=['GET', 'POST'])
def VolunteerInfos(username,ID,SN,Time,Date,Place,Content,Grade,Class):
    if request.method=='POST':
        return render_template('index.html',AlertInfo='错误的请求类型')
    else:
        return render_template('volunteer_info.html',volunteerinfo=Volunteer.VolunteerInfos(username,ID,SN,Time,Date,Place,Content,Grade,Class))
    
@app.route('/VI/<vi>/',methods=['GET', 'POST'])
def VI(vi):
    UserInfo,l,AlertInfo=Volunteer.VI(vi,request)
    return render_template('VI.html',username=UserInfo['username'],ID=UserInfo['ID'],SN=UserInfo['SN'],Time=UserInfo['Time'],Date=UserInfo['Date'],Place=UserInfo['Place'],Content=UserInfo['Content'],EM=UserInfo['EM'],t=l,AlertInfo=AlertInfo)

@app.route('/file/<filename>/',methods=['GET', 'POST'])
def file(filename):
    path='files/'+filename.replace("@","/")
    if os.path.exists(path):
        for root,dirs,files in os.walk(path, topdown=False):
            pass# print(root,dirs,files)
        r=render_template('show_files.html',filelist=files,Files=filename)
    else: r=render_template('index.html',AlertInfo='文件不存在')
    return r

@app.route('/showfile/<files>/<filename>/',methods=['GET', 'POST'])
def showfile(files,filename):
    file='files/'+files.replace("@","/")+'/'+filename.replace("@","/")
    if os.path.exists(file):
        r=send_file(file,as_attachment=False)
    else: r=render_template('index.html',AlertInfo='文件不存在')
    return r

@app.route('/BCVH/',methods=['GET', 'POST'])
def BCVH():
    BCVHs=AdminCheckEM.BCVH()
    return render_template('BCVHs.html',BCVHs=BCVHs)

@app.route('/ACEM/<vi>/',methods=['GET', 'POST'])
def ACEM(vi):
    UserInfo,l,AlertInfo=AdminCheckEM.ACEM(vi,request)
    if UserInfo=='Error':
        return render_template('BCVHs.html',AlertInfo=AlertInfo,BCVHs=l)
    else:
        return render_template('CVH.html',username=UserInfo['username'],ID=UserInfo['ID'],Time=UserInfo['Time'],Date=UserInfo['Date'],Place=UserInfo['Place'],Content=UserInfo['Content'],SN=UserInfo['SN'],EM=UserInfo['EM'],t=l,AlertInfo=AlertInfo)

@app.route('/VSA/<Name>/<Place>/<Content>/<Time>/<StartTime>/<EndTime>',methods=['GET', 'POST'])
def VSA(Name,Place,Content,Time,StartTime,EndTime):
    if request.method=='GET':
        VSA=VSAs.Show_VSA(Name,Place,Content,StartTime,EndTime,Time)[0]
        if type(VSA)==type({"":""}):
            PromotionPoster=VSA['PromotionPoster']
            return render_template('ChangeVSA.html',ChangeVSA_Name=Name,ChangeVSA_Place=Place,ChangeVSA_Content=Content,ChangeVSA_StartTime=StartTime.replace("_",":"),ChangeVSA_EndTime=EndTime.replace("_",":"),ChangeVSA_Time=Time,ChangeVSA_PromotionPoster=PromotionPoster)
        else:
            return render_template('ChangeVSA.html',ChangeVSA_Name=Name,ChangeVSA_Place=Place,ChangeVSA_Content=Content,ChangeVSA_StartTime=StartTime.replace("_",":"),ChangeVSA_EndTime=EndTime.replace("_",":"),ChangeVSA_Time=Time,ChangeVSA_PromotionPoster=PromotionPoster)
    else:
        AlertInfo,new_VSA=VSAs.VSA_change(Name,Place,Content,StartTime,EndTime,Time,request)
        return render_template('ChangeVSA.html',ChangeVSA_Name=new_VSA['Name'],ChangeVSA_Place=new_VSA['Place'],ChangeVSA_Content=new_VSA['Content'],ChangeVSA_StartTime=new_VSA['StartTime'].replace(":","_"),ChangeVSA_EndTime=new_VSA['EndTime'].replace(":","_"),ChangeVSA_Time=new_VSA['Time'],AlertInfo=AlertInfo)
    
@app.route('/show_VSA/<Name>/<Place>/<Content>/<Time>/<StartTime>/<EndTime>',methods=['GET', 'POST'])
def shhow_VSA(Name,Place,Content,Time,StartTime,EndTime):
    if request.method=='GET':
        VSA=VSAs.Show_VSA(Name,Place,Content,StartTime,EndTime,Time)[0]
        if type(VSA)==type({"":""}):
            PromotionPoster=VSA['PromotionPoster']
            return render_template('VSA.html',ChangeVSA_Name=Name,ChangeVSA_Place=Place,ChangeVSA_Content=Content,ChangeVSA_StartTime=StartTime.replace("_",":"),ChangeVSA_EndTime=EndTime.replace("_",":"),ChangeVSA_Time=Time,ChangeVSA_PromotionPoster=PromotionPoster)
        else:
            return render_template('VSA.html',ChangeVSA_Name=Name,ChangeVSA_Place=Place,ChangeVSA_Content=Content,ChangeVSA_StartTime=StartTime.replace("_",":"),ChangeVSA_EndTime=EndTime.replace("_",":"),ChangeVSA_Time=Time,ChangeVSA_PromotionPoster=PromotionPoster)
    else:
        AlertInfo,new_VSA=VSAs.VSA_change(Name,Place,Content,StartTime,EndTime,Time,request)
        return render_template('VSA.html',ChangeVSA_Name=new_VSA['Name'],ChangeVSA_Place=new_VSA['Place'],ChangeVSA_Content=new_VSA['Content'],ChangeVSA_StartTime=new_VSA['StartTime'].replace(":","_"),ChangeVSA_EndTime=new_VSA['EndTime'].replace(":","_"),ChangeVSA_Time=new_VSA['Time'],AlertInfo=AlertInfo)

@app.route('/VSA_info/<is_admin>/<Name>/<Place>/<Content>/<StartTime>/<EndTime>/<Time>/',methods=['GET', 'POST'])
def VSA_Info(is_admin,Name,Place,Content,StartTime,EndTime,Time):
    VSA=VSAs.Search_VSA(Name,Place,Content,StartTime,EndTime,Time)
    return render_template('VSA_info.html',VSAs=VSA,is_admin=is_admin)

@app.route('/output/<type>/',methods=['GET', 'POST'])
def outputfile(type):
    is_err,r=Output.Output(type,send_file)
    if is_err==True:
        r=render_template('index.html',AlertInfo='错误的链接!\n请手动关闭该页面!',Replace='')
    return r

@app.route('/export/<file_type>/<search_type>/<requirements>/',methods=['GET', 'POST'])
def exportfile(file_type,search_type,requirements):
    is_err,r=Output.Export(file_type,search_type,requirements,send_file)
    if is_err==True:
        r=render_template('index.html',AlertInfo='错误的链接!\n请手动关闭该页面!',Replace='')
    return r


@app.errorhandler(404)
def page_not_found(msg):
    return render_template('404.html',msg=msg)

@app.errorhandler(500)
def server_error(msg):
    return render_template('500.html',msg=msg)

if __name__ =="__main__":
    app.run(debug=DeBug,host=HOST,port=PORT)

    #111#111