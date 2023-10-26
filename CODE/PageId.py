class PageId :
    def __init__(self, FileIdx = -1,PageIdx= -1, ):
        self.PageIdx = PageIdx
        self.FileIdx = FileIdx
    def isValid(self):
        return self.FileIdx!=-1
