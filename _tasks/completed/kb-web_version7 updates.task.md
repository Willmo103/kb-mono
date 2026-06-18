# Updates to kb-web version 7

## Refactor code to make package more manageable

the server.py file is almost 2000 lines of code at this point and needs to be broken up a little

This task should include

- using fastAPI routers and files like utils.py, models.py, etc to breakup the code in kb-web/src/kb-web/server.py into a more manageable size
- all functionality must remain the same
- all changes to codebase should be documented in the README and any other documentation

## Create a 'cron' job fetching a specific url on a recuring basis with custom instructions

I want to create a new feature that allows a 'cron' job to be setup wherein a user supplies a url (for now) and have that content fetched, then processed into a specific output based on a user's prompt to the AI

This process should include a prompt template that allows the user to specify any of the source's fecthed_page attrs as prompt variables e.g. {html_content} {md_content} etc. we alos need a way to display information about  one or more of former 'runs' of the cronjob and/or its results e.g. "if there are changes on these two webpages.. {last_run.md_content} -- \n\n {current_fetched.md_content}... parse out the tables as json objects in codeblocks with a title that includes the date"... parse out tables as json objects in codeblocks with a title that includes the date .

Since this shall be able to operate as its own independant source of data we can offer options as to where we want to output the data, like "should it be a video, or and article, or something else, or nothing at all; just spwaning further actions based on the result: like sending a notification to the user if somthing cannot be fetched or as a daily source of news to digest

cron jobs should be only optionally resulting in a creation of a new database object, but also may allow for the process to result in one or more files created on the server and made available to download, or remin private. (temporary or at a specific place and indexed for future display)

There should be logs accessabable on the server for cron jobs, they should also optionally notify the user about their successes or failures.

## Updating the server infastructure (admin features)

I want to add server logs viweable on the server admin page.
I want to post errors to gotify in full with the stack and other exectuon information.

## Graph visualizer for simularity of objects

I want to view a graph view of the embedding neighbors and such (like the obsidsian thing) of the objects in my database. I want to see clusters using the embeddings and things like tags, sites, creators, etc.

## Collections

I want to create a collections field where a collection may be created and then various items may be added to or removed from the specific collectio. basically I want a way to group iported items in a way where I may consider them in an isolated fashion. For now collections will just have a title and many-to-one connections to fetched_pages lets get a way for the user to create a collection and also allow the user to request an agent to "suggest collections" where the agent just gets the titles of all un-grouped items and returns a suggested grouping with titles for the collection. the admin user my accept the collection, modify it, or re-roll with some instruction.

add a collection link in the top and side navbars that will take us to the collection view or a specific collecion view.
ON the article or video page only; display the collection(s) the article/video belongs to
