import re

def structure_for_llm(resume_text: str) -> str:
    name_match = re.search(r"^[A-Z][a-z]+\s+[A-Z][a-z]+", resume_text)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", resume_text)
    phone_matches = re.findall(r"(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{2,5}\)?[\s\-]?)?\d{6,10}", resume_text)
    phones = [p for p in phone_matches if len(re.sub(r"[^0-9]", "", p)) >= 10]

    preamble = []
    if name_match:
        preamble.append(f"NAME: {name_match.group(0)}")
    if email_match:
        preamble.append(f"EMAIL: {email_match.group(0)}")
    if phones:
        preamble.append(f"PHONE: {phones[0]}")  # take first valid one

    full_input = "\n".join(preamble) + "\n\nFULL RESUME:\n" + resume_text
    return full_input
