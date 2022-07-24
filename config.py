import os

TOKEN = os.environ['TOKEN']
PORT = int(os.environ.get('PORT',5000))
BASE_URL = os.environ['BASE_URL']
USER1 = int(os.environ['user1'])
USER2 = int(os.environ['user2'])
TEST_USER = int(os.environ['testUser'])