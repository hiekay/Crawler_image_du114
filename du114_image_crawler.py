#coding:utf-8
"""
  Author:  Sparrow
  Purpose: downloading image from www.lofter.com in every blog's page once.
  Created: 2016-7.4
  Email: sparrow629@163.com
"""
from __future__ import print_function
from bs4 import BeautifulSoup
import urllib
import re
import os

global Urls
global Category
URLs =  {1:'http://www.du114.com/gaoqingtaotu/xiuren/',
			 2:'http://www.du114.com/a/Mygirl/',
			 3:'http://www.du114.com/a/Beautyleg/',
			 4:'http://www.du114.com/a/TGOD/',
			 5:'http://www.du114.com/gaoqingtaotu/TuiGirl/',
			 6:'http://www.du114.com/gaoqingtaotu/youguowang/',
			 7:'http://www.du114.com/a/s-cute/',
			 8:'http://www.du114.com/a/TopQueen/',
			 9:'http://www.du114.com/a/DGC/',
			 10:'http://www.du114.com/a/Bomb.tv/',
			 11:'http://www.du114.com/a/RQ_STARxiezhen/',
			 12:'http://www.du114.com/a/Tpimage/',
			 13:'http://www.du114.com/a/3Agirl/',
			 14:'http://www.du114.com/a/simei/',
			 15:'http://www.du114.com/a/rosi/',
			 16:'http://www.du114.com/a/ligui/',
			 17:'http://www.du114.com/a/disi/',
			 18:'http://www.du114.com/a/Ru1mm/',
			 19:'http://www.du114.com/a/siwameinv/'
			 }
Category = { 1:'秀人套图',
			 2:'美媛馆',
			 3:'Beautyleg写真',
			 4:'推女神',
			 5:'TuiGirl推女郎',
			 6:'尤果网',
			 7:'s-cute',
			 8:'TopQueen',
			 9:'DGC',
			 10:'Bombtv',
			 11:'RQ_STAR写真',
			 12:'Tpimage',
			 13:'3Agirl',
			 14:'丝魅VIP',
			 15:'ROSI写真',
			 16:'丽柜写真',
			 17:'disi印象',
			 18:'Ru1mm如壹',
			 19:'丝袜系列套图',
			 20:'全部下载',
			 0:'自选粘贴限套图第一页url',
			 111:'某一tag标签页'
			   }

def getHtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

def getImage(html,mode):
	Soup = BeautifulSoup(html, 'lxml')
	# print Soup
	imagetag = Soup.select('#picBody > p > a > img ')[0]
	filenametag = Soup.select('body > div.w1200 > div.w960.r > div.articleBox > div.articleTitle > h1')
	filename = filenametag[0].get_text()

	imgurl = imagetag.get('src')


	if mode == 1:
		foldernames = Soup.select('body > div.w1200 > div.w960.r > div.articleBox > div.position > a')[-1]
		foldername = foldernames.get_text()
		# print(foldernames,foldername,sep='\n')
		path = 'imgdownload/%s/' % foldername

	elif mode == 3:
		foldernames = Soup.select('body > div.w1200 > div.w960.r > div.articleBox > div.position > a')[-1]
		foldername = foldernames.get_text()
		# print(foldernames,foldername,sep='\n')
		path = 'imgdownload/%s/%s/' % (foldername,Themename)
		# print(Themenametag,path,sep='\n')

	elif mode == 0:

		path = 'imgdownload/%s/' % Foldername

	if not os.path.exists(path):
		os.makedirs(path)
	target = path + '%s.jpg' % filename
	urllib.urlretrieve(imgurl, target)

	print(filename,imgurl,sep='\n')
	print("Downloading file to %s" % target)

def Findallpic(html,firsturl):
	Soup = BeautifulSoup(html, 'lxml')

	global Themename
	Themenametag = Soup.select('body > div.w1200 > div.w960.r > div.articleBox > div.articleTitle > h1')
	Themename = Themenametag[0].get_text()

	pagenumtag = Soup.select('body > div.w1200 > div.w960.r > div.articleBox > div.pages > ul > li > a')
	pagenumtext = pagenumtag[0].get_text()
	reg_num = '[0-9]*'
	finalpagenumber = int(re.findall(reg_num,pagenumtext)[1])
	PicUrllist = {1:firsturl
			   }
	firsturllink = firsturl[:-5]
	print('''-----------------------------------------------------------
			此套图共有%s张图片''' % finalpagenumber)

	for i in range(2,finalpagenumber+1):
		picurl = firsturllink + '_' + str(i) + '.html'
		PicUrllist[i] = picurl
	# print(PicUrllist)
	return PicUrllist

def ListCategoryUrl(num):
	print(num, Category[num], URLs[num], sep=' => ')
	return URLs[num]

def FindAllPage(html,currenturl):
	Soup = BeautifulSoup(html, 'lxml')
	finalpagetag = Soup.select('body > div.w1200 > div.w960.r > div.pages > ul > li > a')
	if finalpagetag:
		finalpage = finalpagetag[-1].get('href')
		reg_page = r'list_.*_(.*)\.html'
		finalpagenumber = int(re.findall(reg_page,finalpage)[0])

		reg_list = r'(list_.*_).*\.html'
		page_list = re.findall(reg_list,finalpage)[0]
		i = 0
		PageList = {}
		print("共有%s页" % finalpagenumber,page_list)
		for i in range(1,finalpagenumber+1):
			page = currenturl + page_list + str(i) + '.html'
			PageList[i] = page
			# print(page)
		# print("this is pagetlist:",PageList)
	else:
		PageList = {1:currenturl}
	return PageList



def SelectTheme(html,key):
	Soup = BeautifulSoup(html, 'lxml')
	ThemeTag = Soup.select('#imgList > ul > li > span.both.title > a')
	# print(ThemeTag)
	Themelist = {}

	Themecount = key * 100 + 1
	for href in ThemeTag:
		Themelist[Themecount]=(href.get('href'))
		Themecount += 1

	Titlelist = []
	for title in ThemeTag:
		Titlelist.append(title.get('title'))

	Themecount = key * 100 + 1
	for i in range(0,len(Titlelist)):
		print(Themecount+i,Titlelist[i],sep='=>')

	# print(Themelist)
	return Themelist

def PathMode():
	pathMode = 0
	while not ((pathMode == 1) or (pathMode == 3)):
		print("-----------------------------------------\n",
			  "所有图片下载在同一目录下请输入数字 1\n",
			  "选择套图根据名称分别下载在独立子目录请输入数字 3")
		pathMode = int(raw_input('请输入数字选择保存图片的目录的方式:'))
	return pathMode

def getTagImg(html):
	Soup = BeautifulSoup(html, 'lxml')

	global Foldername

	foldernames = Soup.select('body > div.w1200 > div.w960.r > div > div.top_content > h1 > a')[-1]
	Foldername = foldernames.get_text()
	print(foldernames, Foldername, sep='\n')
	Themelist = SelectTheme(html,0)
	print(Themelist)
	for key1 in Themelist:
		Theme_url = Themelist[key1]
		Pics_url_list = Findallpic(getHtml(Theme_url), Theme_url)
		pic_count = 0
		for key2 in Pics_url_list:
			getImage(getHtml(Pics_url_list[key2]),0)
			pic_count +=1
	print('--------------------成功下载了%s张图片--------------------' % pic_count)

if __name__ == '__main__':
	#1.测试图片下载和找图片功能
	# Copy_url = 'http://www.du114.com/gaoqingtaotu/xiuren/109837.html'
	# Pics_url_list = Findallpic(getHtml(Copy_url),Copy_url)
	# pic_count = 0
	# for key in Pics_url_list:
	# 	getImage(getHtml(Pics_url_list[key]),3)
	# 	pic_count += 1
	# print('--------------------成功下载了%s张图片--------------------' % pic_count)

	#2.测试tag下载功能
	# Copy_url = 'http://www.du114.com/tag/1295.html'
	# getTagImg(getHtml(Copy_url))


	Quit_program = 'Y'
	while not Quit_program == 'N':
		for key in URLs:
			print(key, Category[key], URLs[key], sep=' => ')
		print('20 =>', Category[20])
		print('0 =>', Category[0])
		print('111 =>',Category[111])
		num = -1
		while not Category.has_key(num):
			num = input('选择一个系列的对应数字进行下载: ')

		if URLs.has_key(num):
			category_url = ListCategoryUrl(num)
			category_html = getHtml(category_url)
			Pagelists = FindAllPage(category_html,category_url)

			ThemeLists = {}
			for key in Pagelists:
				print("%s 页" % key,Pagelists[key],sep='=>')
				pagehtml = getHtml(Pagelists[key])
				themelist = SelectTheme(pagehtml,key)
				Themecounts = themelist.keys()
				for i in Themecounts:
					ThemeLists[i] = themelist[i] #把每一页的Themes写入list字典得到所有图的首页url
			print("共有%s幅套图" % len(ThemeLists))

			print('''
			上面是每一页对应的套图名称,你可以往上浏览过后
			选择下载模式:
			1.先下载该系列所有封面预览图
			2.按页下载
			3.按主题下载
			4.下载此系列全部套图
			''')
			Mode = {1:'先下载该系列所有预览图',
					2:'按页下载',
					3:'按主题下载',
					4:'下载此系列全部套图'
					}

			select_downloading_mode = 0
			while not Mode.has_key(select_downloading_mode) :
				select_downloading_mode = int(raw_input('请输入下载模式对应的数字: '))
			print('你选择了 %s.%s' % (select_downloading_mode,Mode[select_downloading_mode]))

			if select_downloading_mode == 1:
				for key in ThemeLists:
					themehtml = getHtml(ThemeLists[key])
					getImage(themehtml,select_downloading_mode)
				print('成功下载了%s张预览图' % len(ThemeLists.keys()))

			elif select_downloading_mode == 2:
				chose_quit = 'Y'
				while not chose_quit == 'N':
					for key in Pagelists:
						print("%s 页" % key, Pagelists[key], sep='=>')

					pageNumber = 0
					while not Pagelists.has_key(pageNumber):
						pageNumber = int(raw_input("请输入你要下载的页码:"))

					print('第%s页的套图名称如下:' % pageNumber)
					pagehtml = getHtml(Pagelists[pageNumber])
					current_page_themelist = SelectTheme(pagehtml, pageNumber)

					Path_Mode = PathMode()

					ent = raw_input('取消下载请按[q],继续请回车:')
					if not (ent == 'q'):
						for key in current_page_themelist:
							list_url = current_page_themelist[key]
							PicUrlList = Findallpic(getHtml(list_url),list_url)
							for key in PicUrlList:
								pic_html = PicUrlList[key]
								getImage(getHtml(pic_html),Path_Mode)
						Number = len(current_page_themelist.keys())*len(PicUrlList.keys())
						print('--------------------成功下载了%s张图片--------------------' % Number)

					chose_quit = raw_input('继续选择下载请按键[Y],退出请按键[N]:')

			elif select_downloading_mode == 3:
				chose_quit = 'Y'

				while not chose_quit == 'N':
					Theme_number = int(raw_input("请根据上面的套图名称对应的编号输入数字:"))
					Theme_url = ThemeLists[Theme_number]
					Pics_url_list = Findallpic(getHtml(Theme_url),Theme_url)
					pic_count = 0
					for key in Pics_url_list:
						getImage(getHtml(Pics_url_list[key]),select_downloading_mode)
						pic_count +=1
					print('--------------------成功下载了%s张图片--------------------' % pic_count)

					chose_quit = raw_input('继续选择下载请按键[Y],退出请按键[N]:')

			elif select_downloading_mode == 4:

				Path_Mode = PathMode()
				pic_count = 0
				for key1 in ThemeLists:
					Theme_url = ThemeLists[key1]
					Pics_url_list = Findallpic(getHtml(Theme_url),Theme_url)
					for key2 in Pics_url_list:
						getImage(getHtml(Pics_url_list[key2]),Path_Mode)
						pic_count +=1
				print('--------------------成功下载了%s张图片--------------------' % pic_count)

		else:
			print(Category[num])
			if num == 0:
				chose_quit = 'Y'
				while not chose_quit == 'N':
					Copy_url = raw_input('请把要下载的套图首页的链接地址粘贴到此:')
					Pics_url_list = Findallpic(getHtml(Copy_url),Copy_url)
					pic_count = 0
					for key in Pics_url_list:
						getImage(getHtml(Pics_url_list[key]),3)
						pic_count += 1
					print('--------------------成功下载了%s张图片--------------------' % pic_count)

					chose_quit = raw_input('继续选择下载请按键[Y],退出请按键[N]:')

			if num == 111:
				chose_quit = 'Y'
				while not chose_quit == 'N':
					Copy_url = raw_input('请把要下载标签页的链接地址粘贴到此:')
					getTagImg(getHtml(Copy_url))
					chose_quit = raw_input('继续选择下载请按键[Y],退出请按键[N]:')

			if num == 20:
				print("正在研究多线程下载")
				# break
		Quit_program = raw_input('继续选择下载请按键[Y],退出程序请按键[N]:')
