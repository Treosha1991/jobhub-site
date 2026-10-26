# jobhub-site

## Support publication candidate, 25.10.2026

Edition: **support-web-2026-10-25-v1**. On 26.10.2026 the owner explicitly
approved this edition and publishing all four pages to jobhub.today, then
continuing Paddle verification. This commit prepares that authorised
publication. Live payment activation is expressly excluded. Deployment and
Paddle submission results must be verified separately, not inferred from Git.

Local branch `codex/paddle-review-pages-20261025`, based on main `855a328`.
The owner approved monthly prices before applicable taxes: 249/449/749 PLN
for 20/50/100 simultaneously active workers. Custom requires a separate quote;
no minimum or annual plan was approved. Prices do not prove demand or margins.

Four publication-candidate pages, each in RU/EN/PL/UK:

- `support-pricing.html` — software scope, limits, monthly prices and activation.
- `support-subscription-terms.html` — proposed supplier terms for future billing.
- `support-refunds.html` — cancellation, refunds and mandatory buyer rights.
- `support-privacy.html` — subscription/payment supplement, distinct data roles.

All pages retain an explicit prelaunch/no-purchase notice and `noindex`.
The supplier terms apply only after separate acceptance before a future
Support purchase, not automatically to existing customers on publication.
There is no Paddle.js, payment form, checkout, key or Live product. The only
homepage change is a footer link to Support pricing. Existing published terms
and privacy text are unchanged. The six public payload files were checked
against the exact SHA-256 approval manifest before committing (6/6 match).

Regenerate with `python tools/build_support_commerce.py`; verify navigation
with `python tools/check_site.py`. Preview: `python -m http.server 8774 --bind
127.0.0.1`, then `http://127.0.0.1:8774/support-pricing.html?lang=ru`.

Final-edition verification: local links/assets/anchors PASS for all 17 pages; 32 actual browser
cases (4 new pages × 4 languages × 390/1440 px) PASS, no horizontal overflow or
encoding corruption, four visible language controls, no forms or frames.
Language-button switching and the terms link preserve the selected language.
Evidence: `T:/JobApp/output/support-commerce-final-browser-qa-20261025.json`,
`support-commerce-final-pricing-20261025.png`. No forms, frames or Paddle
scripts are present. Generator compilation and `git diff --check` PASS.

Publication approval of this edition was received 26.10.2026. Before real workforce-data activation, separately verify
production subprocessors/regions/transfer safeguards, specific retention,
backup rotation/erasure and the required Art. 28 processing agreement and its
acceptance. These are not a prerequisite for preparing/submitting vendor
website review; a website review does not authorise real workforce-data use.
The privacy supplement covers billing/account purposes and states that work
processing terms are provided before those data are accepted. It does not
claim that a DPA has already been signed or prescribe an invented backup term.
Paddle seller/domain/product approval, production acceptance and authorisation
for real payments remain separate. Verify public URLs after deployment before
using them on Paddle onboarding step 3.

Material terms for owner review: monthly prices before applicable taxes;
auto-renewal; immediate free upgrade for the remaining paid period and new
price next payment; next-period downgrade with future admission cap;
cancellation at paid-period end; no automatic refund just for cancellation;
mandatory rights/Paddle refund rules; lawful workforce-data responsibility;
limited software-use licence; proportionate suspension; Polish supplier law
without waiving mandatory buyer protection; no retrospective changes to
previous Apple/Google purchases; no fixed SLA or unconditional refund promise.

Primary references checked 25.10.2026:

- https://www.paddle.com/help/start/account-verification/what-is-domain-verification
- https://www.paddle.com/legal/refund-policy
- https://www.paddle.com/legal/buyer-terms
- https://www.paddle.com/legal/privacy
- https://prawakonsumenta.uokik.gov.pl/prawo-odstapienia-od-umowy/

The broad JobHub vacancy/legacy Store products are disclosed in the copy and
excluded from the proposed Paddle purchase; acceptance of the shared brand
and domain by Paddle is not assumed.
