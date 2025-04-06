#coding=UTF-8
import time,pymongo,ast
from openpyxl import Workbook


from tools import Tools
from volunteer import Volunteer

class Output():

    def __init__():
        return "?????"
    
    def OutputTxt(send_file):
        t=int(time.time())
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        with open('files/files/txt/用户数据{}.txt'.format(t),'a',encoding='utf-8') as f1:
            f1.write('按下Ctrl+S可保存!\n')
            for i in list(Users.find({})):
                UserVH=''
                VTimes=0
                VTime=0
                VHistory=list(i['VolunteerHistory'])
                for j in range(len(VHistory)):
                    VTimes=len(list(VHistory))
                    VTime+=float(list(VHistory[j])[0])
                    VH='='*15+'\n第'+str(j+1)+'次志愿服务:\n时长:'+VHistory[j][0]+'\n时间:'+VHistory[j][1]+'\n地点:'+VHistory[j][2]+'\n内容:'+VHistory[j][3]+'\n'
                    UserVH+=VH
                    if float(VTime)==int(VTime):
                        VTime=int(VTime)
                    else:
                        VTime='Null'
                UserInfo='='*30+'\n用户名:'+str(i['username'])+'\n密码:'+str(i['password'])+'\n身份:'+str(i['IsAdmin'])+'\n昵称:'+str(i['ID'])+'\n学号:'+str(i['SN'])+'\n志愿服务次数:'+str(VTimes)+'\n志愿服务时长:'+str(VTime)+'\n'
                f1.write(UserInfo+UserVH)
            f1.close()
        return send_file('files/files/txt/用户数据{}.txt'.format(t),as_attachment=False)
    
    def ExportSheet(filename,send_file):
        UserIP,UserPORT=Tools.LoadUser()
        clict=pymongo.MongoClient(UserIP,UserPORT)
        db=clict['Users']
        Users=db['Users']
        n=0
        workbook=Workbook()
        sheet=workbook.active
        sheet['A1']='账号'
        sheet['B1']='用户名'
        sheet['C1']='密码'
        sheet['D1']='身份'
        sheet['E1']='昵称'
        sheet['F1']='学号'
        sheet['G1']='志愿服务次数'
        sheet['H1']='志愿服务时长(分钟)'
        for i in list(Users.find({})):
            n+=1
            VTime=0
            VHistory=list(i['VolunteerHistory'])
            VTimes=len(VHistory)
            for j in range(len(VHistory)):
                VTime+=float(VHistory[j][0])
                if float(VTime)==int(VTime):
                    VTime=int(VTime)
                else:
                    VTime='Null'
            l=[n,'username','password','IsAdmin','ID','SN',VTimes,VTime]
            STR='ABCDEFGH'
            for j in range(len(STR)):
                if j in [0,6,7]: sheet[STR[j]+str(n+1)]=str(l[j])
                else: sheet[STR[j]+str(n+1)]=str(i[l[j]])
        workbook.save(filename=filename)
        return send_file(filename)
    
    def Output(type,send_file):
        if type=='txt':
            is_error,r=False,Output.OutputTxt(send_file)
        elif type=='xls':
            filename='export'+str(int(time.time()))
            is_error,r=False,Output.ExportSheet('files/files/xls/'+filename+'.xls',send_file)
        elif type=='xlsx':
            filename='export'+str(int(time.time()))
            is_error,r=False,Output.ExportSheet('files/files/xlsx/'+filename+'.xlsx',send_file)
        else:
            is_error,r=True,'格式异常'
        return is_error,r
    
    def ExportVIs(filename,send_file,VIs=[]):
        L=['SN','C&G','username','ID','Date','Place','Content','Time']
        if len(VIs)>2:
            VIs=ast.literal_eval(VIs)
            eval_VIs=[]
            for i in VIs:
                l=[]
                strs=''
                is_val=False
                for j in range(len(i[0])):
                    if i[0][j]==':':
                        is_val=not is_val
                    if i[0][j]=='|' or j==len(i[0])-1:
                        l.append(strs[1:]) if i[0][j]=='|' else l.append(strs[1:]+i[0][j])
                        strs=''
                        is_val=False
                    else:
                        strs+=i[0][j] if is_val else ""
                eval_VIs.append(l)
            eval_VIs=[eval_VI[:-1]+[eval_VI[-1][:-2]] for eval_VI in eval_VIs]
            volunteerinfo=[[eval_VI[2]]+[eval_VI[3]]+[eval_VI[0]]+[eval_VI[0][:4]]+[eval_VI[0][4:6]]+[eval_VI[0][6:]]+[eval_VI[4]]+[eval_VI[5]]+[eval_VI[6]]+[eval_VI[7]] for eval_VI in eval_VIs]#用户名 昵称 8位学号 年级(届) 班级 2位学号 志愿服务日期 志愿服务地点 志愿服务内容 记录志愿服务时长(分钟)
        else:
            volunteerinfo=[]
        if len(volunteerinfo)==0:
            pass
        else:#用户名 昵称 8位学号 年级(届) 班级 2位学号 志愿服务日期 志愿服务地点 志愿服务内容 记录志愿服务时长(分钟)
            workbook=Workbook()
            sheet=workbook.active
            words='ABCDEFGHIJK'
            sheet['A1']='志愿服务序号'
            sheet['B1']='用户名'
            sheet['C1']='昵称'
            sheet['D1']='8位学号'
            sheet['E1']='年级(届)'
            sheet['F1']='班级'
            sheet['G1']='2位学号'
            sheet['H1']='志愿服务日期'
            sheet['I1']='志愿服务地点'
            sheet['J1']='志愿服务内容'
            sheet['K1']='记录志愿服务时长(分钟)'
            for vi_n in range(len(volunteerinfo)):
                for word_n in range(len(words)):
                    if word_n==0:
                        sheet['{}{}'.format(words[word_n],vi_n+2)]=vi_n+1
                    else:
                        sheet['{}{}'.format(words[word_n],vi_n+2)]=volunteerinfo[vi_n][word_n-1]
            workbook.save(filename=filename)
        return False,send_file(filename)
    
    def Export(file_type,search_type,requirements,send_file):
        if file_type=='txt':
            is_error,r=True,'不支持'
        elif file_type=='xls':
            filename='export'+str(int(time.time()))
            is_error,r=Output.ExportVIs('files/files/xls/'+filename+'.xls',send_file,VIs=requirements)
        elif file_type=='xlsx':
            filename='export'+str(int(time.time()))
            is_error,r=Output.ExportVIs('files/files/xlsx/'+filename+'.xlsx',send_file,VIs=requirements)
        else:
            is_error,r=True,'格式异常'
        return is_error,r