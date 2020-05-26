# -*- coding: UTF-8 -*-
import os
import difflib
from django.http import HttpResponse
import urllib.parse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
@csrf_exempt
def submit(request):
	return render(request,"index.html");
@csrf_exempt
def recommend(request):
    qn=request.GET.get('name')
    if qn!=None:
        productMap={}
        product=[]
        inShop=[set() for i in range(0,10000)]
        recommendList=[]
        with open('all.txt','r') as fin:
            n=int(fin.readline())
            for i in range(0,n):
                line=fin.readline().strip('\n')
                line=line.split(' ')
                inShop[int(line[0])].add(int(line[5]))
            n=int(fin.readline())
            Max=0
            for i in range(0,n):
                line=fin.readline().strip('\n')
                line=line.split(' ')
                productMap[line[0]]=(line[1],line[2])
                sim=difflib.SequenceMatcher(None,qn,line[1]).ratio()
                if sim>Max:
                    Max=sim
                    product=line
                    
            if product==[]:
                return HttpResponse('cannot find similar product')
        
            while True:
                line=fin.readline().strip('\n').strip('L').strip(':')
                if line=='':
                    break
                line=line.split(' ')
                x=int(line[0])
                n=int(line[1])
                for i in range(0,n):
                    line=fin.readline().strip('\n').rstrip().split(' ')
                    if product[0] in line:
                        recommendList=line
        for i in range(0,len(recommendList)):
            recommendList[i]=(recommendList[i],productMap[recommendList[i]][0],productMap[recommendList[i]][1],inShop[int(recommendList[i])])
        res={'id':product[0],'name':product[1],'price':product[2],'result':recommendList}
        #return HttpResponse(res)
        data='商品编号：'+res['id']+'<br/>商品名称：'+res['name']+'<br/>商品价格：'+res['price']+'<br/><br/>推荐列表：<br/>'
        for item in res['result']:
            if item[0]==product[0]:
                continue
            data=data+'商品编号：'+item[0]+'<br/>商品名称：'+item[1]+'<br/>商品价格：'+item[2]+'<br/>可以在以下便利店购买：'
            for sh in item[3]:
                data=data+str(sh)+'  '
            data=data+'<br/><br/>'
        return HttpResponse(data)
    else:
        return HttpResponse('please input product name')
    
    
