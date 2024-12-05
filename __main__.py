from collections import defaultdict
from time import time

avg_events = ['222', '333', '333fm', '333oh', '444', '555', '666', '777', 'skewb', 'pyram', 'minx', 'sql', 'clock']
single_events = ['333bf', '444bf', '555bf', '333mbf']

wcs = ['WC1982', 'WC2003', 'WC2005', 'WC2007', 'WC2009', 'WC2011', 'WC2013', 'WC2015', 'WC2017', 'WC2019', 'WC2023']

def better_than_worlds(person_single, person_average, worlds_single, worlds_average):

    for event in avg_events:
        if event in worlds_average:
            if event in person_average:
                if person_average[event] > worlds_average[event]:
                    return False
            else:
                return False
        elif event in worlds_single: # megaaminx 2003, 2005
            if event in person_single:
                if person_single[event] > worlds_single[event]:
                    return False
            else:
                return False

    for event in single_events:
        if event in worlds_single:
            if event in person_single:
                if person_single[event] > worlds_single[event]:
                        return False
            else:
                return False
    
    return True

if __name__ == '__main__':

    time_start = time()

    personal_records_single = defaultdict(dict)
    with open('WCA_export/WCA_export_RanksSingle.tsv') as singles:
        for line in singles:
            data = line.rstrip('\n').split('\t')
            if data[0] != 'personId':
                personId = data[0]
                eventId = data[1]
                best = data[2]
                personal_records_single[personId][eventId] = int(best)

    personal_records_average = defaultdict(dict)
    with open('WCA_export/WCA_export_RanksAverage.tsv') as averages:
        for line in averages:
            data = line.rstrip('\n').split('\t')
            if data[0] != 'personId':
                personId = data[0]
                eventId = data[1]
                best = data[2]
                personal_records_average[personId][eventId] = int(best)

    print(f'Loaded PRs in {time() - time_start}s')

    time_start2 = time()

    wc_bests_single = defaultdict(dict)
    wc_bests_avg = defaultdict(dict)

    with open('WCA_export/Wca_export_Results.tsv', encoding='utf-8') as results:
        for line in results:
            data = line.rstrip('\n').split('\t')
            if data[0] != 'competitionId':
                competition = data[0]
                event = data[1]
                roundType = data[2]
                pos = int(data[3])
                best = int(data[4])
                average = int(data[5])
                if (competition in wcs) and (pos == 1) and (roundType in ['c', 'f']) and (best > 0):
                    if event in avg_events:
                        if average != 0:
                            wc_bests_avg[competition][event] = average
                        wc_bests_single[competition][event] = best # old formats do kurwy nedzy xd
                    if event in single_events:
                        wc_bests_single[competition][event] = best

    print(f'Read worlds winning results in {time() - time_start2}')

    time_start3 = time()

    people = list(personal_records_single.keys())

    people_best = defaultdict(int)
    people_count = defaultdict(int)
    wc_count = defaultdict(int)

    for person in people:
        for wc in wcs:
            if better_than_worlds(personal_records_single[person], personal_records_average[person], wc_bests_single[wc], wc_bests_avg[wc]):
                people_best[person] = int(wc[2:])
                people_count[person] += 1
                people_count[wc] += 1
    
    people.sort(key = lambda x: people_best[x], reverse=True)

    with open('results.csv', 'w') as writefile:
        for pos, person in enumerate(people):
            writefile.write('\t'.join([str(pos), person, str(people_best[person]), str(people_count[person])]))
            writefile.write('\n')

    print(f'Calculated gts in {time() - time_start3}')
    
    while True:
        id = input('')
        if id == 'quit':
            break
        if id in people:
            print(people_best[id], people_count[id])