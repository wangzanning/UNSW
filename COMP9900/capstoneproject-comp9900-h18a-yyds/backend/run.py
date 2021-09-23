from app import app
import apis.auth
import apis.users
import apis.recipes
import apis.feeds
import apis.search

if __name__ == '__main__':
    app.run(debug=True)