

class UserCompanyAdapter:

    @staticmethod
    def to_json(results):
        return [{
            "id": result.User.id,
            'first_name': result.User.first_name,
            'email': result.User.email,
        } for result in results]
