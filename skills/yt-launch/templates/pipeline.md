# pipeline.md

Optional. Only for a channel whose videos come out of a production pipeline - n8n, Make, a script of
your own - rather than being written in the chat. Lives at `.claude/youtube/pipeline.md`, next to
`voice.md`. `/yt-review` and `/yt-ship` read it to know where things are; without it they ask, and
work on whatever you paste.

Write what is true of this channel's pipeline. Nothing in the skills assumes a particular tool.

## Videos
<!-- How a video is named, so "/yt-review 0412" finds it. The folder pattern, and where the folders
live. -->
code:
folder:

## Script
<!-- Where the script arrives (a local file, a Google Doc in Drive...), and whether Claude can write
to it. "read-only" means the skills hand back text for you to paste - production reads the
original, not a copy. -->
where:
access: read-only
format: |
  <!-- The markers the pipeline parses, exactly as they appear - e.g. the title line, the
  thumbnail line, how a scene starts, the narration label. The skills keep them intact. -->

## Sources
<!-- The file that holds the sources for each video. A fact that is not in it does not go into
the video. -->
file:

## After editing
<!-- What the video folder holds once it is edited: the subtitles, the audio per scene, the final
video. And where /yt-ship writes its output. -->
subtitles:
audio:
video:
output:

## After publishing
<!-- What has to be updated once the video is actually public, and where. /yt-ship reminds; it
never does it. -->
