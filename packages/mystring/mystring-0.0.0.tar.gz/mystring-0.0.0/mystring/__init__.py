class string(str):
    def rep(self,substring):
        self = string(self.replace(substring,''))
        return self