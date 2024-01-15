import json
import requests

BLUEPRINT_ID = 3
DEVLAKE_BASEURL = 'http://54.236.25.78:4000/api/'
GITHUB_BASEURL = 'https://api.github.com/'
GITHUB_REPO = 'devlake-extract'
GITHUB_REPO_OWNER = 'bsamitha'
PRIVATE_TOKEN = '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'
VERIFY_SSL_CERTIFICATE = True


def dl_get(endpoint):
    response = requests.get(
        DEVLAKE_BASEURL + endpoint,
        verify=VERIFY_SSL_CERTIFICATE
    )

    if response.status_code != 200:
        raise Exception("Unable to read data")

    return response.json()


def github_post_request(endpoint, data):
    response = requests.post(
        GITHUB_BASEURL + endpoint,
        headers={'Authorization': f'Bearer %s' % PRIVATE_TOKEN,
                 'X-GitHub-Api-Version': '2022-11-28',
                 'Accept': 'application/vnd.github+json'},
        verify=VERIFY_SSL_CERTIFICATE,
        data=json.dumps(data)
    )

    if response.status_code != 201:
        raise Exception("Unable to write data!")

    return response.json()


blueprint = dl_get(f'blueprints/%s' % BLUEPRINT_ID)
projectName = blueprint['projectName'] if 'projectName' in blueprint else None
print(f'gitlab project %s found' % projectName)
if not projectName:
    raise Exception("No project found")
# create github issue
issue = github_post_request(f'repos/%s/%s/issues' % (GITHUB_REPO_OWNER, GITHUB_REPO), {
    'title': f'gl issue: %s' % projectName,
    'body': 'created by devlake lab exercise script'
})
print(f'github issue %s created.' % str(issue['id']))
