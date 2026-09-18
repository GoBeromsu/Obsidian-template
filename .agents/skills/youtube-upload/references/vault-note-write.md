# Vault note write

Own the tracking-note assembly, frontmatter property calls, and the re-upload update path for Step 6.

Write transcript and feedback to temp files first (avoids shell ARG_MAX for long
videos), then assemble the note body with Feedback BEFORE Transcript. This step
is reached only after semantic validation passed:

```bash
cat > /tmp/yt_upload_transcript.md << 'TRANSCRIPT_EOF'
<transcript_text>
TRANSCRIPT_EOF

# Step 5.5 must have produced a non-empty feedback file.
[ -s /tmp/yt_upload_feedback.md ] || { echo "ERROR: feedback file missing/empty — rerun Step 5.5" >&2; exit 1; }

# Build the successful validation snippet from Step 3.5's report.
[ "$(jq -r '.passed' /tmp/yt_validate_report.json)" = "true" ] || {
  echo "ERROR: semantic validation did not pass; no upload or note mutation" >&2
  exit 1
}
cat > /tmp/yt_validation_snippet.md << 'VALIDATION_EOF'
## Validation

- ✅ Validation: passed
VALIDATION_EOF

# Assemble inline — `<<'EOF'` would NOT expand $(cat ...) (see Caveats).
obsidian create vault=Ataraxia \
  path="15. Work/02 Area/Youtube/<title>.md" \
  content="$({
    echo "## Feedback"
    echo
    cat /tmp/yt_upload_feedback.md
    echo
    cat /tmp/yt_validation_snippet.md
    echo
    echo "## Transcript"
    echo
    cat /tmp/yt_upload_transcript.md
  })"
```

Then set frontmatter properties (key=value syntax, NOT --flag style):

```bash
NOTE_PATH="15. Work/02 Area/Youtube/<title>.md"

obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=type value=video < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=video_id value="<video_id>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=source value="<youtube_url>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=date_published value="<YYYY-MM-DD>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=duration_seconds value="<duration>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=language value="<detected_or_specified_language>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=status value="done" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=tags value="reference,reference/video,youtube/uploaded" type=list < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=title value="<generated_title>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=description value="<first_line_of_description>" < /dev/null
obsidian property:set vault=Ataraxia path="${NOTE_PATH}" name=image value="https://img.youtube.com/vi/<video_id>/maxresdefault.jpg" < /dev/null
```

**Re-upload (delete + new) case.** The note already exists from the original
upload — do NOT `obsidian create` a duplicate. Resolve the existing note path
(usually the same `15. Work/02 Area/Youtube/<title>.md`; if the title changed,
find it with `obsidian search vault=Ataraxia query="video_id: <old_video_id>"`),
then run only the `property:set` calls that change — `video_id`, `source`, and
`image` to the new video, plus `date_published` to today — against that path.
Leave the transcript/feedback body intact.

**Important**: create and mutate this tracking note through `obsidian create` / `obsidian property:set` via Bash — the vault-access convention for the Ataraxia vault — not the Edit/Write tools.
