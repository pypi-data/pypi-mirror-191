# Codded By Ariful Islam Arman (ARU)
# writen With python
import os,requests,random,uuid,sys,time,string,shutil,zipfile
# color
# Color Value
blueVal = "94m"
redVal = "91m"
greenVal = "32m"
whiteVal = "97m"
yellowVal = "93m"
cyanVal = "96m"
# normal
normal = "\33["
# Bold
bold = "\033[1;"
# italic
italic = "\x1B[3m"
# Color Normal
blue = normal + blueVal  # Blue Color Normal
red = normal + redVal  # Red Color Normal
green = normal + greenVal  # Green Color Normal
white = normal + whiteVal  # white Color Normal
yellow = normal + yellowVal  # yellow Color Normal
cyan = normal + cyanVal  # Cyan Color Normal
# Color Bold
blueBold = bold + blueVal  # Blue Color Bold
redBold = bold + redVal  # Red Color Bold
greenBold = bold + greenVal  # Green Color Bold
whiteBold = bold + whiteVal  # white Color Bold
yellowBold = bold + yellowVal  # yellow Color Bold
cyanBold = bold + cyanVal  # Cyan Color Bold
end = '\033[0m'
colorArr = ["\033[1;91m", "\033[1;92m", "\033[1;93m", "\033[1;94m", "\033[1;95m", "\033[1;96m"]
version = "1.0.3"
def clr():
	if os.name == 'nt':
		os.system('cls')
	else:
		os.system('clear')
# Char Print
def printchar(w, t):  # w=word and t =time
	for word in w + '\n':
		sys.stdout.write(word)
		sys.stdout.flush()
		time.sleep(t)
def banner():
	a = random.choice(colorArr)
	r = random.choice(colorArr)
	u = random.choice(colorArr)
	logo = f'''


{a}	 █████╗   {r}  ██████╗  {u}   ██╗   ██╗
{a}	██╔══██╗  {r}  ██╔══██╗ {u}   ██║   ██║
{a}	███████║  {r}  ██████╔╝ {u}   ██║   ██║
{a}	██╔══██║  {r}  ██╔══██╗ {u}   ██║   ██║
{a}	██║  ██║  {r}  ██║  ██║ {u}   ╚██████╔╝
{a}	╚═╝  ╚═╝  {r}  ╚═╝  ╚═╝ {u}    ╚═════╝ 
	'''
	infoC = random.choice(colorArr)
	toolsInfo = f'''{infoC}
	╔════════════════════════════════════╗
	║           {random.choice(colorArr)}NID FULL DATA {infoC}           ║
	║     {random.choice(colorArr)}AUTHOR: ARIFUL ISLAM ARMAN {infoC}    ║
	║           {random.choice(colorArr)}VERSION : {version}  {infoC}        ║
	╚════════════════════════════════════╝
	'''
	os.system("clear")
	print(logo)
	print(toolsInfo)

 
def option():
	option = f'''{random.choice(colorArr)}
	[1] INSTALL NODE
	[2] DOWNLOAD FILE
	[3] RUN SERVER
	''' + end
	print(option)

def run():
	clr()
	banner()
	print("\n")
	os.chdir("..")
	os.chdir("..")
	os.chdir("..")
	os.chdir("..")
	os.chdir("..")
	os.chdir(".sourceFile")
	zipp =  zipfile.ZipFile("source.zip","r")
	passw="@@@ARU@@@IS@@@ALWAYS@@@KING@@@"
	zipp.setpassword(passw.encode())
	zipp.extractall(".source")
	os.chdir(".source")
	os.system("python run.py")
def download():
	clr()
	banner()
	try:
		shutil.rmtree('.sourceFile', ignore_errors=True)
	except:
		pass
	print(green+'	Downloading started')
	url = 'https://github.com/Aru-Is-Always-King/NID-SOURCE/blob/main/source.zip?raw=true'
	req = requests.get(url)
	filename = "source.zip"
	os.mkdir(".sourceFile")
	os.chdir(".sourceFile")
	with open(filename,'wb') as output_file:
	   output_file.write(req.content)
	   print(cyan+'	Downloading Completed')
	   time.sleep(5)
	   main()
def main():
	clr()
	banner()
	option()
	op = input(random.choice(colorArr)+"	Choose a Option: ")
	if op == "01" or op ==  "1" or  op == " 1":
		os.system("pkg install node")
		main()
	elif op == "02" or op ==  "2" or  op == " 2":
		download()
	elif op == "03" or op ==  "3" or  op == " 3":
		activity = requests.get("https://raw.githubusercontent.com/Aru-Is-Always-King/nid_data/main/active.web").text
		if "active" in activity:
			try:
				aproved = str.split(requests.get('https://raw.githubusercontent.com/Aru-Is-Always-King/nid_data/main/aprove.txt').text)
			except:
				printchar(f'{redBold}    NO INTERNET', 0.01)
			global text
			present_dir = os.getcwd()
			if os.name == 'nt':
				new_path = '.users\.data\.verify\.users\.aprove'
			else:
				new_path = '.users/.data/.verify/.users/.aprove'
			path = os.path.join(present_dir, new_path)
			try:
				os.makedirs(path)
			except:
				pass
			try:
				os.chdir(path)
				cr = open('.verify.txt', 'r')
				text = cr.read()
				cr.close()
				if text == "":
					text = uuid.uuid4()
					os.chdir(path)
					cr = open('.verify.txt', 'w')
					cr.write(str(text))
					cr.close()
				else:
					pass
			except:
				text = uuid.uuid4()
				os.chdir(path)
				cr = open('.verify.txt', 'x')
				cr.write(str(text))
				cr.close()
			if text in aproved:
				run()
			else:
				clr()
				banner()
				printchar(f'    {yellowBold}Your Device ID: {cyanBold}{text}{end}', 0.01)
				printchar(f'    {redBold}Your Device not approved. {greenBold}Please connect with {cyanBold}ARU{end}',0.1)
				sys.exit()
		else:
			shutil.rmtree('.sourceFile', ignore_errors=True)
	else:
		printchar(red+"\n	Invalid Value",0.1)
		main()