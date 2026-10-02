# JobHub Support guide: visual evidence

The public guide at `support-guide.html` describes the current MVP on fictional
data. Its interface examples must never expose a real worker's name, email,
photo, address, document, vehicle registration, chat text, or push token. Use
current accepted builds and the employer web workspace for future captures.
Do not publish a screenshot merely because it looks plausible: verify the
screen, action and resulting state against the installed build and backend.

| Workflow | Current visual | Next clean capture to add |
|---|---|---|
| Employer menu | `assets/support-manager-menu-illustration.png` — **illustration** derived from an owner-provided demo screenshot; the personal avatar was replaced. It is deliberately labelled as an illustration on the page. | Capture the current employer home screen with a generic demo avatar. |
| Worker requests | `assets/support-requests-example.jpg` — owner-provided test screenshot. | Capture the request form with an empty state, selected date and successful submission. |
| Several request dates | `assets/support-request-dates-example.jpg` — owner-provided test screenshot. | Capture the post-decision state as well. |
| Invitation and access | `assets/support-worker-invite-form.jpg` — real production web form with fictional review company and empty fields; no invitation was sent. | Capture the accepted worker invitation in a fictional account. |
| Employer web entry points | `assets/support-employer-web-home.jpg` — real production web workspace for the fictional review company. | Replace the narrow capture with a wider browser capture when available, keeping the same fictional data. |
| Project / crew / dated shift | `assets/support-demo-project-crew.jpg` — project, crew, passenger and published dated shift in an isolated local fictional database. | Worker Today view for the same fictional shift. |
| Housing / transport | `assets/support-demo-housing.jpg` and `assets/support-demo-fleet.jpg` — local fictional housing with occupied/free place and vehicle with available seats. | Driver and route assignment to a fictional worker; worker-side view. |
| Actual hours / correction | No screenshot yet. | Worker submission, employer review and returned correction on the same demo shift. |
| Tasks / announcements / chats | No screenshot yet. | Clean task review states and a synthetic announcement or chat; avoid real message content. |
| Documents and offboarding | No screenshot yet. | Only synthetic document status screens after checking environment flag and legal copy; never show a real HR file. |

The images now on the page are examples, not evidence that all flows have been
accepted on both platforms. Before replacing or adding an image, check image
dimensions, legibility on a phone, localized callouts, and that all named
people/dates are fictional. Keep the guide's textual steps and image captions
consistent with the actual role-specific navigation.

The production review workspace was inspected read-only on 2 October 2026. Its
existing worker/project/housing/vehicle views show a named project, address and
registration plate that have not been independently confirmed as fictional.
Do not publish captures of those views. The two new web captures above contain
only the explicitly fictional review-company label and an empty invitation form.
For the remaining process screenshots, first prepare an isolated fictional
fixture or confirm and replace every identifiable value before capture; do not
alter production records as a side effect of documenting the guide.

The project, housing and fleet captures were made on 2 October 2026 with
`seed_support_demo` in a separate local SQLite database. The added project,
crew, dated shift, vehicle and housing records are fictional. These captures
show the web interface and do not replace device acceptance evidence.
