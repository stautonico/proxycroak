<!-- omit in toc -->

# Contributing to Proxycroak

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways
to help and details about how this project handles them. Please make sure to read the relevant section before making
your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The
community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support
> the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)

## Code of Conduct

This project and everyone participating in it is governed by the
[Proxycroak Code of Conduct](https://github.com/stautonico/proxycroakblob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to .

## I Have a Question

Before you ask a question, it is best to search for existing [Issues](https://github.com/stautonico/proxycroak/issues)
that might help you. In case you have found a suitable issue and still need clarification, you can write your question
in this issue.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/stautonico/proxycroak/issues/new).
- Open a [Discussion](https://github.com/stautonico/proxycroak/discussions/new/choose).
- Provide as much context as you can about what you're running into.
- Provide as much technical detail about the platform you're using/versions of software you're running (for
  contributors.)

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the
> necessary rights to the content and that the content you contribute may be provided under the project license.

> ### Notice Regarding Content Generated by LLMs
> While LLMs can boost workflow efficiency, it's important to refrain from relying solely on LLM-generated content,
> which could lead to unintentional plagiarism. Any material identified as solely LLM-generated will be excluded from the
> project. Feel free to utilize LLMs for coding assistance, but refrain from submitting directly generated code.

### Reporting Bugs

<!-- omit in toc -->

#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to
investigate carefully, collect information and describe the issue in detail in your report. Please complete the
following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version (your branch/fork isn't significantly out of date.)
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment
  components/versions (If you are looking for support, you might
  want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there
  is not already a bug report existing for your bug or error in
  the [bug tracker](https://github.com/stautonico/proxycroak/issues?q=label%3Abug).
- Collect information about the bug:
    - Stack trace (Traceback)
    - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
    - Version of your python interpreter, package versions, etc., depending on what seems relevant.
    - Possibly your input and the output
- Can you reliably reproduce the issue? And can you also reproduce it with older versions?

<!-- omit in toc -->

#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue
> tracker, or elsewhere in public. Instead, sensitive bugs must be sent by email to security@proxycroak.com.
>
> All security information is available in the [security.txt](https://proxycroak.com/.well-known/security.txt)

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/stautonico/proxycroak/issues/new). (Since we can't be sure at this point whether it
  is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to
  recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem
  and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no
  obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs
  with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such
  as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Proxycroak, **including completely new features
and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community
to understand your suggestion and find related suggestions.

<!-- omit in toc -->

#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Perform a [search](https://github.com/stautonico/proxycroak/issues) to see if the enhancement has already been
  suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to
  convince the project's developers of the merits of this feature. Keep in mind that we want features that will be
  useful to the majority of our users and not just a small subset. If you're just targeting a minority of users,
  consider writing an add-on/plugin library.

<!-- omit in toc -->

#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/stautonico/proxycroak/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point
  you can also tell which alternatives do not work for you.
- You may want to **include screenshots and animated GIFs** which help you demonstrate the steps or point out the part
  which the suggestion is related to.
- **Explain why this enhancement would be useful** to most Proxycroak users. You may also want to point out the other
  projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution

> The project includes a `.better-commits.json` to help follow a more consistent commit and branch naming scheme.
> It is not required to use [better-commits](https://github.com/Everduin94/better-commits), however, we highly recommend
> the use of it for convenience when making commits and branches. You can still create commits and branches "the old
> fashioned way" as long as you follow the scheme.

To contribute to the project, you first must create a fork of the project. To fork the project, simply go to the
[project's GitHub page](https://github.com/stautonico/proxycroak), then click "Fork" on the top right of the page. This
will create a copy of the repo on your account.

Once you have a fork of the project, you can clone it to your local machine using your preferred method of accessing git
(either through the command line (`git clone`) or using a GUI (like GitKraken or GitHub Desktop).)

Next, make a branch with a descriptive name. Please create a branch with a descriptive name following this scheme:
`<username>/<branch-type>/<OPTIONAL:issue-number>/<short-description>`.

- **username** - Your GitHub username
- **branch-type** - the category of the branch. Valid options:
    - *feat* - A new feature
    - *fix* - A bug fix
    - *refactor* - A code change that neither fixes a bug nor adds a feature
    - *perf* - A code change that improves performance
    - *test* - Adding missing tests or correcting existing tests
    - *ci* - Changes to our CI configuration files and scripts
    - *chore* - Other changes that do not modify source code/test files
- **issue-number** - An optional field that should correlate with a GitHub issue number (if applicable)
- **short-description**: A brief (70 characters or less) description of the branch's changes

**Note that you can use the `better-branch` command to generate this branch automatically.**

Here are some examples of good branch names:

```
stautonico/feat/21/public-api
stautonico/fix/sv1-broken-images
stautonico/refactor/footer-typo
```

Now, you may make your modifications to the project. **ONLY MODIFY THINGS THAT ARE RELEVANT TO YOUR PULL REQUEST.**
If you're working on a backend API route and find a typo in the frontend or in documentation, **DO NOT CHANGE IT.**
Open a new issue and change it in its own associated pull request. Pull requests that make several random changes cause
confusion and make the maintainers lives harder.

Once you have completed your feature, continue to [Commit Messages](#commit-messages).

## Styleguides

### Commit Messages

Maintaining a consistent commit message format makes it easier to understand what a commit is doing. Commit messages
like
"changed some stuff" isn't helpful.

**You are recommended to use `better-commits` to create your commit messages**

If you do not want to use `better-commits`, you can write your commit messages in the following format:

**Title** - The title of your commit should use the following
format: `<commit-type>(<commit-scope>)<optional:!>: <optional:#issue-number> <description>`

- **commit-type** - the category of the commit. Valid options:
    - *feat* - A new feature
    - *fix* - A bug fix
    - *refactor* - A code change that neither fixes a bug nor adds a feature
    - *perf* - A code change that improves performance
    - *test* - Adding missing tests or correcting existing tests
    - *ci* - Changes to our CI configuration files and scripts
    - *chore* - Other changes that do not modify source code/test files
- **commit-scope** - The scope of which the commit makes changes. Valid options:
    - *backend*
    - *frontend*
    - *docker* - Anything related to the docker containers (Dockerfile, docker-compose.yml, etc.)
    - *tools* - Anything related to utilities the program includes (manage.py, etc.)
    - *other* - Anything that does not fit into any of the other 5 categories
- **!** - If your commit contains any breaking changes, please include an exclamation point (`!`) after the parenthesis.
- **issue-number** - If your commit is directly related to a specific GitHub issue, plese include the number (including
  the `#`)
- **description** - A brief (70 characters or less) description of the commits changes

** Commit body** - The body of your commit should use the following format:

```
<detailed-description>

BREAKING CHANGE: <optional: breaking-change-title>
<optional: breaking-change-description>

DEPRECATED: <optional: deprecated-title>
<optional: deprecated-description>

<optional: additional-footer>

Closes: <optional: ticket-number>
```

- **detailed-description** - A detailed description explaining all the changes included in the commit.
- **breaking-change-title** - A short title explaining what the breaking change in the commit is (if applicable)
- **breaking-change-description** - A detailed description explaining the breaking change.
- **deprecated-title** - A short title explaining what was deprecated (if applicable)
- **deprecated-description** - A detailed description explaining what was deprecated and why
- **additional-footer** - Any other relevant information
- **ticket-number** - A GitHub issue number (if applicable)

Here are some examples of good commit messages:

```
feat(backend): #21 Implemented public API

This commit implements a public-facing REST API, allowing users to interact with proxycroak through a 
REST interface instead of the web interface. This commit adds several new routes including:

- /api/proxies
- /api/decklist
- /api/image/<set_id>/<card_id>

Users must authenticate with the API using the `X-API-Key` header, providing their API key (obtained from the web interface).

Users will be limited to 1000 requests per day, enforced by (bla bla bla)

Closes: #21
```

```
fix(backend)!: Fixed SVI set having invalid set name causing broken images

This commit fixed a bug preventing SVI from providing the correct images. Internally, SVI was written as 
"SV1", causing a problem where the database couldn't retrieve images properly.

BREAKING CHANGE: All decklists including "SV1" will no longer work!
Any decklists that included "SV1" will no longer work. They must now all be written as "SVI".
```

```
refactor(frontend): Fixed a few typos in the frontend

Several words were misspelled in the frontend including:

- (in footer) "Pokémon" written as "pokmeon"
- (in features page) "bookmark bar" written as "bokmark bar"
- (in help page) "Discord" written as "disscord"
```

### Pull Requests

Pull requests should follow the same descriptive format as [commit messages](#commit-messages). To submit a pull request
include the same format of title and description you would in a commit message, but scoped to cover changes in all
the commits

## Attribution

This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!