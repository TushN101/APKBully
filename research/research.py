
import requests

headers = {
    "Content-Type": "application/json"
}

data = {
    "model": "d1-omni:600m",
    "state": None,
    "questions": {
        "contains_secrets": {
            "type": "noul",
            "instructions": "Does this line contain a genuine authentication secret, not merely a SHA hash, checksum, UUID, commit hash, or random string?",
            "criteria": {
                "true": "A plausible authentication credential.",
                "false": "A non-credential string."
            }
        }
    }
}


def scanner(secrets: list) -> dict:
    totalTests = len(secrets)
    testPositive = 0
    testNegative = 0
    above70 = 0
    above50 = 0

    for counter, secret in enumerate(secrets, start=1):
        print(f"Processing secret {counter}/{totalTests}")

        data["state"] = secret

        response = requests.post(
            "http://10.0.2.2:11434/v1/systemone",
            headers=headers,
            json=data,
            timeout=120
        )

        response.raise_for_status()
        result = response.json()["answers"]["contains_secrets"]["noul"]

        print("Got result:", result)

        if result > 0.7:
            above70 += 1
            testPositive += 1
        else:
            testNegative += 1

        if result > 0.5:
            above50 += 1

        print(f"Processed {counter}/{totalTests}")

    return {
        "totalTests": totalTests,
        "testPositive": testPositive,
        "testNegative": testNegative,
        "totalAbove70": above70,
        "totalAbove50": above50
    }


def realSecrets() -> list:
    with open("realsecrets.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]


def fakeSecrets() -> list:
    with open("falsepositives.txt", "r") as file:
        return [line.strip() for line in file if line.strip()]


def main():
    print("--- REAL SECRETS ---")
    print(scanner(realSecrets()))

    print("\n--- FALSE SECRETS ---")
    print(scanner(fakeSecrets()))


if __name__ == "__main__":
    main()
