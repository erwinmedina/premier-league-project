In order to simplify my racism problem, I focused on players that were foreign (non-domestic).
I used wikipedia's page: https://en.wikipedia.org/wiki/List_of_foreign_Premier_League_players
This has a list of player information, their country of origin, clubs they played for, and how long they were there for.

However, I also had to normalize the data since the incident report didn't have a 1-1 match with the player names on wikipedia.
I treated the incident report as the source of truth as it had the majority of all data. 
I used a script to normalize some of the unique characters that aren't in english, and handling some names by hand.
I also utilized my skillset with excel to find names that would appear on my player info dataset, but not the incident report.
This took the majority of my time, as ensuring there were one to one matches was difficult. 
I'm positive that i've missed players, and my data isn't perfect but I narrowed that gap.

Finalized file is the `Player Information v2`