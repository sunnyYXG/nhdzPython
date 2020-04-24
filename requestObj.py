import requests
import bs4
import os
from requestSetting import settingObject

def download_file(web_url):
	req = requests.get(web_url)
	soup = bs4.BeautifulSoup(req.text, 'html.parser')
	# 查找图片资源
	img_list = soup.select('.vpic_wrap img')
	if img_list == []:
		print('找不到图片资源')
	else:
		for img_info in img_list:
			file_url = img_info.get('bpic')
			write_file(file_url, 1)

	# 查找视频资源
	video_list = soup.select('.threadlist_video a')
	if video_list == []:
		print('找不到视频资源')
	else:
		for video_info in video_list:
			file_url = video_info.get('data-video')
			write_file(file_url, 2)

	print('资源下载结束', web_url)
	next_link = soup.select('#frs_list_pager .next')
	if next_link == []:
		print('下载资源结束')
	else:
		file_url = next_link[0].get('href')
		download_file('https:' + file_url)

	
def write_file(file_url, file_type):
	# 写入文件
	respose = requests.get(file_url)
	if file_type == 1:
		file_folder = 'nhdzImages'
	elif file_type == 2:
		file_folder = 'nhdzVideos'
	else:
		file_folder = 'nhdzOther'
	# 路径存在则返回True,路径损坏返回False
	folder = os.path.exists(file_folder)


	# 如果文件不存在 就创建文件
	if not folder:
		os.makedirs(file_folder)

	# 返回文件名
	file_name = os.path.basename(file_url)
	# 查找字符在字符串中出现的下标  若查不到返回-1
	str_index = file_name.find('?')
	if str_index > 0:
		# 字符串截取
		file_name = file_name[:str_index]
	# 拼接文件路径
	file_path = os.path.join(file_folder, file_name)
	# 用’wb’调用open()，以写二进制的方式打开一个新文件
	image_file = open(file_path, 'wb')
	# 利用Respose对象的iter_content()方法循环
	for chunk in respose.iter_content(10000):
		image_file.write(chunk)
	# 文件写入完成
	image_file.close()


if __name__ == '__main__':
	setobj = settingObject()
	download_file(setobj.webUrl)








	