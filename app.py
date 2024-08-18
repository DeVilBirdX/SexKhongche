from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

comments = []

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comments</title>
</head>
<body>
    <h1>Leave a Comment</h1>
    <form id="commentForm">
        <input type="text" id="username" placeholder="Your Name" required>
        <textarea id="message" placeholder="Your Comment" required></textarea>
        <button type="submit">Submit</button>
    </form>
    <h2>Comments:</h2>
    <ul id="commentsList"></ul>

    <script>
        const form = document.getElementById('commentForm');
        const commentsList = document.getElementById('commentsList');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const message = document.getElementById('message').value;

            const response = await fetch('/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, message })
            });

            if (response.ok) {
                document.getElementById('username').value = '';
                document.getElementById('message').value = '';
                loadComments();
            }
        });

        async function loadComments() {
            const response = await fetch('/comments');
            const comments = await response.json();
            commentsList.innerHTML = comments.map(comment => `<li><strong>${comment.username}:</strong> ${comment.message}</li>`).join('');
        }

        loadComments();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html)

@app.route('/comments', methods=['GET'])
def get_comments():
    return jsonify(comments)

@app.route('/comments', methods=['POST'])
def add_comment():
    data = request.json
    comment = {'username': data['username'], 'message': data['message']}
    comments.append(comment)
    return jsonify(comment), 201

if __name__ == '__main__':
    app.run(debug=True)