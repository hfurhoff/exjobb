if __name__ == '__main__':
	import sys, os
	thisdir = "..\\"
	if not thisdir in sys.path:
		sys.path.append(thisdir)
	from view.gui import GUI
	GUI()