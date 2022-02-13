from typing import Iterable, Mapping

class Value :

    def __init__(self, table: str, columns: tuple, values: tuple) :
        self.__table = table
        lenCol = len(columns)
        lenVal = len(values)
        lenMin = lenCol
        if lenCol > lenVal : lenMin = lenVal
        self.__columns = ()
        self.__values = values[:lenMin]
        for i in range(lenMin) :
            self.__columns += (str(columns[i]),)

    def table(self) -> str :
        return self.__table

    def columns(self) -> tuple :
        return self.__columns

    def values(self) -> tuple :
        return self.__values

    @classmethod
    def create(cls, inputValue) :
        columns = ()
        values = ()
        if isinstance(inputValue, Mapping) :
            columns = tuple(inputValue.keys())
            values = tuple(inputValue.values())
        elif isinstance(inputValue, Iterable) :
            (columns, values) = cls.parsePair(inputValue)
        return Value(cls.table, columns, values)

    @classmethod
    def createMulti(cls, multiValues) -> tuple :
        valuesObjects = ()
        if isinstance(multiValues, Iterable) :
            for val in multiValues :
                valuesObjects += (cls.create(val),)
        return valuesObjects

    @classmethod
    def parsePair(cls, pairs: Iterable) -> tuple :
        if isinstance(pairs[0], str) and len(pairs) == 2 :
            return ((pairs[0],), (pairs[1],))
        columns = ()
        values = ()
        for pair in pairs :
            if isinstance(pair, Mapping) and len(pair) :
                key = next(iter(pair.keys()))
                columns += (key,)
                values += (pair[key],)
            elif isinstance(pair, Iterable) and len(pair) == 2 :
                columns += (pair[0],)
                values += (pair[1],)
        return (columns, values)