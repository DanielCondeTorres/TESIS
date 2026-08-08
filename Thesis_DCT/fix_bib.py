import re

with open("references.bib", "r") as f:
    content = f.read()

# 1. Add missing DOIs
content = content.replace(
    "@article{bacterial_bilayer_1,\n author = {Raetz, CR and Dowhan, William},",
    "@article{bacterial_bilayer_1,\n doi = {10.1016/S0021-9258(19)40001-X},\n author = {Raetz, CR and Dowhan, William},"
)

content = content.replace(
    "@article{Gilmer2017,\n author = {Justin Gilmer",
    "@article{Gilmer2017,\n doi = {10.48550/arXiv.1704.01212},\n author = {Justin Gilmer"
)

# For feynman1982simulating, the user didn't give the DOI, but said "es un articulo de periodico".
# The user might have meant cecilia1964 but let's just leave feynman1982simulating alone, or add its actual DOI.
# Since the user specifically said: "feynman1982simulating: es un articulo de periodico" I'll just not add a DOI.

# 2. Fix journal names
replacements = {
    "journal = {Rev. Mod. Phys.}": "journal = {Reviews of Modern Physics}",
    "journal = {Phys. Rev. Lett.}": "journal = {Physical Review Letters}",
    "journal = {J. Chim. Phys.}": "journal = {Journal de Chimie Physique}",
    "journal = {Phys. Rev. A}": "journal = {Physical Review A}",
    "journal = {Phys. Rev.}": "journal = {Physical Review}",
    "journal = {J. Chem. Soc.{, Faraday Trans. 2}": "journal = {Journal of the Chemical Society, Faraday Transactions 2}",
}
for old, new in replacements.items():
    content = content.replace(old, new)

# 3. Misc fixes
content = content.replace("volume = {02310095419}", "volume = {19}")
content = content.replace("journal = {Nature Biotechnology 2006 24:12}", "journal = {Nature Biotechnology}")
content = re.sub(r"\s*isbn\s*=\s*\{0123456789\},?\n", "\n", content)
content = content.replace("Sodium Dodecyl Sulfate Micelles,}", "Sodium Dodecyl Sulfate Micelles}")

# 4. Fix newlines in URLs and eprints for cd_2, cd_4, afm_5, experiments_2, fluo_3, gamma
keys_to_fix = ["cd_2", "cd_4", "afm_5", "experiments_2", "fluo_3", "gamma"]

def fix_urls(match):
    block = match.group(0)
    # Remove all newlines and spaces within the { ... } of url and eprint
    def clean_field(m):
        cleaned = re.sub(r"[\n\s]+", "", m.group(2))
        return m.group(1) + "{" + cleaned + "}"
    block = re.sub(r"(eprint\s*=\s*)\{([^}]+)\}", clean_field, block)
    block = re.sub(r"(url\s*=\s*)\{([^}]+)\}", clean_field, block)
    return block

for key in keys_to_fix:
    pattern = r"(@article\{" + key + r",.*?^\})"
    content = re.sub(pattern, fix_urls, content, flags=re.DOTALL | re.MULTILINE)

# 5. Check GBD2021CausesOfDeath author formatting
# Ensure it has double braces. If not, add them.
def fix_gbd_author(match):
    return "author = {{GBD 2021 Causes of Death Collaborators}}"

content = re.sub(r"author\s*=\s*\{GBD 2021 Causes of Death Collaborators\}", fix_gbd_author, content)

with open("references.bib", "w") as f:
    f.write(content)

print("Done")
