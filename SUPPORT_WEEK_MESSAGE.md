# Weekly planning message

Status: main message approved by the owner for website publication on 2026-10-11.
The full-rhyme alternative remains a separate, unapproved campaign concept.
Based on the owner's idea: "One click — and everything is ready for the whole week..."
Site base: origin/main 73d57bc, rechecked 2026-10-11. Existing video, downloads, access conditions and other pages are preserved.

## Recommended English version

Audience: **For staffing agencies and workforce coordinators**

Headline: **Plan the week. Publish in one click.**

Explanation: Select your crew’s workdays and shift times. Publish them together — each worker sees their own shifts in the JobHub app.

The headline has the owner's week/click consonance and a two-part rhythm. It is a near rhyme, not a perfect English rhyme. It separates preparation from the single publication action. It does not imply that inviting people, assigning vehicles, arranging housing or approving hours happens in one click.

## Why this message

The buyer should recognize their job before reading the slogan. A coordinator is preparing several dates for an existing crew. Once the dates and shift times are selected, the publication action publishes the selected dates together. Connected workers can then view their individual published shifts. This is a concrete reason to look at the product demo.

"Everything is ready" should not be used as an unqualified promise. A schedule also does not replace all of the company's coordination work. The wider product story remains projects, crews, transport, housing, hours and work communication in one workspace.

## Other useful cuts of the same idea

- Short campaign caption: **One click to publish the week.** Pair it with selected calendar dates, followed by a worker's own schedule.
- Full spoken line: **Pick the days, set the shift times, and publish the week in one click. Everyone sees their own shifts in JobHub.**
- Optional separate concept with a full rhyme: **Your week in view. For every crew.** `view / crew` is a true rhyme. This is an alternative for review, not an approved replacement or claim of originality.
- End card: **JobHub Support · Plan the week. Publish in one click.** Then `jobhub.today` and an invitation to the five-minute presentation.

Do not splice the slogan into the already approved reel dialogue as a new advertising narrator. In a future reel, it can be a short visual end card after the characters have shown the publication action. The owner's audio and V05/V06 stay unchanged.

## Localized headline and audience

| Language | Audience | Headline |
| --- | --- | --- |
| EN | For staffing agencies and workforce coordinators | Plan the week. Publish in one click. |
| RU | Для агентств и координаторов рабочих команд | Спланируйте неделю. Опубликуйте одним нажатием. |
| PL | Dla agencji pracy i koordynatorów zespołów | Zaplanuj tydzień. Opublikuj jednym kliknięciem. |
| UK | Для агенцій і координаторів робочих команд | Сплануйте тиждень. Опублікуйте одним натисканням. |

Localizations prioritize natural wording and the same promise; they do not force an English rhyme into every language. Dutch video availability does not imply Dutch app or site support.

## Placement

Prepared on the home-page first screen: logo and JobHub Support name → audience → headline → concrete explanation → three short steps → existing demo and guide actions. The existing video continues to show the manager and worker sides. Avoid repeating the full slogan in every section or every news article.

For demos and advertising, pair the message with a prepared crew and selected dates. Show the publication action, then the worker schedule. Do not show unprepared housing or transport magically appearing after publication.

## Product evidence and verification boundary

Read-only code check, backend checkout `T:/JobApp/_codex_backend_workspace_production`, HEAD `acffb6e`:

- `templates/support/project_first_workspace.html`: calendar selection named `work_dates`, start/end/break fields, one submit action `shifts_publish`.
- `support/services/project_crews.py`: selected-date publication service.
- Existing web/API test names cover selected-day publication and worker calendars.
- `JOBHUB_SUPPORT_SOURCE_OF_TRUTH.md` v1.25 and current release plan were checked. This messaging task did not run a live write or a new deployment/device acceptance scenario.

The single click means publishing a prepared set of selected shifts in an existing crew, within the manager's permissions. It does not promise whole-company readiness, error-free planning, automatic payroll or automatic translation.

## Search and measurement

The audience wording and explanation make the page easier for a buyer to understand. Do not claim that a slogan automatically increases a hidden score or search ranking. Google's guidance stresses helpful, accurate, people-first content and descriptive headings, without a ranking guarantee.

Sources checked 2026-10-09:

- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide

Keep the descriptive page title and metadata. Do not stuff the slogan with repeated search phrases, fabricate ratings, or add hidden keyword text.

After publication, assess real interest: visits reaching the video, demo-request actions, and feedback from agency owners. Actual emails received are stronger evidence than mailto clicks. No tracking, analytics service or advertising campaign is added by this local copy change.
