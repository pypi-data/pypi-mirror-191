#!/usr/bin/python3
import argparse
import pytopdrawer


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("topfile", type=str,help="url/file/string")
	parser.add_argument("-p", "--powheg", action="store_true",help="add powheg lines")
	parser.add_argument("-m","--mcfm", action="store_true",help="add mcfm lines")
	args = parser.parse_args()
	tops = pytopdrawer.read(args.topfile,args.powheg,args.mcfm)
	for t in tops:
		t.show()

main()