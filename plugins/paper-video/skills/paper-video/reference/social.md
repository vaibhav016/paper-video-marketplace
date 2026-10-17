# Social package

## Cuts (`scripts/social_cuts.py`, run with the venv python)

```bash
PY=$(bash $SKILL/scripts/setup_env.sh)/bin/python
# one clip per thread post (scene names; Scene@a-b trims, A+B joins)
$PY $SKILL/scripts/social_cuts.py clips video/media video video/thread_videos \
    "1_hook=Hook" "2_problem_a=Problem@-27.8" "3_problem_b=Problem@28.4-" "4_idea=Idea" "8_results=Results+Outro"
# ~40 s teaser with 0.4 s crossfades; the last frame is held 2.5 s
$PY $SKILL/scripts/social_cuts.py teaser video/media video video/video_40s.mp4 \
    "Results@4.9-8.6" "Problem@40.5-53" "Idea@17.5-26.5" "Method@5.5-14.5" "Results@17.4-21.8"
```

To pick cut points, make a contact sheet of each scene at 1–2 s intervals. Then check the exact frames around a cut
(`ffmpeg -ss T -i S.mp4 -frames:v 1 x.png`).
- Cut *after* a fade completes.
- Start a teaser on a fully drawn frame, ideally the headline result.
- End each clip on a complete frame.

## X thread

- One post per scene works well: each post explains its clip in the clip's own words, and the clip carries the visual.
  A typical thread: one post per clip, plus a final text post with the link and the credit.
- Each post is ≤ 280 characters, with any link counted as 23. Run `count_posts.py thread.md` after every edit.
- An X post holds either a video or images, not both.
- Put the paper link in the last post, not the first; link posts tend to get less reach.
- Post 1 must work alone, muted. State the problem and the result, with a concrete number.
- When listing gains, name each task ("Task A +9.9, Task B +12.0"), never a bare list of numbers.

## LinkedIn

- Write one post of ~1,500–2,000 characters with the full video attached. LinkedIn has no 2:20 cap.
- The first ~210 characters show before "see more". Put the problem and the paper's one-line answer there.
- Use short paragraphs and a 3-bullet results block with exact numbers.
- End with the link, the credit and 3–4 hashtags.

## Writing rules (thread, LinkedIn, captions)

- Plain sentences. No hype ("groundbreaking", "game-changer"), no emojis, no "it's not X, it's Y", no colon reveals,
  no rhythm-driven three-item lists.
- Say "best average accuracy among the methods we compare", not "SOTA", unless the paper claims SOTA and supports it.
- Every number matches `FACTS.md` and the paper. Scope claims the way the paper scopes them.

## Posting

- Post Tue–Thu, 8–10 am US Eastern. Better still, post on the morning the arXiv listing appears, when aggregators pick papers up.
- Submit to HF Daily Papers the same day.
- Ask your co-authors and lab to quote-post within the first hour.
- Cross-post to r/MachineLearning (`[R]`), Bluesky and LinkedIn.
- Don't repost the identical content; X down-ranks duplicates. Post a new hook and quote the old thread.
- If the paper is under double-blind review, check the venue's policy before naming the authors.
