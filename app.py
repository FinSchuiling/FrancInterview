import json

from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)


@app.route('/')
def index_view():
    # get current user
    username = request.args.get('username')

    # open files
    with open('./users.json', 'r') as f:
        with open('./posts.json', 'r') as file:
            users = f.read()
            posts = file.read()

            # convert data to python objects
            usersDict = json.loads(users)
            postsDict = json.loads(posts)

            # get users the current user follows
            following = usersDict[username]

            # populate timeline with posts from users followed
            timeline = []
            for user in following:
                for post in postsDict[user]:
                    post["user"] = user
                    timeline.append(post)

            # add current users posts to timeline
            for post in postsDict[username]:
                post["user"] = username
                timeline.append(post)

    # sort timeline with most recent posts first
    timeline.sort(reverse=True, key=lambda x: x['time'])

    return render_template('index.html', username=username, string=timeline)


@app.route('/users')
def users_view():
    with open('./users.json', 'r') as f:
        users = f.read()
    return Response(users, mimetype="application/json")


@app.route('/posts')
def posts_view():
    with open('./posts.json', 'r') as f:
        posts = f.read()

    return Response(posts, mimetype="application/json")


if __name__ == '__main__':
    app.run(host='127.0.0.1')
