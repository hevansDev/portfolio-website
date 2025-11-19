---
title: How to use AI to write documentation that actually works
tags: [AI, Documentation, Swimm, Article]
status: published
---

Writing documentation is an oft maligned part of the software development process. It takes time away from solving technical problems and can feel like an unending task., new changes and versions can make your newly updated quick-start or API reference rapidly out of date. It comes as no surprise then that there are now many tools offering to take the pain out of this process by automating some or all of the work required to produce documentation with AI.

I've seen the importance of good docs first hand. Good documentation helps teams to communicate a vision for a project both internally and with external stakeholders which in turn can lead to dodging costly misunderstandings, and can make the actual source code of the project better by keeping the whole team aligned on what they are building. In contrast bad documentation could see you wasting hours providing support to get new devs onboarded to a project. Worse still, in the case of competing products, it could see people opt to use different products entirely, even if they are less feature rich, simply because it's easier to understand how to use them. 

Given the importance of good documentation, is it actually possible to use AI tools to make the process of producing documentation easier without degrading the overall quality? In this blog I will explore using Swimm, an AI documentation tool, to document one of my personal projects to try to answer this question.


# What is Swimm?

![Swimm website landing page](/content/images/swimm.png)

Swimm is billed as an AI agent powered "knowledge management tool for code" launched by Swimm Tech in October 2019. In practice, Swimm supports two main use cases: automatically generating documentation using an index of your project source code and providing explanations to developers to help them understand complex or unfamiliar code. I chose to try out writing docs with Swimm because of its ability to generate recommendations for documentation updates based on source code whilst it's being written. After a week of re-recording instructional videos due to some product features changing, that seemed like a very appealing idea!

# Generating documentation with Swimm

<center><iframe width="100%" height="500" src="https://www.youtube.com/embed/dZaa7CdbI08?si=MqvNGajSK2Q1zACp" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></center>

<center>Video of my first attempt at using Swimm to generate documentation</center>

I chose my [ASCII art photo booth project](https://hughevans.dev/everything-i-made-in-2024/#:~:text=ASCII%20Art%20Photo%20Booth%20for%20EMF%20Camp) that I built out for [EMF Camp 2024](https://www.emfcamp.org/) to test out the Swimm automatic documentation feature because I know the project code well, it's a very simple project consisting of one file, and I already have a basic README for the project to benchmark any AI generated docs against.

To get started I [created an account](https://app.swimm.io/register) via the Swimm website and connected it to my GitHub account, I then downloaded the [Swimm VSCode plugin](https://marketplace.visualstudio.com/items?itemName=Swimm.swimm) to my locally checked out project. I was then able to create a new markdown file with documentation for the `main.py` file in my project simply by using the generate option in the Swimm VSCode plugin and providing a title and prompt. Here's the prompt I provided:

> How to deploy your own ASCII booth with this project


> Explain how to setup this project by running the code on a raspberry pi with a webcam and thermal printer attached. You should wherever possible link to other documentation about how to acomplish more complex steps like setting up a raspberr ypi for the first time, selecting a thermal printer, creating a mastodon account, and so on. You should format the documentation as a set of step by step instructions documenting each part of the process


Looking at the generated file the results were pretty mixed. In some areas like the introduction Swimm did a great job of understanding the purpose of the code and context of the project, giving a nice break down of what the documentation is about and outlining the steps required to get the project working.

![Introduction of a piece of documentation produced by Swimm](/content/images/swimm1.png)

Things start to break down a little in the next section, whilst Swimm clearly makes an attempt at following the instruction in the prompt to "link to other documentation about how to accomplish more complex steps" the second step here is vaguer than I would like, and the last step fails to explain how to correctly install the dependencies. 

![Instructions on how to set up project as generated by Swimm](/content/images/swimm2.png)

Swimm missed the necessary command to install dependencies in the last step. This is likely because we did not index the entire project for [Retrieval Augmented Generation (RAG)](https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/) or pass in the rest of the project as context. Currently, we only have the option to provide one file, so the agent behind Swimm is completely unaware of our handily available requirements file.

The rest of the documentation produced is a high level view of each function in the `main.py` file that Swimm appears to be primarily designed to produce. This could be useful - particularly as it can quickly be regenerated as docs are updated, but I feel this kind of documentation is out of place in the setup guide I instructed the agent to produce.

![Function level explanation produced by Swimm](/content/images/swimm3.png)

Finally, I tried out the killer feature I was really excited for: automatic suggestion generation in response to code changes. Unfortunately, this turned out to not be as automatic as I had first hoped: I added a new function to `main.py` but had to select the _Add to existing doc_ option on the new function to get Swimm to produce a suggestion. When it did, it added it to the end of the Markdown file instead of in the proper location, not exactly what I'd been hoping for but still a very quick way of fixing gaps in the documentation.

![Docs for new function generate by Swimm](/content/images/swimm4.png)


# Does Swimm really make it easier to write good documentation?

I really like some aspects of the Swimm agent and think it could be useful both to generate drafts of docs and to help make suggestions for updates and improvements to existing code, however Swimm alone does not generate good documentation. The documentation produced by Swimm did not contain all of the expected information a user would need to get started from a setup guide - particularly for a project like this one with both hardware and software components. Adding to the case against Swimm and bad news if you like to work with separate docs and source code repos: the Swimm VSCode plugin doesn't appear to be able to cope with a VSCode project that contains multiple `.git` directories.

Overall I think Swimm shows a lot of promise, its live tracking of changes to source code combined with a slick VSCode integration makes for a more polished experience than other competing tools, but I don't think I'll be incorporating it into my day-to-day work just yet. I'm sure that with more time I could get better results from Swimm, but ultimately like many tools I've found that the work to get desired results is not significantly less than simply writing the desired documentation, and that's before you factor in the $28 cost for the table stakes of AI code generation and CI CD integration.

It's clear though that AI code documentation tools like Swimm can generate at the very least basic documentation, with the potential to do far more in future as the technology behind them improves, and the products themselves mature. There may come a time when such tools become a prominent feature of the docs writing process, but for me that time isn't just yet.