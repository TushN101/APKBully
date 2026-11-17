# Can Local AI Make BetterLeaks Better?

The idea was simple: **What if we combined BetterLeaks with a locally hosted LLM to reduce false positives?**

BetterLeaks already does a good job finding potential secrets, but like any pattern-based scanner, it can occasionally flag hashes, identifiers, and other non-sensitive strings.

I wanted to experiment with adding a second layer: let BetterLeaks find potential leaks, then pass those findings to a local AI model to determine whether they actually look like secrets.

---

The proposed pipeline was:

`APK → BetterLeaks → Local LLM Verification → Final Findings`

---

### First, BetterLeaks

I tested BetterLeaks against two sample sets.

For testing, I used the [SecretsTest repository](https://github.com/BonJarber/SecretsTest/blob/main/config.py), which contains examples of credentials from AWS, Google Cloud, GitHub, Slack, Stripe, Twilio, and other providers, alongside hashes and public keys intended to act as false positives.

| Test case | Result |
|---|---:|
| Real sample | 35 potential leaks detected |
| False-positive samples (5) | 0 detections |

BetterLeaks performed well on these tests. However, occasional false positives involving hashes and other edge cases made the idea of a contextual verification layer interesting.

---

### Then, the AI Experiment

I wanted to see whether a small model running entirely locally could act as that verification layer.

**Model:** `d1-omni:600m` by Liquid AI  
**Runtime:** Ollama  
**Hosting:** Local  
**API:** `/v1/systemone`  
**Decision type:** `noul`

Each candidate line was sent individually to the model with the following question:

```json
{
  "model": "d1-omni:600m",
  "state": "<candidate line>",
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
```

The model returned a `noul` score representing P(TRUE). I tested two thresholds: greater than 0.70 and greater than 0.50.

**Positive test cases — 66 samples**

| Metric | > 0.70 | > 0.50 |
|---|---:|---:|
| Detected | 0 | 17 |
| Missed | 66 | 49 |
| Detection rate | 0% | 25.76% |

**Negative test cases — 5 samples**

| Metric | > 0.70 | > 0.50 |
|---|---:|---:|
| Correctly rejected | 4 | 3 |
| Incorrectly flagged | 1 | 2 |
| False positive rate | 20% | 40% |

---

### So, What Went Wrong?

Honestly, the model was simply not good enough for this task.

It struggled to recognize common credential formats, including AWS access keys, Google API keys, access tokens, and private keys.

One particularly concerning result was that a private-key sample received a score of approximately **0.575**, while a public-key sample in the negative dataset received approximately **0.731**.

This is exactly the kind of inconsistency we cannot afford in a security scanner.

The proposed combination would actually make detection worse:

- At 0.70, the model would reject all 66 positive-labelled samples.
- At 0.50, it would still reject 49 out of 66 positive-labelled samples.
- Meanwhile, it would continue allowing some negative samples through.

Using this model as a verification gate would trade occasional false positives for a massive increase in missed secrets.

---

### Final Decision

**The BetterLeaks + AI approach was not integrated into APKBully.**

BetterLeaks already provided useful detection results, while the experimental model was too unreliable to safely filter its findings.

The experiment demonstrated that simply adding an LLM does not automatically improve an existing detection pipeline. The verification model needs to be at least as reliable as the detector itself, especially when missed credentials can have serious security consequences.

Perhaps a better model, a fine-tuned classifier, or a more specialized secret-detection approach could make this architecture worthwhile in the future.

For now, BetterLeaks stays in the pipeline, and the AI experiment stays in the research folder.

---

*Note: These are preliminary results from the tested samples, not a comprehensive evaluation of BetterLeaks or Liquid AI. The negative dataset contains only five samples, and the positive-labelled corpus has not been independently validated for live credential status. The BetterLeaks and AI experiments were conducted separately, not as an integrated end-to-end pipeline.*
