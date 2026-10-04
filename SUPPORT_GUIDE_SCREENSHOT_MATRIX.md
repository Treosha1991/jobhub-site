# JobHub Support guide: localized visual set

`support-guide.html` uses 14 matching desktop/web screenshots in each of four
languages (`ru`, `en`, `pl`, `uk`). They live in
`assets/support-guide/<lang>/<shot>.jpg`. The page has 15 image placements:
`project` is used in both the walkthrough and the extra-screen gallery.
`assets/app.js` changes the image, its full-size link and its alt text with the
page language; it does not load the other three language sets until selected.
Each locale has the same shot names and pixel dimensions. `tools/check_site.py`
checks that every referenced shot exists in all four languages.

| Shot | What the screenshot explains |
|---|---|
| `demo-request` | Demo request entry point on the site. |
| `home` | Company workspace, navigation and shortcuts. |
| `workers` | Worker list, assignments and invitation entry point. |
| `team` | Staff invitation and access permissions. |
| `worker-invite` | Worker email invitation, manager and coordinator fields. |
| `project` | Project, crew, driver, passengers and published shift calendar. |
| `requests` | Fictional day-off request, manager comment and decision controls. |
| `tasks` | Sent task with assigned worker and status navigation. |
| `announcement` | Unsaved fictional announcement with a title, text, one selected recipient and acknowledgement checkbox. |
| `timesheet` | Week grid with planned and actual hours. |
| `timesheet-detail` | Review modal, confirmation and correction controls. |
| `csv` | Report dates, export button, review queue and scope filters. |
| `housing` | Occupied and available housing places. |
| `fleet` | Vehicle, available seats, driver and route. |

All captures were made on 4 October 2026 from the isolated local
`tmp/support-guide-demo.sqlite3` fixture, using the employer web UI. The
fictional worker request and submitted time entry exist only in that local
fixture. The announcement is deliberately unsaved. No pilot or production
worker data was copied. Interface chrome follows the selected language;
project names, worker names and other user-entered text retain the language in
which they were entered. This is normal product behavior and is explained in
the gallery introduction.

The local browser validation checked the language switch, image paths, full-size
links and captions. In a separate backend worktree, the timesheet weekday
headings, project calendar month and two fleet table headings were corrected
for language consistency before the final captures. These backend changes are
local until reviewed and deployed, so the guide's new localized captures should
not be published against an older production backend without that check.

These are explanatory examples, not evidence that every workflow has passed on
both mobile platforms. Future mobile illustrations should use current accepted
builds and fictional accounts. Never publish an image with a real worker's
name, email, photo, address, document, vehicle registration, chat text or token.
