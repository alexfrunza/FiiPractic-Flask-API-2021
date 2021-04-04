
class CompanyAdapter:

    @staticmethod
    def to_json(results):
        return [{
            'id': company.id,
            'name': company.name,
            'country': company.country
        } for company in results]

    def to_object(self, body):
        for key, value in body.items():
            if hasattr(self, key):
                setattr(self, key, value)
