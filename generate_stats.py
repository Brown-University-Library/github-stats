import sys
import csv
import datetime
import prettytable
import collections

def date_filter(row, compDate, diff):
    data_date = datetime.datetime(
        year=int(row[0]), month=int(row[1]), day=int(row[2]) )
    return compDate - data_date < diff

def row_stats(rows):
    repo_count = len({ row[4] for row in rows })
    total_commits = len(rows)
    line_total = sum([ int(row[-1]) for row in rows ])
    return (repo_count, total_commits, line_total)

def main(inFile):
    with open(inFile, 'r') as f:
        rdr = csv.reader(f)
        rows = [ row for row in rdr ]

    one_year = datetime.timedelta(days=365) 
    today = datetime.datetime.today()
    recent = [ row for row in rows
        if date_filter(row, today, one_year) ]

    year_total = prettytable.PrettyTable()
    year_total.field_names = [
        'Total Projects', 'Total Commits', 'Total Edits' ]
    year_total.add_row( row_stats(recent) )

    print(year_total)

    by_month = collections.defaultdict(list)
    for row in recent:
        by_month[row[1]].append(row)

    month_tables = []
    for month in by_month:
        month_table = prettytable.PrettyTable()
        month_table.field_names = [ 'Total Projects',
            'Total Commits', 'Total Edits' ]
        month_table.add_row( row_stats(by_month[month]))
        month_tables.append( (int(month), month_table) )

    for table in sorted(month_tables):
        print(table[0])
        print(table[1])
    
if __name__ == "__main__":
    infile = sys.argv[1]
    main(infile)