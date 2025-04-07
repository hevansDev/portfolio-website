---
title: Does AI actually make you more productive? Speed running my job with Cursor.
tags: [AI, Cursor, Tooling, Article]
layout: post
image: /assets/images/cursor_thumbnail.png
---

![Speed running my job with cursor thumbnail]({{ site.baseurl }}/assets/images/cursor_thumbnail.png)

Last week at [TurinTech](https://www.turintech.ai/) we had a workshop on agentic AI with an unusual challenge: complete a work task without writing any code manually; the goal was to see if we could boost our productivity using these tools. I'm fairly skeptical of using agentic tools at work - my concern was that I would spend as much (or even more) time vetting AI generated work than I would have doing them manually - even without considering that, could I really be productive with my hands tied behind my back?. I decided to try speedrunning a common task in my day to day work to see if I could really improve my productivity.

## The Speedrun Setup

### Cursor%

* Use [Cursor](https://www.cursor.com/) exclusively to add an optimization example to our team's GitHub repo 

* Add a fully documented example to our optimization repo using only AI-generated code

* No manual typing of code allowed, only prompting and editing AI suggestions

### Any%

* Add a fully documented example to our optimization repo manually using my normal approach

I specifically chose the task of adding an example to this repo as it is both a task I have to do frequently and a task I thought it would be simple for an agentic tool to complete as it just involves copying data from one place to another and reformatting it as a basic report. It was my hope that the simplicity of the sample task would help avoid [an automation rabbit hole](https://xkcd.com/1319/) and give the agent the best possible chance to be genuinely useful.

Usually once I complete an optmisation or someone shares a PR with an optimisation with I manually copy the template directory, write a short summary of the project, copy the data across, and where appropriate add a demo which you can use to show the difference in peformance before and after the optimisation. For my speedrun I would see if I could complete the same task as a tool assisted speedrun using only Cursor without interacting with anything other than the terminal and chat.

The specific example I was documenting in both cases was a DataStax Langflow Optimisation by Jordan Frazier ([see the PR here](https://github.com/langflow-ai/langflow/pull/7248)) who used our tool [Artemis](https://www.turintech.ai/artemis) to improve the performance of the Langflow Python library.


<center>
  <iframe width="560" height="315" src="https://www.youtube.com/embed/PTAhBZ56238?si=zgdVzjayJzw8itYZ" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</center>
<center>Writing examples manually takes 11 minutes and involves constant context-switching</center>

<center>
  <iframe width="560" height="315" src="https://www.youtube.com/embed/YmoHR-LTTbg?si=bYEWRseweGPkdD_c" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</center>
<center>Completing the same task in under 9 minutes without typing code</center>

## My Experience with Cursor

For the challenge I would have to provide Cursor with the relevant information as context and then prompt it to create the example directory, this would have been easier if I had used [MCP](https://modelcontextprotocol.io/introduction), but I wasn't familiar with that approach yet, so instead I just copied the body of the PR into the chat. Cursor did an excellent job of parsing and formatting the data from the PR, completing them with only a handful of prompts. I was particularly happy with how easy cursor made it reformat data as Markdown tables, a task that can often be tedious.

## Run Stats

Once I was done speed running the creation of this example both with and without Cursor I found that using Cursor enabled me to complete the task 20.59% faster. Initially I was surprised that it still took 79.41% of my usual time but reviewing the footage it became clear that once the time saved in the manual tasks likes updating tables (including a neat "skip" of removing the need for a separate table creation step entirely) and writing an overview was accounted for most of the remaining time spent adding the example was spent waiting for processes like zipping files, cloning repos, and adding LFS files which always take a fixed time. Even a modest 20% time saving though can be extremely valuable: the average salary for Solution Engineers in the UK is £57,500/year, this means that if each task is completed 2 minutes and 19 seconds faster that represents approximately £1.07 saved in my time per task. At £15.40 monthly, Cursor Pro pays for itself after adding just 15 new examples.

## When Cursor Gets Stuck: The AI Loop Run Killer

It's worth mentioning that during my first attempt at this run I tried to get Cursor to make a script to demo the optimisation, even after a few hours of trying, it was clear that it simply could not do this. Cursor's attempts at producing a demo script ranged between irrelevant to outright broken and even with a lot of feedback it was unable to produce anything usable, instead it kept getting stuck in loops of making and undoing the same changes. It's possible with a better approach I could have got better results here but either way I was forced to skip this step in both attempts in order to complete the challenge. 

## Lessons for Documentation Tasks

The appeal of AI-written documentation is significant, as I have previously written about before in [here]({{ site.baseurl }}/how-to-use-AI-to-write-documentation-that-actually-works/) when I wrote about [Swimm](https://swimm.io/). Documentation tasks particularly benefit from AI assistance, as demonstrated in the videos, because they often involve repetitive formatting and data organization that AI can handle efficiently. In short automating the boring stuff frees you up to work on the interesting, challenging, or (whisper it) fun parts of a project that AI can't do.

One key takeaway from this run is the importance of having good examples for Cursor to draw on as context for inference.  By using the existing contents of a repo AI tools like Cursor could, hypothetically, help maintain consistency across a collaborative repository in this way, reducing discrepancies and ensuring a uniform style across documentation. This requires providing a lot of documentation as context though which can lead to issues like [loss of fluency](https://huggingface.co/blog/tomaarsen/attention-sinks#limitations-for-chat-assistant-llms:~:text=Loss%20of%20Fluency,assistant%3A%20assistant%3A) and running into context window limits. 

I mitigated these issues by providing a few high-quality, well-structured examples as context which ensures that Cursor can generate accurate and useful outputs - in this project I provided the template that contributors use to add examples to this project which helped guide Cursor to produce a response in the correct format. 

## The Productivity Verdict

To recap using Cursor did in fact give me the ability to complete 26% more examples in the same timeframe and potentially helped me write more consistent documentation across examples. Whilst I still can't replace all manual steps of this particular task with Cursor and still had to spend time thoroughly checking the output it did save me time, so I will likely use Cursor to help with adding future examples. Looking at the numbers, Cursor Pro clearly pays for itself after adding just 15 examples - making it a worthwhile investment purely from a productivity standpoint.

Would you try the "no manual coding" challenge after seeing these results? The best speedrun routes are found as a result of sharing techniques. I'm curious if anyone else has found 'skips' or optimizations I missed in their own AI-assisted workflows.

---

Did you know you can use Artemis Intelligence to keep your documentation up to date? Find out more on the [TurinTech AI Developer page](https://www.turintech.ai/developer).