# kb stack `kb-web` Updates -- `v5`

## Add html_page.links to the HTMl Page view

- I want to be able to view the scraped links on the `/view/page` route.
 - I only want to view links that are under the same domain as the originating page.
 - want to filter any heading links out of the displayed links list. heading links are links that start with `#` in the `href` attribute.
 - I want to be able to ingest links by clicking them and then confirming in a *modal* not (not an alert); subbmitting them to the ingeston pipeline.

## I want to create a new page viewing a virtual table 'sites'.
Which are just a grouping of the the urls by their basename. e.g. all imported sites that sarted with `https://github.com` should be grouped under the basename `github.com`. When viewing a page for a specific `site` I want to see all of the pages that belong to that site.

- I want to have a wiki for the site that is generated from the wiki articles of the pages

## display the similar sites on a left-side bar

...instead on inline with the page contents

## display the original markdown **as markdown** like the wiki descriptions

but keep it collapsible on the page.

