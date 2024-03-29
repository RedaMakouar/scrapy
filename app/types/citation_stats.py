from sqlalchemy import TypeDecorator,JSON


class YearlyIncreasedBy:
    def __init__(self, fromYear: str, toYear: str, increasedBy: int):
        self.fromYear = fromYear
        self.toYear = toYear
        self.increasedBy = increasedBy;

    def fromOriginJson(json: dict[str, any]):
        return YearlyIncreasedBy(
            fromYear=json["startKey"],
            toYear=json["endKey"],
            increasedBy=json["count"]
        );

    def serialize(self) -> dict: 
        return {
            "from_year": self.fromYear,
            "to_year": self.toYear,
            "increased_by": self.increasedBy
        }

    def __repr__(self):
        return f'<YearlyIncreasedBy fromYear={self.fromYear} toYear={self.toYear} increasedBy={self.increasedBy}>'

        
class CitationStats:
    def __init__(self, allCitationsCount: int, keyCitationsCount: int, incrementStats: list[YearlyIncreasedBy]):
        self.allCitationsCount = allCitationsCount
        self.keyCitationsCount = keyCitationsCount
        self.incrementStats = incrementStats;
        
    def fromOriginJson(json: dict[str, any]):
        return CitationStats(
            allCitationsCount=json["numCitations"], 
            keyCitationsCount=json["numKeyCitations"],
            incrementStats=[
                YearlyIncreasedBy.fromOriginJson(rawIncreasedBy) 
                for rawIncreasedBy in json["citedByBuckets"]
            ]
        );

    def serialize(self) -> dict:
        return {
            "all_citations_count": self.allCitationsCount,
            "key_citations_count": self.keyCitationsCount,
            "increment_stats": [
                stat.serialize()
                for stat in self.incrementStats
            ]
        }

    def __repr__(self):
        return f'''
            CitationStats(
                allCitationsCount: {self.allCitationsCount},
                keyCitationCount: {self.keyCitationsCount},
                incrementStats: {self.incrementStats},
            )
        ''';


class CitationStatsField(TypeDecorator):
    impl = JSON

    def __repr__(self):
        return self.impl.__repr__()
    
    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(JSON)

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        else:
            if isinstance(value, CitationStats):
                return value.serialize()

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return CitationStats.fromOriginJson(value)