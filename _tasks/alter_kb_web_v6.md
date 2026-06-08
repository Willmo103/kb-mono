# Changes to kb-web (v6)
The core objectives here are to start migrating kb-web from a just web-based 'scraper' into a more generalized central 'core' of the kb-stack.

## Create a segmentation in the database for youtube video transcripts

- Create a new `transcripts` table and migrate the youtube video webpages into the `transcripts` table taking the properties from fetched_pages that make the most sense overall and rename them to fit the `transcript` model, but leave space for all future properties that we want from the sources we already have to fit more purposes, basically create a `fat struct` style transcript model that may be used to represent transcripts from various sources and with their own metadata.

- Create a seperate wiki entry prompt and tagging process, I want the wiki to break down the transcript in a cronological manner sumerizing the content into time sections rather than topical sections in the wiki article. I also want the agent to have the metadat from the page as a informant to the content of transcript but not to include it in the transcript iself so it should probably be attached to or injected into the system prompt for the model to segment the content of the transcript

- Display the transcript data using its source and subsource to organize it, so for instanse youtube would be the top level, then the url of the video would be like sub-source and the title would just be pulled from the wiki entry generated and attached back into the database. all other fat struct metadata should be used how ever seen fit.

Example things I want on a Transcript source page for YouTube videos:

- A iframe of the youtube video. NOT set to autoplay
- A any youtube page metadata for the video
- A Summary of the transcript of the youtube video broken down into time-chunked "chaper" summaries with hilighted key points and quotes from the transcript (using md formatting) to hilight the most important parts of the video in a structured way that is easy to read and reference.

Example things I would want on the summary of something like a Podcast transcript (Not coming from youtube)

- A link or description of the source of the audio, whether that be spotify, apple podcasts, or a direct link to an mp3 file for instance.
- A link to a page where the audio player can play the audio directly (using the audio source url)
- A any podcast page metadata for the podcast
- A Summary of the transcript of the podcast broken down into time-chunked "chaper" summaries with hilighted key points and quotes from the transcript (using md formatting) to hilight the most important parts of the podcast in a structured way that is easy to read and reference.

Examples of things I would want from a transcript of a user provided audio file; transcribed by some other portion of the kb-stack (this is an example and not yet implimented or planned, just an example of the flexibility I want in this structure)

- A filename or user-provided `source` information
- A playable link to the source audio (if provided/available)
- any additional metadata about the file or it origins -- basically I want a custom sub-metadata struct for each source type
- a summary of the transcript broken down into time-chunked "chaper" summaries with hilighted key points and quotes from the transcript (using md formatting) to hilight the most important parts of the audio file in a structured way that is easy to read and reference.

### Considerations

Data -- All database that migrate (fetched_pages >> transcripts ) **Must** be migrated in a *strictly **non-destructive*** way, and this must remain part of the codebase as a migration.

## Collections

Create a collections feature.
