class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self
    def isempty(self):
        return self.strip() == ''
    def ad(self, value):
        self = string(self + getattr(self, 'delim', "")  + value)
        return self
    def delim(self, value):
        self.delim = value
    def pre(self, value):
        self = string(value + getattr(self, 'delim', "")  + self)
        return self