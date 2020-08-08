from werkzeug.security import safe_str_cmp
from models.user import UserModel

# Two functions below allow us to retrive users ID or Username without resorting to an iteration.
def authenticate(username, password):
    # there is no username in the key, we gonna return None
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    # Payload is a content of JWT token, and we gonna extract user ID from the payload.
    # We can retrieve the specific user that mathches this payload.
    # MATCHING USER ID AND GIVING CORRECT USER FOR THAT USER ID.
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
