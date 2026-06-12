The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# Behavioral Instruction Manual & Code Standards: DEVOP1

This file serves as the strict behavioral blueprint for the DEVOP1 system. Any AI agent (Antigravity) working on this codebase MUST adhere to these commands.

## 1. Mandatory File Identification Header (CRITICAL)
ALL files (including source code, scripting, configuration files, and even untracked/ignored scratch files) MUST contain the following exact tag formatted as a comment at the top of the file:
```text
i d e n t   " @ ( # ) $ F o r m a t : { p r o j e c t _ n a m e } : { f i l e _ n a m e } : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "
```
*Note: In the template above, the character sequence has been intentionally formatted with spaces between each character (representing the `sed` transformation `s/./& /g`). This prevents Git's clean/smudge filters from matching, interpreting, and modifying this rule documentation file itself.*

To initialize a new file, place the clean version at the top of your file (legible examples are listed below in spaced-out format to prevent active smudge filter matching):
- For Python/Shell files:
  `# i d e n t   " @ ( # ) $ F o r m a t : G i t   p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For SQL files:
  `- - i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For Batch files:
  `: : i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`
- For Markdown/YAML/Dockerfiles/XML:
  `# i d e n t   " @ ( # ) $ F o r m a t : G i t  p r o j e c t   n a m e : f i l e n a m e : % a n : % a e : % a d : % c n : % c e : % c d : % H : % D : % N $ "`

For tracked files, the Git smudge filter (`ident-dynamic`) will automatically expand the placeholder variables with real Git commit and author/committer data during checkouts. Untracked or ignored scratch files must still physically carry this header comment as a repository consistency requirement.

## 2. Git & Taiga Repository Synchronization (CRITICAL)
The Git repository "https://github.com/lanfr144/DEVOP1" and the Taiga repository "https://tree.taiga.io/project/ferro988-devop1/timeline" must be kept in sync with the project at all times!
No changes to project files are allowed without:
1. Creating a corresponding task in the Taiga repository.
2. Updating the task status accordingly.
3. Referencing the Taiga task ID (e.g. `TG-XXX`) inside the Git commit message comments to maintain a complete operational audit trail.
