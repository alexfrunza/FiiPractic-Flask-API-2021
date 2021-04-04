

class UserCompanyAdapter:

    @staticmethod
    def to_json(results):
        return [{
            "id": user_company.user_id,
        } for user_company in results]
