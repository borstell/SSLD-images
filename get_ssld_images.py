import sys,os,re,urllib.request
from bs4 import BeautifulSoup
from PIL import Image

"""
This script collects images from signs in the Swedish Sign Language Dictionary (teckensprakslexikon.su.se)
and creates a composite image of the sign, either side-by-side or overlayed.

The script requires Python packages PIL and bs4, and also Wget + ImageMagick.
"""

def get_signs(num):
	# Collects the images of a sign based on the ID number from the dictionary as input
	top_url = "http://teckensprakslexikon.su.se"
	try:
		url = top_url+"/ord/"+num    #current
		html = urllib.request.urlopen(url)
		soup = BeautifulSoup(html,"html.parser")
		many = [i for i in soup.find_all("img") if i.get("src").endswith("medium.jpg")]
		img = re.findall(r'image: "(.*photo-1.jpg)',soup.text)
		img1_url = top_url+img[0]
		img2_url = img1_url.replace("-photo-1.jpg","-photo-2.jpg")
		img1 = img1_url.split("/")[-1]
		img2 = img2_url.split("/")[-1]
		i1 = num+"_1.jpg"
		i2 = num+"_2.jpg"
		wget1 = "wget -O "+i1+" "+img1_url
		wget2 = "wget -O "+i2+" "+img2_url
		os.system(wget1)
		os.system(wget2)
		if len(many) == 2:
			return [i1,i2]
		else:
			img3_url = img1_url.replace("-photo-1.jpg","-photo-3.jpg")
			img3 = img3_url.split("/")[-1]
			i3 = num+"_3.jpg"
			wget3 = "wget -O "+i3+" "+img3_url
			os.system(wget3)
			if len(many) == 3:
				return [i1,i2,i3]
			if len(many) == 4:
				img4_url = img1_url.replace("-photo-1.jpg","-photo-4.jpg")
				img4 = img4_url.split("/")[-1]
				i4 = num+"_4.jpg"
				wget4 = "wget -O "+i4+" "+img4_url
				os.system(wget4)
				return [i1,i2,i3,i4]
	except:
		print("Error! Sign not found!")

def crop_image(i):
	img = Image.open(i)
	width = img.size[0]
	height = img.size[1]
	x_center = width/2
	y_center = height/2
	cropped = img.crop((x_center-(.8*x_center),y_center-y_center,x_center+(.8*x_center),y_center+y_center))
	cropped.save(i)

def make_composite(imgs):
	# NB: Code partly taken from https://stackoverflow.com/a/30228308
	if len(imgs) < 4: # With less than four images, they are positioned side-by-side
		if len(imgs) == 3: # With three images, they are cropped slightly on the x axis
			for i in imgs:
				crop_image(i)
		images = list(map(Image.open, imgs))
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)
		new_im = Image.new("RGB",(total_width, max_height))
		x_offset = 0
		for im in images:
			new_im.paste(im, (x_offset,0))
			x_offset += im.size[0]
		new_im.save(imgs[0].split("_")[0]+".jpg")
	elif len(imgs) == 4: # With four images, they are arrange in a 2x2 grid
		images = list(map(Image.open, imgs))
		widths, heights = zip(*(i.size for i in images))
		total_width = max(sum(widths[:2]),sum(widths[2:]))
		max_height = max(heights)*2
		new_im = Image.new("RGB",(total_width,max_height))
		x_offset = 0
		y_offset = images[0].size[1]
		for im in images[:2]:
			new_im.paste(im,(x_offset,0))
			x_offset += im.size[0]
		x_offset = 0
		for im in images[2:]:
			new_im.paste(im,(x_offset,y_offset))
			x_offset += im.size[0]
		new_im.save(imgs[0].split("_")[0]+".jpg")

def make_overlay(a,b,outname):
	# Makes an overlay image
	new_im = outname
	img1 = a
	img2 = b
	string = "convert %s %s -alpha set \
					-compose dissolve -define compose:args='25' \
					-gravity Center -composite %s" % (img2, img1, new_im)
	os.system(string)

def make_images(all_nums,overlay):
	# Iterates over the inputted IDs and creates the images (and removes the individual frames)
	for num in all_nums:
		if len(num) < 5:
			num = num.zfill(5)
		imgs = get_signs(num)
		if overlay == True:
			outname = imgs[0].split("_")[0]+".jpg"
			if len(imgs) == 2:
				make_overlay(imgs[0],imgs[1],outname)
			elif len(imgs) == 3:
				out1 = outname.split(".")[0]+"_A"+".jpg"
				make_overlay(imgs[0],imgs[1],out1)
				make_overlay(out1,imgs[2],outname)
			elif len(imgs) == 4:
				out1 = outname.split(".")[0]+"_A"+".jpg"
				out2 = outname.split(".")[0]+"_B"+".jpg"
				make_overlay(imgs[0],imgs[1],out1)
				make_overlay(imgs[2],imgs[3],out2)
				make_composite([out1,out2])
		else:
			make_composite(imgs)
		for img in imgs:
			os.system("rm "+img)
		for f in os.listdir():
			if f.endswith("_A.jpg") or f.endswith("_B.jpg"):
				os.system("rm "+f)

def main():
	# If additional argument "-o" or "-overlay" is added from command line, output image is an overlay
	# ... if not, the output is a side-by-side concatenation
	overlay = False
	try:
		if len(sys.argv) > 2:
			if sys.argv[2] in ["-o","-overlay"]:
				overlay = True
			else:
				print('Error! Argument "%s" not recognized. Ignoring extra argument.' % sys.argv[2])
		nums = sys.argv[1].split(",")
		make_images(nums,overlay)
	except:
		print('Error! The correct input is "python3 get_ssld_images.py {signID}" or "python3 get_ssld_images.py {signID} -o" or "python3 get_ssld_images.py {signID} -overlay"')

if __name__=="__main__":
	main()
