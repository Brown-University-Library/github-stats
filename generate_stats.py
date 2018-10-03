import sys
import csv
import datetime
import prettytable
import collections
import statistics

def days_since(dayDiff, year, month, day):
    diff = datetime.timedelta(days=dayDiff) 
    today = datetime.datetime.today()
    data_date = datetime.datetime(
        year=int(year), month=int(month), day=int(day) )
    return today - data_date < diff

def row_stats(rows):
    repo_count = len({ row[4] for row in rows })
    total_commits = len(rows)
    edits_total = sum([ int(row[-1]) for row in rows ])
    edits_median = statistics.median([ int(row[-1]) for row in rows ])
    return (repo_count, total_commits, edits_total, edits_median)

def main(inFile):
    with open(inFile, 'r') as f:
        rdr = csv.reader(f)
        rows = [ row for row in rdr ]

    recent = [ row for row in rows
        if days_since(365, row[0], row[1], row[2]) ]

    year_month = collections.defaultdict(list)
    mos = 0.0
    for row in recent:
        year_month[(int(row[0]), int(row[1]) )].append(row)

    year_totals = collections.Counter()
    month_table = prettytable.PrettyTable()
    month_table.field_names = [ 'Date', 'Total Projects',
        'Total Commits', 'Median Commit Edits', 'Total Edits' ]

    month_data = []
    for yrmn in year_month:
        dt = datetime.datetime(year=yrmn[0], month=yrmn[1], day=1)
        date_str = datetime.datetime.strftime(dt, '%Y-%b')
        repos, commits, edits_t, edits_m = row_stats(year_month[yrmn])
        month_data.append( ( dt,
            (date_str, repos, commits, edits_m, edits_t) ) )
        year_totals['repos'] += repos
        year_totals['commits'] += commits
        year_totals['edits'] += edits_t
        mos += 1

    for md in sorted(month_data):
        month_table.add_row(md[1])
    month_table.align = 'r'
    month_table.align['Date'] = 'l'
    print(month_table)

    year_avgs = prettytable.PrettyTable()
    year_avgs.field_names = [
        'Projects/Month', 'Commits/Month', 'Edits/Month' ]
    year_avgs.add_row( ( round(year_totals['repos']/mos, 2),
        round(year_totals['commits']/mos, 2),
        round(year_totals['edits']/mos, 2) ) )

    year_avgs.align = 'r'
    print(year_avgs)
    
if __name__ == "__main__":
    infile = sys.argv[1]
    main(infile)