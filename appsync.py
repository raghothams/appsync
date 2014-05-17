#!/usr/bin/python

# script to find Applications installed on OSX
#
# OSX command :
# mdfind "kMDItemKind == 'Application'" -onlyin  /Applications
#


import subprocess
import re

def main():
  output = None

  try:
    # create a subprocess to run the command to get all applications installed
    p = subprocess.Popen(["mdfind", "kMDItemKind == 'Application'", 
          "-onlyin", "/Applications"], stdout=subprocess.PIPE, 
          stderr=subprocess.PIPE)

    # run the subprocess and get the results
    output = p.communicate()

  except Exception as e:
    print e
    # exit with non zero - indicating error
    exit(1)

  if output and not output[1]:

    # read stdout
    output = output[0]
    apps = output.split("\n")

    # remove empty strings
    apps = [app for app in apps if app]

    # filter only the application name from the path of application
    app_names=[]
    for app in apps:
        app_path_parts = app.split("/")
        app_names.append(app_path_parts[-1])

    # write app names to a file
    with open("apps.txt", "w") as wf:
        for app_name in app_names:
            wf.write(app_name + "\n")

if __name__ == "__main__":
  main()


