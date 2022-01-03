# Automate “Last modified” dates in your documentation


Automating repetitive documentation tasks will eliminate human error and keep your documentation structured. 


The purpose of this article is to explain how you can automatically update XML data, in this case the last modified date. My hope is that you can leverage this to build out your own automation to increase productivity and accuracy in your own work.

Imagine that you’re working on a release history page. The release history has a section that contains the last modified of each API. 
The following XML snippet, named `lastmodified.xml`, represents structured XML for a release history.

```
<file name="Release history">
        <update name="API01">
                <type>Create</type>
                <returns>TXT</returns>
                <maxSize>1000</maxSize>
                <lastModified>2021-11-07</lastModified>
        </update>
        <update name="API02">
                <type>Update</type>
                <returns>TXT</returns>
                <maxSize>1000</maxSize>
                <lastModified>2021-10-29</lastModified>
        </update>
</file>
```

A developer has instructed you to update the documentation around the max size that your API can create and update. This request is easy enough. However, the developer is unsure when they’re going to make this change public. 
You stage your changes for the max size. Then, on the day the documenation should go live, your developer communicates to you that they’ve updated the API and your documenation should also update. 

With a few lines of code, you can automatically update your “last modified field”.

Add the following python file in the same directory as your XML file:

```
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
    metafile = "lastmodified.xml"
    print("\n====Before updating:====")
    print_file_content(metafile)
    updater = TimestampUpdater(metafile)
    updater.updateLastModified()
    print("\n====After updating:====")
    print_file_content(metafile)
```

Save and run your python script to update your `lastmodified.xml` file. 

The following is an example output:

```
<file name="Release history">
        <update name="API01">
                <type>Create</type>
                <returns>PDF</returns>
                <maxSize>1200</maxSize>
                <lastModified>2022-01-03</lastModified>
        </update>
        <update name="API02">
                <type>Update</type>
                <returns>PDF</returns>
                <maxSize>1200</maxSize>
                <lastModified>2022-01-03</lastModified>
        </update>
</file>
```

The XML attribute correctly updated to today’s date. You can now publish your XML without the fear that you’ve applied your date’s format incorrectly, forgot to close an XML tag, or that something has become out of date.



Let me know if how you would leverage automation in your own documentation. I’d love to hear any additional ideas and work flows you use. 

## Sources:

I used the following sources for inspiration for this post:

* [Date time](https://docs.python.org/3/library/datetime.html) documentation. 
* [ElementTree XML](https://docs.python.org/3/library/xml.etree.elementtree.html) documentation. 
* [Stack Overflow](https://stackoverflow.com/questions/63605557/updating-xml-node-value-using-the-condition-in-python) question and answers.

