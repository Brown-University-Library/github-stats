import sys
import datetime
import collections
import csv

from github import Github

dtformat = '%Y-%m-%dT%H:%M:%SZ'

def main(user, psw, outFile):
    g = Github(user, psw)
    user = g.get_user(login=user)
    bul = g.get_organization(login="Brown-University-Library")
    bul_repos = bul.get_repos()
    print("Getting relevant BUL repos")
    user_repos = [ r for r in bul_repos
        if user in r.get_contributors() ]
    print("Repos acquired")
    rows = []
    print("Getting repo commits:")
    for repo in user_repos:
        print("....{0}".format(repo.name))
        commits = [ c for c in repo.get_commits(author=user) ]
        for commit in commits:
            raw = commit.raw_data
            committer = raw['commit']['committer']
            stats = raw['stats']
            dt = datetime.datetime.strptime(
                committer['date'], dtformat)
            row = ( dt.year, dt.month, dt.day,
                repo.name, repo.url, commit.url,
                stats['additions'], stats['deletions'],
                stats['total'] )
            rows.append(row)

    with open(outFile, 'w') as f:
        wrtr = csv.writer(f)
        for row in rows:
            wrtr.writerow(row)

    print("Data written to: {0}".format(outfile))

if __name__ == "__main__":
    user = sys.argv[1]
    passw= sys.argv[2]
    if len(sys.argv) == 4:
        outfile = sys.argv[3]
    else:
        outfile = '{0}_github-stats.csv'.format(user)
    main(user, passw, outfile)