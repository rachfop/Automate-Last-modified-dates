import xml.etree.ElementTree as ET
from datetime import datetime


class TimestampUpdater:
    # Constructor
    def __init__(self, filepath):
        self.meta_file = filepath
        self.tree = ET.parse(self.meta_file)

    # To get xml data
    def getMetadataTree(self):
        return self.tree

    # to get xml data root
    def getMetadataRoot(self):
        return self.tree.getroot()

    # to compare current date to lastmodified date
    def updateLastModified(self):
        today = datetime.now()
        # add your XML paths here
        for testfile in self.getMetadataRoot().findall("update"):
            lastmodified = testfile.find("lastModified")
            previous_update = datetime.strptime(lastmodified.text, "%Y-%m-%d")
            if previous_update < today:
                lastmodified.text = today.strftime("%Y-%m-%d")
                self.getMetadataTree().write(self.meta_file)


# print lastmodified date to file
def print_file_content(filename):
    with open(filename, "r") as fh:
        for line in fh:
            print(line.rstrip())


# print diff to console
if __name__ == "__main__":
    # rename your file name here
    metafile = "Automate-Last-modified-dates/lastmodified.xml"
    print("\n====Before updating:====")
    print_file_content(metafile)
    updater = TimestampUpdater(metafile)
    updater.updateLastModified()
    print("\n====After updating:====")
    print_file_content(metafile)
