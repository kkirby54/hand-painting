import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# Data directory and state file
DATA_DIR = Path("data")
STATE_FILE = DATA_DIR / "generation_state.json"

PROMPT_TEMPLATE = (
    "A detailed, hand-drawn graphite pencil sketch on textured drawing paper, "
    "mimicking the style of a page from a studio ghibli artist's sketchbook. "
    "The image focuses on {detailed_content}. "
    "The drawing relies on visible, confident pencil strokes to define basic shapes, "
    "using cross-hatching and dense shading to create simple volume and fuzzy textures. "
    "The eyes should have distinct white highlights against dark graphite. "
    "The background is minimalist, showing only the grain of the off-white paper and faint smudges, "
    "keeping the entire focus on the character. "
    "Natural, soft lighting suggests a real-life drawing context."
)

DETAILED_CONTENTS = [
    "a cluster of small Susuwatari (dust bunnies). They are essentially fuzzy, dense black circles created by scribbled, compacted graphite lines, with two distinct, wide circular white areas for eyes staring forward. The edges are soft and indistinct due to the fur texture.",
    "a single Kodama (tree spirit) head standing. It has a slightly wobbly, rounded rectangular head shape drawn with a clean but organic pencil outline. Three simple, dark, irregular circular holes represent its eyes and mouth.",
    "the small white Totoro (Chibi-Totoro) and the medium blue Totoro (Chu-Totoro) walking together. Chibi-Totoro is a simple, tiny, round bun-shape with rabbit-like ears, rendered with minimal shading. Chu-Totoro is a larger, rounded oval body defined by soft outlines and faint belly marking lines, carrying a small sack.",
    "the face of No-Face (Kaonashi). It is focused on a long, vertical oval mask shape defined by a clean outer line. The characteristic markings under the eyes and above the mouth are filled with soft grey graphite shading, and a tiny, subtle line indicates the mouth.",
    "Ponyo in her fish form. A very round, human-like face with big eyes is attached to a small, chubby, simple fish body with tiny fins. The entire shape is smooth and curved, rendered with gentle, flowing pencil lines.",
    
    "Jiji the black cat sitting stiffly in a front-facing pose. The focus is on his sleek, solid black silhouette created with dense, dark graphite shading. His large, pointed ears are disproportionately big compared to his head, and his wide, oval white eyes stand out sharply against the dark fur.",
    "Calcifer the fire demon burning on a log. He has a teardrop-shaped body with jagged, flickering edges drawn with loose, energetic pencil strokes to mimic fire. His large, expressive eyes and mouth are sketched with thick lines, conveying a grumpy but cute expression.",
    "Ootori-Sama (the giant duck spirit) standing. The drawing emphasizes the massive, egg-shaped volume of its body using soft, rounded hatching. It has a single leaf on its head, a tiny beak, and small webbed feet that look comically small supporting the large body.",
    "Boh transformed into a mouse, standing on hind legs. He is extremely chubby and round, rendered with soft, curved contour lines to emphasize his squishy weight. He has round mouse ears and tiny paws, looking slightly confused.",
    "the large Totoro standing upright, holding a simple umbrella. The drawing captures the iconic pear-shaped silhouette. The fur texture on his belly is detailed with inverted 'V' markings. The umbrella is sketched with straight, confident lines, contrasting with Totoro's fuzzy, round outline.",

    "a full-body sketch of No-Face (Kaonashi) standing quietly. The long, black, tube-like body is rendered with soft, vertical graphite shading to suggest a heavy, semi-transparent fabric texture. His arms hang loosely by his sides, and the white mask face is the focal point with high contrast against the dark body.",
    "a close-up portrait of Sosuke from 'Ponyo'. He has a round face and a short bowl-cut hairstyle. The hair is rendered with blocky, distinct pencil strokes to show the clumps and volume of the hair. His expression is serious and determined, with simple round eyes and a small button nose.",
    "a close-up of Mei from 'My Neighbor Totoro'. She has her signature pigtails held by hair ties, rendered with loose, curvy lines to show the hair's bounce. Her expression is joyful and energetic with a wide-open mouth (shouting or laughing), showing her teeth, captured with dynamic facial lines.",
    "Kiki's face viewed directly from the front. The large ribbon on her head is sketched with soft shading to show the fabric folds and volume. Her uneven bangs frame her face, drawn with quick, feathered strokes. Her eyes are large and reflective, with detailed pupils characteristic of the Ghibli style.",
    "Chihiro showing a shocked or surprised expression. Her eyes are wide open, detailed with distinct pupils and highlights to convey emotion. Her mouth is slightly open in a gasp. Her hair is pulled back into a high ponytail, but loose wisps of hair fall around her face, drawn with fine, faint pencil lines.",

    "a close-up portrait of Howl Jenkins Pendragon with dark short hair. The drawing focuses on delicate, elegant pencil strokes to render the fine texture of his hair falling over his forehead. He wears his signature earrings, and his expression is calm and charming with long eyelashes and distinct, deep eyes.",
    "San (Princess Mononoke) wearing her red clay mask and white wolf-fur cape. The mask is rendered with smooth, clean gradients, while the fur cape creates a contrast with rough, scribbled, and dense pencil textures. The circular eyes and mouth of the mask are dark and hollow, creating a mysterious atmosphere.",
    "a dynamic sketch of Kiki flying on her broomstick, viewed from the side. Her dark dress billows backwards, showing realistic fabric folds and wrinkles caused by the wind. Her hair flies wildly behind her. Her hands grip the broom handle tightly, and Jiji clings nervously to the back bristles. The lines are swift and gestural to suggest speed.",
    "a medium shot of the large Totoro sitting by the water (implied), holding a fishing rod. His posture is slumped and relaxed, emphasizing his heavy, rounded bottom. His tiny paws gently hold the thin rod. A small leaf is on his head, and he stares blankly at the line, capturing a quiet, whimsical moment.",
]
