import sys
import datetime
import collections
import csv

from github import Github

dtformat = '%Y-%m-%dT%H:%M:%SZ'

def main(login, psw, target, outFile):
    g = Github(login, psw)
    user = g.get_user(login=target)
    bul = g.get_organization(login="Brown-University-Library")
    bul_repos = bul.get_repos()
    print("Getting relevant BUL repos")
    user_repos = [ r for r in bul_repos
        if user in r.get_contributors() ]
    print("Repos acquired")
    rows = []
    today = datetime.datetime.today()
    diff = datetime.timedelta(days=365)
    since = today - diff
    print("Getting repo commits:")
    for repo in user_repos:
        print("....{0}".format(repo.name))
        try:
            commits = [ c for c in repo.get_commits(
                author=user, since=since) ]
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
        except:
            print("API rate limit exceeded")
            break

    with open(outFile, 'w') as f:
        wrtr = csv.writer(f)
        for row in rows:
            wrtr.writerow(row)

    print("Data written to: {0}".format(outfile))

if __name__ == "__main__":
    login = sys.argv[1]
    passw = sys.argv[2]
    if len(sys.argv) == 4:
        target = sys.argv[3]
    else:
        target = login
    if len(sys.argv) == 5:
        outfile = sys.argv[4]
    else:
        outfile = '{0}_github-stats.csv'.format(target)
    main(login, passw, target, outfile)