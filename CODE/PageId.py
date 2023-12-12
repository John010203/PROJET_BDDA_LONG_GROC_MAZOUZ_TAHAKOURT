class PageId :
    def __init__(self, FileIdx = -1,PageIdx= -1, ):
        self.FileIdx = FileIdx
        self.PageIdx = PageIdx
    def isValid(self):
        return self.FileIdx!=-1
    
    def __str__(self):
        return "FileId : "+ str(self.FileIdx) + " PageId " +str(self.PageIdx)
    
    def __eq__(self,pId):
        if pId == None:
            return False
        return self.PageIdx == pId.PageIdx and self.FileIdx == pId.FileIdx
