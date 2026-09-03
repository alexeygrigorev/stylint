# Preparing an Offline Course Kit That Works Without Network Access

Our June 2026 workshop met in a basement classroom with one access point and 34 students. Ten minutes into the first exercise, the network collapsed, and we lost the entire hands-on session.

I wrote this piece as a synthetic style exercise, and every project and measurement is invented.

I had brought slides, but slides don't run a workshop. For the July session in the same venue, I prepared an offline kit with local copies of every package, dataset, notebook, and command.

In this post, I'll cover:

- the environment I shipped on USB drives
- how I verified the kit before the session
- the printed fallback I used for failures
- how the offline session actually ran
- what I'll change in August

## Build the Environment

The core kit fits in 1.8 GB. I used a small Linux virtual machine with Python 3.12, Jupyter, pandas, and scikit-learn. Students could run the VM with VirtualBox on a laptop with 8 GB of RAM.

I picked a virtual machine because students arrived with Windows, macOS, and Linux laptops. Docker would have been smaller, but the venue's machines couldn't guarantee virtualization support. The VM gave us one path I could test everywhere.

The USB layout stayed simple:

```text
course-kit/
  README.txt
  course-vm.ova
  dataset/
  notebooks/
  slides/
  fallback/
```

I also copied the same files to a local Raspberry Pi access point. The Pi served the notebooks over HTTP at `192.168.44.10`, so students with a working VM could choose either path.

## Verify Before the Session

I ran a checklist on three borrowed laptops. The set included a 2019 Windows machine with 8 GB RAM, a 2021 MacBook Air, and an older Linux ThinkPad. Each test started from an empty user account because that best matched what students would bring.

My checks covered the full student path:

- import the virtual machine in under six minutes
- start Jupyter and open the first notebook
- run the first three cells without a network
- load the 1.1 million-row sample file
- open the fallback HTML page from `fallback/index.html`

The Windows test caught a path bug. A notebook used `/home/student/course-kit`, which failed on a mounted USB drive. I changed all notebook paths to relative paths and reran the checks. On the second pass, every laptop finished in 11 to 14 minutes.

Then I asked two teaching assistants to follow the printed instructions without speaking to me. One tried to skip the verification cell, and that exposed the second issue: a missing warning if Python started with the wrong kernel. We added a one-line version check.

## Prepare Printed Fallbacks

The printed kit has one A4 page per exercise. Each page shows the goal, the exact cells to run, expected output, and a "if this fails" box. It also lists two discussion questions students can answer if their machine can't run the exercise.

For the hardest exercise, I prepared a paper worksheet with 14 rows of input data. Students calculated precision and recall by hand for a tiny classifier. This sounds like a regression, but it became the clearest explanation of false positives all day.

I printed 40 packets because 34 people had registered, and that allowed for no-shows and extra helpers. I also packed three USB drives in separate bags, since one bag tends to end up in the wrong room.

## Run the Offline Session

On the day, the venue's network was still poor. The Raspberry Pi served 21 notebooks, and 27 students ran the virtual machine successfully. Four students paired with neighbors after their laptops failed the RAM check.

The exercise schedule held:

- 10 minutes for setup and verification
- 25 minutes for the data-cleaning notebook
- 30 minutes for the model notebook
- 15 minutes for the paper fallback exercise
- 10 minutes for questions

We finished six minutes late, which felt like a win for a room with one shared access point. The Pi's average page load was 2.3 seconds, and the access point never dropped during the session. The slowest step remained importing the virtual machine on two older Windows laptops.

Feedback forms came from 29 students. Twenty-five of them rated the hands-on part useful or highly useful on the form, and three asked for more time on data cleaning.

## Change It in August

The next kit will use a smaller environment. The VM works, but six minutes of import is a bad opening act. I plan to test Docker on the venue laptops a week early. I'll keep the VM as the fallback if virtualization support is still uneven.

I also want students to verify their laptop before they arrive. A one-page self-check can test free RAM, free disk space, and virtualization support in five minutes. That would leave more classroom time for the model exercise.

The paper exercise stays because it saved the session for four students. It also gave everyone a shared mental model before we discussed metrics.

## Lessons Learned

An offline course kit turns network trouble from a cancellation into a slower setup. The preparation cost about 14 hours, and most of it went into testing on machines I didn't own. That testing found problems no checklist would have predicted.

I'll publish the USB layout and checklist in a future post after the August test. Subscribe if you want to see whether the smaller environment survives a different room.
