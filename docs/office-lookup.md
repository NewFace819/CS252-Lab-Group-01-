# Office lookup

The assistant first checks full office names and the existing Vietnamese/English
aliases. If none matches, a complete word longer than three characters from an
office name can identify it, for example `training` for `Training Office`.
Generic words such as `office` and `department` do not identify a particular office.
Short aliases such as `IT` continue to work as before.

Partial lookup returns a location only when one office matches. If several offices
match, the assistant lists their names and asks the user to specify an office.
It does not select a location based on CSV row order.

Names, rooms and hours come from `data/offices.csv`. At the time of this change,
that file is empty; live lookups need the data owner's work in issue #10. This
change does not add or claim verified campus locations.

Run `python -m pytest -q` to check partial names, existing names/aliases, ambiguous
names, whole-word boundaries and the CSV-loading path. Tests use explicitly
synthetic rooms and hours, independent of the live CSV.
