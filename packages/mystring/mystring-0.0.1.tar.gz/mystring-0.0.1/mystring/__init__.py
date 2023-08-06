class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self
    def isempty(self):
        return self.strip() == ''