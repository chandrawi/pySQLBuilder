from typing import Iterable
from .Column import Column

class Clause :

    CLAUSE_WHERE = 1
    CLAUSE_HAVING = 2

    OPERATOR_DEFAULT = 0
    OPERATOR_EQUAL = 1
    OPERATOR_NOT_EQUAL = 2
    OPERATOR_GREATER = 3
    OPERATOR_GREATER_EQUAL = 4
    OPERATOR_LESS = 5
    OPERATOR_LESS_EQUAL = 6
    OPERATOR_LIKE = 7
    OPERATOR_NOT_LIKE = 8
    OPERATOR_BETWEEN = 9
    OPERATOR_NOT_BETWEEN = 10
    OPERATOR_IN = 11
    OPERATOR_NOT_IN = 12
    OPERATOR_NULL = 13
    OPERATOR_NOT_NULL = 14

    CONJUNCTIVE_NONE = 0
    CONJUNCTIVE_AND = 1
    CONJUNCTIVE_OR = 2
    CONJUNCTIVE_NOT_AND = 3
    CONJUNCTIVE_NOT_OR = 4

    clauseType = 0
    nestedConjunctive = CONJUNCTIVE_NONE
    nestedLevel = 0

    def __init__(self, column, operator: int, value, conjunctive: int, level: int) :
        self.__column = column
        if operator > 0 and operator <= 14 :
            self.__operator = operator
        else :
            self.__operator = self.OPERATOR_DEFAULT
        self.__value = value
        if conjunctive > 0 and conjunctive <= 4 :
            self.__conjunctive = conjunctive
        else :
            self.__conjunctive = self.CONJUNCTIVE_NONE
        self.__level = level

    def column(self) :
        return self.__column

    def operator(self) -> int :
        return self.__operator

    def value(self) :
        return self.__value

    def conjunctive(self) -> int :
        return self.__conjunctive

    def level(self, input: int = -1) -> int :
        if input != -1 : self.__level = input
        return self.__level

    @classmethod
    def create(cls, clauseType: int, column, operator, values, conjunctive: int) :
        columnObject = Column.create(column)
        validOperator = cls.getOperator(operator)
        validValues = cls.getValues(values, validOperator)
        conjunctive = cls.getConjunctive(clauseType, conjunctive)
        nestedLevel = cls.nestedLevel
        cls.clauseType = clauseType
        cls.nestedLevel = 0
        return Clause(columnObject, validOperator, validValues, conjunctive, nestedLevel)

    @classmethod
    def getOperator(cls, operator) -> int :
        if isinstance(operator, int) :
            validOperator = operator
        else :
            if operator == '=' or operator == '==' :
                validOperator = Clause.OPERATOR_EQUAL
            elif operator == '!=' or operator == '<>' :
                validOperator = Clause.OPERATOR_NOT_EQUAL
            elif operator == '>' :
                validOperator = Clause.OPERATOR_GREATER
            elif operator == '>=' :
                validOperator = Clause.OPERATOR_GREATER_EQUAL
            elif operator == '<' :
                validOperator = Clause.OPERATOR_LESS
            elif operator == '<=' :
                validOperator = Clause.OPERATOR_LESS_EQUAL
            elif operator == 'BETWEEN' :
                validOperator = Clause.OPERATOR_BETWEEN
            elif operator == 'NOT BETWEEN' :
                validOperator = Clause.OPERATOR_NOT_BETWEEN
            elif operator == 'LIKE' :
                validOperator = Clause.OPERATOR_LIKE
            elif operator == 'NOT LIKE' :
                validOperator = Clause.OPERATOR_NOT_LIKE
            elif operator == 'IN' :
                validOperator = Clause.OPERATOR_IN
            elif operator == 'NOT IN' :
                validOperator = Clause.OPERATOR_NOT_IN
            elif operator == 'NULL' or operator == 'IS NULL' :
                validOperator = Clause.OPERATOR_NULL
            elif operator == 'NOT NULL' or operator == 'IS NOT NULL' :
                validOperator = Clause.OPERATOR_NOT_NULL
            else :
                validOperator = Clause.OPERATOR_DEFAULT
        return validOperator

    @classmethod
    def getValues(cls, values, operator: int) :
        valid = True
        if operator == Clause.OPERATOR_BETWEEN or operator == Clause.OPERATOR_NOT_BETWEEN :
            if isinstance(values, Iterable) :
                valid = len(values) == 2
        if operator == Clause.OPERATOR_IN or operator == Clause.OPERATOR_NOT_IN :
            valid = isinstance(values, Iterable)
        if valid :
            return values
        else :
            raise Exception('Invalid input values for Where or Having clause')

    @classmethod
    def getConjunctive(cls, clauseType: int, conjunctive: int) -> int :
        if clauseType == cls.clauseType :
            if conjunctive == Clause.CONJUNCTIVE_NONE :
                if cls.nestedConjunctive == Clause.CONJUNCTIVE_NONE : return Clause.CONJUNCTIVE_AND
                else : return cls.nestedConjunctive
            else :
                return conjunctive
        else :
            return Clause.CONJUNCTIVE_NONE
