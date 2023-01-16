class TableRelations():
    pass

    tableName = ""

    tableFroms = []

    scriptFiles = ""

    def to_str(self):
        return "tableName:" + self.tableName + " tablefroms:" + "".join(self.tableFroms)+" scriptFiles:" + self.scriptFiles
