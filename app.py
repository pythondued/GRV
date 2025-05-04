from flask import Flask, render_template
import requests

app = Flask(__name__)

GITHUB_USERNAME = 'pythondued'
GITHUB_API_URL = f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100'


@app.route('/')
def index():
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100&page={page}'
        response = requests.get(url)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return render_template('index.html', repos=repos)

@app.route('/repo/<name>')
def repo_commits(name):
    commits_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{name}/commits'
    response = requests.get(commits_url)
    commits = response.json()
    return render_template('commits.html', repo=name, commits=commits)


@app.route('/repo/<repo>/commit/<sha>')
def commit_detail(repo, sha):
    commit_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{repo}/commits/{sha}'
    response = requests.get(commit_url)
    commit = response.json()
    return render_template('commit_detail.html', repo=repo, commit=commit)


if __name__ == '__main__':
    app.run(debug=True)