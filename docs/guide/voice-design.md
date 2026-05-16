# Voice Design

<p class="so-intro">Describe the speaker via attributes — gender, age, pitch, accent, dialect, whisper.</p>

Describe the speaker via attributes — no reference audio needed.

```python
from strands_omnivoice import omnivoice_design

omnivoice_design(
    text="Welcome to the future.",
    output="/tmp/v.wav",
    instruct="female, young adult, high pitch, british accent",
)
```

## Hear the differences

The same text in four different designed voices:

<div class="so-audio"
     data-src="../assets/audio/design_uk_elderly.mp3"
     data-label="female, elderly, low pitch, british accent"
     data-tag="storyteller"
     data-text='"Once upon a time, in a land far far away, there lived a wise old story-teller."'></div>

<div class="so-audio"
     data-src="../assets/audio/design_us_male.mp3"
     data-label="male, middle-aged, american accent"
     data-tag="newscaster"
     data-text='"Houston, we have a problem. Repeat — Houston, we have a problem."'></div>

<div class="so-audio"
     data-src="../assets/audio/design_whisper.mp3"
     data-label="female, young adult, whisper"
     data-tag="suspense"
     data-text='"And then, when no one was watching, everything went silent."'></div>

<div class="so-audio"
     data-src="../assets/audio/design_indian.mp3"
     data-label="male, young adult, indian accent"
     data-tag="welcome"
     data-text='"Welcome, my friend. Today I will tell you about the wonders of the universe."'></div>

## Attribute Categories

`instruct` is a comma-separated list. **Within** each category, only one value is
allowed; **across** categories, combine freely.

| Category | Values |
|---|---|
| Gender | `male`, `female` |
| Age | `child`, `teenager`, `young adult`, `middle-aged`, `elderly` |
| Pitch | `very low pitch`, `low pitch`, `moderate pitch`, `high pitch`, `very high pitch` |
| Style | `whisper` |
| English accent *(EN text only)* | `american accent`, `british accent`, `australian accent`, `canadian accent`, `indian accent`, `chinese accent`, `korean accent`, `portuguese accent`, `russian accent`, `japanese accent` |
| Chinese dialect *(ZH text only)* | `四川话`, `陕西话`, `东北话`, `云南话`, `河南话`, `贵州话`, `桂林话`, `济南话`, `石家庄话`, `甘肃话`, `宁夏话`, `青岛话` |

## Examples

```python
"female, young adult, high pitch, british accent"
"male, elderly, low pitch, whisper"
"女, 青年, 四川话"
"middle-aged, indian accent"   # gender omitted — model fills in
```

## Tips

- **Case-insensitive** — `Male`, `MALE`, `male` are equivalent.
- **Mix English + Chinese** — auto-normalised internally.
- **Less is more** — if a combination behaves oddly, simplify.

See the [upstream voice-design reference](https://github.com/k2-fsa/OmniVoice/blob/master/docs/voice-design.md)
for the canonical attribute table.
