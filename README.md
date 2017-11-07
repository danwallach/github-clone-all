# github-clone-all.py 

If you have a GitHub project with an ever-growing number of repos, and
you want to automatically clone all those repos to your desktop all at
once, such as downloading hundreds of student code repos for grading,
then this script is for you.

## Installation


1) If you haven't already done this, you'll first need to `pip install
requests` for a necessary library.

2) Get a GitHub token with all the "Repo" privileges. You do
this on the GitHub website
[(instructions)](https://github.com/blog/1509-personal-api-tokens). 

3) Optionally, edit the `defautGithubProject` variable to reflect your
   project's name (e.g., for `https://github.com/RiceComp215`, the
   project name is `RiceComp215`). You can also install your GitHub
   API token in the `defaultGithubToken` variable.

## Usage

Now let's say you want to get every repo beginning with `comp215-week06`.
You can simply run `python github-clone-all.py --prefix comp215-week06 --out codedump-week06`
and it will create the directory `codedump-week06` and will check out all
of the repos sharing the given prefix.
