# -*- coding: UTF-8 -*-
import os
import difflib
from django.http import HttpResponse
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from ERP.models import Bom,Coa,Mas,Stock
import time,datetime
import math
import heapq
def lzh(s):
    s=str(s)
    return s+'&nbsp;'

@csrf_exempt
def getbom(request):
    response=lzh('零件号')+lzh('描述')+lzh('装配数量')+lzh('单位')+lzh('层次')+'</br></br>'
    items=Bom.objects.filter().values()
    for item in items:
        for key in item:
            t=item[key]
            response+=lzh(t)
        response+='</br>'
    return HttpResponse(response)
@csrf_exempt
def getcoa(request):
    response=lzh('父物料号')+lzh('父物料名称')+lzh('子物料号')+lzh('子物料名称')+lzh('构成数')+lzh('配料提前期')+lzh('供应商提前期')+'</br></br>'
    items=Coa.objects.filter().values()
    for item in items:
        for key in item:
            t=item[key]
            response+=lzh(t)
        response+='</br>'
    return HttpResponse(response)
@csrf_exempt
def getmas(request):
    response=lzh('物料号')+lzh('名称')+lzh('单位')+lzh('调配方式')+lzh('损耗率')+lzh('作业提前期')+'</br></br>'
    items=Mas.objects.filter().values()
    for item in items:
        for key in item:
            t=item[key]
            response+=lzh(t)
        response+='</br>'
    return HttpResponse(response)
@csrf_exempt
def getstock(request):
    response=lzh('物料号')+lzh('物料名称')+lzh('工序库存')+lzh('资材库存')+'</br></br>'
    items=Stock.objects.filter().values()
    for item in items:
        for key in item:
            t=item[key]
            response+=lzh(t)
        response+='</br>'
    return HttpResponse(response)

@csrf_exempt
def updbom(request):
    str=request.GET.get('str')
    items=str.split('~')
    if len(items)==0:
        return HttpResponse('input format error')
    for item in items:
        item=item.split(' ')
        if len(item)!=5:
            return HttpResponse('input format error')
    #print(items)
    for item in items:
        item=item.split(' ')
        if Bom.objects.filter(id=item[0]).exists():
            Bom.objects.filter(id=item[0]).update(id=item[0],name=item[1],num=int(item[2]),unit=item[3],layer=int(item[4]))
        else:
            Bom.objects.filter(id=item[0]).create(id=item[0],name=item[1],num=int(item[2]),unit=item[3],layer=int(item[4]))
        
    return getbom(None)
@csrf_exempt
def updcoa(request):
    str=request.GET.get('str')
    items=str.split('~')
    if len(items)==0:
        return HttpResponse('input format error')
    for item in items:
        item=item.split(' ')
        if len(item)!=7:
            return HttpResponse('input format error')
    #print(items)
    for item in items:
        item=item.split(' ')
        if Coa.objects.filter(fid=item[0],sid=item[2]).exists():
            Coa.objects.filter(fid=item[0],sid=item[2]).update(fid=item[0],fname=item[1],sid=item[2],sname=item[3],num=int(item[4]),cleadtime=item[5],sleadtime=item[6])
        else:
            Coa.objects.filter(fid=item[0],sid=item[2]).create(fid=item[0],fname=item[1],sid=item[2],sname=item[3],num=int(item[4]),cleadtime=item[5],sleadtime=item[6])
    return getcoa(None)
@csrf_exempt
def updmas(request):
    str=request.GET.get('str')
    items=str.split('~')
    if len(items)==0:
        return HttpResponse('input format error')
    for item in items:
        item=item.split(' ')
        if len(item)!=6:
            return HttpResponse('input format error')
    #print(items)
    for item in items:
        item=item.split(' ')
        if Mas.objects.filter(id=item[0]).exists():
            Mas.objects.filter(id=item[0]).update(id=item[0],name=item[1],unit=item[2],method=item[3],lossrate=float(item[4]),leadtime=int(item[5]))
        else:
            Mas.objects.filter(id=item[0]).create(id=item[0],name=item[1],unit=item[2],method=item[3],lossrate=float(item[4]),leadtime=int(item[5]))
    return getmas(None)
@csrf_exempt
def updstock(request):
    str=request.GET.get('str')
    items=str.split('~')
    if len(items)==0:
        return HttpResponse('input format error')
    for item in items:
        item=item.split(' ')
        if len(item)!=4:
            return HttpResponse('input format error')
    #print(items)
    for item in items:
        item=item.split(' ')
        if Stock.objects.filter(id=item[0]).exists():
            Stock.objects.filter(id=item[0]).update(id=item[0],name=item[1],ostock=int(item[2]),mstock=int(item[3]))
        else:
            Stock.objects.filter(id=item[0]).create(id=item[0],name=item[1],ostock=int(item[2]),mstock=int(item[3]))
    return getstock(None)


@csrf_exempt
def homepage(request):
    return render(request,"homepage.html")
@csrf_exempt
def BOM(request):
    return render(request,"BOM.html")
@csrf_exempt
def COA(request):
    return render(request,"COA.html")
@csrf_exempt
def MAS(request):
    return render(request,"MAS.html")
@csrf_exempt
def stk(request):
    return render(request,"stock.html")
@csrf_exempt
def ERP(request):
    return render(request,"ERP.html")
class CompareAble:  
    def __init__(self,a,b,c,d,e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
    def __lt__(self,other):
        if self.e<other.e:
            return 1
        elif self.e>other.e:
            return 0
        if self.c<other.c:
            return 1
        return 0
def bfs(items):
    ret=''
    pq=[]
    for st in items:
        st=st.split(' ')
        st[1]=int(st[1])
        st[2]=datetime.date(*map(int,st[2].split('-')))
        st.append(st[2])
        m=Mas.objects.filter(name=st[0]).values()[0]
        meth=0
        if m['method']=='生产':
            st[2]=st[2]-datetime.timedelta(days=m['leadtime'])
        else:
            meth=1
            c=Coa.objects.filter(sname=st[0]).values()[0]
            st[2]=st[2]-datetime.timedelta(days=c['cleadtime']+c['sleadtime'])
        heapq.heappush(pq,CompareAble(st[0],st[1],st[2],st[3],meth))
    while pq:
        tmp=heapq.heappop(pq)
        tmp=[tmp.a,tmp.b,tmp.c,tmp.d,tmp.e]
        #print(tmp)
        s=Stock.objects.filter(name=tmp[0]).values()[0]
        ostock,mstock=s['ostock'],s['mstock']
        if tmp[1]<=ostock:
            ostock-=tmp[1]
            tmp[1]=0
        else:
            tmp[1]-=ostock
            ostock=0

        if tmp[1]<=mstock:
            mstock-=tmp[1]
            tmp[1]=0
        else:
            tmp[1]-=mstock
            mstock=0
        Stock.objects.filter(name=tmp[0]).update(ostock=ostock,mstock=mstock)
        if tmp[1]==0:
            tmp[2]=tmp[3]
        m=Mas.objects.filter(name=tmp[0]).values()[0]
        ret+=lzh(m['method'])+lzh(m['id'])+lzh(tmp[0])+lzh(tmp[1])+lzh(tmp[2])+lzh(tmp[3])+'</br>'
        
        nxt=Coa.objects.filter(fname=tmp[0]).values()
        #print(nxt)
        for c in nxt:
            m=Mas.objects.filter(id=c['sid']).values()[0]
            num,date=tmp[1],tmp[2]
            #print(m)
            if m['method']=='生产':
                meth=0
                date=date-datetime.timedelta(days=m['leadtime'])
                num=math.ceil(num*c['num']/(1-m['lossrate']))
            else:
                meth=1
                date=date-datetime.timedelta(days=c['cleadtime']+c['sleadtime'])
                num=math.ceil(num*c['num']/(1-m['lossrate']))
            heapq.heappush(pq,CompareAble(c['sname'],num,date,tmp[2],meth))
    return ret
    
@csrf_exempt
def compute(request):
    response=lzh('调配方式')+lzh('物料号')+lzh('物料名称')+lzh('需求数量')+lzh('日程下达日期')+lzh('日程完成日期')+'</br></br>'
    str=request.GET.get('str')
    items=str.split('~')
    if len(items)==0:
        return HttpResponse('input format error')
    for item in items:
        item=item.split(' ')
        if len(item)!=3:
            return HttpResponse('input format error')
    #print(items)
    response+=bfs(items)
    return HttpResponse(response)
    
    
