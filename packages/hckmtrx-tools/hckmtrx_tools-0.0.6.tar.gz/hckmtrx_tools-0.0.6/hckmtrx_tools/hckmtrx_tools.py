# function to get above the fileSystemObject - n additional folder above with a parameter (default value 0)
def GetDirectory(fileSystemObject: str, directoriesAbove: int = 0) -> str:
    # loop for n many additional folders
    for i in range(directoriesAbove + 1):
        # strip \ from the right (necessary if fileSystemObject is a folder)
        fileSystemObject = fileSystemObject.strip("\\")
        # loop from end
        for j in range(-1, -len(fileSystemObject), -1):
            # until first \ was found
            if fileSystemObject[j] == "\\":
                # remove the end of variable and break
                fileSystemObject = fileSystemObject[:j + 1]
                break

    # return the new fileSystemObject
    return fileSystemObject