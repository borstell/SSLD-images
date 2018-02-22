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
		return [i1,i2]
	except:
		print("Error! Sign not found!")

def make_composite(imgs,overlay):
	# NB: Code partly taken from https://stackoverflow.com/a/30228308
	# If argument overlay is set to False (default), the images are concatenated side-by-side
	# ... if overlay is True, the images are overlayed with the first image (starting position) set to 25% transparency)
	if overlay == False:
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
	else:
		new_im = imgs[0].split("_")[0]+".jpg"
		img1 = imgs[0]
		img2 = imgs[1]
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
		make_composite(imgs,overlay)
		for img in imgs:
			os.system("rm "+img)

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
