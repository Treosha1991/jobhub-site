# JobHub Support guide: visual evidence

The public guide at `support-guide.html` describes the current MVP on fictional
data. Its interface examples must never expose a real worker's name, email,
photo, address, document, vehicle registration, chat text, or push token. Use
current accepted builds and the employer web workspace for future captures.
Do not publish a screenshot merely because it looks plausible: verify the
screen, action and resulting state against the installed build and backend.

| Workflow | Current visual | Next clean capture to add |
|---|---|---|
| Demo request | `assets/support-demo-request.jpg` — current local guide hero, with a callout added in HTML. | Verify the mail composer opens on a public device after publication. |
| Employer menu | `assets/support-demo-home-desktop.jpg` — wide desktop capture from an isolated fictional company; the earlier `assets/support-manager-menu-illustration.png` remains labelled as an illustration in the image gallery. | Compare the navigation with the connected pilot organization before publication, without publishing its worker data. |
| Worker requests | `assets/support-demo-requests-desktop.jpg` — current manager queue and decision form with a fictional request. The two older mobile request screenshots were withdrawn from the public guide because their on-screen schedule-change copy is now inaccurate. | Capture the current worker request submission and post-decision screen on a test device. |
| Several request dates | No current visual in the guide. | Capture each date and its independent decision state in a current test build. |
| Invitation and access | `assets/support-demo-workers-desktop.jpg` and `assets/support-demo-team-desktop.jpg` — fictional desktop worker list and staff access; `assets/support-worker-invite-form.jpg` shows the empty fictional review-company invitation form. | Capture acceptance of a worker invitation in a fictional mobile account. |
| Employer web entry points | `assets/support-demo-home-desktop.jpg` — wide desktop workspace for a fictional company; the earlier `assets/support-employer-web-home.jpg` remains in the gallery. | Validate against the connected pilot organization's current desktop menus. |
| Project / crew / dated shift | `assets/support-demo-project-desktop.jpg` — fictional desktop project and dated shift; `assets/support-demo-project-crew.jpg` remains in the gallery. | Worker Today view for the same fictional shift. |
| Housing / transport | `assets/support-demo-housing.jpg` and `assets/support-demo-fleet.jpg` — local fictional housing with occupied/free place and vehicle with available seats. | Driver and route assignment to a fictional worker; worker-side view. |
| Actual hours / correction | `assets/support-demo-timesheet.jpg`, `assets/support-demo-timesheet-detail.jpg` — fictional week and manager review modal with a single synthetic submitted entry. | Worker submission and returned correction on a physical device. |
| CSV for accounting | `assets/support-demo-csv.jpg` — full fictional timesheet and report controls; the local download was inspected as semicolon CSV with scheduled and actual decimal hours. | Check an accountant-scoped account's permission and its own browser download. |
| Tasks / announcements / chats | `assets/support-demo-tasks-desktop.jpg` and `assets/support-demo-announcements-desktop.jpg` — fictional task list and filled announcement draft form. The earlier narrow task capture remains in the gallery. | Capture task review/completion and published announcement or synthetic chat. |
| Documents and offboarding | No screenshot yet. | Only synthetic document status screens after checking environment flag and legal copy; never show a real HR file. |

The images now on the page are examples, not evidence that all flows have been
accepted on both platforms. Before replacing or adding an image, check image
dimensions, legibility on a phone, localized callouts, and that all named
people/dates are fictional. Keep the guide's textual steps and image captions
consistent with the actual role-specific navigation.

The production review workspace was inspected read-only on 2 October 2026. Its
existing worker/project/housing/vehicle views show a named project, address and
registration plate that have not been independently confirmed as fictional.
Do not publish captures of those views. The earlier production web captures in
the gallery contain only the explicitly fictional review-company label and an
empty invitation form.
For the remaining process screenshots, first prepare an isolated fictional
fixture or confirm and replace every identifiable value before capture; do not
alter production records as a side effect of documenting the guide.

The project, housing and fleet captures were made on 2 October 2026 with
`seed_support_demo` in a separate local SQLite database. The added project,
crew, dated shift, vehicle, housing and task records are fictional. These captures
show the web interface and do not replace device acceptance evidence.

On 4 October 2026, the new desktop captures were made from the separate
`tmp/support-guide-demo.sqlite3` fixture using the local release-preflight backend.
One fictional submitted time entry and one fictional day-off request were added
only in that local database so the manager review screens and CSV could be shown.
The generated CSV was downloaded, its header and example totals checked, then
the temporary download removed. No connected
pilot or production worker data was copied into these screenshots. The numbered
callouts are HTML overlays on `support-guide.html`, and each caption explains
the corresponding controls in RU, EN, PL and UK.
