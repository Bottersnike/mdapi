# Unofficial MangaDex API and CLI

Full documentation can be found at
https://mdapi.readthedocs.io/en/latest/py-modindex/. There are no examples
currently, but they will be coming soon.

## Basic API usage

In absence of full examples, here's a brief example snippet:

```py
from mdapi import MdAPI

md = MdAPI()

user = md.user.get_self()
if user is None:
    print("Please login using `mdex login`")
    quit()
print(f"Logged in as {user.username}")

results = md.manga.search("Murenase")
manga = next(results)
print(f"Found {manga.title}")

read_chapters = md.manga.get_read(manga)

chapters = md.manga.get_chapters(manga, order=ChapterSortOrder(chapter="asc"))
chapter = next(chapters)

print(f"First chapter: {chapter.title}")
print("Already read:", chapter.id in read_chapters)

urls = md.chapter.page_urls_for(chapter)
print("First page:")
print(next(urls))

md.chapter.mark_read(chapter)
```

## CLI Commands

To read a chapter, the three commands needed are, in order:

- `mdex search [query here]`
- `mdex chapters [manga uuid]`
- `mdex read [chapter uuid]`

Additionally, `mdex login`, `mdex logout`, and `mdex whoami` are provided.
These can be used to generate a `.mdauth` file without requiring a call to
`md.auth.login()` from code with a plaintext password. They will also be used
in future when additional functionality is added to the CLI.
