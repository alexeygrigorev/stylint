# Updating Code Samples After a Library Release

This synthetic style exercise describes a fictional library release with invented version numbers. All names, counts and dates below are fictional, and no real events are reported.

Last October I released version 0.9.0 of a small Python helper for CSV reports. I kept 26 code samples across a README, a tutorial and six guides. Within two days, three users reported that five samples failed against the new release.

I first patched samples one by one as reports arrived. That approach fixed the reported sample while leaving neighboring samples broken, and users kept filing the same class of report. After the sixth report I stopped patching and rebuilt the whole sample set from a clean matrix.

The full pass took one evening and caught 11 broken samples out of 26. Most failures came from two renamed arguments, and the rest came from a changed default. That evening produced a checklist I now run after every minor release.

In this post, I'll share:

- how I freeze a version matrix before touching samples
- how I run every sample clean in fresh environments
- how I fix failures in dependency order
- how I write changelog notes from the fixes
- what the checklist costs and where it still falls short

## 1. Freeze The Version Matrix

I start by recording the exact versions under test in one file. The matrix lists the library version, the Python version and the versions of three dependencies. For the 0.9.0 pass, I recorded Python 3.11 and 3.12, Pandas 2.1 and 2.2, plus the library at 0.9.0.

The matrix lives in a small text file at the repo root.

I wrote the file by hand because it changes rarely and stays readable in review:

```text
library: 0.9.0
python: 3.11, 3.12
pandas: 2.1, 2.2
pytest: 8.1
runner: fresh virtual environment per sample
```

I run the oldest supported combination first, then the newest one. Failures on the oldest combination usually reveal removed arguments, while failures on the newest reveal changed defaults. Recording both ends first keeps the later runs honest.

Skipping this step caused my original mess. I had tested 0.9.0 only against Python 3.12 and Pandas 2.2, so samples that failed on older combinations reached users. The matrix adds ten minutes and removes that blind spot.

## 2. Run Every Sample Clean

With the matrix frozen, I extract every sample into its own runnable file. A small extractor, a Python script that copies fenced blocks into files, reads the README, the tutorial and each guide. It wrote 26 files into a temporary folder in about four seconds.

I run each file in a fresh virtual environment with the recorded versions installed.

The runner script loops over the folder and records pass or fail per file:

```bash
uv run python scripts/run_samples.py --matrix versions.txt --folder /tmp/samples
```

The first clean run found 11 failures out of 26 samples. Seven failures raised a type error from two renamed keyword arguments, and four failures produced wrong output because the date default changed. No sample failed for dependency reasons, which told me the matrix was sound.

I keep the run output as a simple log with one line per sample. The log records the file name, the Python version, the Pandas version and the first error line. That log becomes the work list for the next step.

## 3. Fix Failures In Order

I fix library-level renames before sample-level mistakes, because one rename can repair several samples in one edit. The 0.9.0 release renamed `date_col` to `date_column` and `sep` to `delimiter`. Updating those two names fixed seven samples with the same two edits.

The remaining four failures needed individual attention:

- two samples relied on the old Sunday week start
- one sample passed a string where the new code expects a date object
- one sample read a removed example CSV path

Each fix goes back into the docs source, never only into the extracted file. I edit the README or guide, rerun the extractor and confirm the extracted copy passes. That round trip takes longer, but it keeps docs and tests identical.

After the second full run, 25 of 26 samples passed. The last failure was a flaky time-zone assertion in the tutorial, and I rewrote the assertion to compare dates rather than datetimes. The third run passed all 26 samples on both Python versions.

## 4. Write Changelog Notes

I write changelog entries from the failure log rather than from memory. Each entry names the sample, the old call and the new call, so users can update copied code. The 0.9.0 notes listed nine changed calls across the 11 fixed samples.

Each entry uses three fixed lines that name the sample, the old call and the new call.

Two entries from the fictional 0.9.0 notes read as follows:

```text
renamed date_col to date_column in report() and monthly()
changed default week start from Sunday to Monday in weekly()
```

I group entries by impact rather than by file. Renames come first because they break copied code loudly, and default changes come second because they alter output silently. Silent changes get an extra example line showing old output versus new output.

I publish the notes with the sample run log attached to the release. Users see which combinations passed, and I see the exact evidence behind the release. The attachment habit started after a user asked which Pandas version a fix targeted.

## 5. Keeping The Working Parts

The checklist now runs in about three hours for 26 samples. Extraction takes minutes, the two full runs take 40 minutes each and the changelog takes the rest. The 0.9.0 pass caught every reported failure plus six unreported ones, and no sample reports arrived in the following month.

The process taught me a narrower lesson than "test the docs". Testing one sample proves little, testing all samples on one combination proves more and testing all samples on both ends of the matrix proves enough. That matrix makes the difference between patching reports and preventing them.

Gaps remain because the checklist covers only Python samples. The repo also holds four shell snippets for installation, and those still get manual review. My next addition is a second extractor for shell blocks with one clean container per snippet.

I'll write about that shell runner in a future post. If you want to follow along, don't forget to subscribe.
