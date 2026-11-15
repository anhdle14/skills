# Q3 on-call notes (raw)

- 41 pages in Q3, up from 29 in Q2
- 17 of the 41 were the disk-usage alert on the batch hosts; all auto-resolved within 10 min
- Mia and Theo carried most nights in August because two people were on leave
- runbook for the payments webhook alert was wrong twice (pointed at the old dashboard)
- nobody got paged for the 2 real outages in time - both were noticed by support first
- idea: drop the disk alert threshold change? or route it to a ticket instead of a page
- people want a handoff doc at rotation change
