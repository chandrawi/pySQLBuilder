from .BaseQuery import BaseQuery
from .Manipulation import Manipulation
from ..Builder import BaseBuilder, UpdateBuilder
from ..Structure import Table, Value

class Update(BaseQuery) :

    def __init__(self, translator: int, bindingOption: int) :
        BaseQuery.__init__(self)
        self.builder = UpdateBuilder()
        self.builder.builderType(BaseBuilder.UPDATE)
        self.translator = translator
        self.bindingOption = bindingOption
        self.man = Manipulation()

    def update(self, table) :
        if table :
            tableObject = Table.create(table)
            self.builder.setTable(tableObject)
        else :
            raise Exception("Table name is not defined")
        return self

    def values(self, values) :
        valueObject = Value.create(values)
        self.builder.addValue(valueObject)
        return self

    def beginWhere(self) :
        self.man.beginClause()
        return self

    def beginAndWhere(self) :
        self.man.beginAndClause()
        return self

    def beginOrWhere(self) :
        self.man.beginOrClause()
        return self

    def beginNotAndWhere(self) :
        self.man.beginNotAndClause()
        return self

    def beginNotOrWhere(self) :
        self.man.beginNotOrClause()
        return self

    def endWhere(self) :
        self.man.endClause(self.man.CLAUSE_WHERE, self.builder)
        return self

    def where(self, column, operator: str, value = None) :
        clauseObject = self.man.andClause(self.man.CLAUSE_WHERE, column, operator, value)
        self.builder.addWhere(clauseObject)
        return self

    def andWhere(self, column, operator: str, value = None) :
        clauseObject = self.man.andClause(self.man.CLAUSE_WHERE, column, operator, value)
        self.builder.addWhere(clauseObject)
        return self

    def orWhere(self, column, operator: str, value = None) :
        clauseObject = self.man.orClause(self.man.CLAUSE_WHERE, column, operator, value)
        self.builder.addWhere(clauseObject)
        return self

    def notAndWhere(self, column, operator: str, value = None) :
        clauseObject = self.man.notAndClause(self.man.CLAUSE_WHERE, column, operator, value)
        self.builder.addWhere(clauseObject)
        return self

    def notOrWhere(self, column, operator: str, value = None) :
        clauseObject = self.man.notOrClause(self.man.CLAUSE_WHERE, column, operator, value)
        self.builder.addWhere(clauseObject)
        return self

    def limit(self, limit, offset = None) :
        limitObject = self.man.createLimit(limit, offset)
        self.builder.setLimit(limitObject)
        return self

    def offset(self, offset) :
        limitObject = self.man.offset(offset)
        self.builder.setLimit(limitObject)
        return self
