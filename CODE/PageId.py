class PageId :
    def __init__(self, PageIdx= -1, FileIdx = -1):
        self.PageIdx = PageIdx
        self.FileIdx = FileIdx
    def isValid(self):
        return self.FileIdx!=-1
