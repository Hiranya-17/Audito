from datetime import datetime, timezone
import hashlib
import os
from Mongo import users_collection
from pymongo.errors import DuplicateKeyError

def create_user(username, email, plain_password):
  salt = os.urandom(16).hex()
  hashed = hashlib.pbkdf2_hmac(
      "sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100_000
  ).hex()
  password_hash = f"{salt}${hashed}"

  clean_username = username.strip()
  clean_email = email.strip().lower()
  user_doc = {
      "username": clean_username,
      "email": clean_email,
      "password_hash": password_hash,
      "created_at": datetime.now(timezone.utc),
  }

  try:
    result = users_collection.insert_one(user_doc)
    print(
      f'Success! User {clean_username} is ready to rock out!'
      f'Email: {clean_email}. ID: {result.inserted_id}'
    )
    return result.inserted_id
  except DuplicateKeyError as e:
    raise ValueError("Username or email is already taken.") from e