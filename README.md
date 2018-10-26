# DOCUMENTATION

Functions:
*CRD DB

*CRUD Table
** CREATE
** SHOW
** DROP
** USE
** (ALTER)

*CRUD Data
** INSERT
** DELETE
** SELECT + Filters

Example usage:
=> POST
requests.post('endpoint', {db, table, SQL_request})
or
requests.post('endpoint/db/table', {SQL_request})
