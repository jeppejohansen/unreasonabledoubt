# Show available recipes.
default:
    @just --list

# Create an empty blog draft and its working directories.
[arg("slug", pattern="[a-z][a-z0-9]*(?:_[a-z0-9]+)*")]
[positional-arguments]
make-blog slug:
    @test ! -e "blogs/$1" && test ! -L "blogs/$1" || { echo "Already exists: blogs/$1" >&2; exit 1; }
    @mkdir "blogs/$1"
    @touch "blogs/$1/blog.md"
    @mkdir "blogs/$1/src" "blogs/$1/assets" "blogs/$1/data" "blogs/$1/figures" "blogs/$1/tables"
    @touch "blogs/$1/src/.gitkeep" "blogs/$1/assets/.gitkeep" "blogs/$1/data/.gitkeep" "blogs/$1/figures/.gitkeep" "blogs/$1/tables/.gitkeep"
    @echo "Created blogs/$1/blog.md with src/, assets/, data/, figures/, and tables/."

# Create a Typst math note and its working directories.
[arg("slug", pattern="[a-z][a-z0-9]*(?:_[a-z0-9]+)*")]
[positional-arguments]
make-math-note slug:
    @test ! -e "math_notes/$1" && test ! -L "math_notes/$1" || { echo "Already exists: math_notes/$1" >&2; exit 1; }
    @mkdir "math_notes/$1"
    @cp templates/math_note.typ "math_notes/$1/note.typ"
    @mkdir "math_notes/$1/src" "math_notes/$1/assets" "math_notes/$1/data" "math_notes/$1/figures" "math_notes/$1/tables"
    @touch "math_notes/$1/src/.gitkeep" "math_notes/$1/assets/.gitkeep" "math_notes/$1/data/.gitkeep" "math_notes/$1/figures/.gitkeep" "math_notes/$1/tables/.gitkeep"
    @echo "Created math_notes/$1/note.typ with src/, assets/, data/, figures/, and tables/."

# Previous name for make-blog.
new-post slug: (make-blog slug)
